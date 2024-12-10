import os

from onecode import file_output


def geo_file_output(
    path: str,
    type: str,
    prefix: str = "",
    group: bool = False,
    release: bool = False,
    key: str = None,
    **kwargs
):
    extra = {}
    groupping = {}

    if group:
        filename, _ = os.path.splitext(path)
        if os.path.isdir(path):
            extra = { 'regex': '.*' }
        else:
            extra = { 'regex': f'.*({os.path.basename(filename)}).*' }

        groupping = { 'group': True }

    if release:
        extra = {
            **extra,
            'release': True
        }

    return file_output(
        **{
            'key': key if key is not None else path,
            'value': path,
            'properties': {
                'type': type,
                **extra,
            },
            'file_version_props': {
                **kwargs
            },
            **groupping,
            'outputPath': os.path.dirname(os.path.join('/', os.path.relpath(path, prefix)))
        },
        make_path=True
    )
