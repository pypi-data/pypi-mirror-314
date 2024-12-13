from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flavor import Flavor
    from ..models.policy_location import PolicyLocation


T = TypeVar("T", bound="PolicySpec")


@_attrs_define
class PolicySpec:
    """Policy specification

    Attributes:
        flavors (Union[Unset, List['Flavor']]): Types of hardware available for deployments
        locations (Union[Unset, List['PolicyLocation']]): PolicyLocations is a local type that wraps a slice of Location
        resource_types (Union[Unset, List[str]]): PolicyResourceTypes is a local type that wraps a slice of
            PolicyResourceType
        type (Union[Unset, str]): Policy type, can be location or flavor
    """

    flavors: Union[Unset, List["Flavor"]] = UNSET
    locations: Union[Unset, List["PolicyLocation"]] = UNSET
    resource_types: Union[Unset, List[str]] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flavors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                componentsschemas_flavors_item = (
                    componentsschemas_flavors_item_data.to_dict()
                )
                flavors.append(componentsschemas_flavors_item)

        locations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.locations, Unset):
            locations = []
            for componentsschemas_policy_locations_item_data in self.locations:
                componentsschemas_policy_locations_item = (
                    componentsschemas_policy_locations_item_data.to_dict()
                )
                locations.append(componentsschemas_policy_locations_item)

        resource_types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.resource_types, Unset):
            resource_types = self.resource_types

        type = self.type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if locations is not UNSET:
            field_dict["locations"] = locations
        if resource_types is not UNSET:
            field_dict["resourceTypes"] = resource_types
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.flavor import Flavor
        from ..models.policy_location import PolicyLocation

        d = src_dict.copy()
        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(
                componentsschemas_flavors_item_data
            )

            flavors.append(componentsschemas_flavors_item)

        locations = []
        _locations = d.pop("locations", UNSET)
        for componentsschemas_policy_locations_item_data in _locations or []:
            componentsschemas_policy_locations_item = PolicyLocation.from_dict(
                componentsschemas_policy_locations_item_data
            )

            locations.append(componentsschemas_policy_locations_item)

        resource_types = cast(List[str], d.pop("resourceTypes", UNSET))

        type = d.pop("type", UNSET)

        policy_spec = cls(
            flavors=flavors,
            locations=locations,
            resource_types=resource_types,
            type=type,
        )

        policy_spec.additional_properties = d
        return policy_spec

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
