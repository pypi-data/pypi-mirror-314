"""Validator configuration."""

import json
import re
from abc import ABC
from enum import Enum
from typing import TYPE_CHECKING, Any

from validio_sdk._api.api import execute_mutation
from validio_sdk.client import Session
from validio_sdk.exception import ValidioError
from validio_sdk.graphql_client.enums import (
    CategoricalDistributionMetric as LegacyCategoricalDistributionMetric,
)
from validio_sdk.graphql_client.enums import (
    NumericAnomalyMetric as LegacyNumericAnomalyMetric,
)
from validio_sdk.graphql_client.enums import (
    NumericDistributionMetric as LegacyNumericDistributionMetric,
)
from validio_sdk.graphql_client.enums import NumericMetric as LegacyNumericMetric
from validio_sdk.graphql_client.enums import (
    RelativeTimeMetric as LegacyRelativeTimeMetric,
)
from validio_sdk.graphql_client.enums import (
    RelativeVolumeMetric as LegacyRelativeVolumeMetric,
)
from validio_sdk.graphql_client.enums import VolumeMetric as LegacyVolumeMetric
from validio_sdk.resource import FieldSelector
from validio_sdk.resource._diffable import Diffable
from validio_sdk.resource._errors import ManifestConfigurationError
from validio_sdk.resource._field_selector import (
    FromFieldSelector,
    SelectorWithFieldName,
)
from validio_sdk.resource._resource import Resource
from validio_sdk.resource._serde import (
    CONFIG_FIELD_NAME,
    _api_create_input_params,
    _api_update_input_params,
    _encode_resource,
    get_config_node,
)
from validio_sdk.resource._util import _rename_dict_key
from validio_sdk.resource.filters import Filter
from validio_sdk.resource.segmentations import Segmentation
from validio_sdk.resource.sources import (
    DemoSource,
    ObjectStorageSource,
    Source,
    StreamSource,
)
from validio_sdk.resource.tags import Tag
from validio_sdk.resource.thresholds import (
    DifferenceThreshold,
    DynamicThreshold,
    FixedThreshold,
    LegacyComparisonOperator,
    LegacyDecisionBoundsType,
    LegacyDifferenceOperator,
    LegacyDifferenceType,
    Threshold,
)
from validio_sdk.resource.windows import (
    FileWindow,
    GlobalWindow,
    TumblingWindow,
    Window,
)
from validio_sdk.scalars import JsonPointer

if TYPE_CHECKING:
    from validio_sdk.code._import import ImportContext
    from validio_sdk.resource._diff import DiffContext


class CategoricalDistributionMetric(str, Enum):
    """Metric for categorical distribution."""

    ADDED = "ADDED"
    CHANGED = "CHANGED"
    RELATIVE_ENTROPY = "RELATIVE_ENTROPY"
    REMOVED = "REMOVED"


class NumericAnomalyMetric(str, Enum):
    """Metric for numeric anomaly."""

    COUNT = "COUNT"
    PERCENTAGE = "PERCENTAGE"


class NumericDistributionMetric(str, Enum):
    """Metric for numeric distribution."""

    MAXIMUM_RATIO = "MAXIMUM_RATIO"
    MEAN_RATIO = "MEAN_RATIO"
    MINIMUM_RATIO = "MINIMUM_RATIO"
    RELATIVE_ENTROPY = "RELATIVE_ENTROPY"
    STANDARD_DEVIATION_RATIO = "STANDARD_DEVIATION_RATIO"
    SUM_RATIO = "SUM_RATIO"


class NumericMetric(str, Enum):
    """Metric for numeric."""

    MAX = "MAX"
    MEAN = "MEAN"
    MIN = "MIN"
    STD = "STD"
    SUM = "SUM"


class RelativeTimeMetric(str, Enum):
    """Metric for relative time."""

    MAXIMUM_DIFFERENCE = "MAXIMUM_DIFFERENCE"
    MEAN_DIFFERENCE = "MEAN_DIFFERENCE"
    MINIMUM_DIFFERENCE = "MINIMUM_DIFFERENCE"


class RelativeVolumeMetric(str, Enum):
    """Metric for relative volume."""

    COUNT_RATIO = "COUNT_RATIO"
    PERCENTAGE_RATIO = "PERCENTAGE_RATIO"


