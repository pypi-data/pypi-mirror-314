from typing import Any, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeploymentServerlessConfigType0")


@_attrs_define
class DeploymentServerlessConfigType0:
    """Configuration for a serverless deployment

    Attributes:
        last_pod_retention_period (Union[None, Unset, str]): The minimum amount of time that the last replica will
            remain active AFTER a scale-to-zero decision is made
        max_num_replicas (Union[None, Unset, int]): The maximum number of replicas for the deployment.
        metric (Union[None, Unset, str]): Metric watched to make scaling decisions. Can be "cpu" or "memory" or "rps" or
            "concurrency"
        min_num_replicas (Union[None, Unset, int]): The minimum number of replicas for the deployment. Can be 0 or 1 (in
            which case the deployment is always running in at least one location).
        scale_down_delay (Union[None, Unset, str]): The time window which must pass at reduced concurrency before a
            scale-down decision is applied. This can be useful, for example, to keep containers around for a configurable
            duration to avoid a cold start penalty if new requests come in.
        scale_up_minimum (Union[None, Unset, int]): The minimum number of replicas that will be created when the
            deployment scales up from zero.
        stable_window (Union[None, Unset, str]): The sliding time window over which metrics are averaged to provide the
            input for scaling decisions
        target (Union[None, Unset, str]): Target value for the watched metric
    """

    last_pod_retention_period: Union[None, Unset, str] = UNSET
    max_num_replicas: Union[None, Unset, int] = UNSET
    metric: Union[None, Unset, str] = UNSET
    min_num_replicas: Union[None, Unset, int] = UNSET
    scale_down_delay: Union[None, Unset, str] = UNSET
    scale_up_minimum: Union[None, Unset, int] = UNSET
    stable_window: Union[None, Unset, str] = UNSET
    target: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_pod_retention_period: Union[None, Unset, str]
        if isinstance(self.last_pod_retention_period, Unset):
            last_pod_retention_period = UNSET
        else:
            last_pod_retention_period = self.last_pod_retention_period

        max_num_replicas: Union[None, Unset, int]
        if isinstance(self.max_num_replicas, Unset):
            max_num_replicas = UNSET
        else:
            max_num_replicas = self.max_num_replicas

        metric: Union[None, Unset, str]
        if isinstance(self.metric, Unset):
            metric = UNSET
        else:
            metric = self.metric

        min_num_replicas: Union[None, Unset, int]
        if isinstance(self.min_num_replicas, Unset):
            min_num_replicas = UNSET
        else:
            min_num_replicas = self.min_num_replicas

        scale_down_delay: Union[None, Unset, str]
        if isinstance(self.scale_down_delay, Unset):
            scale_down_delay = UNSET
        else:
            scale_down_delay = self.scale_down_delay

        scale_up_minimum: Union[None, Unset, int]
        if isinstance(self.scale_up_minimum, Unset):
            scale_up_minimum = UNSET
        else:
            scale_up_minimum = self.scale_up_minimum

        stable_window: Union[None, Unset, str]
        if isinstance(self.stable_window, Unset):
            stable_window = UNSET
        else:
            stable_window = self.stable_window

        target: Union[None, Unset, str]
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if last_pod_retention_period is not UNSET:
            field_dict["last_pod_retention_period"] = last_pod_retention_period
        if max_num_replicas is not UNSET:
            field_dict["max_num_replicas"] = max_num_replicas
        if metric is not UNSET:
            field_dict["metric"] = metric
        if min_num_replicas is not UNSET:
            field_dict["min_num_replicas"] = min_num_replicas
        if scale_down_delay is not UNSET:
            field_dict["scale_down_delay"] = scale_down_delay
        if scale_up_minimum is not UNSET:
            field_dict["scale_up_minimum"] = scale_up_minimum
        if stable_window is not UNSET:
            field_dict["stable_window"] = stable_window
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_last_pod_retention_period(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_pod_retention_period = _parse_last_pod_retention_period(
            d.pop("last_pod_retention_period", UNSET)
        )

        def _parse_max_num_replicas(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_num_replicas = _parse_max_num_replicas(d.pop("max_num_replicas", UNSET))

        def _parse_metric(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric = _parse_metric(d.pop("metric", UNSET))

        def _parse_min_num_replicas(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_num_replicas = _parse_min_num_replicas(d.pop("min_num_replicas", UNSET))

        def _parse_scale_down_delay(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scale_down_delay = _parse_scale_down_delay(d.pop("scale_down_delay", UNSET))

        def _parse_scale_up_minimum(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        scale_up_minimum = _parse_scale_up_minimum(d.pop("scale_up_minimum", UNSET))

        def _parse_stable_window(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stable_window = _parse_stable_window(d.pop("stable_window", UNSET))

        def _parse_target(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        target = _parse_target(d.pop("target", UNSET))

        deployment_serverless_config_type_0 = cls(
            last_pod_retention_period=last_pod_retention_period,
            max_num_replicas=max_num_replicas,
            metric=metric,
            min_num_replicas=min_num_replicas,
            scale_down_delay=scale_down_delay,
            scale_up_minimum=scale_up_minimum,
            stable_window=stable_window,
            target=target,
        )

        deployment_serverless_config_type_0.additional_properties = d
        return deployment_serverless_config_type_0

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
