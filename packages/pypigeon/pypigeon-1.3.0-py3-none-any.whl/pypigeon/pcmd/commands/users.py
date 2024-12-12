from pypigeon.pigeon_core.api.user import user_delete_user
from pypigeon.pigeon_core.api.user import user_get_users
from pypigeon.pigeon_core.models import UserGetUsersResponse200
from pypigeon.pigeon_core.paginator import Paginator

from .base_commands import BaseCommands


class UsersCommands(BaseCommands):
    """Operations on users"""

    def list(self) -> None:
        """List users."""
        pager = Paginator[UserGetUsersResponse200](user_get_users, self.core)

        data = []
        for page in pager.paginate():
            data.extend([u.to_dict() for u in page.users])

        self._output(data, preferred_type="table")

    @BaseCommands._with_arg("username")
    def delete(self) -> None:
        """Delete a user."""
        user_delete_user.sync(self.args.username, client=self.core)