class VolumeMetric(str, Enum):
    """Metric for volume."""

    COUNT = "COUNT"
    DUPLICATES_COUNT = "DUPLICATES_COUNT"
    DUPLICATES_PERCENTAGE = "DUPLICATES_PERCENTAGE"
    PERCENTAGE = "PERCENTAGE"
    UNIQUE_COUNT = "UNIQUE_COUNT"
    UNIQUE_PERCENTAGE = "UNIQUE_PERCENTAGE"


class Reference(Diffable):
    """
    Represents configuration for reference validators.

    See the Validio docs for more info on reference configuration
    https://docs.validio.io/docs/reference-source-config
    """

    def __init__(
        self,
        source: Source,
        window: Window,
        history: int,
        offset: int,
        filter: Filter | None = None,
    ):
        """
        Constructor.

        :param source: The reference source to attach the validator to. (immutable)
        :param window: The window in the reference source to attach the
            validator to. (immutable)
        :param history: Over how many windows metric will be calculated
            for the reference source
        :param offset: By how many windows in the past the reference
            calculation is shifted.
        :param filter: Optional filter on the data processed from the
            reference source.
        """
        self.source_name = source.name
        self.window_name = window.name
        self.history = history
        self.offset = offset
        if filter is None:
            self.filter_name = None
        elif filter._in_resource_mode():
            self.filter_name = filter.name

        self.filter = filter

    def _filter_resource_mode(self) -> bool:
        return hasattr(self, "filter_name")

    def _force_filter_expression_mode(self) -> None:
        if self._filter_resource_mode():
            delattr(self, "filter_name")

    def _immutable_fields(self) -> set[str]:
        return {"source_name", "window_name"}

    def _mutable_fields(self) -> set[str]:
        fields = {"history", "offset"}
        if self._filter_resource_mode():
            fields.add("filter_name")

        return fields

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        return {} if self._filter_resource_mode() else {"filter": self.filter}

    def _import_str(
        self,
        indent_level: int,
        import_ctx: "ImportContext",
        inits: list[tuple[str, Any, str | None]] | None = None,
    ) -> str:
        inits = list(inits or [])
        source = import_ctx.get_variable(Source, self.source_name)
        window = import_ctx.get_variable(Window, self.window_name)
        inits = [*inits, ("source", source, None), ("window", window, None)]
        if self.filter_name:
            filter_ = import_ctx.get_variable(Filter, self.filter_name)
            inits.append(("filter", filter_, None))
        return super()._import_str(
            indent_level=indent_level,
            import_ctx=import_ctx,
            inits=inits,
        )

    def _reference_source_config_create_input(
        self, ctx: "DiffContext"
    ) -> dict[str, Any]:
        source_id = ctx.sources[self.source_name]._must_id()
        window_id = ctx.windows[self.window_name]._must_id()

        return {
            "sourceId": source_id,
            "windowId": window_id,
            "offset": self.offset,
            "history": self.history,
            **self._filter_api_input(ctx),
        }

    def _reference_source_config_update_input(
        self, ctx: "DiffContext"
    ) -> dict[str, Any]:
        return {
            "offset": self.offset,
            "history": self.history,
            **self._filter_api_input(ctx),
        }

    def _filter_api_input(
        self,
        ctx: "DiffContext",
    ) -> dict[str, Any]:
        if self._filter_resource_mode():
            return {
                "filterId": (
                    ctx.filters[self.filter_name]._must_id()
                    if self.filter_name is not None
                    else None
                )
            }

        return {
            "filter": (
                self.filter._api_json_filter_expression_create_input()
                if self.filter
                else None
            )
        }

    def _encode(self) -> dict[str, object]:
        return json.loads(
            json.dumps(
                {
                    k: v
                    for k, v in self.__dict__.items()
                    # If we're in resource mode, do not include `self.filter`
                    # that's only used as a fallback if we need to diff and
                    # it's only called on the server version (which doesn't use
                    # the encode/decode functionality)
                    if (not self._filter_resource_mode()) or k != "filter"
                },
                default=lambda o: o._encode(),
            )
        )

    @staticmethod
    def _decode(
        obj: dict[str, Any],
        all_sources: dict[str, Source],
        all_windows: dict[str, Window],
        all_filters: dict[str, Filter],
    ) -> "Reference":
        source_name = obj["source_name"]
        window_name = obj["window_name"]
        if source_name not in all_sources:
            raise ValidioError(
                f"invalid configuration: no such reference source {source_name}"
            )
        if window_name not in all_windows:
            raise ValidioError(
                f"invalid configuration: no such reference window {source_name}"
            )

        source = all_sources[source_name]
        window = all_windows[window_name]
        filter_ = Validator._decode_filter(obj, all_filters)

        # Remove the fields that are not compatible with the constructor.
        # We have the objects themselves now, so they will be repopulated by
        # the constructor accordingly.
        obj = {
            k: v
            for k, v in obj.items()
            if k not in {"source_name", "window_name", "filter_name"}
        }

        return Reference(
            **{
                **obj,
                "source": source,
                "window": window,
                "filter": filter_,
            }
        )  # type:ignore


