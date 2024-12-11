import json
from datetime import timedelta
from wallaroo import expression
from wallaroo.checks import Expression, Variables, instrument, dns_compliant


class ModelVersion:
    def __init__(self, name):
        self.name = name
        self.inputs = Variables(name, "input")
        self.outputs = Variables(name, "output")

    def bindings(self, inputs, outputs):
        return {f"{self.name}.input": inputs, f"{self.name}.output": outputs}


def fraud(model, v):
    return model.bindings({}, [[v]])


def single_validation(e: Expression):
    return instrument({"test": e}, [], ["test"])


class TestChecks:
    def test_values_expression(self, snapshot):
        model = ModelVersion("ccfraud")
        one_of = model.outputs[0][0].one_of(0.0, 1.0)
        snapshot.assert_match(json.dumps([one_of.top_json()], indent=4), "values.json")
        snapshot.assert_match(
            json.dumps(single_validation(one_of), indent=4), "gauges.json"
        )

    def test_bounds_expression(self, snapshot):
        model = ModelVersion("ccfraud")
        high_fraud = model.outputs[0][0] >= 0.95
        snapshot.assert_match(
            json.dumps([high_fraud.top_json()], indent=4), "bounds.json"
        )
        snapshot.assert_match(
            json.dumps(single_validation(high_fraud), indent=4), "gauges.json"
        )

    def test_model_drift(self, snapshot):
        model = ModelVersion("ccfraud")
        shadow = ModelVersion("ccfraud_shadow")
        model_drift = expression.abs(model.outputs[0][0] - shadow.outputs[0][0]) < 0.01
        snapshot.assert_match(
            json.dumps([model_drift.top_json()], indent=4), "drift.json"
        )
        snapshot.assert_match(
            json.dumps(single_validation(model_drift), indent=4), "gauges.json"
        )

    def test_aggregate_function(self, snapshot):
        model = ModelVersion("ccfraud")
        high_fraud = expression.count(
            model.outputs[0][0] >= 0.95, "5h", timedelta(minutes=1)
        )
        alert = high_fraud <= 10
        snapshot.assert_match(
            json.dumps(
                instrument({"high_fraud": alert.left.expression()}, ["high_fraud"], []),
                indent=4,
            ),
            "aggregate.json",
        )
        assert (
            alert.promql("high_fraud:left")
            == "sum by (pipeline_id) (pipeline_gauge:high_fraud:left) <= 10"
        )

    def test_dns_compliant(self, snapshot):
        assert dns_compliant("wallaroo") == True
        assert dns_compliant("foo42bar") == True
        assert dns_compliant("foo-bar42") == True
        assert dns_compliant("foo-bar42-") == False
        assert dns_compliant("") == False
        assert dns_compliant("42foo") == False
        assert dns_compliant("hello world") == False
        assert dns_compliant("hello,world") == False
        assert (
            dns_compliant(
                "wallaroowallaroowallaroowallaroowallaroowallaroowallaroowallaroowallaroowallaroo"
            )
            == False
        )
