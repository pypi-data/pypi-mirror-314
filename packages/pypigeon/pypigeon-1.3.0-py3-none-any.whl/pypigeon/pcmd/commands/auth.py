from pypigeon.pigeon_core.api.auth import auth_get_session
from pypigeon.pigeon_core.models import AuthGetSessionResponse200

from .base_commands import BaseCommands


class AuthCommands(BaseCommands):
    """Authentication and authorization operations"""

    def whoami(self) -> None:
        """Information about your current session"""
        session = auth_get_session.sync(client=self.core)
        if not isinstance(session, AuthGetSessionResponse200):
            raise Exception("could not read session")

        self._output(session.to_dict())