class Validator(Resource, ABC):
    """Base class for a validator resources.

    https://docs.validio.io/docs/validators
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        threshold: Threshold,
        display_name: str | None,
        filter: Filter | None = None,
        reference: Reference | None = None,
        initialize_with_backfill: bool = False,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param name: Unique resource name assigned to the validator. (immutable)
        :param window: The window to attach the validator to. (immutable)
        :param segmentation: The segmentation to attach the validator to. (immutable)
        :param threshold: A threshold configuration to attach to the validator.
            Note: While a threshold's configuration can be updated, it is not
            possible to change the threshold type after the validator has been
            created.
        :param filter: Optional filter to attach to the validator.
            https://docs.validio.io/docs/validators#filters
        :param reference: Configuration for reference validators
        :param initialize_with_backfill: If set to true, will wait for an
            explicit source backfill before the validator can start
            processing data.
            https://docs.validio.io/docs/validators#backfill
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=window._resource_graph,
        )

        if window.source_name != segmentation.source_name:
            raise ManifestConfigurationError(
                f"invalid {self.__class__.__name__} validator '{name}': "
                f"window source '{window.source_name}' does not match "
                f"segmentation source '{segmentation.source_name}'"
            )

        source = window._resource_graph._find_source(window.source_name)
        if not source:
            raise ValidioError(
                f"invalid {self.__class__.__name__} validator '{name}': "
                f"missing source '{window.source_name}' for window '{window.name}'"
            )

        _validate_source_window_compatibility(source, window)

        self.source_name: str = source.name
        self.window_name: str = window.name
        self.segmentation_name: str = segmentation.name
        if filter is None:
            self.filter_name = None
        elif filter._in_resource_mode():
            self.filter_name = filter.name
        self.filter = filter

        self.threshold = threshold
        self.reference = reference
        self.initialize_with_backfill: bool = initialize_with_backfill
        self.description = description
        self.tag_names = [t.name for t in tags] if tags is not None else []

        # Ensure always sorted
        self.tag_names.sort()

        source.add(self.name, self)

        if filter and not filter._in_resource_mode():
            self.add_deprecation(
                "Validator's filter uses the deprecated "
                "filter configuration syntax. "
                "This will be unsupported in a future release. "
                "Please switch to using Filter resources by specifying "
                "a 'name' and 'source' argument to the filter"
            )
        if (
            self.reference is not None
            and self.reference.filter is not None
            and not self.reference.filter._in_resource_mode()
        ):
            self.add_deprecation(
                "Reference filter for validator uses the deprecated "
                "filter configuration syntax. "
                "This will be unsupported in a future release. "
                "Please switch to using Filter resources by specifying "
                "a 'name' and 'source' argument to the filter"
            )

        self._check_threshold_deprecation()

    def _filter_resource_mode(self) -> bool:
        return hasattr(self, "filter_name")

    def _force_filter_expression_mode(self) -> None:
        if self._filter_resource_mode():
            delattr(self, "filter_name")
        if self.reference:
            self.reference._force_filter_expression_mode()

    def _check_threshold_deprecation(self) -> None:
        if isinstance(self.threshold, DynamicThreshold):
            if isinstance(
                self.threshold.decision_bounds_type, LegacyDecisionBoundsType
            ):
                self.add_enum_deprecation(self.threshold.decision_bounds_type)
        elif isinstance(self.threshold, DifferenceThreshold):
            if isinstance(self.threshold.difference_type, LegacyDifferenceType):
                self.add_enum_deprecation(self.threshold.difference_type)

            if isinstance(self.threshold.operator, LegacyDifferenceOperator):
                self.add_enum_deprecation(self.threshold.operator)
        elif isinstance(self.threshold, FixedThreshold):
            if isinstance(self.threshold.operator, LegacyComparisonOperator):
                self.add_enum_deprecation(self.threshold.operator)
        else:
            raise ValidioError(f"unknown threshold: {self.threshold}")

    def _maybe_set_field_selector(
        self, field_name: str, field: JsonPointer | FieldSelector
    ) -> str:
        if isinstance(field, str):
            return field

        self.add_deprecation(
            "Field selectors are deprecated and will be removed in a future release. "
            "Please switch to specifying validators explicitly or importing them "
            "into the project. "
        )

        self._field_selector = SelectorWithFieldName(
            field_name=field_name,
            field_selector=field,
        )
        return "<UNRESOLVED>"

    def _maybe_set_reference_field_selector(
        self,
        field_name: str,
        field: JsonPointer | FromFieldSelector,
        source_field_name: str,
        source_field_value: JsonPointer | FieldSelector,
    ) -> str:
        if isinstance(field, str):
            return field

        if not isinstance(source_field_value, FieldSelector):
            raise ManifestConfigurationError(
                f"invalid configuration for validator {self.name}: source field"
                f" {source_field_name} (value={source_field_value}) does not use a"
                " field selector; reference field can only be used with a matching"
                " source field selector"
            )

        self._reference_field_selector = {"field_name": field_name}
        return "<UNRESOLVED>"

    def _validate_reference_filter_no_field_selector(self) -> None:
        if (
            self.reference
            and self.reference.filter
            and hasattr(self.reference.filter, "_field_selector")
        ):
            raise ManifestConfigurationError(
                f"invalid {self.__class__.__name__} '{self.name}': "
                "field selector not allowed in a reference filter configuration"
            )

    def _validate_unique_field_selector(self) -> None:
        if (
            hasattr(self, "_field_selector")
            and self.filter
            and hasattr(self.filter, "_field_selector")
        ):
            raise ManifestConfigurationError(
                f"invalid {self.__class__.__name__} '{self.name}': "
                "field selector cannot be used in both source field "
                "and filter at the same time "
            )

        self._validate_reference_filter_no_field_selector()

    def _validate_no_field_selector(self) -> None:
        position = None
        if hasattr(self, "_field_selector"):
            position = f"field '{self._field_selector.field_name}'"
        elif self.filter and hasattr(self.filter, "_field_selector"):
            position = "filter configuration"

        if position:
            raise ManifestConfigurationError(
                f"invalid {self.__class__.__name__} '{self.name}': "
                f"field selector not allowed in {position}"
            )

        self._validate_reference_filter_no_field_selector()

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        objects: dict[str, Diffable | list[Diffable] | None] = {
            "threshold": self.threshold,
        }
        if not self._filter_resource_mode():
            objects["filter"] = self.filter
        if self.reference:
            objects["reference"] = self.reference

        return objects

    def _nested_mutable_parents(self) -> dict[str, str | None]:
        if not self.reference or not self.reference._filter_resource_mode():
            return {}
        return {"filter_name": self.reference.filter_name}

    def _supports_filter(self) -> bool:
        """Returns true if the validator supports filters."""
        return True

    def _supports_metric(self) -> bool:
        """Returns true if the validator supports metric property."""
        return True

    def _immutable_fields(self) -> set[str]:
        fields = {
            "source_name",
            "window_name",
            "segmentation_name",
        }

        if self._supports_metric():
            fields.add("metric")

        return fields

    def _mutable_fields(self) -> set[str]:
        fields = {
            *super()._mutable_fields(),
            *{"description"},
        }

        if self._supports_filter() and self._filter_resource_mode():
            fields.add("filter_name")

        return fields

    def _ignored_fields(self) -> set[str]:
        return {
            # initialize_with_backfill is treated as a hint on the backend.
            # So what the client sets is not necessarily what the server will
            # return back. The field is also unused after validator creation
            # so that it doesn't matter to diff it. So we ignore it always.
            "initialize_with_backfill",
        }

    def _replace_on_type_change_fields(self) -> set[str]:
        # We can't switch threshold type e.g. going from dynamic to fixed
        # threshold without re-creating the validator.
        return {"threshold"}

    def resource_class_name(self) -> str:
        """Returns the base class name."""
        return "Validator"

    def _source_config_create_input(self, ctx: "DiffContext") -> dict[str, Any]:
        source_id = ctx.sources[self.source_name]._id.value
        segmentation_id = ctx.segmentations[self.segmentation_name]._id.value
        window_id = ctx.windows[self.window_name]._id.value

        return {
            "sourceId": source_id,
            "segmentationId": segmentation_id,
            "windowId": window_id,
            **self._filter_api_input(ctx),
        }

    def _source_config_update_input(self, ctx: "DiffContext") -> dict[str, Any]:
        return self._filter_api_input(ctx)

    def _filter_api_input(
        self,
        ctx: "DiffContext",
    ) -> dict[str, Any]:
        if self._filter_resource_mode():
            return {
                "filterId": (
                    ctx.filters[self.filter_name]._id.value
                    if self.filter_name is not None
                    else None
                )
            }

        return {
            "filter": (
                self.filter._api_json_filter_expression_create_input()
                if self.filter
                else None
            )
        }

    def _api_create_input(self, _namespace: str, ctx: "DiffContext") -> Any:
        overrides = {
            "sourceConfig": self._source_config_create_input(ctx),
            "tagIds": [ctx.tags[name]._must_id() for name in self.tag_names],
        }

        if self.reference is not None:
            overrides[
                "referenceSourceConfig"
            ] = self.reference._reference_source_config_create_input(ctx)

        return {
            **_api_create_input_params(
                self,
                skip_fields={"tagNames"},
                overrides=overrides,
            ),
            "threshold": self.threshold._api_create_input(),
        }

    def _api_update_input(self, _namespace: str, ctx: "DiffContext") -> Any:
        overrides: dict[str, Any] = {
            "tagIds": [ctx.tags[name]._must_id() for name in self.tag_names],
        }

        if self._supports_filter():
            overrides["sourceConfig"] = self._source_config_update_input(ctx)

        if self.reference is not None:
            overrides[
                "referenceSourceConfig"
            ] = self.reference._reference_source_config_update_input(ctx)

        return _api_update_input_params(
            self,
            skip_fields={"tagNames"},
            overrides=overrides,
        )

    def _api_create_arguments(self) -> dict[str, str]:
        return {
            "input": f"{self.__class__.__name__}CreateInput!",
            "threshold": f"{self.threshold.__class__.__name__}CreateInput!",
        }

    def _api_create_method_name(self) -> str:
        name = self.__class__.__name__
        lc_first = name[0].lower() + name[1:]

        return f"{lc_first}With{self.threshold.__class__.__name__}Create"

    async def _api_update(
        self,
        namespace: str,
        ctx: "DiffContext",
        session: Session,
    ) -> None:
        # Update the validator
        await super()._api_update(namespace, ctx, session=session)

        # For validators, update the threshold as well. Those have
        # an explicit update api.
        method_name = f"validatorWith{self.threshold.__class__.__name__}Update"
        arguments = {
            "input": f"ValidatorWith{self.threshold.__class__.__name__}UpdateInput!"
        }
        api_input = {"input": self.threshold._api_update_input(self._must_id())}

        response = await execute_mutation(
            session,
            method_name,
            arguments,
            api_input,
            resource_class_name=self.resource_class_name().lower(),
            returns="id",
        )

        self._check_graphql_response(
            response=response,
            method_name=method_name,
            response_field=None,
        )

    def _encode(self) -> dict[str, object]:
        skip_fields = {"reference"} if self.reference is None else set({})
        if self._filter_resource_mode():
            skip_fields.add("filter")
        return _encode_resource(self, skip_fields=skip_fields)

    @staticmethod
    def _decode_pending(ctx: "DiffContext") -> None:
        for name, (cls, obj) in ctx.pending_validators_raw.items():
            config_obj = obj[CONFIG_FIELD_NAME]
            window_name = config_obj["window_name"]
            segmentation_name = config_obj["segmentation_name"]

            if window_name not in ctx.windows:
                raise ValidioError(
                    f"failed to decode validator {name}: missing window {window_name}"
                )
            if segmentation_name not in ctx.segmentations:
                raise ValidioError(
                    f"failed to decode validator {name}: missing segmentation"
                    f" {segmentation_name}"
                )

            window = ctx.windows[window_name]
            segmentation = ctx.segmentations[segmentation_name]

            ctx.validators[name] = Validator._decode(
                ctx, cls, obj, window, segmentation
            )

    @staticmethod
    def _decode(
        ctx: "DiffContext",
        cls: type,
        obj: dict[str, Any],
        window: Window,
        segmentation: Segmentation,
    ) -> "Validator":
        obj = get_config_node(obj)

        filter_ = Validator._decode_filter(obj, ctx.filters)

        obj = {
            k: v
            for k, v in obj.items()
            if k
            not in {
                # Drop fields here that are not part of the constructor.
                # They will be reinitialized by the constructor.
                "source_name",
                "window_name",
                "segmentation_name",
                "filter_name",
            }
        }

        threshold = Threshold._decode(obj["threshold"])

        reference = (
            Reference._decode(
                obj["reference"],
                ctx.sources,
                ctx.windows,
                ctx.filters,
            )
            if obj.get("reference")
            else None
        )

        # If the validator uses a field selector, then replace the corresponding
        # field with the selector - since they are both the same field from the
        # constructor's pov.
        FieldSelector._replace(obj)

        # Similarly, if the validator uses a reference field selector, replace it.
        if "_reference_field_selector" in obj:
            selector_obj = obj["_reference_field_selector"]
            obj[selector_obj["field_name"]] = FieldSelector.reference()
            del obj["_reference_field_selector"]

        tags = [ctx.tags[name] for name in obj.get("tag_names", [])]
        del obj["tag_names"]

        return cls(
            **{
                **obj,
                "window": window,
                "segmentation": segmentation,
                "threshold": threshold,
                "tags": tags,
                **({"filter": filter_} if filter_ else {}),
                **({"reference": reference} if reference else {}),
            }
        )

    @staticmethod
    def _decode_filter(
        obj: dict[str, Any],
        all_filters: dict[str, "Filter"],
    ) -> Filter | None:
        if "filter_name" in obj:
            # Resource mode
            filter_name = obj["filter_name"]
            if filter_name and filter_name not in all_filters:
                raise ValidioError(
                    f"invalid configuration: no such filter {filter_name}"
                )
            filter_ = all_filters.get(filter_name)
        else:
            # JsonFilterExpression mode.
            filter_ = Filter._decode(obj["filter"], None) if obj.get("filter") else None

        return filter_


class NumericValidator(Validator):
    """A Numeric validator resource.

    https://docs.validio.io/docs/numeric
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: NumericMetric | LegacyNumericMetric,
        source_field: JsonPointer | FieldSelector,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_field: Field to monitor. (immutable)
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyNumericMetric):
            self.add_enum_deprecation(metric)

        self.metric = NumericMetric(metric) if isinstance(metric, str) else metric
        self.source_field: str = self._maybe_set_field_selector(
            "source_field", source_field
        )

        self._validate_unique_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field",
                "metric",
            },
        }


