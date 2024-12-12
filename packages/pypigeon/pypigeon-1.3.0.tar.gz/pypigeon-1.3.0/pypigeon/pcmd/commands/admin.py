from pypigeon.pigeon_core.api.admin import admin_grant_admin
from pypigeon.pigeon_core.api.admin import admin_list_admins
from pypigeon.pigeon_core.models import AdminGrantAdminAdminListRequest
from pypigeon.pigeon_core.models import AdminOperationsItem

from .base_commands import BaseCommands
from .config import ConfigCommands


class AdminCommands(BaseCommands):
    """Administrative operations"""

    config = ConfigCommands

    def list_admins(self) -> None:
        """List system admins and privileges."""
        rv = admin_list_admins.sync(client=self.core)

        self._output(
            [
                {"subject_id": r.subject_id, "operations": ",".join(r.operations)}
                for r in rv.grants
            ],
            preferred_type="table",
        )

        if rv.operations:
            print()
            print("Operations:")
            for op in rv.operations:
                print("-", op)

    @BaseCommands._with_arg("subject_id")
    @BaseCommands._with_arg("operations", nargs="+")
    def grant_admin(self) -> None:
        """Grant admin privilege to a subject ID."""
        rv = admin_list_admins.sync(client=self.core)

        for grant in rv.grants:
            if grant.subject_id == self.args.subject_id:
                grant.operations = list(
                    set(grant.operations)
                    | {AdminOperationsItem(op) for op in self.args.operations}
                )

        admin_grant_admin.sync(
            body=AdminGrantAdminAdminListRequest(grants=rv.grants), client=self.core
        )

        print("Updated", self.args.subject_id, " -- now admins are:")
        self.list_admins()

    @BaseCommands._with_arg("subject_id")
    def revoke_admin(self) -> None:
        """Revoke all admin privileges from a user."""
        admins = admin_list_admins.sync(client=self.core)

        new_grants = [g for g in admins.grants if g.subject_id != self.args.subject_id]
        if new_grants == admins.grants:
            raise ValueError(f"{self.args.subject_id} is not listed in admins")

        admin_grant_admin.sync(
            body=AdminGrantAdminAdminListRequest(grants=new_grants), client=self.core
        )
