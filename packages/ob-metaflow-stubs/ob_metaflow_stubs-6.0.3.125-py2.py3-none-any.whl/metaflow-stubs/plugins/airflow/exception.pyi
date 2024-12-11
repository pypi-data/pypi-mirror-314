######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.36.3+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-10T22:06:22.160043                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

