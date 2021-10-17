from io import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import permissions, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser


from courses.models import MaterialProblemType, MaterialProblemTypeSandboxCache

from ...serializers import MaterialProblemTypeSerializer, \
    MaterialProblemTypeSandboxCacheSerializer
from ...permissions import IsMaterialProblemTypeAuthor

from ...tasks import build_sandbox

from .pagination import StandardResultsSetPagination


class MaterialProblemTypeViewSet(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.DestroyModelMixin,
                                 # MaterialTypeModulesMixin,
                                 viewsets.GenericViewSet,
                                 ):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsMaterialProblemTypeAuthor)
    pagination_class = StandardResultsSetPagination
    serializer_class = MaterialProblemTypeSerializer
    serializer_class_cache = MaterialProblemTypeSandboxCacheSerializer
    # serializer_class_module = MaterialProblemTypeSandboxModuleSerializer
    queryset = MaterialProblemType.objects.\
        select_related('author__user__profile'). \
        prefetch_related('modules__author__user__profile',
                         'directories',
                         'modules'
                         ).all()
    lookup_field = 'uuid'

    # override RetrieveModelMixin
    def retrieve(self, request, *args, **kwargs):
        if 'uuid' in kwargs and kwargs['uuid'] == 'new':
            # get or create 'new' sandbox skeleton
            try:
                instance = self.queryset.get(slug='new')
            except MaterialProblemType.DoesNotExist:
                assert False, 'You need to create a sanbdox with "new" slug berofe using this app! ' \
                              '(manage.py loaddata from fixtures)'
                # instance = self.create_new_from_json(request)
        else:
            # regular instance
            instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # @transaction.atomic
    # TODO rewrite with SQL
    def clone_sandbox(self):
        # clone sandbox
        initial_sandbox = self.get_object()

        initial_modules = initial_sandbox.modules.all()
        initial_directories = initial_sandbox.directories.all()

        # clone sandbox
        # based on https://docs.djangoproject.com/en/2.2/topics/db/queries/#copying-model-instances
        initial_sandbox.pk = None
        initial_sandbox.uuid = None
        initial_sandbox.official = False
        initial_sandbox.save()

        new_old_dir_pks = {}

        # clone directories
        for directory in initial_directories:
            old_dir_pk = directory.pk

            directory.pk = None
            directory.sandbox = initial_sandbox
            directory.save()
            new_dir_pk = directory.pk

            new_old_dir_pks[old_dir_pk] = new_dir_pk

        # re-save parent
        for directory in initial_sandbox.directories.all():
            if directory.directory:
                directory.directory_id = new_old_dir_pks[directory.directory_id]
                directory.save()

        # clone modules
        for module in initial_modules:
            module.pk = None
            module.sandbox = initial_sandbox

            if module.directory:
                module.directory_id = new_old_dir_pks[module.directory_id]

            module.save()

        return initial_sandbox

    # fork sandbox/MaterialProblemType
    @action(methods=['POST'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated, ], )
    def fork(self, request, *args, **kwargs):

        forked_material_problem_type = self.clone_sandbox()

        serializer = self.get_serializer(forked_material_problem_type)

        return Response(serializer.data)

    # publish sandbox/MaterialProblemType
    # call publish celery task
    @action(methods=['POST'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated, IsMaterialProblemTypeAuthor], )
    def publish(self, request, *args, **kwargs):

        # forked_material_problem_type = self.clone_sandbox()
        #
        # serializer = self.get_serializer(forked_material_problem_type)
        uuid = self.get_object().uuid
        build_sandbox.delay(str(uuid))
        return Response({'state': 'start'})

    @action(methods=['POST'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated, ], )
    # TODO check problem type owner permission
    def cache(self, request, *args, **kwargs):
        # save transpiled data

        # get version
        version = request.data.get('version', None)
        if not version:
            raise ValidationError('version field not found')

        sandbox = self.get_object()

        json_data = request.data.get('data', None)

        if not json_data:
            raise ValidationError('data field not found')

        buff = StringIO(json_data)

        buff.seek(0, 2)
        file_data = InMemoryUploadedFile(buff, 'data', 'file_name', None, buff.tell(), None)

        # FIXME why we need to check is str?
        # if type(json_data) is str:
        #     json_data = json.loads(json_data)

        data = {'data': file_data, 'version': version}

        try:
            # try to get existing cache
            cache = MaterialProblemTypeSandboxCache.objects.get(
                version=version,
                sandbox=sandbox
            )
            serializer = self.serializer_class_cache(cache, data=data)
        except MaterialProblemTypeSandboxCache.DoesNotExist:
            serializer = self.serializer_class_cache(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(sandbox=sandbox)

        return Response(serializer.data)