from typing import Any, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentDeploymentHistoryEvent")


@_attrs_define
class AgentDeploymentHistoryEvent:
    """Agent deployment history event

    Attributes:
        end (Union[None, Unset, str]): End time
        error (Union[None, Unset, str]): Error message
        name (Union[Unset, str]): Name of the function or agent
        parameters (Union[Unset, str]): Parameters
        start (Union[None, Unset, str]): Start time
        status (Union[Unset, str]): Status, eg: running, success, failed
        sub_function (Union[None, Unset, str]): Function used in kit if a kit was used
        took (Union[None, Unset, int]): Number of milliseconds it took to complete the event
        type (Union[Unset, str]): Type, one of function or agent
    """

    end: Union[None, Unset, str] = UNSET
    error: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    parameters: Union[Unset, str] = UNSET
    start: Union[None, Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    sub_function: Union[None, Unset, str] = UNSET
    took: Union[None, Unset, int] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end: Union[None, Unset, str]
        if isinstance(self.end, Unset):
            end = UNSET
        else:
            end = self.end

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        name = self.name

        parameters = self.parameters

        start: Union[None, Unset, str]
        if isinstance(self.start, Unset):
            start = UNSET
        else:
            start = self.start

        status = self.status

        sub_function: Union[None, Unset, str]
        if isinstance(self.sub_function, Unset):
            sub_function = UNSET
        else:
            sub_function = self.sub_function

        took: Union[None, Unset, int]
        if isinstance(self.took, Unset):
            took = UNSET
        else:
            took = self.took

        type = self.type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if end is not UNSET:
            field_dict["end"] = end
        if error is not UNSET:
            field_dict["error"] = error
        if name is not UNSET:
            field_dict["name"] = name
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if start is not UNSET:
            field_dict["start"] = start
        if status is not UNSET:
            field_dict["status"] = status
        if sub_function is not UNSET:
            field_dict["sub_function"] = sub_function
        if took is not UNSET:
            field_dict["took"] = took
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_end(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end = _parse_end(d.pop("end", UNSET))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        name = d.pop("name", UNSET)

        parameters = d.pop("parameters", UNSET)

        def _parse_start(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        start = _parse_start(d.pop("start", UNSET))

        status = d.pop("status", UNSET)

        def _parse_sub_function(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sub_function = _parse_sub_function(d.pop("sub_function", UNSET))

        def _parse_took(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        took = _parse_took(d.pop("took", UNSET))

        type = d.pop("type", UNSET)

        agent_deployment_history_event = cls(
            end=end,
            error=error,
            name=name,
            parameters=parameters,
            start=start,
            status=status,
            sub_function=sub_function,
            took=took,
            type=type,
        )

        agent_deployment_history_event.additional_properties = d
        return agent_deployment_history_event

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
