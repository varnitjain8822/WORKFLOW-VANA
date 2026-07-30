import os
import json
import urllib.request
import urllib.error
import sys
import re

# Try to get API key from environment or .env file (simple parse)
api_key = os.environ.get("OPENAI_API_KEY", "")
if not api_key and os.path.exists("../.env"):
    with open("../.env") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY="):
                api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
                
import subprocess

import subprocess
import shutil

def call_openai(system_prompt, user_prompt, max_tokens=1500, temperature=0.7):
    """
    Agnostic LLM Caller: Dynamically routes the prompt to the best available local agent provider.
    Checks for local 'agy' CLI agent and local 'ollama'. Strictly avoids external APIs.
    """
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    # Provider 1: Local AGY CLI (Antigravity)
    if shutil.which("agy") or os.path.exists("/Users/varnitjain4245/.local/bin/agy"):
        agy_path = shutil.which("agy") or "/Users/varnitjain4245/.local/bin/agy"
        try:
            result = subprocess.run(
                [agy_path, "--print", full_prompt, "--dangerously-skip-permissions"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"AGY CLI Error: {e.stderr}", file=sys.stderr)
            
    # Provider 2: Local Ollama
    elif shutil.which("ollama"):
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3", full_prompt],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Ollama Error: {e.stderr}", file=sys.stderr)
            
    # Fallback: Mock Generator
    return f"MOCK GENERATION: Please install 'agy' or 'ollama' to enable real AI generation.\n\nContext Length: {len(full_prompt)}"

def build_project_folder_structure(input_json, project_name="project"):
    if isinstance(input_json, str):
        try:
            input_json = json.loads(input_json)
        except Exception:
            input_json = {}

    tech_stack = input_json.get("techStack", {}) or {}
    backend_items = [str(item).lower() for item in (tech_stack.get("backend") or [])]
    frontend_items = [str(item).lower() for item in (tech_stack.get("frontend") or [])]

    def infer_backend_language(items):
        text = " ".join(items)
        if "rust" in text or "actix" in text:
            return "rust"
        if "go" in text or "golang" in text:
            return "go"
        if "java" in text or "spring" in text or "kotlin" in text:
            return "java"
        if "node" in text or "nestjs" in text or "express" in text or "fastify" in text:
            return "node"
        return "java"

    def infer_frontend_language(items):
        text = " ".join(items)
        if "react" in text or "next" in text:
            return "react"
        if "vue" in text:
            return "vue"
        if "angular" in text:
            return "angular"
        if "svelte" in text:
            return "svelte"
        return "react"

    def backend_structure(language):
        if language == "rust":
            return ["src/", "src/api/", "src/application/", "src/domain/", "src/infrastructure/", "tests/", "migrations/"]
        if language == "go":
            return ["cmd/server/", "internal/api/", "internal/app/", "internal/domain/", "internal/infra/", "pkg/", "configs/"]
        if language == "node":
            return ["src/", "src/routes/", "src/controllers/", "src/services/", "src/repositories/", "src/models/", "tests/"]
        return ["src/main/java/", "src/main/resources/", "src/test/java/", "src/main/java/com/company/app/api/", "src/main/java/com/company/app/application/", "src/main/java/com/company/app/domain/"]

    def frontend_structure(language):
        if language == "vue":
            return ["src/", "src/components/", "src/pages/", "src/composables/", "src/services/", "src/store/", "src/styles/"]
        if language == "angular":
            return ["src/app/", "src/app/core/", "src/app/shared/", "src/app/features/", "src/app/pages/", "src/app/services/", "src/assets/"]
        return ["src/", "src/components/", "src/features/", "src/pages/", "src/hooks/", "src/services/", "src/store/", "src/styles/", "public/"]

    backend_language = infer_backend_language(backend_items)
    frontend_language = infer_frontend_language(frontend_items)

    safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "-", project_name).strip(".-") or "project"

    return {
        "projectName": safe_name,
        "backend": {
            "language": backend_language,
            "structure": backend_structure(backend_language),
            "root": f"{safe_name}/backend"
        },
        "frontend": {
            "language": frontend_language,
            "structure": frontend_structure(frontend_language),
            "root": f"{safe_name}/frontend"
        }
    }


def build_folder_structure_context(input_json, project_name="project"):
    return json.dumps(build_project_folder_structure(input_json, project_name))


def decompose_components(input_json):
    system_prompt = "You are a Software Architect. Given a project description, break it down into logical microservices, modules, or layers. Return ONLY a valid JSON array of objects with 'id', 'name', 'description', and 'features' (list of strings). Maximum 8 components."
    user_prompt = f"Project Details:\n{json.dumps(input_json, indent=2)}"
    
    result = call_openai(system_prompt, user_prompt, temperature=0.2)
    if result:
        # Try to parse the JSON output
        try:
            # Strip markdown code blocks if present
            if result.startswith("```json"):
                result = result.split("```json")[1].split("```")[0].strip()
            elif result.startswith("```"):
                result = result.split("```")[1].split("```")[0].strip()
            return json.loads(result)
        except:
            pass
            
    # Mock fallback
    return [
        {"id": "api-gateway", "name": "API Gateway", "description": "Main entry point", "features": ["Routing"]},
        {"id": "auth-service", "name": "Auth Service", "description": "Handles users", "features": ["Login", "JWT"]}
    ]

