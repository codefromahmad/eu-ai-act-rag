from app.models.evidence import ProfileEvidence
from app.services.evidence_selection_service import (
    EvidenceSelectionService,
)


def test_selects_human_oversight_evidence():

    evidence = [
        ProfileEvidence(
            field="human_oversight",
            value="Human review",
            page_number=4,
            quote=(
                "HR staff review recommendations "
                "before final decisions."
            ),
        ),
        ProfileEvidence(
            field="training_data",
            value="Candidate dataset",
            page_number=5,
            quote="Training data is collected from applicants.",
        ),
    ]

    service = EvidenceSelectionService()

    result = service.select_for_requirement(
        requirement_id="REQ-014",
        evidence=evidence,
    )

    assert len(result) == 1
    assert result[0].field == "human_oversight"


def test_returns_empty_list_when_no_relevant_evidence():

    evidence = [
        ProfileEvidence(
            field="human_oversight",
            value="Human review",
            page_number=4,
            quote="HR staff review recommendations.",
        ),
    ]

    service = EvidenceSelectionService()

    result = service.select_for_requirement(
        requirement_id="REQ-010",
        evidence=evidence,
    )

    assert result == []