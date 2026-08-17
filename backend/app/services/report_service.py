import json

from app.models.analysis_result import (
    FullComplianceAnalysis,
)
from app.models.report import (
    ComplianceReport,
    ReportSummary,
)
from app.models.system_profile import SystemProfile
from app.services.llm_service import LLMService


class ReportService:

    def __init__(self):
        self.llm = LLMService()

    def generate_report(
        self,
        profile: SystemProfile,
        analysis: FullComplianceAnalysis,
    ) -> ComplianceReport:

        system_prompt = """
You are generating a preliminary EU AI Act compliance report.

Use only the supplied system profile and compliance analysis summary.

Important rules:

1. Do not invent facts.
2. Do not change compliance statuses.
3. Do not change the deterministic compliance score.
4. Treat missing information separately from non-compliance.
5. Keep the executive summary concise.
6. Strengths must come from positive or partial evidence.
7. Weaknesses must come from partial or non-compliant findings.
8. Missing information must come from unknown findings.
9. Recommendations must be based only on the supplied assessments.
10. Do not invent legal references.
11. Return only valid JSON.
"""

        # Do NOT send full EU AI Act legal text again.
        # The report generator only needs summarized assessment results.
        assessment_summaries = []

        for assessment in analysis.assessments:

            assessment_summaries.append(
                {
                    "requirement_id": assessment.requirement_id,
                    "status": assessment.status.value,
                    "explanation": assessment.explanation,
                    "user_evidence": assessment.user_evidence,
                    "recommendations": assessment.recommendations,
                    "legal_references": [
                        reference.article
                        for reference in assessment.legal_references
                    ],
                }
            )

        payload = {
            "system_profile": profile.model_dump(),

            "risk_classification": (
                analysis.risk_classification.model_dump()
            ),

            "score": analysis.score.model_dump(),

            "assessments": assessment_summaries,
        }

        schema = ReportSummary.model_json_schema()

        user_prompt = f"""
Generate the summary section of a preliminary
EU AI Act compliance report.

INPUT:

{json.dumps(payload, indent=2)}

Return JSON matching this schema:

{json.dumps(schema, indent=2)}
"""

        raw_response = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        summary_data = json.loads(
            raw_response
        )

        summary = ReportSummary.model_validate(
            summary_data
        )

        # The final report still contains the complete original
        # assessments, including verified legal evidence.
        return ComplianceReport(
            risk_classification=analysis.risk_classification,
            score=analysis.score,
            summary=summary,
            assessments=analysis.assessments,
        )