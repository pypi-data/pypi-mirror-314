from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric import Metric
    from ..models.qps import QPS
    from ..models.resource_deployment_metrics_inference_per_region_type_0 import (
        ResourceDeploymentMetricsInferencePerRegionType0,
    )
    from ..models.resource_deployment_metrics_inference_per_second_per_region_type_0 import (
        ResourceDeploymentMetricsInferencePerSecondPerRegionType0,
    )
    from ..models.resource_deployment_metrics_query_per_region_per_code_type_0 import (
        ResourceDeploymentMetricsQueryPerRegionPerCodeType0,
    )
    from ..models.resource_deployment_metrics_query_per_second_per_region_per_code_type_0 import (
        ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0,
    )


T = TypeVar("T", bound="ResourceDeploymentMetrics")


@_attrs_define
class ResourceDeploymentMetrics:
    """Metrics for a single resource deployment (eg. model deployment, function deployment)

    Attributes:
        inference_global (Union[Unset, List['Metric']]): Array of metrics
        inference_per_region (Union['ResourceDeploymentMetricsInferencePerRegionType0', None, Unset]): Historical
            requests (in last 24 hours) per location, for the model deployment
        inference_per_second_global (Union[Unset, List['Metric']]): Array of metrics
        inference_per_second_per_region (Union['ResourceDeploymentMetricsInferencePerSecondPerRegionType0', None,
            Unset]): Historical requests per second (RPS) per location, for the model deployment
        query_global (Union[Unset, float]): Number of requests done on the resource for the model deployment
        query_per_code_global (Union[Unset, QPS]): Query per second per element, can be per response status code (e.g.
            200, 400) or per location
        query_per_region (Union[Unset, QPS]): Query per second per element, can be per response status code (e.g. 200,
            400) or per location
        query_per_region_per_code (Union['ResourceDeploymentMetricsQueryPerRegionPerCodeType0', None, Unset]): Number of
            requests done on the resource for the model deployment
        query_per_second_global (Union[Unset, float]): RPS value (in last 24 hours) for the model deployment globally
        query_per_second_per_code_global (Union[Unset, QPS]): Query per second per element, can be per response status
            code (e.g. 200, 400) or per location
        query_per_second_per_region (Union[Unset, QPS]): Query per second per element, can be per response status code
            (e.g. 200, 400) or per location
        query_per_second_per_region_per_code (Union['ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0',
            None, Unset]): RPS value (in last 24 hours) per response status code per location, for the model deployment
    """

    inference_global: Union[Unset, List["Metric"]] = UNSET
    inference_per_region: Union["ResourceDeploymentMetricsInferencePerRegionType0", None, Unset] = UNSET
    inference_per_second_global: Union[Unset, List["Metric"]] = UNSET
    inference_per_second_per_region: Union["ResourceDeploymentMetricsInferencePerSecondPerRegionType0", None, Unset] = (
        UNSET
    )
    query_global: Union[Unset, float] = UNSET
    query_per_code_global: Union[Unset, "QPS"] = UNSET
    query_per_region: Union[Unset, "QPS"] = UNSET
    query_per_region_per_code: Union["ResourceDeploymentMetricsQueryPerRegionPerCodeType0", None, Unset] = UNSET
    query_per_second_global: Union[Unset, float] = UNSET
    query_per_second_per_code_global: Union[Unset, "QPS"] = UNSET
    query_per_second_per_region: Union[Unset, "QPS"] = UNSET
    query_per_second_per_region_per_code: Union[
        "ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0", None, Unset
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_deployment_metrics_inference_per_region_type_0 import (
            ResourceDeploymentMetricsInferencePerRegionType0,
        )
        from ..models.resource_deployment_metrics_inference_per_second_per_region_type_0 import (
            ResourceDeploymentMetricsInferencePerSecondPerRegionType0,
        )
        from ..models.resource_deployment_metrics_query_per_region_per_code_type_0 import (
            ResourceDeploymentMetricsQueryPerRegionPerCodeType0,
        )
        from ..models.resource_deployment_metrics_query_per_second_per_region_per_code_type_0 import (
            ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0,
        )

        inference_global: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inference_global, Unset):
            inference_global = []
            for componentsschemas_array_metric_item_data in self.inference_global:
                componentsschemas_array_metric_item = componentsschemas_array_metric_item_data.to_dict()
                inference_global.append(componentsschemas_array_metric_item)

        inference_per_region: Union[Dict[str, Any], None, Unset]
        if isinstance(self.inference_per_region, Unset):
            inference_per_region = UNSET
        elif isinstance(self.inference_per_region, ResourceDeploymentMetricsInferencePerRegionType0):
            inference_per_region = self.inference_per_region.to_dict()
        else:
            inference_per_region = self.inference_per_region

        inference_per_second_global: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inference_per_second_global, Unset):
            inference_per_second_global = []
            for componentsschemas_array_metric_item_data in self.inference_per_second_global:
                componentsschemas_array_metric_item = componentsschemas_array_metric_item_data.to_dict()
                inference_per_second_global.append(componentsschemas_array_metric_item)

        inference_per_second_per_region: Union[Dict[str, Any], None, Unset]
        if isinstance(self.inference_per_second_per_region, Unset):
            inference_per_second_per_region = UNSET
        elif isinstance(
            self.inference_per_second_per_region, ResourceDeploymentMetricsInferencePerSecondPerRegionType0
        ):
            inference_per_second_per_region = self.inference_per_second_per_region.to_dict()
        else:
            inference_per_second_per_region = self.inference_per_second_per_region

        query_global = self.query_global

        query_per_code_global: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query_per_code_global, Unset):
            query_per_code_global = self.query_per_code_global.to_dict()

        query_per_region: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query_per_region, Unset):
            query_per_region = self.query_per_region.to_dict()

        query_per_region_per_code: Union[Dict[str, Any], None, Unset]
        if isinstance(self.query_per_region_per_code, Unset):
            query_per_region_per_code = UNSET
        elif isinstance(self.query_per_region_per_code, ResourceDeploymentMetricsQueryPerRegionPerCodeType0):
            query_per_region_per_code = self.query_per_region_per_code.to_dict()
        else:
            query_per_region_per_code = self.query_per_region_per_code

        query_per_second_global = self.query_per_second_global

        query_per_second_per_code_global: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query_per_second_per_code_global, Unset):
            query_per_second_per_code_global = self.query_per_second_per_code_global.to_dict()

        query_per_second_per_region: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query_per_second_per_region, Unset):
            query_per_second_per_region = self.query_per_second_per_region.to_dict()

        query_per_second_per_region_per_code: Union[Dict[str, Any], None, Unset]
        if isinstance(self.query_per_second_per_region_per_code, Unset):
            query_per_second_per_region_per_code = UNSET
        elif isinstance(
            self.query_per_second_per_region_per_code, ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0
        ):
            query_per_second_per_region_per_code = self.query_per_second_per_region_per_code.to_dict()
        else:
            query_per_second_per_region_per_code = self.query_per_second_per_region_per_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inference_global is not UNSET:
            field_dict["inference_global"] = inference_global
        if inference_per_region is not UNSET:
            field_dict["inference_per_region"] = inference_per_region
        if inference_per_second_global is not UNSET:
            field_dict["inference_per_second_global"] = inference_per_second_global
        if inference_per_second_per_region is not UNSET:
            field_dict["inference_per_second_per_region"] = inference_per_second_per_region
        if query_global is not UNSET:
            field_dict["query_global"] = query_global
        if query_per_code_global is not UNSET:
            field_dict["query_per_code_global"] = query_per_code_global
        if query_per_region is not UNSET:
            field_dict["query_per_region"] = query_per_region
        if query_per_region_per_code is not UNSET:
            field_dict["query_per_region_per_code"] = query_per_region_per_code
        if query_per_second_global is not UNSET:
            field_dict["query_per_second_global"] = query_per_second_global
        if query_per_second_per_code_global is not UNSET:
            field_dict["query_per_second_per_code_global"] = query_per_second_per_code_global
        if query_per_second_per_region is not UNSET:
            field_dict["query_per_second_per_region"] = query_per_second_per_region
        if query_per_second_per_region_per_code is not UNSET:
            field_dict["query_per_second_per_region_per_code"] = query_per_second_per_region_per_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric import Metric
        from ..models.qps import QPS
        from ..models.resource_deployment_metrics_inference_per_region_type_0 import (
            ResourceDeploymentMetricsInferencePerRegionType0,
        )
        from ..models.resource_deployment_metrics_inference_per_second_per_region_type_0 import (
            ResourceDeploymentMetricsInferencePerSecondPerRegionType0,
        )
        from ..models.resource_deployment_metrics_query_per_region_per_code_type_0 import (
            ResourceDeploymentMetricsQueryPerRegionPerCodeType0,
        )
        from ..models.resource_deployment_metrics_query_per_second_per_region_per_code_type_0 import (
            ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0,
        )

        d = src_dict.copy()
        inference_global = []
        _inference_global = d.pop("inference_global", UNSET)
        for componentsschemas_array_metric_item_data in _inference_global or []:
            componentsschemas_array_metric_item = Metric.from_dict(componentsschemas_array_metric_item_data)

            inference_global.append(componentsschemas_array_metric_item)

        def _parse_inference_per_region(
            data: object,
        ) -> Union["ResourceDeploymentMetricsInferencePerRegionType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                inference_per_region_type_0 = ResourceDeploymentMetricsInferencePerRegionType0.from_dict(data)

                return inference_per_region_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceDeploymentMetricsInferencePerRegionType0", None, Unset], data)

        inference_per_region = _parse_inference_per_region(d.pop("inference_per_region", UNSET))

        inference_per_second_global = []
        _inference_per_second_global = d.pop("inference_per_second_global", UNSET)
        for componentsschemas_array_metric_item_data in _inference_per_second_global or []:
            componentsschemas_array_metric_item = Metric.from_dict(componentsschemas_array_metric_item_data)

            inference_per_second_global.append(componentsschemas_array_metric_item)

        def _parse_inference_per_second_per_region(
            data: object,
        ) -> Union["ResourceDeploymentMetricsInferencePerSecondPerRegionType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                inference_per_second_per_region_type_0 = (
                    ResourceDeploymentMetricsInferencePerSecondPerRegionType0.from_dict(data)
                )

                return inference_per_second_per_region_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceDeploymentMetricsInferencePerSecondPerRegionType0", None, Unset], data)

        inference_per_second_per_region = _parse_inference_per_second_per_region(
            d.pop("inference_per_second_per_region", UNSET)
        )

        query_global = d.pop("query_global", UNSET)

        _query_per_code_global = d.pop("query_per_code_global", UNSET)
        query_per_code_global: Union[Unset, QPS]
        if isinstance(_query_per_code_global, Unset):
            query_per_code_global = UNSET
        else:
            query_per_code_global = QPS.from_dict(_query_per_code_global)

        _query_per_region = d.pop("query_per_region", UNSET)
        query_per_region: Union[Unset, QPS]
        if isinstance(_query_per_region, Unset):
            query_per_region = UNSET
        else:
            query_per_region = QPS.from_dict(_query_per_region)

        def _parse_query_per_region_per_code(
            data: object,
        ) -> Union["ResourceDeploymentMetricsQueryPerRegionPerCodeType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                query_per_region_per_code_type_0 = ResourceDeploymentMetricsQueryPerRegionPerCodeType0.from_dict(data)

                return query_per_region_per_code_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceDeploymentMetricsQueryPerRegionPerCodeType0", None, Unset], data)

        query_per_region_per_code = _parse_query_per_region_per_code(d.pop("query_per_region_per_code", UNSET))

        query_per_second_global = d.pop("query_per_second_global", UNSET)

        _query_per_second_per_code_global = d.pop("query_per_second_per_code_global", UNSET)
        query_per_second_per_code_global: Union[Unset, QPS]
        if isinstance(_query_per_second_per_code_global, Unset):
            query_per_second_per_code_global = UNSET
        else:
            query_per_second_per_code_global = QPS.from_dict(_query_per_second_per_code_global)

        _query_per_second_per_region = d.pop("query_per_second_per_region", UNSET)
        query_per_second_per_region: Union[Unset, QPS]
        if isinstance(_query_per_second_per_region, Unset):
            query_per_second_per_region = UNSET
        else:
            query_per_second_per_region = QPS.from_dict(_query_per_second_per_region)

        def _parse_query_per_second_per_region_per_code(
            data: object,
        ) -> Union["ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                query_per_second_per_region_per_code_type_0 = (
                    ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0.from_dict(data)
                )

                return query_per_second_per_region_per_code_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceDeploymentMetricsQueryPerSecondPerRegionPerCodeType0", None, Unset], data)

        query_per_second_per_region_per_code = _parse_query_per_second_per_region_per_code(
            d.pop("query_per_second_per_region_per_code", UNSET)
        )

        resource_deployment_metrics = cls(
            inference_global=inference_global,
            inference_per_region=inference_per_region,
            inference_per_second_global=inference_per_second_global,
            inference_per_second_per_region=inference_per_second_per_region,
            query_global=query_global,
            query_per_code_global=query_per_code_global,
            query_per_region=query_per_region,
            query_per_region_per_code=query_per_region_per_code,
            query_per_second_global=query_per_second_global,
            query_per_second_per_code_global=query_per_second_per_code_global,
            query_per_second_per_region=query_per_second_per_region,
            query_per_second_per_region_per_code=query_per_second_per_region_per_code,
        )

        resource_deployment_metrics.additional_properties = d
        return resource_deployment_metrics

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
