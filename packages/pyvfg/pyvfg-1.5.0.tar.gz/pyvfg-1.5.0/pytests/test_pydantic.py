import json

import pytest
import pyvfg
from pydantic import BaseModel, ValidationError
from pyvfg import VFGPydanticType


# Create a model class that uses this annotation as a field
class VFGModel(BaseModel):
    vfg: VFGPydanticType


@pytest.fixture
def sprinkler_vfg() -> str:
    with open("./test_data/small/sprinkler_factor_graph_vfg.json", "r") as f:
        return f.read()


def test_model_passthrough(sprinkler_vfg):
    vfg = pyvfg.vfg_from_json(sprinkler_vfg)
    model = VFGModel(vfg=vfg)


def test_model_from_json_str(sprinkler_vfg):
    model = VFGModel(vfg=sprinkler_vfg)


def test_model_from_json_object(sprinkler_vfg):
    model = VFGModel(vfg=json.loads(sprinkler_vfg))


def test_model_from_str_invalid():
    with pytest.raises(ValidationError):
        model = VFGModel(vfg="test")


def test_model_from_unsupported_python_type_invalid():
    with pytest.raises(ValidationError):
        model = VFGModel(vfg="test")


def test_model_dump(sprinkler_vfg):
    model = VFGModel(vfg=sprinkler_vfg)
    print(model.model_dump())


def test_model_sdump_json(sprinkler_vfg):
    model = VFGModel(vfg=sprinkler_vfg)
    print(model.model_dump_json())


def test_model_json_schema(sprinkler_vfg):
    model = VFGModel(vfg=sprinkler_vfg)
    print(json.dumps(model.model_json_schema()))
