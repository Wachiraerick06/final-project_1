import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.ai_reviewer import review_code_ai
from services.static_analysis import run_static_analysis

app = FastAPI(title="AI Code Reviewer API")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins, or replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class CodeInput(BaseModel):
    code: str

# Response model
class ReviewOutput(BaseModel):
    quality_score: int
    bugs: list
    security_issues: list
    suggestions: list
    docstring: str

@app.post("/review", response_model=ReviewOutput)
async def review_code(code_input: CodeInput):
    code = code_input.code

    if not code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    # --- Run static analysis first ---
    static_results = run_static_analysis(code)
    
    # --- Run AI review via GPT-4 ---
    ai_results = review_code_ai(code)

    # --- Combine static analysis bugs with AI bugs ---
    combined_bugs = static_results.get("bugs", []) + ai_results.get("bugs", [])
    
    # --- Build final output ---
    final_output = ReviewOutput(
        quality_score=ai_results.get("quality_score", 0),
        bugs=combined_bugs,
        security_issues=ai_results.get("security_issues", []),
        suggestions=ai_results.get("suggestions", []),
        docstring=ai_results.get("docstring", "")
    )

    return final_output
