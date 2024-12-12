import re

def is_url(path: object):
    """Check if the path is a url or something else.

    Args:
        path: path of the file
    """
    return isinstance(path, str) and re.match(r"^(http://|https://)", path.lower())


def is_resource(path: object):
    """Check if the path is a reference to a dataset resource.

    Args:
        path: path of the file
    """

    RESOURCE_PREFIX_STR = 'resource://'

    return isinstance(path, str) and path[0:len(RESOURCE_PREFIX_STR)] == RESOURCE_PREFIX_STR