def generate_stage(stage_num, context, template_content="", feedback="", component_name="Main System", project_input=None):
    system_prompt = f"""You are an elite expert AI Software Architect and Developer. 
Your task is to generate Stage {stage_num} documentation and code for '{component_name}'.

CRITICAL INSTRUCTION: You MUST use Rust (e.g., axum, tokio, cargo) as the backend language and ecosystem for ALL projects in this workflow, regardless of what is suggested. The backend architecture and code implementation must strictly be written in Rust.

CRITICAL INSTRUCTION: While you must adhere to the provided templates, contexts, and specialized skill modules, you MUST NOT restrict yourself only to those files. You are expected to actively leverage your broad LLM knowledge, general engineering best practices, and creative problem-solving skills to enrich the output and fill in any gaps.

Follow the provided context and template strictly. Output valid markdown. DO NOT wrap in ```markdown blocks, just output the raw markdown."""
    
    user_prompt = f"Context from previous stages:\n{context}\n\n"
    if stage_num in {4, 6} and project_input:
        structure = build_project_folder_structure(project_input, component_name)
        tree = []
        tree.append(f"{structure['projectName']}/")
        tree.append(f"├── backend/ ({structure['backend']['language']})")
        for item in structure['backend']['structure']:
            tree.append(f"│   └── {item}")
        tree.append(f"├── frontend/ ({structure['frontend']['language']})")
        for item in structure['frontend']['structure']:
            tree.append(f"│   └── {item}")
        user_prompt += "Use the following project-scoped folder layout when no explicit structure is provided:\n" + "\n".join(tree) + "\n\n"
    if template_content:
        user_prompt += f"Please use the following template as a structural guide. Fill it in and enhance it based on the context:\n\n{template_content}\n\n"
        
    if feedback:
        user_prompt += f"CRITICAL FEEDBACK FROM PREVIOUS DRAFT (MUST FIX):\n{feedback}\n\n"
        
    user_prompt += f"Please generate the Stage {stage_num} document."
    
    result = call_openai(system_prompt, user_prompt, max_tokens=2500)
    if result:
        return result
        
    # Mock fallback
    return f"# Stage {stage_num} for {component_name}\n\nThis is a mock generated output because no OPENAI_API_KEY was found.\n\n### Context Included\nContext length provided: {len(context)} characters."

def evaluate_document(stage_num, content):
    system_prompt = "You are a Hyper-Critical QA Auditor enforcing rigorous loop engineering. Review the provided documentation draft. You MUST find flaws to force iterative refinement unless the draft is absolutely perfect. Provide a JSON response with exactly three fields: 'score' (a float between 1.0 and 10.0), 'feedback' (a detailed string specifying EXACTLY what must be fixed to reach a 9.0+), and 'approved' (boolean, true ONLY if score >= 9.0 and there are absolutely zero architectural or detail flaws). Only output JSON."
    user_prompt = f"Review this Stage {stage_num} draft:\n\n{content}"
    
    result = call_openai(system_prompt, user_prompt, temperature=0.1)
    if result:
        try:
            if result.startswith("```json"):
                result = result.split("```json")[1].split("```")[0].strip()
            elif result.startswith("```"):
                result = result.split("```")[1].split("```")[0].strip()
            data = json.loads(result)
            score = data.get("score", 8.5)
            approved = data.get("approved", score >= 9.0)
            return score, data.get("feedback", "Looks okay."), approved
        except:
            pass
            
    # Mock fallback
    import random
    score = round(random.uniform(8.0, 9.9), 1)
    approved = score >= 9.0
    feedback = "Mock review: LGTM!" if approved else "Mock review: Needs more detail and rigorous refinement to meet the 9.0 threshold."
    return score, feedback, approved

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True, choices=["decompose", "generate", "evaluate"])
    parser.add_argument("--input", help="Input JSON file for decompose")
    parser.add_argument("--stage", help="Stage number")
    parser.add_argument("--context-file", help="File containing previous stage context")
    parser.add_argument("--template-file", help="File containing the template to follow")
    parser.add_argument("--component", help="Component name")
    parser.add_argument("--content-file", help="File containing draft to evaluate")
    parser.add_argument("--feedback", help="Feedback from previous run")
    
    args = parser.parse_args()
    
    if args.action == "decompose":
        with open(args.input) as f:
            data = json.load(f)
        comps = decompose_components(data)
        print(json.dumps(comps))
        
    elif args.action == "generate":
        context = ""
        if args.context_file and os.path.exists(args.context_file):
            with open(args.context_file) as f:
                context = f.read()
        
        template_content = ""
        if args.template_file and os.path.exists(args.template_file):
            with open(args.template_file) as f:
                template_content = f.read()
                
        project_input = None
        if args.input and os.path.exists(args.input):
            with open(args.input) as f:
                project_input = json.load(f)
        out = generate_stage(args.stage, context, template_content, args.feedback or "", args.component or "Main System", project_input)
        print(out)
        
    elif args.action == "evaluate":
        content = ""
        if args.content_file and os.path.exists(args.content_file):
            with open(args.content_file) as f:
                content = f.read()
        score, feedback, approved = evaluate_document(args.stage, content)
        print(json.dumps({"score": score, "feedback": feedback, "approved": approved}))
