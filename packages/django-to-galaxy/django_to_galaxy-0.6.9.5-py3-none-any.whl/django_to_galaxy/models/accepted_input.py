from django.db import models


class Format(models.Model):
    format = models.CharField(max_length=200, unique=True)
    """Format on the galaxy side."""

    def __str__(self):
        return f"{self.format}"


class WorkflowInput(models.Model):
    galaxy_step_id = models.IntegerField(null=False)
    """Step id on the galaxy side."""
    label = models.CharField(max_length=100, blank=True)
    """Label on the galaxy side."""
    workflow = models.ForeignKey("Workflow", null=False, on_delete=models.CASCADE)
    """Workflow id."""
    formats = models.ManyToManyField("Format")
    """Accepted input formats on the galaxy side."""
    optional = models.BooleanField(default=False)
    """Workflow input optional information on the galaxy side."""

    def __str__(self):
        return f"{self.label} of {self.workflow!r}"

    def __repr__(self):
        return f"Input: {self!s}"
