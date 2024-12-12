from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.tool_call_type import ToolCallType, check_tool_call_type

if TYPE_CHECKING:
    from ..models.function import Function


T = TypeVar("T", bound="ToolCall")


@_attrs_define
class ToolCall:
    """
    Attributes:
        function (Function):
        id (str):
        type_ (ToolCallType):
    """

    function: "Function"
    id: str
    type_: ToolCallType

    def to_dict(self) -> dict[str, Any]:
        function = self.function.to_dict()

        id = self.id

        type_: str = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Function": function,
                "ID": id,
                "Type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.function import Function

        d = src_dict.copy()
        function = Function.from_dict(d.pop("Function"))

        id = d.pop("ID")

        type_ = check_tool_call_type(d.pop("Type"))

        tool_call = cls(
            function=function,
            id=id,
            type_=type_,
        )

        return tool_call
