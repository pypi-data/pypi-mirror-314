from bioblend.galaxy.objects import wrappers
from django.db import models

from .history import History
from .invocation import Invocation
from .galaxy_element import GalaxyElement

from django_to_galaxy.utils import load_galaxy_invocation_time_to_datetime


class Workflow(GalaxyElement):
    """Table for Galaxy workflows."""

    galaxy_owner = models.ForeignKey(
        "GalaxyUser", null=False, on_delete=models.CASCADE, related_name="workflows"
    )
    """Galaxy user that owns the workflow."""

    @property
    def galaxy_workflow(self) -> wrappers.Workflow:
        """Galaxy object using bioblend."""
        if getattr(self, "_galaxy_workflow", None) is None:
            self._galaxy_workflow = self._get_galaxy_workflow()
        return self._galaxy_workflow

    def _get_galaxy_workflow(self) -> wrappers.Workflow:
        """Get galaxy object using bioblend."""
        return self.galaxy_owner.obj_gi.workflows.get(self.galaxy_id)

    def invoke(self, datamap: dict, history: History) -> wrappers.Invocation:
        """
        Invoke workflow using bioblend.

        Args:
            datamap: dictionnary to link dataset to workflow inputs
            history: history obj the dataset(s) come from

        Returns:
            Invocation object from bioblend
        """
        galaxy_inv = self.galaxy_workflow.invoke(
            datamap, history=history.galaxy_history
        )
        # Create invocations
        invocation = Invocation(
            galaxy_id=galaxy_inv.id,
            galaxy_state=galaxy_inv.state,
            workflow=self,
            history=history,
            create_time=load_galaxy_invocation_time_to_datetime(galaxy_inv),
        )
        invocation.save()
        # Create output files
        invocation.create_output_files()
        return invocation

    def __repr__(self):
        return f"Workflow: {super().__str__()}"
