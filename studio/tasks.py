import json
import requests
import base64
import io
import tarfile

from functools import wraps

from celery import shared_task

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from courses.models import MaterialProblemType


# https://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html#ensuring-a-task-is-only-executed-one-at-a-time
def skip_if_running(f):
    task_name = f'{f.__module__}.{f.__name__}'

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        workers = self.app.control.inspect().active()

        for worker, tasks in workers.items():
            for task in tasks:
                # if (task_name == task['name'] and
                #         tuple(args) == tuple(task['args']) and
                #         kwargs == task['kwargs'] and
                #         self.request.id != task['id']):
                #     return f'task {task_name} ({args}, {kwargs}) is running on {worker}, skipping'

                # ensure that we have only one task of any deploying at time
                if task_name == task['name'] and self.request.id != task['id']:
                    return f'task {task_name} is running on {worker}, skipping'

        return f(self, *args, **kwargs)

    return wrapped


def recursive_delete(full_path):
    dirs, files = default_storage.listdir(full_path)
    for file in files:
        filepath = f'{full_path}{file}'
        default_storage.delete(filepath)
    for _dir in dirs:
        new_dir = f'{full_path}{_dir}/'
        recursive_delete(new_dir)


@shared_task(bind=True)
@skip_if_running
def build_sandbox(self, material_type_uuid, sandbox_type='create_react_app'):
    if sandbox_type == 'create_react_app':
        # TODO build and save built on S3
        mpt = MaterialProblemType.objects.get(uuid=material_type_uuid)

        # get sandbox
        if not mpt:
            return 'Material type not found'

        # convert file system structure to code-runner:
        # "files": [
        #     {
        #       "name": "main.py",
        #       "content": "print(input('Number from stdin: '))"
        #     }
        #   ]

        # create directory tree
        # TODO add Modified Preorder Tree Traversal method to sandbox FS structure (django-mptt)
        directories = []

        def populate_children(current_directory):
            for directory in mpt.directories.all():
                if directory.directory and str(directory.directory.uuid) == current_directory['uuid']:
                    new_child_dir = {
                        'uuid': str(directory.uuid),
                        'name': directory.name,
                        'path': "{}{}/".format(current_directory['path'], directory.name),
                        'children': []
                    }
                    populate_children(new_child_dir)
                    new_dir['children'].append(new_child_dir)

        # populate dirs
        for directory in mpt.directories.all():
            if not directory.directory:
                new_dir = {
                    'uuid': str(directory.uuid),
                    'name': directory.name,
                    'path': "{}/".format(directory.name),
                    'children': []
                }
                populate_children(new_dir)
                directories.append(new_dir)

        # populate files
        files = []
        tsconfig_in_place = False
        for module in mpt.modules.all():
            path = module.name
            if module.name == 'tsconfig.json':
                tsconfig_in_place = True

            if module.directory:
                # add file path if fine inside directory
                for _dir in directories:
                    if str(module.directory.uuid) == _dir['uuid']:
                        path = '{}{}'.format(_dir['path'], module.name)

            new_file = {
                'content': module.code,
                'name': path
            }
            files.append(new_file)

        if not tsconfig_in_place:
            pass
            # add default tsconfig.json
            # files.append({"content":
            #     json.dumps({
            #         'compilerOptions': {
            #             "module": "commonjs",
            #             "target": "ES6",
            #             "lib": [
            #                 "esnext.asynciterable",
            #                 "es6",
            #                 "dom",
            #                 "es2017.object",
            #                 "es2017.sharedmemory"
            #             ],
            #             "allowSyntheticDefaultImports": True,
            #             "resolveJsonModule": True,
            #             "jsx": "react",
            #             "allowJs": True,
            #             "noEmit": True,
            #             "strict": True
            #         },
            #         'exclude': [
            #             'node_modules',
            #             'build',
            #             'scripts',
            #             'acceptance-tests',
            #             'webpack',
            #             'jest',
            #             'src/setupTests.ts',
            #         ], }),
            #     "name": "tsconfig.json"
            # })
            # files.append({"content":
            #     json.dumps({
            #         'compilerOptions': {
            #             "module": "commonjs",
            #             "target": "ES6",
            #             "lib": [
            #                 "esnext.asynciterable",
            #                 "es6",
            #                 "dom",
            #                 "es2017.object",
            #                 "es2017.sharedmemory"
            #             ],
            #             "allowSyntheticDefaultImports": True,
            #             "resolveJsonModule": True,
            #             "jsx": "react",
            #             "allowJs": True,
            #             "noEmit": True,
            #             "strict": True
            #         },
            #         'exclude': [
            #             'node_modules',
            #             'build',
            #             'scripts',
            #             'acceptance-tests',
            #             'webpack',
            #             'jest',
            #             'src/setupTests.ts',
            #         ], }),
            #     "name": "tsconfig.json"
            # })

        request_data = {
            "image": "vermusl/create-react-app",
            "payload": {
                "language": "buildcreatereactapp",
                "files": files
            }
        }

        headers = {'X-Access-Token': settings.RUN_CODE_SERVER_ACCESS_TOKEN}

        r = requests.post(settings.RUN_CODE_SERVER_URL, data=json.dumps(request_data), headers=headers)

        json_result = r.json()
        # return info to celery task
        if json_result['error']:
            return r.text
        else:
            # save files in media storage
            base_path = 'mpt_builds/{}/'.format(material_type_uuid)

            if default_storage.exists(base_path):
                # delete old dir if exist
                recursive_delete(base_path)

            # TODO catch errors
            archive_binary = io.BytesIO(base64.b64decode(json_result['stdout']))
            with tarfile.open(fileobj=archive_binary, mode='r:gz') as tf:
                for tarinfo in tf.getmembers():
                    if tarinfo.isfile():
                        # unpack file and save it in django storage
                        default_storage.save(
                            '{}{}'.format(base_path, tarinfo.name),
                            ContentFile(tf.extractfile(tarinfo).read())
                        )
            return 'success'
    return 'selected type is not support'