class VolumeValidator(Validator):
    """A Volume validator resource.

    https://docs.validio.io/docs/volume
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: VolumeMetric | LegacyVolumeMetric,
        source_fields: list[str] | None = None,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        # Deprecated.
        optional_source_field: JsonPointer | FieldSelector | None = None,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_fields: List of fields for the DUPLICATES and UNIQUE metrics.
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param optional_source_field: Deprecated. (immutable)
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyVolumeMetric):
            self.add_enum_deprecation(metric)

        self.metric = (
            metric if isinstance(metric, VolumeMetric) else VolumeMetric(metric)
        )

        self.optional_source_field: str | None = None
        if optional_source_field:
            self.optional_source_field = self._maybe_set_field_selector(
                "optional_source_field", optional_source_field
            )

        self.source_fields = source_fields if source_fields else []

        self._validate_unique_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{"optional_source_field", "source_fields", "metric"},
        }

    def _api_create_input(self, namespace: str, ctx: "DiffContext") -> Any:
        api_input = super()._api_create_input(namespace, ctx)
        _rename_dict_key(api_input["input"], "optionalSourceField", "sourceField")

        return api_input


class NumericDistributionValidator(Validator):
    """A Numeric distribution validator resource.

    https://docs.validio.io/docs/numeric-distribution
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: NumericDistributionMetric | LegacyNumericDistributionMetric,
        source_field: JsonPointer | FieldSelector,
        reference_source_field: JsonPointer | FromFieldSelector,
        reference: Reference,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_field: Field to monitor. (immutable)
        :param reference_source_field: Reference field to compare against. (immutable)
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            reference=reference,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyNumericDistributionMetric):
            self.add_enum_deprecation(metric)

        self.metric = (
            metric
            if isinstance(metric, NumericDistributionMetric)
            else NumericDistributionMetric(metric)
        )

        self.source_field: str = self._maybe_set_field_selector(
            "source_field", source_field
        )
        self.reference_source_field: str = self._maybe_set_reference_field_selector(
            "reference_source_field",
            reference_source_field,
            "source_field",
            source_field,
        )

        self._validate_unique_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field",
                "reference_source_field",
            },
        }


