import json

import pytest

from validio_sdk.exception import ValidioError
from validio_sdk.resource import (
    FieldSelector,
    channels,
    credentials,
    filters,
    notification_rules,
    segmentations,
    sources,
    tags,
    validators,
    windows,
)
from validio_sdk.resource._field_selector import FieldDataType
from validio_sdk.resource._resource import Resource, ResourceDeprecation, ResourceGraph
from validio_sdk.resource._serde import custom_resource_graph_encoder
from validio_sdk.resource.filters import NullFilter, NullFilterOperator
from validio_sdk.resource.notification_rules import IssueTypename
from validio_sdk.resource.thresholds import DynamicThreshold
from validio_sdk.resource.validators import (
    NumericDistributionMetric,
    NumericMetric,
    Reference,
    VolumeMetric,
)
from validio_sdk.resource.windows import WindowTimeUnit


def test__should_build_resource_graph_from_resource_constructors() -> None:
    g = ResourceGraph()

    t1 = tags.Tag(key="t1", value="v1", __internal__=g)
    t2 = tags.Tag(key="t2", value="v2", __internal__=g)

    c1 = credentials.GcpCredential(
        name="c1", credential="svc-acct", enable_catalog=True, __internal__=g
    )
    c2 = credentials.DemoCredential("c2", ignore_changes=True, __internal__=g)

    ch1 = channels.SlackChannel(
        name="ch1",
        application_link_url="foo",
        slack_channel_id="sid",
        token="token",
        signing_secret="secret",
        timezone="utc",
        interactive_message_enabled=True,
        __internal__=g,
    )
    ch2 = channels.WebhookChannel(
        name="ch2",
        application_link_url="foo",
        webhook_url="bar",
        auth_header="secretz",
        __internal__=g,
    )
    ch3 = channels.MsTeamsChannel(
        name="ch3",
        application_link_url="foo",
        ms_teams_channel_id="cid",
        client_id="id",
        client_secret="secret",
        interactive_message_enabled=True,
        timezone="utc",
        __internal__=g,
    )

    s1 = sources.DemoSource("s1", credential=c2, tags=[t1])
    s2 = sources.DemoSource("s2", credential=c2)

    # Multiple segmentations on a source
    s3 = sources.GcpBigQuerySource(
        "s3",
        credential=c1,
        project="proj",
        dataset="dataset",
        table="tab",
        cursor_field="curs",
        lookback_days=32,
        schedule="* * * * *",
    )
    segmentations.Segmentation("seg4", source=s3)
    segmentations.Segmentation("seg5", source=s3)

    f1 = filters.NullFilter(
        name="f1",
        source=s1,
        field="drums",
    )

    f2 = filters.NullFilter(
        name="f2",
        source=s1,
        field="soul",
        operator=NullFilterOperator.IS_NOT,
    )

    f3 = NullFilter(
        name="f3",
        source=s1,
        field=FieldSelector(data_type=FieldDataType.BOOLEAN),
    )

    seg1 = segmentations.Segmentation(
        name="seg1",
        source=s1,
        filter=f1,
    )

    w1 = windows.TumblingWindow(
        "w1",
        source=s1,
        data_time_field="created_at",
        window_size=1,
        time_unit=WindowTimeUnit.DAY,
    )

    seg2 = segmentations.Segmentation("seg2", source=s2)
    # Multiple windows on a source
    w2 = windows.TumblingWindow(
        "w2",
        source=s2,
        data_time_field="updated_at",
        window_size=2,
        time_unit=WindowTimeUnit.MINUTE,
    )
    windows.TumblingWindow(
        "w3",
        source=s2,
        data_time_field="updated_at",
        window_size=1,
        time_unit=WindowTimeUnit.HOUR,
    )

    for field in ["age", "amount"]:
        validators.NumericValidator(
            f"mean_of_{field}",
            window=w1,
            segmentation=seg1,
            metric=NumericMetric.MEAN,
            source_field=field,
        )

    validators.NumericDistributionValidator(
        "max_ratio",
        window=w2,
        segmentation=seg2,
        metric=NumericDistributionMetric.MAXIMUM_RATIO,
        threshold=DynamicThreshold(14),
        source_field=FieldSelector(data_type=FieldDataType.NUMERIC),
        reference_source_field=FieldSelector.reference(),
        filter=f1,
        reference=Reference(
            source=s1,
            window=w1,
            history=14,
            offset=2,
            filter=f2,
        ),
        tags=[t2],
    )

    validators.VolumeValidator(
        "null_count",
        window=w1,
        segmentation=seg1,
        metric=VolumeMetric.COUNT,
        filter=f3,
    )

    notification_rules.NotificationRule(
        name="r1",
        channel=ch1,
        conditions=notification_rules.Conditions(
            source_condition=notification_rules.SourceNotificationRuleCondition(
                sources=[s1, s3],
            ),
            type_condition=notification_rules.TypeNotificationRuleCondition(
                types=[IssueTypename.SchemaChangeSourceError],
            ),
        ),
    )
    notification_rules.NotificationRule(
        name="r2",
        channel=ch2,
    )

    notification_rules.NotificationRule(
        name="r3",
        channel=ch3,
    )

    expected_config = """
{
  "sub_graphs": {
    "_node_type": "sub_graph",
    "Tag": {
      "t1:v1": {
        "_node_type": "Tag",
        "config_field": {
          "key": "t1",
          "value": "v1"
        },
        "ignore_changes": false
      },
      "t2:v2": {
        "_node_type": "Tag",
        "config_field": {
          "key": "t2",
          "value": "v2"
        },
        "ignore_changes": false
      }
    },
    "Credential": {
      "c1": {
        "_node_type": "GcpCredential",
        "ignore_changes": false,
        "config_field": {
          "name": "c1",
          "display_name": "c1",
          "credential": "svc-acct",
          "enable_catalog": true
        },
        "_children": {
          "_node_type": "_children",
          "Source": {
            "s3": {
              "_node_type": "GcpBigQuerySource",
              "ignore_changes": false,
              "config_field": {
                "name": "s3",
                "description": null,
                "display_name": "s3",
                "jtd_schema": null,
                "project": "proj",
                "dataset": "dataset",
                "tag_names": [],
                "table": "tab",
                "cursor_field": "curs",
                "lookback_days": 32,
                "schedule": "* * * * *"
              },
              "_children": {
                "_node_type": "_children",
                "Segmentation": {
                  "seg4": {
                    "_node_type": "Segmentation",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "seg4",
                      "display_name": "seg4",
                      "fields": [],
                      "filter_name": null
                    }
                  },
                  "seg5": {
                    "_node_type": "Segmentation",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "seg5",
                      "display_name": "seg5",
                      "fields": [],
                      "filter_name": null
                    }
                  }
                }
              }
            }
          }
        }
      },
      "c2": {
        "_node_type": "DemoCredential",
        "config_field": {
          "name": "c2",
          "display_name": "c2"
        },
        "ignore_changes": true,
        "_children": {
          "_node_type": "_children",
          "Source": {
            "s1": {
              "_node_type": "DemoSource",
              "ignore_changes": false,
              "config_field": {
                "name": "s1",
                "description": null,
                "display_name": "s1",
                "jtd_schema": null,
                "tag_names": ["t1:v1"]
              },
              "_children": {
                "_node_type": "_children",
                "Segmentation": {
                  "seg1": {
                    "_node_type": "Segmentation",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "seg1",
                      "display_name": "seg1",
                      "fields": [],
                      "filter_name": "f1"
                    }
                  }
                },
                "Window": {
                  "w1": {
                    "_node_type": "TumblingWindow",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "w1",
                      "display_name": "w1",
                      "data_time_field": "created_at",
                      "window_size": 1,
                      "time_unit": "DAY",
                      "window_timeout_disabled": false
                    }
                  }
                },
                "Filter": {
                  "f1": {
                    "_node_type": "NullFilter",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "f1",
                      "display_name": "f1",
                      "field": "drums",
                      "operator": "IS"
                    }
                  },
                  "f2": {
                    "_node_type": "NullFilter",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "f2",
                      "display_name": "f2",
                      "field": "soul",
                      "operator": "IS_NOT"
                    }
                  },
                  "f3": {
                    "_node_type": "NullFilter",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "f3",
                      "display_name": "f3",
                      "_field_selector": {
                        "field_name": "field",
                        "field_selector": {
                          "data_type": "BOOLEAN",
                          "nullable": null,
                          "regex": null
                        }
                      },
                      "field": "<UNRESOLVED>",
                      "operator": "IS"
                    }
                  }
                },
                "Validator": {
                  "mean_of_age": {
                    "_node_type": "NumericValidator",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "mean_of_age",
                      "description": null,
                      "display_name": "mean_of_age",
                      "source_name": "s1",
                      "window_name": "w1",
                      "segmentation_name": "seg1",
                      "filter_name": null,
                      "tag_names": [],
                      "threshold": {
                        "_node_type": "DynamicThreshold",
                        "sensitivity": 3.0,
                        "decision_bounds_type": "UPPER_AND_LOWER"
                      },
                      "initialize_with_backfill": false,
                      "metric": "MEAN",
                      "source_field": "age"
                    }
                  },
                  "mean_of_amount": {
                    "_node_type": "NumericValidator",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "mean_of_amount",
                      "description": null,
                      "display_name": "mean_of_amount",
                      "source_name": "s1",
                      "window_name": "w1",
                      "segmentation_name": "seg1",
                      "filter_name": null,
                      "tag_names": [],
                      "threshold": {
                        "_node_type": "DynamicThreshold",
                        "sensitivity": 3.0,
                        "decision_bounds_type": "UPPER_AND_LOWER"
                      },
                      "initialize_with_backfill": false,
                      "metric": "MEAN",
                      "source_field": "amount"
                    }
                  },
                  "null_count": {
                    "_node_type": "VolumeValidator",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "null_count",
                      "description": null,
                      "display_name": "null_count",
                      "source_name": "s1",
                      "window_name": "w1",
                      "segmentation_name": "seg1",
                      "filter_name": "f3",
                      "tag_names": [],
                      "threshold": {
                        "_node_type": "DynamicThreshold",
                        "sensitivity": 3.0,
                        "decision_bounds_type": "UPPER_AND_LOWER"
                      },
                      "initialize_with_backfill": false,
                      "metric": "COUNT",
                      "optional_source_field": null,
                      "source_fields": []
                    }
                  }
                }
              }
            },
            "s2": {
              "_node_type": "DemoSource",
              "ignore_changes": false,
              "config_field": {
                "name": "s2",
                "description": null,
                "display_name": "s2",
                "jtd_schema": null,
                "tag_names": []
              },
              "_children": {
                "_node_type": "_children",
                "Segmentation": {
                  "seg2": {
                    "_node_type": "Segmentation",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "seg2",
                      "display_name": "seg2",
                      "fields": [],
                      "filter_name": null
                    }
                  }
                },
                "Window": {
                  "w2": {
                    "_node_type": "TumblingWindow",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "w2",
                      "display_name": "w2",
                      "data_time_field": "updated_at",
                      "window_size": 2,
                      "time_unit": "MINUTE",
                      "window_timeout_disabled": false
                    }
                  },
                  "w3": {
                    "_node_type": "TumblingWindow",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "w3",
                      "display_name": "w3",
                      "data_time_field": "updated_at",
                      "window_size": 1,
                      "time_unit": "HOUR",
                      "window_timeout_disabled": false
                    }
                  }
                },
                "Validator": {
                  "max_ratio": {
                    "_node_type": "NumericDistributionValidator",
                    "ignore_changes": false,
                    "config_field": {
                      "name": "max_ratio",
                      "description": null,
                      "display_name": "max_ratio",
                      "source_name": "s2",
                      "window_name": "w2",
                      "segmentation_name": "seg2",
                      "filter_name": "f1",
                      "tag_names": ["t2:v2"],
                      "threshold": {
                        "_node_type": "DynamicThreshold",
                        "sensitivity": 14.0,
                        "decision_bounds_type": "UPPER_AND_LOWER"
                      },
                      "reference": {
                        "source_name": "s1",
                        "window_name": "w1",
                        "history": 14,
                        "offset": 2,
                        "filter_name": "f2"
                      },
                      "initialize_with_backfill": false,
                      "metric": "MAXIMUM_RATIO",
                      "source_field": "<UNRESOLVED>",
                      "_field_selector": {
                        "field_name": "source_field",
                        "field_selector": {
                            "data_type": "NUMERIC",
                            "nullable": null,
                            "regex": null
                        }
                      },
                      "reference_source_field": "<UNRESOLVED>",
                      "_reference_field_selector": {
                        "field_name": "reference_source_field"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "Channel": {
      "ch1": {
        "_node_type": "SlackChannel",
        "ignore_changes": false,
        "config_field": {
          "name": "ch1",
          "display_name": "ch1",
          "application_link_url": "foo",
          "webhook_url": null,
          "slack_channel_id": "sid",
          "token": "token",
          "signing_secret": "secret",
          "interactive_message_enabled": true,
          "timezone": "utc"
        },
        "_children": {
          "_node_type": "_children",
          "NotificationRule": {
            "r1": {
              "_node_type": "NotificationRule",
              "ignore_changes": false,
              "config_field": {
                "name": "r1",
                "display_name": "r1",
                "conditions": {
                  "_node_type": "Conditions",
                  "owner_condition": null,
                  "segment_conditions": null,
                  "severity_condition": null,
                  "source_condition": {
                    "_node_type": "SourceNotificationRuleCondition",
                    "sources": [
                      "s1",
                      "s3"
                    ]
                  },
                  "tag_conditions": null,
                  "type_condition": {
                    "_node_type": "TypeNotificationRuleCondition",
                    "types": [
                      "SchemaChangeSourceError"
                    ]
                  }
                }
              }
            }
          }
        }
      },
      "ch2": {
        "_node_type": "WebhookChannel",
        "ignore_changes": false,
        "config_field": {
          "name": "ch2",
          "display_name": "ch2",
          "application_link_url": "foo",
          "webhook_url": "bar",
          "auth_header": "secretz"
        },
        "_children": {
          "_node_type": "_children",
          "NotificationRule": {
            "r2": {
              "_node_type": "NotificationRule",
              "ignore_changes": false,
              "config_field": {
                "name": "r2",
                "display_name": "r2",
                "conditions": {
                  "_node_type": "Conditions",
                  "owner_condition": null,
                  "segment_conditions": null,
                  "severity_condition": null,
                  "source_condition": null,
                  "tag_conditions": null,
                  "type_condition": null
                }
              }
            }
          }
        }
      },
      "ch3": {
        "_node_type": "MsTeamsChannel",
        "ignore_changes": false,
        "config_field": {
          "name": "ch3",
          "display_name": "ch3",
          "application_link_url": "foo",
          "webhook_url": null,
          "ms_teams_channel_id": "cid",
          "client_id": "id",
          "client_secret": "secret",
          "interactive_message_enabled": true,
          "timezone": "utc"
        },
        "_children": {
          "_node_type": "_children",
          "NotificationRule": {
            "r3": {
              "_node_type": "NotificationRule",
              "ignore_changes": false,
              "config_field": {
                "name": "r3",
                "display_name": "r3",
                "conditions": {
                  "_node_type": "Conditions",
                  "owner_condition": null,
                  "segment_conditions": null,
                  "severity_condition": null,
                  "source_condition": null,
                  "tag_conditions": null,
                  "type_condition": null
                }
              }
            }
          }
        }
      }
    }
  },
  "_deprecations": []
}
"""

    # Ignore deprecation warnings.
    assert len(g._deprecations) == 4  # noqa: PLR2004
    g._deprecations = []

    # Serialize the graph.
    graph_json_str = json.dumps(
        g,
        default=custom_resource_graph_encoder,
        indent=2,
    )

    graph_json = json.loads(graph_json_str)
    expected = json.loads(expected_config)
    assert graph_json == expected

    # Now decode it and encode it again. If decode is correct,
    # we should end up with the exact same encoding.
    (decoded_graph, _) = ResourceGraph._decode(graph_json)
    re_encoded_graph_str = json.dumps(
        decoded_graph,
        default=custom_resource_graph_encoder,
        indent=2,
    )

    actual = json.loads(re_encoded_graph_str)
    actual["_deprecations"] = []
    assert json.loads(graph_json_str) == actual


