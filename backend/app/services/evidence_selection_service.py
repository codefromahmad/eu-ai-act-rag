from app.models.evidence import ProfileEvidence


class EvidenceSelectionService:

    REQUIREMENT_KEYWORDS = {
        "REQ-009": [
            "risk",
            "risk_controls",
            "monitoring",
            "mitigation",
        ],

        "REQ-010": [
            "data governance",
            "training data",
            "validation data",
            "testing data",
            "dataset",
            "bias",
        ],

        "REQ-011": [
            "technical documentation",
            "documentation",
            "system documentation",
        ],

        "REQ-012": [
            "logging",
            "logs",
            "record keeping",
            "record-keeping",
        ],

        "REQ-013": [
            "transparency",
            "instructions",
            "information",
            "explainability",
        ],

        "REQ-014": [
            "human oversight",
            "human_oversight",
            "human review",
            "manual review",
            "override",
        ],

        "REQ-015": [
            "accuracy",
            "robustness",
            "cybersecurity",
            "security",
            "performance",
        ],
    }

    def select_for_requirement(
        self,
        requirement_id: str,
        evidence: list[ProfileEvidence],
    ) -> list[ProfileEvidence]:

        keywords = self.REQUIREMENT_KEYWORDS.get(
            requirement_id,
            [],
        )

        selected: list[ProfileEvidence] = []

        for item in evidence:

            searchable_text = " ".join(
                [
                    item.field or "",
                    item.value or "",
                    item.quote or "",
                ]
            ).lower()

            if any(
                keyword.lower() in searchable_text
                for keyword in keywords
            ):
                selected.append(item)

        return selected