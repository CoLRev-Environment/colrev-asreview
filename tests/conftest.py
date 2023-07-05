#! /usr/bin/env python
"""Conftest for colrev-asreview"""
from __future__ import annotations

import os

import colrev.review_manager
import pytest


@pytest.fixture(scope="session", name="base_repo_review_manager")
def fixture_base_repo_review_manager(session_mocker, tmp_path_factory):  # type: ignore
    """Fixture returning the base review_manager"""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    session_mocker.patch(
        "colrev.env.environment_manager.EnvironmentManager.get_name_mail_from_git",
        return_value=("Tester Name", "tester@email.de"),
    )

    session_mocker.patch(
        "colrev.env.environment_manager.EnvironmentManager.register_repo",
        return_value=(),
    )

    test_repo_dir = tmp_path_factory.mktemp("base_repo")  # type: ignore

    session_mocker.patch.object(
        colrev.env.environment_manager.EnvironmentManager,
        "registry_yaml",
        test_repo_dir / "reg.yaml",
    )
    session_mocker.patch.object(
        colrev.env.environment_manager.EnvironmentManager,
        "registry",
        test_repo_dir / "reg.json",
    )
    os.chdir(test_repo_dir)
    colrev.review_manager.get_init_operation(
        review_type="literature_review",
        target_path=test_repo_dir,
        light=True,
    )
    review_manager = colrev.review_manager.ReviewManager(
        path_str=str(test_repo_dir), force_mode=True
    )

    review_manager.get_load_operation()
    git_repo = review_manager.dataset.get_repo()
    if review_manager.in_ci_environment():
        git_repo.config_writer().set_value("user", "name", "Tester").release()
        git_repo.config_writer().set_value("user", "email", "tester@mail.com").release()

    return review_manager
