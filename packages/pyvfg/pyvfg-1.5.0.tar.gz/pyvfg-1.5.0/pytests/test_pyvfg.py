# -*- coding: utf-8 -*-

import numpy as np
import pytest
import pyvfg


@pytest.fixture
def sprinkler_vfg() -> str:
    with open("./test_data/small/sprinkler_factor_graph_vfg.json", "r") as f:
        return f.read()


def test_vfg_from_json(sprinkler_vfg):
    graph = pyvfg.vfg_from_json(sprinkler_vfg)

    # check graph
    assert graph is not None, "Graph should be created from JSON"
    assert len(graph.variables) == 4, "Sprinkler graph should have 4 variables"
    assert graph.version == "0.3.0", "Graph version should be the latest version"


def test_vfg_to_json(sprinkler_vfg):
    import json

    tmp_graph = pyvfg.vfg_from_json(sprinkler_vfg)
    graph_json2 = pyvfg.vfg_to_json(tmp_graph)

    graph = json.loads(sprinkler_vfg)
    graph2 = json.loads(graph_json2)

    assert len(graph["variables"]) == len(
        graph2["variables"]
    ), "Setting the graph lets us get the same variable count"
    assert len(graph["factors"]) == len(
        graph2["factors"]
    ), "Setting the graph gets us the same factor count"


def test_set_graph(sprinkler_vfg):
    graph = pyvfg.vfg_from_json(sprinkler_vfg)
    pyvfg.set_graph(graph)
    graph2 = pyvfg.get_graph()

    assert graph == graph2, "Setting the graph lets us get the same graph"


def test_probability_distribution():
    assert (
        pyvfg.ProbabilityDistribution.Categorical
        == pyvfg.ProbabilityDistribution.Categorical
    )
    assert (
        pyvfg.ProbabilityDistribution.CategoricalConditional
        == pyvfg.ProbabilityDistribution.CategoricalConditional
    )

    assert (
        pyvfg.ProbabilityDistribution.Categorical
        != pyvfg.ProbabilityDistribution.CategoricalConditional
    )

    assert int(pyvfg.ProbabilityDistribution.Categorical) == 0
    assert int(pyvfg.ProbabilityDistribution.CategoricalConditional) == 1


def test_role():
    assert pyvfg.FactorRole.Transition == pyvfg.FactorRole.Transition
    assert pyvfg.FactorRole.Preference == pyvfg.FactorRole.Preference
    assert pyvfg.FactorRole.Likelihood == pyvfg.FactorRole.Likelihood
    assert pyvfg.FactorRole.InitialStatePrior == pyvfg.FactorRole.InitialStatePrior

    assert pyvfg.FactorRole.Transition != pyvfg.FactorRole.Preference
    assert pyvfg.FactorRole.Transition != pyvfg.FactorRole.Likelihood
    assert pyvfg.FactorRole.Preference != pyvfg.FactorRole.Likelihood
    assert pyvfg.FactorRole.Likelihood != pyvfg.FactorRole.InitialStatePrior

    assert int(pyvfg.FactorRole.Transition) == 1
    assert int(pyvfg.FactorRole.Preference) == 2
    assert int(pyvfg.FactorRole.Likelihood) == 3
    assert int(pyvfg.FactorRole.InitialStatePrior) == 4


def test_create_vfg():
    graph = pyvfg.VFG(
        factors=[
            pyvfg.Factor(
                variables=["rain"],
                distribution=pyvfg.ProbabilityDistribution.Categorical,
            )
        ],
        variables={"rain": pyvfg.DiscreteVariableNamedElements(["on", "off"], None)}
    )
    assert graph != pyvfg.VFG.default()

def test_nice_names():
    assert "%s" % (type(pyvfg.FactorRole.Transition)) == "<class 'pyvfg.FactorRole'>"
    assert "%s" % (type(pyvfg.VFG.default())) == "<class 'pyvfg.VFG'>"
    assert "%s" % (type(pyvfg.Factor.default())) == "<class 'pyvfg.Factor'>"
    assert "%s" % (type(pyvfg.DiscreteVariableNamedElements([]))) == "<class 'pyvfg.DiscreteVariableNamedElements'>"
    assert "%s" % (type(pyvfg.DiscreteVariableAnonymousElements(0))) == "<class 'pyvfg.DiscreteVariableAnonymousElements'>"
    assert "%s" % (type(pyvfg.ProbabilityDistribution.Categorical)) == "<class 'pyvfg.ProbabilityDistribution'>"


def test_factor(sprinkler_vfg):
    graph = pyvfg.vfg_from_json(sprinkler_vfg)
    factors = graph.factors

    assert isinstance(factors, list)

    for factor in factors:
        assert isinstance(factor.variables, list)
        assert isinstance(factor.distribution, pyvfg.ProbabilityDistribution)
        assert isinstance(factor.values, np.ndarray)
        assert factor.role == pyvfg.FactorRole.NoRole


def test_vfg(sprinkler_vfg):
    graph = pyvfg.vfg_from_json(sprinkler_vfg)

    assert isinstance(graph.version, str)
    assert isinstance(graph.factors, list)
    assert isinstance(graph.variables, dict)

def test_validate(sprinkler_vfg):
    graph = pyvfg.vfg_from_json(sprinkler_vfg)
    pyvfg.validate_graph(graph)

def test_validate_failure():
    with pytest.raises(pyvfg.JsonSerializationError):
        pyvfg.vfg_from_json("not_json")
    with pytest.raises(pyvfg.JsonSerializationError):
        pyvfg.vfg_from_json("{}")

def test_variable_export(sprinkler_vfg):
    """
    Tests that our Variable type is properly exported to python
    :param sprinkler_vfg: from fixture
    :return: None
    """
    graph = pyvfg.vfg_from_json(sprinkler_vfg)
    rain_var = graph.variables["rain"]
    match type(rain_var):
        case pyvfg.DiscreteVariableNamedElements:
            assert isinstance(rain_var.elements, list)
            assert isinstance(rain_var.role, pyvfg.VariableRole)
        case _:
            assert False, "Should be a discrete variable with named elements"


def test_types_export(sprinkler_vfg):
    """
    Tests that the types exactly align with what we expect.
    :param sprinkler_vfg: from fixture
    :return: None
    """
    vfg = pyvfg.vfg_from_json(sprinkler_vfg)
    assert type(vfg) == pyvfg.VFG, "root type should be pyvfg.VFG"
    assert type(vfg.factors[0]) == pyvfg.Factor, "Factor type should be pyvfg.Factor"
    assert type(vfg.variables["cloudy"]) == pyvfg.DiscreteVariableNamedElements, "Variable type should be pyvfg.DiscreteVariableNamedElements"

def test_version_export() -> None:
    """
    Tests that __version__ is exported
    :return: None
    """
    import re

    assert hasattr(pyvfg, "__version__")
    assert isinstance(pyvfg.__version__, str)
    re.match("\\d+\\.\\d+\\.\\d+", pyvfg.__version__)
