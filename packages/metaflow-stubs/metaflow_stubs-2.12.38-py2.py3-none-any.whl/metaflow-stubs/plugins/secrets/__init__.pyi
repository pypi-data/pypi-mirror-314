######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.38                                                                                #
# Generated on 2024-12-08T03:54:57.938741                                                            #
######################################################################################################

from __future__ import annotations

import typing
import abc
if typing.TYPE_CHECKING:
    import abc

from . import secrets_decorator as secrets_decorator
from . import inline_secrets_provider as inline_secrets_provider

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

