import importlib


def get_simple_serializer_class(name):
    module = importlib.import_module('apps.notification.serializers')
    serializer_class = None

    if name == 'namespace':
        serializer_class = module.NamespaceSerializer

    if name == 'group':
        serializer_class = module.SimpleGroupSerializer

    return serializer_class
