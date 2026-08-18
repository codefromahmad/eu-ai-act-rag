from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.exceptions.llm_exceptions import (
    LLMQuotaExceededError,
)
from app.main import app


client = TestClient(app)


def test_oversized_document_returns_413():

    # Current limit:
    # 10 MB
    oversized_content = (
        b"a"
        * (
            10
            * 1024
            * 1024
            + 1
        )
    )

    response = client.post(
        "/api/documents/extract",
        files={
            "file": (
                "large.txt",
                BytesIO(
                    oversized_content
                ),
                "text/plain",
            )
        },
    )

    assert response.status_code == 413

    assert response.json() == {
        "detail": (
            "The uploaded file is too large. "
            "Maximum allowed size is 10 MB."
        )
    }


def test_llm_quota_exhaustion_returns_503():

    with patch(
        "app.api.routes.documents."
        "CompliancePipelineService"
    ) as pipeline_class:

        pipeline = (
            pipeline_class.return_value
        )

        pipeline.analyze_document.side_effect = (
            LLMQuotaExceededError(
                "Quota exhausted."
            )
        )

        response = client.post(
            "/api/documents/report",
            files={
                "file": (
                    "system.txt",
                    BytesIO(
                        b"AI recruitment system"
                    ),
                    "text/plain",
                )
            },
        )

    assert response.status_code == 503

    assert response.json() == {
        "detail": (
            "The AI service has temporarily "
            "exhausted its usage quota. "
            "Please try again later."
        )
    }