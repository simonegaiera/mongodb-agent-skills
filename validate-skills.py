from pathlib import Path
from skills_ref import validate, read_properties, to_prompt

# All skill directories in this repository
SKILL_DIRS = [
    Path("mongodb-schema-design"),
    Path("mongodb-query-and-index-optimize"),
    Path("mongodb-transactions-consistency"),
    Path("mongodb-ai"),
]

# Validate all skill directories
all_valid = True
for skill_dir in SKILL_DIRS:
    problems = validate(skill_dir)
    if problems:
        all_valid = False
        print(f"[FAIL] {skill_dir.name}: {problems}")
    else:
        props = read_properties(skill_dir)
        print(f"[OK]   {props.name} v{props.metadata.get('version', 'N/A')} - {props.description[:80]}...")

if all_valid:
    print("\nAll skills passed validation.\n")
else:
    print("\nSome skills have validation errors.\n")

# Generate prompt for all skills
print("=" * 60)
print("Generated Agent Prompt")
print("=" * 60)
prompt = to_prompt(SKILL_DIRS)
print(prompt)