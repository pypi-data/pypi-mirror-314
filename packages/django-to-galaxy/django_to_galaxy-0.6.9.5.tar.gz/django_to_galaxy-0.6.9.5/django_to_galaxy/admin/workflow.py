from django.contrib import admin

from django_to_galaxy.models.workflow import Workflow
from django_to_galaxy.models.accepted_input import WorkflowInput, Format

from .galaxy_element import GalaxyElementAdmin


@admin.register(Workflow)
class WorkflowAdmin(GalaxyElementAdmin):
    list_display = (
        "id",
        "name",
        "annotation",
        "galaxy_id",
        "published",
        "galaxy_owner",
        "get_tags",
    )
    readonly_fields = (
        "id",
        "name",
        "annotation",
        "galaxy_id",
        "published",
        "galaxy_owner",
        "get_tags",
    )

    def get_tags(self, obj):
        return ", ".join([p.label for p in obj.tags.all()])


@admin.register(Format)
class FormatAdmin(GalaxyElementAdmin):
    list_display = (
        "id",
        "format",
    )
    readonly_fields = (
        "id",
        "format",
    )


@admin.register(WorkflowInput)
class WorkflowInputAdmin(GalaxyElementAdmin):
    list_display = (
        "id",
        "galaxy_step_id",
        "label",
        "workflow",
        "get_formats",
        "optional",
    )
    readonly_fields = (
        "id",
        "galaxy_step_id",
        "label",
        "workflow",
        "get_formats",
        "optional",
    )

    def get_formats(self, obj):
        return ", ".join([p.format for p in obj.formats.all()])
