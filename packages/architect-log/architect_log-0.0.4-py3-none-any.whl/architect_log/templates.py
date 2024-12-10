ADR_TEMPLATE = """# ADR {number}: {title}

## Status
Status: **{status}**

## Context
Describe the issue, challenges, and objectives. Include any relevant project, technical, or business considerations.

## Considered Options
* **Option 1**: Brief description of the option.
  - **Pros**: 
    - Benefit 1
  - **Cons**: 
    - Drawback 1
* **Option 2**: Brief description of the option.
  - **Pros**: 
    - Benefit 1
  - **Cons**: 
    - Drawback 1

## Decision
We have decided to [describe the chosen solution]. This decision was made because [reasoning behind the decision].

## Consequences
### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2
"""

ADR_TEMPLATE_MINIMAL = """# ADR {number}: {title}

## Status
Status: **{status}**

## Context
Describe the issue, challenges, and objectives. Include any relevant project, technical, or business considerations.

## Decision
We have decided to [describe the chosen solution]. This decision was made because [reasoning behind the decision].

## Consequences
- Consequence 1
- Consequence 2
"""