class CategoricalDistributionValidator(Validator):
    """A Categorical distribution validator resource.

    https://docs.validio.io/docs/categorical-distribution
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: CategoricalDistributionMetric | LegacyCategoricalDistributionMetric,
        source_field: JsonPointer | FieldSelector,
        reference_source_field: JsonPointer | FromFieldSelector,
        reference: Reference,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_field: Field to monitor. (immutable)
        :param reference_source_field: Reference field to
            compare against. (immutable)
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            reference=reference,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyCategoricalDistributionMetric):
            self.add_enum_deprecation(metric)

        self.metric = (
            metric
            if isinstance(metric, CategoricalDistributionMetric)
            else CategoricalDistributionMetric(metric)
        )

        self.source_field: str = self._maybe_set_field_selector(
            "source_field", source_field
        )
        self.reference_source_field: str = self._maybe_set_reference_field_selector(
            "reference_source_field",
            reference_source_field,
            "source_field",
            source_field,
        )

        self._validate_unique_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field",
                "reference_source_field",
            },
        }


class NumericAnomalyValidator(Validator):
    """A Numeric anomaly validator resource.

    https://docs.validio.io/docs/numeric-anomaly
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: NumericAnomalyMetric | LegacyNumericAnomalyMetric,
        source_field: JsonPointer | FieldSelector,
        reference_source_field: JsonPointer | FromFieldSelector,
        reference: Reference,
        sensitivity: float,
        minimum_absolute_difference: float,
        minimum_relative_difference_percent: float,
        minimum_reference_datapoints: float | None = None,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_field: Field to monitor. (immutable)
        :param reference_source_field: Reference field to
            compare against. (immutable)
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            reference=reference,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyNumericAnomalyMetric):
            self.add_enum_deprecation(metric)

        self.metric = (
            metric
            if isinstance(metric, NumericAnomalyMetric)
            else NumericAnomalyMetric(metric)
        )
        self.sensitivity = sensitivity
        self.minimum_absolute_difference = minimum_absolute_difference
        self.minimum_relative_difference_percent = minimum_relative_difference_percent
        self.minimum_reference_datapoints = minimum_reference_datapoints

        self.source_field: str = self._maybe_set_field_selector(
            "source_field", source_field
        )
        self.reference_source_field: str = self._maybe_set_reference_field_selector(
            "reference_source_field",
            reference_source_field,
            "source_field",
            source_field,
        )

        self._validate_unique_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field",
                "reference_source_field",
                "sensitivity",
                "minimum_absolute_difference",
                "minimum_relative_difference_percent",
                "minimum_reference_datapoints",
            },
        }


