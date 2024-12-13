from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_connection_config import IntegrationConnectionConfig
    from ..models.integration_connection_secret import IntegrationConnectionSecret
    from ..models.labels_type_0 import LabelsType0


T = TypeVar("T", bound="IntegrationConnection")


@_attrs_define
class IntegrationConnection:
    """Integration Connection

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        config (Union[Unset, IntegrationConnectionConfig]): Integration config
        display_name (Union[Unset, str]): Integration connection display name
        integration (Union[Unset, str]): Integration type
        labels (Union['LabelsType0', None, Unset]): Labels
        name (Union[Unset, str]): Integration connection name
        secret (Union[Unset, IntegrationConnectionSecret]): Integration secret
        workspace (Union[Unset, str]): Workspace name
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    config: Union[Unset, "IntegrationConnectionConfig"] = UNSET
    display_name: Union[Unset, str] = UNSET
    integration: Union[Unset, str] = UNSET
    labels: Union["LabelsType0", None, Unset] = UNSET
    name: Union[Unset, str] = UNSET
    secret: Union[Unset, "IntegrationConnectionSecret"] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.labels_type_0 import LabelsType0

        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        display_name = self.display_name

        integration = self.integration

        labels: Union[None, Unset, dict[str, Any]]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, LabelsType0):
            labels = self.labels.to_dict()
        else:
            labels = self.labels

        name = self.name

        secret: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret, Unset):
            secret = self.secret.to_dict()

        workspace = self.workspace

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
        if config is not UNSET:
            field_dict["config"] = config
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if integration is not UNSET:
            field_dict["integration"] = integration
        if labels is not UNSET:
            field_dict["labels"] = labels
        if name is not UNSET:
            field_dict["name"] = name
        if secret is not UNSET:
            field_dict["secret"] = secret
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.integration_connection_config import IntegrationConnectionConfig
        from ..models.integration_connection_secret import IntegrationConnectionSecret
        from ..models.labels_type_0 import LabelsType0

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, IntegrationConnectionConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = IntegrationConnectionConfig.from_dict(_config)

        display_name = d.pop("display_name", UNSET)

        integration = d.pop("integration", UNSET)

        def _parse_labels(data: object) -> Union["LabelsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_labels_type_0 = LabelsType0.from_dict(data)

                return componentsschemas_labels_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LabelsType0", None, Unset], data)

        labels = _parse_labels(d.pop("labels", UNSET))

        name = d.pop("name", UNSET)

        _secret = d.pop("secret", UNSET)
        secret: Union[Unset, IntegrationConnectionSecret]
        if isinstance(_secret, Unset):
            secret = UNSET
        else:
            secret = IntegrationConnectionSecret.from_dict(_secret)

        workspace = d.pop("workspace", UNSET)

        integration_connection = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            config=config,
            display_name=display_name,
            integration=integration,
            labels=labels,
            name=name,
            secret=secret,
            workspace=workspace,
        )

        integration_connection.additional_properties = d
        return integration_connection

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
