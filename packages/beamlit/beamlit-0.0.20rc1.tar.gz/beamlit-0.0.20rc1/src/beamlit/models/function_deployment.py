from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deployment_serverless_config_type_0 import DeploymentServerlessConfigType0
    from ..models.flavor import Flavor
    from ..models.function_deployment_configuration_type_0 import FunctionDeploymentConfigurationType0
    from ..models.function_deployment_pod_template_type_0 import FunctionDeploymentPodTemplateType0
    from ..models.function_kit import FunctionKit
    from ..models.labels_type_0 import LabelsType0
    from ..models.runtime import Runtime
    from ..models.store_function_parameter import StoreFunctionParameter


T = TypeVar("T", bound="FunctionDeployment")


@_attrs_define
class FunctionDeployment:
    """Function deployment configuration

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        configuration (Union['FunctionDeploymentConfigurationType0', None, Unset]): Function configuration, this is a
            key value storage. In your function you can retrieve the value with config[key]
        description (Union[Unset, str]): Function description, very important for the agent function to work with an LLM
        enabled (Union[None, Unset, bool]): Whether the function deployment is enabled
        environment (Union[Unset, str]): The name of the environment
        flavors (Union[Unset, List['Flavor']]): Types of hardware available for deployments
        function (Union[Unset, str]): The name of the function
        integration_connections (Union[Unset, List[str]]):
        kit (Union[Unset, List['FunctionKit']]): The kit of the function deployment
        labels (Union['LabelsType0', None, Unset]): Labels
        parameters (Union[Unset, List['StoreFunctionParameter']]): Function parameters, for your function to be callable
            with Agent
        pod_template (Union['FunctionDeploymentPodTemplateType0', None, Unset]): The pod template, should be a valid
            Kubernetes pod template
        policies (Union[Unset, List[str]]):
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        serverless_config (Union['DeploymentServerlessConfigType0', None, Unset]): Configuration for a serverless
            deployment
        store_id (Union[Unset, str]): Create from a store registered function
        workspace (Union[Unset, str]): The workspace the function deployment belongs to
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    configuration: Union["FunctionDeploymentConfigurationType0", None, Unset] = UNSET
    description: Union[Unset, str] = UNSET
    enabled: Union[None, Unset, bool] = UNSET
    environment: Union[Unset, str] = UNSET
    flavors: Union[Unset, List["Flavor"]] = UNSET
    function: Union[Unset, str] = UNSET
    integration_connections: Union[Unset, List[str]] = UNSET
    kit: Union[Unset, List["FunctionKit"]] = UNSET
    labels: Union["LabelsType0", None, Unset] = UNSET
    parameters: Union[Unset, List["StoreFunctionParameter"]] = UNSET
    pod_template: Union["FunctionDeploymentPodTemplateType0", None, Unset] = UNSET
    policies: Union[Unset, List[str]] = UNSET
    runtime: Union[Unset, "Runtime"] = UNSET
    serverless_config: Union["DeploymentServerlessConfigType0", None, Unset] = UNSET
    store_id: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_serverless_config_type_0 import DeploymentServerlessConfigType0
        from ..models.function_deployment_configuration_type_0 import FunctionDeploymentConfigurationType0
        from ..models.function_deployment_pod_template_type_0 import FunctionDeploymentPodTemplateType0
        from ..models.labels_type_0 import LabelsType0

        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        configuration: Union[Dict[str, Any], None, Unset]
        if isinstance(self.configuration, Unset):
            configuration = UNSET
        elif isinstance(self.configuration, FunctionDeploymentConfigurationType0):
            configuration = self.configuration.to_dict()
        else:
            configuration = self.configuration

        description = self.description

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

        function = self.function

        integration_connections: Union[Unset, List[str]] = UNSET
        if not isinstance(self.integration_connections, Unset):
            integration_connections = self.integration_connections

        kit: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.kit, Unset):
            kit = []
            for kit_item_data in self.kit:
                kit_item = kit_item_data.to_dict()
                kit.append(kit_item)

        labels: Union[Dict[str, Any], None, Unset]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, LabelsType0):
            labels = self.labels.to_dict()
        else:
            labels = self.labels

        parameters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)

        pod_template: Union[Dict[str, Any], None, Unset]
        if isinstance(self.pod_template, Unset):
            pod_template = UNSET
        elif isinstance(self.pod_template, FunctionDeploymentPodTemplateType0):
            pod_template = self.pod_template.to_dict()
        else:
            pod_template = self.pod_template

        policies: Union[Unset, List[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        runtime: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.to_dict()

        serverless_config: Union[Dict[str, Any], None, Unset]
        if isinstance(self.serverless_config, Unset):
            serverless_config = UNSET
        elif isinstance(self.serverless_config, DeploymentServerlessConfigType0):
            serverless_config = self.serverless_config.to_dict()
        else:
            serverless_config = self.serverless_config

        store_id = self.store_id

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
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if environment is not UNSET:
            field_dict["environment"] = environment
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if function is not UNSET:
            field_dict["function"] = function
        if integration_connections is not UNSET:
            field_dict["integration_connections"] = integration_connections
        if kit is not UNSET:
            field_dict["kit"] = kit
        if labels is not UNSET:
            field_dict["labels"] = labels
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if pod_template is not UNSET:
            field_dict["pod_template"] = pod_template
        if policies is not UNSET:
            field_dict["policies"] = policies
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if serverless_config is not UNSET:
            field_dict["serverless_config"] = serverless_config
        if store_id is not UNSET:
            field_dict["store_id"] = store_id
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.deployment_serverless_config_type_0 import DeploymentServerlessConfigType0
        from ..models.flavor import Flavor
        from ..models.function_deployment_configuration_type_0 import FunctionDeploymentConfigurationType0
        from ..models.function_deployment_pod_template_type_0 import FunctionDeploymentPodTemplateType0
        from ..models.function_kit import FunctionKit
        from ..models.labels_type_0 import LabelsType0
        from ..models.runtime import Runtime
        from ..models.store_function_parameter import StoreFunctionParameter

        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        def _parse_configuration(data: object) -> Union["FunctionDeploymentConfigurationType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                configuration_type_0 = FunctionDeploymentConfigurationType0.from_dict(data)

                return configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FunctionDeploymentConfigurationType0", None, Unset], data)

        configuration = _parse_configuration(d.pop("configuration", UNSET))

        description = d.pop("description", UNSET)

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

        function = d.pop("function", UNSET)

        integration_connections = cast(List[str], d.pop("integration_connections", UNSET))

        kit = []
        _kit = d.pop("kit", UNSET)
        for kit_item_data in _kit or []:
            kit_item = FunctionKit.from_dict(kit_item_data)

            kit.append(kit_item)

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

        parameters = []
        _parameters = d.pop("parameters", UNSET)
        for parameters_item_data in _parameters or []:
            parameters_item = StoreFunctionParameter.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        def _parse_pod_template(data: object) -> Union["FunctionDeploymentPodTemplateType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pod_template_type_0 = FunctionDeploymentPodTemplateType0.from_dict(data)

                return pod_template_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FunctionDeploymentPodTemplateType0", None, Unset], data)

        pod_template = _parse_pod_template(d.pop("pod_template", UNSET))

        policies = cast(List[str], d.pop("policies", UNSET))

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, Runtime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = Runtime.from_dict(_runtime)

        def _parse_serverless_config(data: object) -> Union["DeploymentServerlessConfigType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_deployment_serverless_config_type_0 = DeploymentServerlessConfigType0.from_dict(data)

                return componentsschemas_deployment_serverless_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DeploymentServerlessConfigType0", None, Unset], data)

        serverless_config = _parse_serverless_config(d.pop("serverless_config", UNSET))

        store_id = d.pop("store_id", UNSET)

        workspace = d.pop("workspace", UNSET)

        function_deployment = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            configuration=configuration,
            description=description,
            enabled=enabled,
            environment=environment,
            flavors=flavors,
            function=function,
            integration_connections=integration_connections,
            kit=kit,
            labels=labels,
            parameters=parameters,
            pod_template=pod_template,
            policies=policies,
            runtime=runtime,
            serverless_config=serverless_config,
            store_id=store_id,
            workspace=workspace,
        )

        function_deployment.additional_properties = d
        return function_deployment

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
