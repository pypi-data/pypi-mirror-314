######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.36.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-09T17:36:48.610720                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException
from .core import resolve_root as resolve_root

TYPE_CHECKING: bool

class UnresolvableDatastoreException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def init_datastorage_object():
    ...

def resolve_storage_backend(pathspec: typing.Union[str, "metaflow.Task"] = None):
    ...

