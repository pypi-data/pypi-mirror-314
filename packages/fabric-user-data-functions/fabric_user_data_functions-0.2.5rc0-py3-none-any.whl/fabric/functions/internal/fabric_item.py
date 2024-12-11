import typing


class FabricItem:
    def __init__(self, alias_name: str, endpoints: typing.Dict[str, typing.Dict[str, str]]):
        self.__alias_name = alias_name
        self.__endpoints = endpoints

    @property
    def alias_name(self) -> typing.Optional[str]:
        return self.__alias_name

    @property
    def endpoints(self) -> typing.Optional[typing.Dict[str, typing.Dict[str, str]]]: # noqa TAE002
        return self.__endpoints
