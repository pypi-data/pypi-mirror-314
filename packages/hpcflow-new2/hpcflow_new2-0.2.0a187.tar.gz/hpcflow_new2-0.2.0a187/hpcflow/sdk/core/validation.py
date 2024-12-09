"""
Schema management.
"""

from importlib import resources

from valida import Schema


def get_schema(filename):
    """
    Get a valida `Schema` object from the embedded data directory.

    Parameter
    ---------
    schema: str
        The name of the schema file within the resources package
        (:py:mod:`hpcflow.sdk.data`).
    """
    package = "hpcflow.sdk.data"
    try:
        fh = resources.files(package).joinpath(filename).open("rt")
    except AttributeError:
        # < python 3.9; `resource.open_text` deprecated since 3.11
        fh = resources.open_text(package, filename)
    schema_dat = fh.read()
    fh.close()
    schema = Schema.from_yaml(schema_dat)
    return schema
