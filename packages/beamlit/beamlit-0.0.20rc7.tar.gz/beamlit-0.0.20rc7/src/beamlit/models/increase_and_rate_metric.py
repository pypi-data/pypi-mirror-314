from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric import Metric


T = TypeVar("T", bound="IncreaseAndRateMetric")


@_attrs_define
class IncreaseAndRateMetric:
    """Metrics for resources

    Attributes:
        inference_global (Union[Unset, Any]): Historical requests for all resources globally
        inference_per_second_global (Union[Unset, list['Metric']]): Array of metrics
        query (Union[Unset, Any]): Number of requests for all resources globally
        query_per_second (Union[Unset, float]): RPS value (in last 24 hours) per location, for all resources globally
    """

    inference_global: Union[Unset, Any] = UNSET
    inference_per_second_global: Union[Unset, list["Metric"]] = UNSET
    query: Union[Unset, Any] = UNSET
    query_per_second: Union[Unset, float] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
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

        increase_and_rate_metric = cls(
            inference_global=inference_global,
            inference_per_second_global=inference_per_second_global,
            query=query,
            query_per_second=query_per_second,
        )

        increase_and_rate_metric.additional_properties = d
        return increase_and_rate_metric

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
