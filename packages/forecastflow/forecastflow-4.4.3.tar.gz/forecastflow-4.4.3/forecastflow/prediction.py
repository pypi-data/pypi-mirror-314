import logging
import time
from io import BytesIO
from typing import TYPE_CHECKING

import pandas as pd

from .api import _v3
from .enums import FileType, Status
from .exceptions import ForecastFlowError, InvalidID, OperationFailed
from . import _storage

if TYPE_CHECKING:
    from . import Model, Project, User

logger = logging.getLogger(__name__)


class Prediction:
    """
    ForecastFlow prediction object
    """

    def __init__(self, model: "Model", prediction_id: str):
        """
        Instantiate object with given prediction ID.

        Args:
            model:
                Model which makes this predict.

            prediction_id:
                ID of prediction you want to open.
        """
        self.model = model
        self.prediction_id = prediction_id
        self.name = None
        self.status = None
        self._document = None
        self.update()

    @property
    def project(self) -> "Project":
        return self.model.project

    @property
    def rid(self) -> str:
        return self.prediction_id

    @property
    def filetype(self) -> "FileType":
        return FileType(self._document.get("type", FileType.CSV))

    @property
    def user(self) -> "User":
        return self.model.project.user

    def get_result(self) -> pd.DataFrame:
        """
        Download the result from ForecastFlow.

        Returns:
            result with primary key and predicted values.
        """
        self.wait_until_done()
        uris = [f["uri"] for f in self._document["files"]]
        filetype = self.filetype
        df_list = []
        for uri in uris:
            with BytesIO() as f:
                _storage.download(file=f, uri=uri, id_token=self.user.id_token)
                f.seek(0)
                if filetype == FileType.CSV:
                    df_list.append(pd.read_csv(f))
                elif filetype == FileType.TSV:
                    df_list.append(pd.read_csv(f, delimiter="\t"))
                elif filetype == FileType.PARQUET:
                    df_list.append(pd.read_parquet(f))
                else:
                    raise ForecastFlowError(f"{filetype} not supported.")
        return pd.concat(df_list, ignore_index=True)

    def update(self):
        """
        update name, status
        """
        self._document = _v3.get_prediction_info(
            id_token=self.user.id_token,
            team_id=self.project.team_id,
            pid=self.project.pid,
            rid=self.rid,
        )

        if self._document["mid"] != self.model.model_id:
            raise InvalidID("Given Prediction ID is not for this model")

        self.name = self._document["name"]
        self.status = Status(self._document["status"])
        self.did = self._document["did"]

        logger.info(f"Prediction '{self.name}': {self.status.value}")

    def wait_until_done(self):
        """
        Wait until ForecastFlow finish prediction.
        """
        while self.status != Status.COMPLETED and self.status != Status.ERROR:
            self.update()
            time.sleep(5)

        if self.status == Status.ERROR:
            document = self._document
            error_info = document.get("errorInfo")
            if error_info is None:
                raise OperationFailed("Predictor quit with Error")
            else:
                raise OperationFailed(
                    f"{error_info['message']}\n"
                    f"error_log_id: {error_info['errorLogId']}"
                )

    def delete_data_source_unused_for_training(self, with_prediction=True) -> None:
        """
        Delete data source which is used only for the prediction.

        Args:
            with_prediction (bool): Whether delete prediction itself.
                                    Default is True

        Returns:
            None: Nothing to return if process finished successfully

        Raises:
            If deletion process failed with some reason,
            it raises OperationFailed exception.
        """
        if with_prediction:
            self.delete_prediction()

        # This endpoint delete data source which is not used for training and testing.
        response = _v3.bulk_delete_data_sources(
            id_token=self.user.id_token,
            team_id=self.model.project.team_id,
            pid=self.model.project.project_id,
            dids=[self.did],
            with_prediction=False,
        )
        # status 0 means operation finished successfully
        if response["status"] != 0:
            raise OperationFailed(f"Data source deletion failed: {response['message']}")

        # Clean up local prediction in the model
        if self.did in self.model.project._data_sources:
            self.model.project._data_sources.pop(self.did)

        logger.info(f"The data source is successfully deleted: {self.did}")

    def delete_prediction(self) -> None:
        """
        Delete prediction itself.

        Args:
            no arguments for this method.

        Returns:
            None: Nothing to return if process finished successfully

        Raises:
            If deletion process failed with some reason,
            it raises OperationFailed exception.
        """
        response = _v3.delete_predict(
            id_token=self.user.id_token,
            team_id=self.model.project.team_id,
            pid=self.model.project.project_id,
            rid=self.rid,
        )

        # status 0 means operation finished successfully
        if response["status"] != 0:
            raise OperationFailed(
                f"Prediction deletion is failed: {response['message']}"
            )

        # Clean up local prediction in the model
        if self.rid in self.model._predictions:
            self.model._predictions.pop(self.rid)

        logger.info(f"The prediction is successfully deleted: {self.rid}")
