import django.apps
from django.db.models.fields.files import FieldFile
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.status import HTTP_404_NOT_FOUND

from django_to_galaxy.models import History, Workflow, GalaxyUser
from django_to_galaxy.api.serializers.invoke_workflow import (
    InvokeWorkflowSerializer,
    ExecuteWorkflowSerializer,
)


class InvokeWorkflowView(GenericAPIView):
    serializer_class = InvokeWorkflowSerializer

    @swagger_auto_schema(
        operation_description="Invoke workflow using data from a history.",
        operation_summary="Invoke workflow using data from a history.",
        tags=["workflows"],
    )
    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # Retrieve history
        try:
            history = History.objects.get(id=data["history_id"])
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": (
                        "Galaxy history with id ",
                        f"<{data['history_id']}> not found!",
                    )
                },
                status=HTTP_404_NOT_FOUND,
            )
        # Retrieve workflow
        try:
            workflow = Workflow.objects.get(id=data["workflow_id"])
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": (
                        "Galaxy workflow with id ",
                        f"<{data['history_id']}> not found!",
                    )
                },
                status=HTTP_404_NOT_FOUND,
            )
        inv = workflow.invoke(data["datamap"], history=history)
        data["message"] = "Workflow successfully invoked."
        data["invocation_id"] = inv.id
        return Response(data=data)


class GetWorkflowDatamapTemplateView(RetrieveAPIView):
    queryset = Workflow.objects.all()

    @swagger_auto_schema(
        operation_description="Get workflow datamap to prepare workflow invocation.",
        operation_summary="Get workflow datamap to prepare workflow invocation.",
        tags=["workflows"],
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        inputs = instance.galaxy_workflow.inputs
        steps = instance.galaxy_workflow.steps
        input_mapping = {}
        datamap_template = {}
        for input_id, input_dict in inputs.items():
            input_mapping[input_id] = {}
            input_mapping[input_id]["label"] = input_dict["label"]
            input_mapping[input_id]["type"] = steps[input_id].type
            input_mapping[input_id]["tool_inputs"] = steps[input_id].tool_inputs

            if steps[input_id].type == "parameter_input":
                datamap_template[input_id] = input_mapping[input_id]["tool_inputs"][
                    "parameter_type"
                ]
            else:
                datamap_template[input_id] = {"id": "", "src": "hda"}
            # TODO: Add template for a collection input

        return Response(
            data={"input_mapping": input_mapping, "datamap_template": datamap_template}
        )


class ExecuteWorkflowView(GenericAPIView):
    serializer_class = ExecuteWorkflowSerializer

    @swagger_auto_schema(
        operation_description="Execute workflow using data from a model and a Galaxy user.",
        operation_summary="Execute workflow using data from a model and a Galaxy user.",
        tags=["workflows"],
    )
    def post(self, request):
        # Get data from POST request
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # Create History -> @TODO to refactor in function
        # - First retrieve galaxy user
        galaxy_user_id = data["galaxy_user_id"]
        try:
            galaxy_user = GalaxyUser.objects.get(id=galaxy_user_id)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": (
                        "Galaxy User with id ",
                        f"<{galaxy_user_id}> not found!",
                    )
                },
                status=HTTP_404_NOT_FOUND,
            )
        history = galaxy_user.create_history()
        # Upload data to history -> @TODO to refactor in function
        # - Retrieve all models
        all_models = django.apps.apps.get_models()
        all_models_dict = {m.__name__.lower(): m for m in all_models}
        fake_datamap = data["fake_datamap"]
        # - Upload each data to history
        datamap = {}
        for input_id, input_object in fake_datamap.items():
            try:
                file = all_models_dict[input_object["model"]].objects.get(
                    id=input_object["id"]
                )
            except ObjectDoesNotExist:
                return Response(
                    {"message": f"File with id <{input_object['id']}> not found!"},
                    status=HTTP_404_NOT_FOUND,
                )
            try:
                file_path = getattr(file, input_object["path_field"])
            except AttributeError:
                return Response(
                    {"message": f"File with id <{input_object['id']}> not found!"},
                    status=HTTP_404_NOT_FOUND,
                )
            if isinstance(file_path, FieldFile):
                file_path = file_path.path
            try:
                file_type = input_object["file_type"]
            except AttributeError:
                return Response(
                    {"message": f"File with id <{input_object['id']}> not found!"},
                    status=HTTP_404_NOT_FOUND,
                )
            history_association = history.upload_file(file_path, file_type=file_type)
            datamap[input_id] = {"id": history_association.id, "src": "hda"}
        # Invoke workflow -> @TODO to refactor in function
        # - Retrieve workflow
        try:
            workflow = Workflow.objects.get(id=data["workflow_id"])
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": (
                        "Galaxy workflow with id ",
                        f"<{data['history_id']}> not found!",
                    )
                },
                status=HTTP_404_NOT_FOUND,
            )
        # - Invoke workflow
        inv = workflow.invoke(datamap, history=history)
        data["message"] = "Workflow successfully invoked."
        data["invocation_id"] = inv.id
        data["datamap"] = datamap
        return Response(data=data)
