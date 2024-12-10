from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.store_agent_labels_type_0 import StoreAgentLabelsType0
    from ..models.store_configuration import StoreConfiguration


T = TypeVar("T", bound="StoreAgent")


@_attrs_define
class StoreAgent:
    """Store agent

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        configuration (Union[Unset, List['StoreConfiguration']]): Store agent configuration
        description (Union[Unset, str]): Store agent description
        display_name (Union[Unset, str]): Store agent display name
        image (Union[Unset, str]): Store agent image
        labels (Union['StoreAgentLabelsType0', None, Unset]): Store agent labels
        name (Union[Unset, str]): Store agent name
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    configuration: Union[Unset, List["StoreConfiguration"]] = UNSET
    description: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    labels: Union["StoreAgentLabelsType0", None, Unset] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.store_agent_labels_type_0 import StoreAgentLabelsType0

        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        configuration: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = []
            for configuration_item_data in self.configuration:
                configuration_item = configuration_item_data.to_dict()
                configuration.append(configuration_item)

        description = self.description

        display_name = self.display_name

        image = self.image

        labels: Union[Dict[str, Any], None, Unset]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, StoreAgentLabelsType0):
            labels = self.labels.to_dict()
        else:
            labels = self.labels

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if image is not UNSET:
            field_dict["image"] = image
        if labels is not UNSET:
            field_dict["labels"] = labels
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.store_agent_labels_type_0 import StoreAgentLabelsType0
        from ..models.store_configuration import StoreConfiguration

        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        configuration = []
        _configuration = d.pop("configuration", UNSET)
        for configuration_item_data in _configuration or []:
            configuration_item = StoreConfiguration.from_dict(configuration_item_data)

            configuration.append(configuration_item)

        description = d.pop("description", UNSET)

        display_name = d.pop("display_name", UNSET)

        image = d.pop("image", UNSET)

        def _parse_labels(data: object) -> Union["StoreAgentLabelsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                labels_type_0 = StoreAgentLabelsType0.from_dict(data)

                return labels_type_0
            except:  # noqa: E722
                pass
            return cast(Union["StoreAgentLabelsType0", None, Unset], data)

        labels = _parse_labels(d.pop("labels", UNSET))

        name = d.pop("name", UNSET)

        store_agent = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            configuration=configuration,
            description=description,
            display_name=display_name,
            image=image,
            labels=labels,
            name=name,
        )

        store_agent.additional_properties = d
        return store_agent

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