class RelativeVolumeValidator(Validator):
    """A Relative volume validator resource.

    https://docs.validio.io/docs/relative-volume
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: RelativeVolumeMetric | LegacyRelativeVolumeMetric,
        reference: Reference,
        source_field: JsonPointer | None = None,
        reference_source_field: JsonPointer | None = None,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_field: Field to monitor. (immutable)
        :param reference_source_field: Reference field to compare
            against. (immutable)
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            reference=reference,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyRelativeVolumeMetric):
            self.add_enum_deprecation(metric)

        self.metric = (
            metric
            if isinstance(metric, RelativeVolumeMetric)
            else RelativeVolumeMetric(metric)
        )
        self.source_field = source_field
        self.reference_source_field = reference_source_field

        self._validate_no_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field",
                "reference_source_field",
            },
        }


class RelativeTimeValidator(Validator):
    """A Relative time validator resource.

    https://docs.validio.io/docs/relative-time
    """

    def __init__(
        self,
        name: str,
        window: Window,
        segmentation: Segmentation,
        metric: RelativeTimeMetric | LegacyRelativeTimeMetric,
        source_field_minuend: JsonPointer,
        source_field_subtrahend: JsonPointer,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """
        Constructor.

        :param source_field_minuend: Timestamp field to monitor. (immutable)
        :param source_field_subtrahend: Reference timestamp to subtract. (immutable)
        :param metric: Metric type for the validator. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        if isinstance(metric, LegacyRelativeTimeMetric):
            self.add_enum_deprecation(metric)

        self.metric = (
            metric
            if isinstance(metric, RelativeTimeMetric)
            else RelativeTimeMetric(metric)
        )
        self.source_field_minuend = source_field_minuend
        self.source_field_subtrahend = source_field_subtrahend

        self._validate_no_field_selector()

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field_minuend",
                "source_field_subtrahend",
            },
        }


