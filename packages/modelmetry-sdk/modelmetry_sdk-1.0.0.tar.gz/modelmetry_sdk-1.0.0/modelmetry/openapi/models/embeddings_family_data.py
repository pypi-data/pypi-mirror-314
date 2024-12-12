from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.options import Options


T = TypeVar("T", bound="EmbeddingsFamilyData")


@_attrs_define
class EmbeddingsFamilyData:
    """
    Attributes:
        inputs (Union[None, list[str]]):
        options (Options):
    """

    inputs: Union[None, list[str]]
    options: "Options"

    def to_dict(self) -> dict[str, Any]:
        inputs: Union[None, list[str]]
        if isinstance(self.inputs, list):
            inputs = self.inputs

        else:
            inputs = self.inputs

        options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Inputs": inputs,
                "Options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.options import Options

        d = src_dict.copy()

        def _parse_inputs(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                inputs_type_0 = cast(list[str], data)

                return inputs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        inputs = _parse_inputs(d.pop("Inputs"))

        options = Options.from_dict(d.pop("Options"))

        embeddings_family_data = cls(
            inputs=inputs,
            options=options,
        )

        return embeddings_family_data
