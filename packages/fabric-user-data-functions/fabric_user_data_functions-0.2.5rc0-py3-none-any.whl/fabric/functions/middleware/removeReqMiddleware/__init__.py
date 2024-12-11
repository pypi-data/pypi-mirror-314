# flake8: noqa: I005
from typing import Dict, Optional
from azure.functions import AppExtensionBase, Context, HttpRequest
from logging import Logger

REQ_PARAMETER = 'req'

class RemoveReqExtension(AppExtensionBase):

    @classmethod
    def init(cls):
        cls.requests: Dict[str, HttpRequest] = {}

    @classmethod
    def pre_invocation_app_level(
        cls, logger: Logger, context: Context,
        func_args: Dict[str, object],
        *args, **kwargs
    ) -> None:
        # Remove the request object from the function arguments
        cls.requests[context.invocation_id] = func_args[REQ_PARAMETER]
        del func_args[REQ_PARAMETER]

    @classmethod
    def post_invocation_app_level(
        cls, logger: Logger, context: Context,
        func_args: Dict[str, object],
        func_ret: Optional[object],
        *args, **kwargs
    ) -> None:
        if context.invocation_id in cls.requests:
            func_args[REQ_PARAMETER] = cls.requests[context.invocation_id]