import logging
import time
import pandas as pd
from collections import OrderedDict
from typing import TYPE_CHECKING, Dict, List

from . import prediction
from .enums import FileType, Status
from .exceptions import OperationFailed
from forecastflow.api import _v3

if TYPE_CHECKING:
    from . import DataSource, Prediction, Project, User

logger = logging.getLogger(__name__)


class Model:
    """
    ForecastFlow model object
    """

    def __init__(self, project: "Project", model_id: str):
        """
        Instantiate object with given model ID.

        Args:
            project:
                Project which model belong to.

            model_id:
                ID of model you want to open.
        """
        self.project = project
        self.model_id = model_id
        self._predictions: Dict[str, "Prediction"] = {}
        self.update()

    @property
    def _document(self) -> dict:
        """
        Returns:
            A document of this model on database
        """
        doc = _v3.get_model_info(
            id_token=self.user.id_token,
            team_id=self.project.team_id,
            pid=self.project.pid,
            mid=self.mid,
        )
        return doc

    @property
    def mid(self) -> str:
        return self.model_id

    @property
    def prediction_schema(self) -> OrderedDict:
        """
        Returns:
            OrderedDict which maps column name to type string like 'float'.

        Notes:
            You want to use forecastflow.util.parse_type if you need native Python type.
        """
        schema_json = self._document["predictionSchema"]  # [{key: type}, ...]
        schema = OrderedDict()
        for column in schema_json:
            key = list(column.keys())[0]
            type_ = column[key]
            schema[key] = type_
        return schema

    @property
    def user(self) -> "User":
        return self.project.user

    @property
    def info(self) -> dict:
        return self._document

    def create_prediction(
        self,
        data_source: "DataSource",
        name: str,
        description: str = "",
        filetype: "FileType" = FileType.CSV,
    ) -> "Prediction":
        """
        Create prediction with data_source.

        Args:
            data_source:
                Data to predict with.

            name:
                Name of predict.

            description:
                Description of predict.

        Returns:
            ForecastFlow prediction object which predicts with given data.
        """
        self.wait_until_done()
        prediction_id = _v3.create_prediction(
            id_token=self.project.user.id_token,
            name=name,
            description=description,
            team_id=self.project.team_id,
            pid=self.project.project_id,
            did=data_source.data_source_id,
            mid=self.model_id,
            filetype=filetype,
        )
        self._predictions[prediction_id] = prediction.Prediction(self, prediction_id)
        return self._predictions[prediction_id]

    def get_prediction(self, prediction_id: str) -> "Prediction":
        """
        Get prediction object with given ID.

        Args:
            prediction_id:
                ID of predict you want.
        Returns:
            ForecastFlow predict object with given ID.
        """
        if prediction_id not in self._predictions:
            self._predictions[prediction_id] = prediction.Prediction(
                self, prediction_id
            )
        return self._predictions[prediction_id]

    def get_importances(self) -> pd.DataFrame:
        """
        Get prediction object with given ID.
        Returns:
            ForecastFlow predict object with given ID.
        """
        res = _v3.get_model_importances(
            id_token=self.user.id_token,
            team_id=self.project.team_id,
            pid=self.project.pid,
            mid=self.mid,
        )
        return pd.DataFrame(res, columns=["features", "importance"])

    def delete(self) -> None:
        """
        Delete model itself.

        Args:
            No arguments for this method.

        Returnes:
            None: Nothing to return if process finished successfully.

        Raises:
            If deletion process failed with some reason,
            it raises OperationFailed exception.
        """
        response = _v3.delete_model(
            id_token=self.project.user.id_token,
            team_id=self.project.team_id,
            pid=self.project.project_id,
            mid=self.model_id,
        )
        if response["status"] != 0:
            raise OperationFailed(f"Model deletion is failed: {response['message']}")

        if self.model_id in self.project._models:
            self.project._models.pop(self.model_id)

        logger.info(f"The model is successfully deleted: {self.model_id}")

    def update(self):
        """
        Update name, status, target and features
        """
        document = self._document

        # self.name = document["name"]
        # self.description = document.get("desc")
        # self.type = document.get("type")
        # self.target = document.get("target")
        # self.features = document.get("features")
        # self.score = document.get("score")
        # self.created_at = document.get("createdAt")
        for key in document.keys():
            setattr(self, key, document.get(key))

        if document["status"] == Status.COMPLETED.value:
            self.status = Status.COMPLETED
        else:
            self.status = Status(document["status"])

        logger.info(f"Training '{self.name}': {self.status.value}")

    def wait_until_done(self):
        """
        Wait until ForecastFlow finish training.
        """
        while self.status != Status.COMPLETED and self.status != Status.ERROR:
            self.update()
            time.sleep(5)

        if self.status == Status.ERROR:
            document = self._document
            error_info = document.get("errorInfo")
            if error_info is None:
                raise OperationFailed("Training quit with Error")
            else:
                raise OperationFailed(
                    f"{error_info['message']}\n"
                    f"error_log_id: {error_info['errorLogId']}"
                )