class FreshnessValidator(Validator):
    """A Freshness validator resource.

    https://docs.validio.io/docs/freshness
    """

    def __init__(
        self,
        name: str,
        window: TumblingWindow,
        segmentation: Segmentation,
        threshold: Threshold = DynamicThreshold(3),
        filter: Filter | None = None,
        initialize_with_backfill: bool = False,
        source_field: JsonPointer | None = None,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """Constructor."""
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            filter=filter,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        self.source_field = source_field

        self._validate_no_field_selector()

    def _supports_metric(self) -> bool:
        return False

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "source_field",
            },
        }


class SqlValidator(Validator):
    """A SQL validator resource.

    https://docs.validio.io/docs/custom-sql
    """

    def __init__(
        self,
        name: str,
        window: TumblingWindow,
        segmentation: Segmentation,
        query: str,
        threshold: Threshold = DynamicThreshold(3),
        initialize_with_backfill: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
        description: str | None = None,
        tags: list[Tag] | None = None,
    ):
        """Constructor.

        :param query: SQL query to execute. (immutable)
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        :param description: Description of the resource.
        :param tags: Tags to add to the resource
        """
        super().__init__(
            name=name,
            window=window,
            segmentation=segmentation,
            threshold=threshold,
            initialize_with_backfill=initialize_with_backfill,
            display_name=display_name,
            ignore_changes=ignore_changes,
            description=description,
            tags=tags,
        )

        for r in [
            r"({{\s*table\s*}})",
            r"({{\s*select_columns\s*}})",
            r"({{\s*group_by_columns\s*}})",
        ]:
            match = re.search(r, query)
            if match:
                self.add_deprecation(
                    f"SQL syntax {match.groups(1)[0]} is deprecated "
                    f"and support will be removed in a future release. "
                    f"Please see the SQL validator documentation for the "
                    f"alternative SQL syntax: "
                    f"https://docs.validio.io/docs/custom-sql"
                )
                break

        self.query = query

        self._validate_no_field_selector()

    def _supports_filter(self) -> bool:
        return False

    def _supports_metric(self) -> bool:
        return False

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        objects: dict[str, Diffable | list[Diffable] | None] = {
            "threshold": self.threshold,
        }

        return objects

    def _mutable_fields(self) -> set[str]:
        return {*super()._mutable_fields(), *{"query"}}

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
        }


def _validate_source_window_compatibility(source: Source, window: Window) -> None:
    """
    Validate source and window compatibility.

    To avoid creating a partial configuration and bail out once the creating of
    the validator is done we do some pre validation of combination we know is
    invalid.
    """
    is_demo_source = isinstance(source, DemoSource)
    is_stream_source = issubclass(source.__class__, StreamSource)
    is_object_storage_source = issubclass(source.__class__, ObjectStorageSource)
    is_warehouse_source = (
        not is_stream_source and not is_object_storage_source and not is_demo_source
    )

    if (isinstance(window, FileWindow) and not is_object_storage_source) or (
        isinstance(window, GlobalWindow) and not is_warehouse_source
    ):
        raise ManifestConfigurationError(
            f"invalid window '{window.__class__.__name__}' on source type "
            f"'{source.__class__.__name__}'"
        )
