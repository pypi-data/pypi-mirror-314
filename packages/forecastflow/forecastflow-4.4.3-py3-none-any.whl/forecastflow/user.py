import logging
from typing import TYPE_CHECKING, Dict, Optional, List

from . import project
from . import _auth
from .util import ExpirationTimer
from forecastflow.api import _v3

if TYPE_CHECKING:
    from . import Project

logger = logging.getLogger(__name__)


class User:
    """
    ForecastFlow user class
    """

    def __init__(self, email: str, password: str) -> None:
        """
        Instantiate object with e-mail and password.

        Args:
            email (str): E-mail to sign in.
            password (str): password for sign in.
        """
        res = _auth.sign_in_with_password(email, password)
        self._id_token: str = res['idToken']
        self.user_id: str = res['localId']
        self._refresh_token: str = res['refreshToken']
        self._expiration_timer = ExpirationTimer(
            int(res['expiresIn']) - 10
        )  # refresh 10 seconds earlier
        self._projects: Dict[str, 'Project'] = {}

    def get_project(self, project_id: str, team_id: Optional[str] = None) -> 'Project':
        """
        Get project with given pid.

        Args:
            project_id:
                Project ID you want to open.

        Returns:
            ForecastFlow Project object with given pid.
        """
        if project_id not in self._projects:
            self._projects[project_id] = project.Project(self, project_id, team_id)
        return self._projects[project_id]
    
    def list_teams(self) -> List[dict]:
        """
        List teams belong to the user.

        Returns:
            List of teams as a type List[dict].
        """
        teams: List[dict] = _v3.list_teams_info(id_token=self._id_token)

        return teams
    
    def list_projects(
            self,
            team_id: str,
            current_page: int = 1,
            items_per_page: int = 50,
            order_type: str = 'asc'
        ) -> List[dict]:
        """
        List projects with a given team id.

        Args:
            team_id (str): team id to fetch related projects.
            current_page (int, optional): Current page number defaults to 1.
            items_per_page (int, optional): Number of items per page defaults to 50.
            order_type (str, optional): Specify asc or desc to order returned projects defaults to asc.

        Returns:
            List of projects data as a type List[dict].
        """
        response: dict = _v3.list_projects_info(
            id_token=self._id_token,
            team_id=team_id,
            current_page=current_page,
            items_per_page=items_per_page,
            order_type=order_type,
        )

        # Rename keys from camel case to snake case for python convention.
        items = []
        for project in response['projectsInfo']:
            items.append({
                'id': project['id'],
                'name': project['name'],
                'desc': project['desc'],
                'created_at': project['createdAt'],
                'last_modified_at': project['lastModifiedAt'],
            })
        
        return {
            'items': items,
            'current_page': response['currentPage'],
            'items_per_page': response['itemsPerPage'],
            'total_items': response['totalItems'],
            'total_pages': response['totalPages']
        }

    @property
    def id_token(self) -> str:
        """
        This method refreshes a ID token if expired.
        """
        if self._expiration_timer.is_expired:
            logger.info('ID Token is expired. Refreshing.')
            res = _auth.refresh_id_token(self._refresh_token)
            id_token: str = res['id_token']
            self._id_token = id_token
            self._expiration_timer = ExpirationTimer(
                int(res['expires_in']) - 10  # refresh 10 seconds earlier
            )
        return self._id_token

    @property
    def uid(self) -> str:
        return self.user_id
