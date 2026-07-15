"""Deployment contract checks for the frontend workflow."""

from pathlib import Path

import yaml


WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/frontend.yml"


def test_deploy_build_uses_live_stack_configuration() -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["deploy"]["steps"]
    step_by_name = {step["name"]: step for step in steps}

    setup_terraform = step_by_name["Set up Terraform"]
    assert setup_terraform["with"]["terraform_version"] == "${{ env.TERRAFORM_VERSION }}"

    resolve_index = next(
        index
        for index, step in enumerate(steps)
        if step["name"] == "Resolve frontend configuration"
    )
    build_index = next(
        index
        for index, step in enumerate(steps)
        if step["name"] == "Build configured frontend"
    )
    assert resolve_index < build_index

    build_environment = step_by_name["Build configured frontend"]["env"]
    assert set(build_environment) == {
        "VITE_API_ENDPOINT",
        "VITE_AWS_REGION",
        "VITE_COGNITO_USER_POOL_ID",
        "VITE_COGNITO_CLIENT_ID",
        "VITE_COGNITO_HOSTED_UI_URL",
    }
