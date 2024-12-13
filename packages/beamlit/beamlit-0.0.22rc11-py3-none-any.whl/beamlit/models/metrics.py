from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.increase_and_rate_metric import IncreaseAndRateMetric
    from ..models.metric import Metric


T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """Metrics for resources

    Attributes:
        inference_global (Union[Unset, Any]): Historical requests for all resources globally
        inference_per_second_global (Union[Unset, list['Metric']]): Array of metrics
        query (Union[Unset, Any]): Number of requests for all resources globally
        query_per_second (Union[Unset, float]): RPS value (in last 24 hours) per location, for all resources globally
        agents (Union[Unset, IncreaseAndRateMetric]): Metrics for resources
        functions (Union[Unset, IncreaseAndRateMetric]): Metrics for resources
        models (Union[Unset, IncreaseAndRateMetric]): Metrics for resources
    """

    inference_global: Union[Unset, Any] = UNSET
    inference_per_second_global: Union[Unset, list["Metric"]] = UNSET
    query: Union[Unset, Any] = UNSET
    query_per_second: Union[Unset, float] = UNSET
    agents: Union[Unset, "IncreaseAndRateMetric"] = UNSET
    functions: Union[Unset, "IncreaseAndRateMetric"] = UNSET
    models: Union[Unset, "IncreaseAndRateMetric"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inference_global = self.inference_global

        inference_per_second_global: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.inference_per_second_global, Unset):
            inference_per_second_global = []
            for componentsschemas_array_metric_item_data in self.inference_per_second_global:
                componentsschemas_array_metric_item = componentsschemas_array_metric_item_data.to_dict()
                inference_per_second_global.append(componentsschemas_array_metric_item)

        query = self.query

        query_per_second = self.query_per_second

        agents: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.agents, Unset):
            agents = self.agents.to_dict()

        functions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.functions, Unset):
            functions = self.functions.to_dict()

        models: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.models, Unset):
            models = self.models.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inference_global is not UNSET:
            field_dict["inference_global"] = inference_global
        if inference_per_second_global is not UNSET:
            field_dict["inference_per_second_global"] = inference_per_second_global
        if query is not UNSET:
            field_dict["query"] = query
        if query_per_second is not UNSET:
            field_dict["query_per_second"] = query_per_second
        if agents is not UNSET:
            field_dict["agents"] = agents
        if functions is not UNSET:
            field_dict["functions"] = functions
        if models is not UNSET:
            field_dict["models"] = models

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.increase_and_rate_metric import IncreaseAndRateMetric
        from ..models.metric import Metric

        if not src_dict:
            return None
        d = src_dict.copy()
        inference_global = d.pop("inference_global", UNSET)

        inference_per_second_global = []
        _inference_per_second_global = d.pop("inference_per_second_global", UNSET)
        for componentsschemas_array_metric_item_data in _inference_per_second_global or []:
            componentsschemas_array_metric_item = Metric.from_dict(componentsschemas_array_metric_item_data)

            inference_per_second_global.append(componentsschemas_array_metric_item)

        query = d.pop("query", UNSET)

        query_per_second = d.pop("query_per_second", UNSET)

        _agents = d.pop("agents", UNSET)
        agents: Union[Unset, IncreaseAndRateMetric]
        if isinstance(_agents, Unset):
            agents = UNSET
        else:
            agents = IncreaseAndRateMetric.from_dict(_agents)

        _functions = d.pop("functions", UNSET)
        functions: Union[Unset, IncreaseAndRateMetric]
        if isinstance(_functions, Unset):
            functions = UNSET
        else:
            functions = IncreaseAndRateMetric.from_dict(_functions)

        _models = d.pop("models", UNSET)
        models: Union[Unset, IncreaseAndRateMetric]
        if isinstance(_models, Unset):
            models = UNSET
        else:
            models = IncreaseAndRateMetric.from_dict(_models)

        metrics = cls(
            inference_global=inference_global,
            inference_per_second_global=inference_per_second_global,
            query=query,
            query_per_second=query_per_second,
            agents=agents,
            functions=functions,
            models=models,
        )

        metrics.additional_properties = d
        return metrics

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
