from app.services.requirement_registry import REQUIREMENTS


print("Total requirements:", len(REQUIREMENTS))

for requirement in REQUIREMENTS:
    print(
        requirement.requirement_id,
        "-",
        requirement.title,
    )