def test__should_reject_config_with_duplicate_names() -> None:
    g = ResourceGraph()

    # Names are only unique per resource type.
    name = "foo"

    c = credentials.DemoCredential(name, __internal__=g)
    with pytest.raises(ValidioError):
        credentials.DemoCredential(name, __internal__=g)

    s = sources.DemoSource(name, credential=c)
    with pytest.raises(ValidioError):
        sources.DemoSource(name, credential=c)

    seg = segmentations.Segmentation(name, source=s)
    with pytest.raises(ValidioError):
        segmentations.Segmentation(name, source=s)

    w = windows.TumblingWindow(
        name,
        source=s,
        data_time_field="created_at",
        window_size=1,
        time_unit=WindowTimeUnit.DAY,
    )
    with pytest.raises(ValidioError):
        windows.TumblingWindow(
            name,
            source=s,
            data_time_field="created_at",
            window_size=1,
            time_unit=WindowTimeUnit.DAY,
        )

    validators.NumericValidator(
        name,
        window=w,
        segmentation=seg,
        threshold=DynamicThreshold(2),
        metric=NumericMetric.MAX,
        source_field="data",
    )
    with pytest.raises(ValidioError):
        validators.NumericValidator(
            name,
            window=w,
            segmentation=seg,
            threshold=DynamicThreshold(2),
            metric=NumericMetric.MAX,
            source_field="data",
        )


class UnittestResource(Resource):
    def __init__(self, name: str, g: ResourceGraph) -> None:
        super().__init__(
            name=name,
            display_name="disp",
            ignore_changes=False,
            __internal__=g,
        )

        self.add_deprecation("global deprecation")
        self.add_field_deprecation("old_field")
        self.add_field_deprecation("old_field", "new_field")

    def resource_class_name(self) -> str:
        """Returns the base class name."""
        return "UnittestResource"

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return set({})

    def _encode(self) -> dict[str, object]:
        return {"name": self.name}


def test_should_register_deprecations() -> None:
    g = ResourceGraph()
    UnittestResource(name="cool_resource", g=g)

    deprecations = sorted(g._deprecations)
    assert len(deprecations) == 3  # noqa: PLR2004

    for i, message in enumerate(
        [
            "Field 'old_field' is deprecated",
            "Field 'old_field' is deprecated, please use 'new_field' instead",
            "global deprecation",
        ]
    ):
        assert deprecations[i] == ResourceDeprecation(
            resource_type="UnittestResource",
            resource_name="cool_resource",
            message=message,
        )
