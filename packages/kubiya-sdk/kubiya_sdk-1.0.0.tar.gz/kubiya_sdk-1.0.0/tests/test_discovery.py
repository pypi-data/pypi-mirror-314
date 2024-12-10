import os
import tempfile

from kubiya_sdk.utils.discovery import discover_workflows_and_tools
from kubiya_sdk.workflows.stateful_workflow import StatefulWorkflow


def create_test_project(base_dir):
    os.makedirs(os.path.join(base_dir, "workflows"))
    with open(os.path.join(base_dir, "workflows", "test_workflow.py"), "w") as f:
        f.write(
            """
from kubiya_sdk.workflows import StatefulWorkflow

def create_test_workflow():
    workflow = StatefulWorkflow("TestWorkflow")

    @workflow.step(name="step1")
    def step1(state):
        return {"result": state["input"] * 2}

    return workflow
"""
        )

    with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
        f.write("kubiya_sdk==1.0.0\n")


def test_discover_workflows_and_tools():
    with tempfile.TemporaryDirectory() as tmpdir:
        create_test_project(tmpdir)

        result = discover_workflows_and_tools(tmpdir)

        assert len(result["workflows"]) == 1
        assert result["workflows"][0]["name"] == "TestWorkflow"
        assert isinstance(result["workflows"][0]["instance"], StatefulWorkflow)
