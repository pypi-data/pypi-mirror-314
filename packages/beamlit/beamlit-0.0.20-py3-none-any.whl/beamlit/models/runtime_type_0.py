from typing import Any, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RuntimeType0")


@_attrs_define
class RuntimeType0:
    """Set of configurations for a deployment

    Attributes:
        args (Union[Unset, List[Any]]): The arguments to pass to the deployment runtime
        command (Union[Unset, List[Any]]): The command to run the deployment
        envs (Union[Unset, List[Any]]): The environment variables to set in the deployment. Should be a list of
            Kubernetes EnvVar types
        image (Union[Unset, str]): The Docker image for the deployment
        model (Union[Unset, str]): The slug name of the origin model. Only used if the deployment is a ModelDeployment
        type (Union[Unset, str]): The type of origin for the deployment
    """

    args: Union[Unset, List[Any]] = UNSET
    command: Union[Unset, List[Any]] = UNSET
    envs: Union[Unset, List[Any]] = UNSET
    image: Union[Unset, str] = UNSET
    model: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        args: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        command: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        envs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = self.envs

        image = self.image

        model = self.model

        type = self.type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args
        if command is not UNSET:
            field_dict["command"] = command
        if envs is not UNSET:
            field_dict["envs"] = envs
        if image is not UNSET:
            field_dict["image"] = image
        if model is not UNSET:
            field_dict["model"] = model
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        args = cast(List[Any], d.pop("args", UNSET))

        command = cast(List[Any], d.pop("command", UNSET))

        envs = cast(List[Any], d.pop("envs", UNSET))

        image = d.pop("image", UNSET)

        model = d.pop("model", UNSET)

        type = d.pop("type", UNSET)

        runtime_type_0 = cls(
            args=args,
            command=command,
            envs=envs,
            image=image,
            model=model,
            type=type,
        )

        runtime_type_0.additional_properties = d
        return runtime_type_0

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
