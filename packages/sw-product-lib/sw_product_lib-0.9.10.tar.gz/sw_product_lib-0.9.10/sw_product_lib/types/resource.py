from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from strangeworks_core.platform.gql import API, Operation
from strangeworks_core.types.resource import Resource as ResourceBase


class ResourceConfigurationValueType(Enum):
    BOOL = "BOOL"
    STRING = "STRING"
    SECURE = "SECURE"
    INT = "INT"
    JSON = "JSON"
    DATE = "DATE"
    FLOAT = "FLOAT"

    def equals(self, type: str) -> bool:
        return self.name == type


class ResourceConfiguration(BaseModel):
    key: str
    value: Any
    value_type: str
    is_editable: bool = True
    is_internal: bool = False

    def __init__(
        self,
        key: str,
        value: Any,
        is_secure: bool = False,
        is_editable: bool = True,
        is_internal: bool = False,
    ):
        val_type = "SECURE" if is_secure else type(value).__name__.upper()
        super().__init__(
            key=key,
            value=value,
            is_editable=is_editable,
            is_internal=is_internal,
            value_type="STRING" if val_type == "STR" else val_type,
        )

    @classmethod
    def from_dict(cls, rc: Dict[str, Any]) -> ResourceConfiguration:
        _value_type = rc["type"]
        _value_key = f"value{_value_type.capitalize()}"
        return cls(
            key=rc["key"],
            value=rc[_value_key],
            is_secure=_value_type == "SECURE",
            is_editable=rc.get("isEditable", True),
            is_internal=rc.get("isInternal", False),
        )

    def to_dict(self) -> Dict[str, Any]:
        valueKey = f"value{self.value_type.capitalize()}"

        return {
            "key": self.key,
            "type": self.value_type,
            "isEditable": self.is_editable,
            "isInternal": self.is_internal,
            valueKey: self.value,
        }


class Resource(ResourceBase):
    configurations: list[ResourceConfiguration] | None = None
    api_url: str | None = None

    def __init__(
        self,
        configurations: Optional[list[dict[str, Any]]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.configurations = (
            list(map(lambda x: ResourceConfiguration.from_dict(x), configurations))
            if configurations
            else None
        )

    @classmethod
    def from_dict(cls, res: Dict[str, Any]) -> Resource:
        """Generate a Resourse object from a dictionary.

        The key names in the dictionary must match field names as specified by the
        GraphQL schema for Resource.

        Parameters
        ----------
        cls
            Class that will be instantiated.
        res: Dict
            Resource object attributes represented as a dictionary.

        Return
        ------
        An intance of the Resource object.
        """
        configs = res.pop("configurations") if "configurations" in res else None
        return cls(
            configurations=configs,
            **res,
        )


create_req = Operation(
    query="""
        mutation resourceCreate(
            $activation_id: String!,
            $status: ResourceStatus!,
            $api_route: String,
            $configurations: [StoreConfigurationInput!],
        ){
            resourceCreate(input: {
                resourceActivationId: $activation_id,
                status: $status,
                api_route: $api_route,
                resourceConfigurations: $configurations,
            }) {
                resource {
                id
                slug
                isDeleted
                status
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
              }
            }
        }
        """
)


def create(
    api: API,
    activation_id: str,
    status: str,
    api_route: Optional[str] = None,
    configurations: Optional[List[ResourceConfiguration]] = None,
) -> Resource:
    """Create a new resource definition on the platform.

    Parameters
    ----------
     api: API
        provides access to the platform API.
    """
    api_args = {
        "activation_id": activation_id,
        "status": status,
        "api_route": api_route,
    }

    if configurations:
        api_args["configurations"] = list(map(lambda x: x.to_dict(), configurations))

    result = api.execute(
        op=create_req,
        **api_args,
    )

    return Resource.from_dict(result["resourceCreate"]["resource"])


list_req = Operation(
    query="""
        query resources($status_list: [ResourceStatus!]){
            resources(status: $status_list) {
                id
                slug
                status
                isDeleted
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
        """
)


def fetch(
    api: API,
    status_list: Optional[List[str]] = None,
) -> Optional[List[Resource()]]:
    """Retrieve a list of available resources.

    Parameters
    ----------
    status_list: Optional(List[str])
        retrieve only those resources whose status is included in this list.
    """
    result = api.execute(op=list_req, **locals())
    return list(map(lambda x: Resource.from_dict(x), result["resources"]))


store_config_op = Operation(
    query="""
        mutation resourceStoreConfiguration(
            $key: String!,
            $resource_slug: String!,
            $type: ResourceConfigurationValueType!,
            $isEditable: Boolean!,
            $isInternal: Boolean!,
            $valueBool: Boolean,
            $valueString: String,
            $valueSecure: String,
            $valueInt: Int,
            $valueJson: String,
            $valueDate: Time,
            $valueFloat: Float,
        ){
            resourceStoreConfiguration(
                input: {
                    resourceSlug: $resource_slug,
                    configuration: {
                        key: $key,
                        type: $type,
                        isEditable: $isEditable,
                        isInternal: $isInternal,
                        valueBool: $valueBool,
                        valueString: $valueString,
                        valueSecure: $valueSecure,
                        valueInt: $valueInt,
                        valueJson: $valueJson,
                        valueDate: $valueDate,
                        valueFloat: $valueFloat,
                    }
                }
            ) {
                resourceConfiguration {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
        """,
)


def store_config(
    api: API,
    resource_slug: str,
    config: ResourceConfiguration,
) -> ResourceConfiguration:
    params = config.to_dict()
    params["resource_slug"] = resource_slug
    result = api.execute(op=store_config_op, **params)
    return ResourceConfiguration.from_dict(
        result["resourceStoreConfiguration"]["resourceConfiguration"]
    )


get_op = Operation(
    query="""
        query resource($resource_slug: String!) {
            resource(resourceSlug: $resource_slug){
                id
                slug
                status
                isDeleted
                dateCreated
                dateUpdated
                configurations {
                    key
                    type
                    valueBool
                    valueString
                    valueSecure
                    valueInt
                    valueJson
                    valueDate
                    valueFloat
                    isEditable
                    isInternal
                }
            }
        }
    """,
)


def get(
    api: API,
    resource_slug: str,
) -> Resource:
    """Retrieve a resource entry from platform."""
    raw_result = api.execute(op=get_op, **locals())
    return Resource.from_dict(raw_result["resource"])
