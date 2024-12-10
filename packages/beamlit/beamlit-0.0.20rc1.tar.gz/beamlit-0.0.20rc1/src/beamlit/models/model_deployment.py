from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flavor import Flavor
    from ..models.labels_type_0 import LabelsType0
    from ..models.model_deployment_pod_template_type_0 import ModelDeploymentPodTemplateType0


T = TypeVar("T", bound="ModelDeployment")


@_attrs_define
class ModelDeployment:
    """An instance of a model, deployed in a specific environment

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        enabled (Union[None, Unset, bool]): If false, the model deployment will not be active nor serve requests
        environment (Union[Unset, str]): The name of the environment in which the model deployment is deployed
        flavors (Union[Unset, List['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, List[str]]):
        labels (Union['LabelsType0', None, Unset]): Labels
        metric_port (Union[None, Unset, int]): The port to serve the metrics on
        model (Union[Unset, str]): The name of the parent model
        model_provider_ref (Union[Unset, Any]): The reference for the origin of the model
        pod_template (Union['ModelDeploymentPodTemplateType0', None, Unset]): The pod template for the deployment.
            Should be a Kubernetes PodTemplateSpec
        policies (Union[Unset, List[str]]):
        runtime (Union[Unset, Any]): Configurations that describe which model is being served and how it is served
        serverless_config (Union[Unset, Any]): The configuration for scaling the model deployment
        serving_port (Union[None, Unset, int]): The port to serve the model on
        workspace (Union[Unset, str]): The workspace the model deployment belongs to
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    enabled: Union[None, Unset, bool] = UNSET
    environment: Union[Unset, str] = UNSET
    flavors: Union[Unset, List["Flavor"]] = UNSET
    integration_connections: Union[Unset, List[str]] = UNSET
    labels: Union["LabelsType0", None, Unset] = UNSET
    metric_port: Union[None, Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    model_provider_ref: Union[Unset, Any] = UNSET
    pod_template: Union["ModelDeploymentPodTemplateType0", None, Unset] = UNSET
    policies: Union[Unset, List[str]] = UNSET
    runtime: Union[Unset, Any] = UNSET
    serverless_config: Union[Unset, Any] = UNSET
    serving_port: Union[None, Unset, int] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.labels_type_0 import LabelsType0
        from ..models.model_deployment_pod_template_type_0 import ModelDeploymentPodTemplateType0

        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        enabled: Union[None, Unset, bool]
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled

        environment = self.environment

        flavors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                componentsschemas_flavors_item = componentsschemas_flavors_item_data.to_dict()
                flavors.append(componentsschemas_flavors_item)

        integration_connections: Union[Unset, List[str]] = UNSET
        if not isinstance(self.integration_connections, Unset):
            integration_connections = self.integration_connections

        labels: Union[Dict[str, Any], None, Unset]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, LabelsType0):
            labels = self.labels.to_dict()
        else:
            labels = self.labels

        metric_port: Union[None, Unset, int]
        if isinstance(self.metric_port, Unset):
            metric_port = UNSET
        else:
            metric_port = self.metric_port

        model = self.model

        model_provider_ref = self.model_provider_ref

        pod_template: Union[Dict[str, Any], None, Unset]
        if isinstance(self.pod_template, Unset):
            pod_template = UNSET
        elif isinstance(self.pod_template, ModelDeploymentPodTemplateType0):
            pod_template = self.pod_template.to_dict()
        else:
            pod_template = self.pod_template

        policies: Union[Unset, List[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        runtime = self.runtime

        serverless_config = self.serverless_config

        serving_port: Union[None, Unset, int]
        if isinstance(self.serving_port, Unset):
            serving_port = UNSET
        else:
            serving_port = self.serving_port

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
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if environment is not UNSET:
            field_dict["environment"] = environment
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if integration_connections is not UNSET:
            field_dict["integration_connections"] = integration_connections
        if labels is not UNSET:
            field_dict["labels"] = labels
        if metric_port is not UNSET:
            field_dict["metric_port"] = metric_port
        if model is not UNSET:
            field_dict["model"] = model
        if model_provider_ref is not UNSET:
            field_dict["model_provider_ref"] = model_provider_ref
        if pod_template is not UNSET:
            field_dict["pod_template"] = pod_template
        if policies is not UNSET:
            field_dict["policies"] = policies
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if serverless_config is not UNSET:
            field_dict["serverless_config"] = serverless_config
        if serving_port is not UNSET:
            field_dict["serving_port"] = serving_port
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.flavor import Flavor
        from ..models.labels_type_0 import LabelsType0
        from ..models.model_deployment_pod_template_type_0 import ModelDeploymentPodTemplateType0

        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        def _parse_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))

        environment = d.pop("environment", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(componentsschemas_flavors_item_data)

            flavors.append(componentsschemas_flavors_item)

        integration_connections = cast(List[str], d.pop("integration_connections", UNSET))

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

        def _parse_metric_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        metric_port = _parse_metric_port(d.pop("metric_port", UNSET))

        model = d.pop("model", UNSET)

        model_provider_ref = d.pop("model_provider_ref", UNSET)

        def _parse_pod_template(data: object) -> Union["ModelDeploymentPodTemplateType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pod_template_type_0 = ModelDeploymentPodTemplateType0.from_dict(data)

                return pod_template_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModelDeploymentPodTemplateType0", None, Unset], data)

        pod_template = _parse_pod_template(d.pop("pod_template", UNSET))

        policies = cast(List[str], d.pop("policies", UNSET))

        runtime = d.pop("runtime", UNSET)

        serverless_config = d.pop("serverless_config", UNSET)

        def _parse_serving_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        serving_port = _parse_serving_port(d.pop("serving_port", UNSET))

        workspace = d.pop("workspace", UNSET)

        model_deployment = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            enabled=enabled,
            environment=environment,
            flavors=flavors,
            integration_connections=integration_connections,
            labels=labels,
            metric_port=metric_port,
            model=model,
            model_provider_ref=model_provider_ref,
            pod_template=pod_template,
            policies=policies,
            runtime=runtime,
            serverless_config=serverless_config,
            serving_port=serving_port,
            workspace=workspace,
        )

        model_deployment.additional_properties = d
        return model_deployment

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
