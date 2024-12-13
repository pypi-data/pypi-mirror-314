"""Window configuration."""

from enum import Enum
from typing import TYPE_CHECKING, Any

from validio_sdk.graphql_client.enums import WindowTimeUnit as LegacyWindowTimeUnit
from validio_sdk.resource._resource import Resource
from validio_sdk.resource._serde import (
    NODE_TYPE_FIELD_NAME,
    ImportValue,
    _api_create_input_params,
    _encode_resource,
    _import_resource_params,
    get_config_node,
)
from validio_sdk.resource.sources import Source

if TYPE_CHECKING:
    from validio_sdk.resource._diff import DiffContext


class WindowTimeUnit(str, Enum):
    """Unit of window time."""

    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"
    MONTH = "MONTH"
    WEEK = "WEEK"


class Window(Resource):
    """
    Base class for a window resource.

    https://docs.validio.io/docs/windows
    """

    def __init__(
        self,
        name: str,
        source: Source,
        display_name: str | None,
        ignore_changes: bool = False,
    ) -> None:
        """
        Constructor.

        :param name: Unique resource name assigned to the window
        :param source: The source to attach the window to
        :param display_name: Human-readable name for the window. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            __internal__=source._resource_graph,
        )
        self.source_name: str = source.name

        source.add(self.name, self)

    def _immutable_fields(self) -> set[str]:
        return {"source_name", "data_time_field"}

    def resource_class_name(self) -> str:
        """Returns the base class name."""
        return "Window"

    def _api_create_input(self, _namespace: str, ctx: "DiffContext") -> Any:
        return _api_create_input_params(
            self,
            overrides={"sourceId": ctx.sources[self.source_name]._must_id()},
        )

    def _encode(self) -> dict[str, object]:
        # Drop fields here that are not part of the constructor for when
        # we deserialize back. They will be reinitialized by the constructor.
        return _encode_resource(self, skip_fields={"source_name"})

    @staticmethod
    def _decode(obj: dict[str, Any], source: Source) -> "Window":
        cls = eval(obj[NODE_TYPE_FIELD_NAME])
        args = get_config_node(obj)

        return cls(**{**args, "source": source})


class GlobalWindow(Window):
    """
    A Global window resource.

    Represent a single window spanning over all the data.
    """

    def __init__(
        self,
        name: str,
        source: Source,
        display_name: str | None = None,
        ignore_changes: bool = False,
    ) -> None:
        """
        Constructor.

        Since a global window spans over all data the constructor needs no
        argument other than a name and a source.

        :param ignore_changes: If set to true, changes to the resource will be ignored.
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        """
        super().__init__(
            name=name,
            display_name=display_name,
            ignore_changes=ignore_changes,
            source=source,
        )

    def _import_params(self) -> dict[str, ImportValue]:
        return _import_resource_params(
            resource=self,
            skip_fields={"data_time_field"},
        )

    def _immutable_fields(self) -> set[str]:
        # We must override the parent class immutable fields because for global
        # windows we don't even have a `data_time_field`.
        return {"source_name"}


class TumblingWindow(Window):
    """A Tumbling window resource."""

    def __init__(
        self,
        name: str,
        source: Source,
        data_time_field: str,
        window_size: int,
        time_unit: WindowTimeUnit | LegacyWindowTimeUnit,
        window_timeout_disabled: bool = False,
        display_name: str | None = None,
        ignore_changes: bool = False,
    ):
        """
        Constructor.

        :param data_time_field: Data time field for the window
        :param window_size: Size of the tumbling window
        :param time_unit: Unit of the specified window_size.
            (minimum window size is 30 minutes)
        :param window_timeout_disabled: Disable timeout for windows before
            closing them.
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        """
        super().__init__(
            name=name,
            source=source,
            display_name=display_name,
            ignore_changes=ignore_changes,
        )

        if isinstance(time_unit, LegacyWindowTimeUnit):
            self.add_enum_deprecation(time_unit)

        self.data_time_field: str = data_time_field
        self.window_size: int = window_size
        self.time_unit = (
            # When we decode, enums are passed in a strings
            time_unit
            if isinstance(time_unit, (WindowTimeUnit, LegacyWindowTimeUnit))
            else WindowTimeUnit(time_unit)
        )
        self.window_timeout_disabled = window_timeout_disabled

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{"time_unit", "window_size"},
        }

    def _mutable_fields(self) -> set[str]:
        return {
            *super()._mutable_fields(),
            *{"window_timeout_disabled"},
        }


class FixedBatchWindow(Window):
    """
    A FixedBatch window resource.

    https://docs.validio.io/docs/windows-configuration#31-fixed-batch-window
    """

    def __init__(
        self,
        name: str,
        source: Source,
        data_time_field: str,
        batch_size: int,
        segmented_batching: bool = False,
        batch_timeout_secs: int | None = None,
        display_name: str | None = None,
        ignore_changes: bool = False,
    ):
        """
        Constructor.

        :param data_time_field: Data time field for the window
        :param batch_size: Number of datapoints that form a Window
        :param segmented_batching: If True, each segment gets a separate
            Window of batch_size length.
        :param batch_timeout_secs: If segmented_batching is True, applies a timeout
            after which any collected datapoints for a segment will be force-processed
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored.
        """
        super().__init__(
            name=name,
            source=source,
            display_name=display_name,
            ignore_changes=ignore_changes,
        )

        self.data_time_field: str = data_time_field
        self.batch_size = batch_size
        self.segmented_batching = segmented_batching
        self.batch_timeout_secs = batch_timeout_secs

    def _immutable_fields(self) -> set[str]:
        return {
            *super()._immutable_fields(),
            *{
                "segmented_batching",
            },
        }

    def _mutable_fields(self) -> set[str]:
        return {
            *super()._mutable_fields(),
            *{"batch_size", "batch_timeout_secs"},
        }


class FileWindow(Window):
    """
    A File window resource.

    https://docs.validio.io/docs/windows-configuration#34-file-window
    """

    def __init__(
        self,
        name: str,
        source: Source,
        data_time_field: str,
        display_name: str | None = None,
        ignore_changes: bool = False,
    ):
        """
        Constructor.

        :param data_time_field: Data time field for the window
        :param display_name: Human-readable name for the validator. This name is
          visible in the UI and does not need to be unique. (mutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        """
        super().__init__(
            name=name,
            source=source,
            display_name=display_name,
            ignore_changes=ignore_changes,
        )

        self.data_time_field: str = data_time_field
