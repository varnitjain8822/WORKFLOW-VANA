# Agentic SDLC Workflow (Native AI Agent Protocol)

This document is an executable protocol for an AI Coding Agent (like Antigravity, Claude, or GitHub Copilot Workspaces) to natively execute the 10-stage SDLC workflow without needing external bash scripts or OpenAI API keys.

## 🎯 Objective
Read the user's project requirements and autonomously decompose the project into microservices/components. Then, iterate through a 10-stage System Development Life Cycle (SDLC) for EACH component, generating production-ready documentation and code scaffolding.

---

## 🛠️ Execution Loop (AI Instructions)

When the user asks you to "Run the SDLC Workflow on [Requirements File]", you must follow these exact steps natively:

### Phase 1: Decomposition
1. Read the provided project requirements file.
2. Analyze the business problem, functional requirements, and architecture needs.
3. Decompose the system into logical, specialized components (e.g., `data-ingestion-service`, `nlp-engine`, `rest-api-gateway`, `frontend-dashboard`).
4. Output a list of these components to the user and ask for confirmation before proceeding.

### Phase 2: The 10-Stage Loop
For **each** approved component, you will create a directory in `output/components/<component-name>/` and generate the following documentation files one by one. 

*Crucial: For each stage, you must read the corresponding template in `workflow_generator_tools/stages/` (if it exists) to guide your structure. Additionally, you should refer to any relevant AI skill files in `workflow_generator_tools/skills/` (such as `web-design` for UI/UX), but DO NOT stick to them rigidly. Use them as reference guidelines, while actively leveraging your own broad LLM knowledge and creative problem-solving skills to enrich the output.*

* **Stage 0: `00-project-brief.md`** - Summary of what this specific component does.
* **Stage 1: `01-requirement-analysis.md`** - Functional/Non-functional requirements for this component.
* **Stage 2: `02-prd.md`** - Product Requirements Document (Stories, KPIs).
* **Stage 3: `03-high-level-design.md`** - Architecture, Tech Stack, Data Flow.
* **Stage 4: `04-low-level-design.md`** - API Specs, DB Schema, State Management.
* **Stage 5: `05-implementation-plan.md`** - Milestones and Sprints.
* **Stage 6: `06-code-implementation.md`** - Actual boilerplate code blocks for the component. *IMPORTANT: Ensure you prepend each code block with a clear file path so it can be extracted later.*
* **Stage 7: `07-code-review.md`** - QA gates and standards.
* **Stage 8: `08-qa-testing.md`** - Unit & Integration test strategies.
* **Stage 9: `09-ui-ux-design.md`** - (Only for frontend components) UI/UX design specs.

**INTERACTIVE APPROVAL GATEWAY:**
Do not pause during the generation of the components. You must generate all 10 stages (0 through 9) for ALL approved components first. Once every single component has been fully documented and generated in the `output/components/` folder, you MUST pause execution and ask the user for overall approval on the entire system architecture. You must present them with the following three options:
1. **Proceed to the next step** (Move on to Phase 4: Code Generation & Extraction)
2. **Move to previous step** (Cancel the current changes)
3. **Write feedback to change** (User provides feedback on specific components or documents, and you must regenerate those specific files based on their feedback)

Do not move to Phase 4 until the user selects option 1!
### Phase 3: Self-Correction (The AI Critic)
You must act as your own "Harsh QA Auditor". Before saving any of the markdown files above to the filesystem:
1. Review your drafted markdown against enterprise standards.
2. If it is too generic, lacks technical depth, or misses constraints from the original requirements, **discard it and rewrite it** with higher quality.
3. Only use the `write_to_file` tool once the document is extremely detailed and accurate.

### Phase 4: Code Generation & Extraction
Once all stages for all components are generated in the `output/components/` folder, you must generate the ACTUAL code. Output the code files directly into a clean, flat folder structure with no unnecessary subdirectories:
- `output/frontend/`: Contains all frontend UI and web code.
- `output/backend/`: Contains all backend APIs, data pipelines, ML models, and infrastructure code.
- `output/components/`: Contains ONLY the markdown documentation generated in Phase 2.

Ensure this structure is clean, strict, and ready for deployment.

---
**Agent:** Begin by acknowledging this protocol and executing Phase 1 on the user's requirements!
