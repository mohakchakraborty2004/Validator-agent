# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os

from validator import DSAProblemValidator, SolutionValidator

app = FastAPI(title="DSA Problem and Solution Validator API", 
              description="An API that validates DSA problems and solutions using Gemini API")

# Configure API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY environment variable is not set")

# Dependency to get validators
def get_problem_validator():
    return DSAProblemValidator(api_key=GEMINI_API_KEY)

def get_solution_validator():
    return SolutionValidator(api_key=GEMINI_API_KEY)

# Request/Response models
class ProblemValidationRequest(BaseModel):
    problem_statement: str

class SolutionValidationRequest(BaseModel):
    problem_statement: str
    solution_code: str
    language: str = "python"

class TestCasesRequest(BaseModel):
    problem_statement: str
    num_test_cases: int = 5

class ValidationResponse(BaseModel):
    is_valid: bool
    reason: str
    suggested_fixes: Optional[List[str]] = None

class SolutionResponse(BaseModel):
    is_correct: bool
    correctness_explanation: str
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    edge_cases_handled: Optional[bool] = None
    edge_cases_explanation: Optional[str] = None
    code_quality_score: Optional[int] = None
    improvement_suggestions: Optional[List[str]] = None

class TestCaseItem(BaseModel):
    input: str
    expected_output: str
    explanation: str

# API endpoints
@app.post("/validate-problem", response_model=ValidationResponse)
async def validate_problem(
    request: ProblemValidationRequest,
    validator: DSAProblemValidator = Depends(get_problem_validator)
):
    """Validate if a DSA problem statement is well-formed and solvable."""
    try:
        result = validator.validate_problem(request.problem_statement)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@app.post("/validate-solution", response_model=SolutionResponse)
async def validate_solution(
    request: SolutionValidationRequest,
    validator: SolutionValidator = Depends(get_solution_validator)
):
    """Validate if a solution correctly solves the given DSA problem."""
    try:
        result = validator.check_solution(
            request.problem_statement,
            request.solution_code,
            request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solution validation error: {str(e)}")

@app.post("/generate-test-cases", response_model=List[TestCaseItem])
async def generate_test_cases(
    request: TestCasesRequest,
    validator: SolutionValidator = Depends(get_solution_validator)
):
    """Generate test cases for a DSA problem."""
    try:
        result = validator.generate_test_cases(
            request.problem_statement,
            request.num_test_cases
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test case generation error: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy", "gemini_api_configured": bool(GEMINI_API_KEY)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)