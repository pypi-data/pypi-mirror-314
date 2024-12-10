import json
from typing import Annotated, Any

import requests
from pydantic import Field, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from pyvfg import VFG, vfg_from_json, vfg_to_json

VFG_SCHEMA_REF_URL = "https://verses-json-schema-registry-gitops-usw1.s3.us-west-1.amazonaws.com/vfg/0_3_0/vfg_0_3_0.json"
VFG_EXAMPLE_REF_URL = "https://verses-json-schema-registry-gitops-usw1.s3.us-west-1.amazonaws.com/vfg/examples/small/sprinkler_factor_graph_vfg.json"

VFG_EXAMPLE_JSON = requests.get(VFG_EXAMPLE_REF_URL).json()


class _VFGPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * JSON strings will be parsed as `VFG` instances by calling `vfg_from_json()`
        * JSON dictionaries will be parsed as `VFG` instances by calling `vfg_from_json()`
        * `VFG` instances will be parsed as `VFG` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return the string from `vfg_to_json()`
        """

        def validate_from_str(value: str) -> VFG:
            # Pydantic will catch the `ValueError` and raise `ValidationError`
            json.loads(value)
            return vfg_from_json(value)

        def validate_from_dict(value: dict[str, Any]) -> VFG:
            return vfg_from_json(json.dumps(value))

        def serialize(instance: VFG) -> str:
            return json.loads(vfg_to_json(instance))

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        from_dict_schema = core_schema.chain_schema(
            [
                core_schema.dict_schema(),
                core_schema.no_info_plain_validator_function(validate_from_dict),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_dict_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(VFG),
                    from_str_schema,
                    from_dict_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(serialize),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """
        Return an external reference to the VFG schema we currently support.
        Using an external URL allows us to bypass pydantic's internal core_schema checking during
        JSON schema retrieval, which would otherwise throw a `KeyError` if we tried to supply
        the JSON schema as an object directly in this method. This allows the consumer of the
        JSON schema (e.g. FastAPI) to fetch the schema on the client side during API doc
        generation.
        """
        return {
            "$ref": VFG_SCHEMA_REF_URL,
        }


VFGPydanticType = Annotated[
    VFG,
    _VFGPydanticAnnotation,
    Field(
        ...,
        examples=[VFG_EXAMPLE_JSON],
    ),
]
