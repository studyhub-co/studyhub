from celery import shared_task


@shared_task
def build_sandbox(material_type_uuid, sandbox_type='create_react_app'):

    if sandbox_type == 'create_react_app':
        # TODO build and save built on S3
        return 'success'
    return 'selected type is not support'
