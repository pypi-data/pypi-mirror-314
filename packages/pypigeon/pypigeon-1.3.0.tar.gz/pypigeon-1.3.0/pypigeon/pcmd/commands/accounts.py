from pypigeon.pigeon_core.api.account import account_create_account
from pypigeon.pigeon_core.models import AccountCreateAccountBody

from .base_commands import BaseCommands


class AccountsCommands(BaseCommands):
    """Operations on accounts"""

    @BaseCommands._with_arg("name")
    def new(self) -> None:
        """Create a new account."""
        rv = account_create_account.sync(
            body=AccountCreateAccountBody(name=self.args.name), client=self.core
        )

        self._output(rv.to_dict())
