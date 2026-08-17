from app.services.llm_service import LLMService


llm = LLMService()

response = llm.generate_json(
    system_prompt="Return only valid JSON.",
    user_prompt="""
Return the following information as JSON:

name: EU AI Act Analyzer
type: RAG system
purpose: EU AI Act compliance analysis
""",
)

print(response)