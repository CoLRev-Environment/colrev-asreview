#! /usr/bin/env python
"""Tests for colrev-asreview"""

import colrev.review_manager

import colrev_asreview.colrev_asreview


def test_asreview(
    base_repo_review_manager: colrev.review_manager.ReviewManager,
) -> None:
    """Test colrev-asreview"""
    prescreen_operation = base_repo_review_manager.get_prescreen_operation()

    settings = {"endpoint": "colrev_asreview.colrev_asreview"}
    asreview = colrev_asreview.colrev_asreview.ASReviewPrescreen(
        prescreen_operation=prescreen_operation, settings=settings
    )
    assert asreview.settings.endpoint == "colrev_asreview.colrev_asreview"
