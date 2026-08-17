from app.models.compliance import (
    ComplianceAssessment,
    ComplianceStatus,
)


class ScoringService:

    STATUS_SCORES = {
        ComplianceStatus.compliant: 1.0,
        ComplianceStatus.partial: 0.5,
        ComplianceStatus.non_compliant: 0.0,
    }

    def calculate_score(
        self,
        assessments: list[ComplianceAssessment],
    ) -> dict:

        total_requirements = len(assessments)

        compliant_count = 0
        partial_count = 0
        non_compliant_count = 0
        unknown_count = 0

        known_scores: list[float] = []

        for assessment in assessments:

            if assessment.status == ComplianceStatus.unknown:
                unknown_count += 1
                continue

            if assessment.status == ComplianceStatus.compliant:
                compliant_count += 1

            elif assessment.status == ComplianceStatus.partial:
                partial_count += 1

            elif assessment.status == ComplianceStatus.non_compliant:
                non_compliant_count += 1

            score = self.STATUS_SCORES[
                assessment.status
            ]

            known_scores.append(score)

        known_requirements = len(known_scores)

        if known_requirements > 0:
            compliance_score = (
                sum(known_scores)
                / known_requirements
            ) * 100
        else:
            compliance_score = None

        if total_requirements > 0:
            coverage = (
                known_requirements
                / total_requirements
            ) * 100
        else:
            coverage = 0.0

        return {
            "compliance_score": (
                round(compliance_score, 2)
                if compliance_score is not None
                else None
            ),
            "coverage": round(coverage, 2),
            "total_requirements": total_requirements,
            "known_requirements": known_requirements,
            "compliant": compliant_count,
            "partial": partial_count,
            "non_compliant": non_compliant_count,
            "unknown": unknown_count,
        }