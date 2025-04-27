# validator.py
import os
from google import genai
from typing import Dict, Any, List, Union

class DSAProblemValidator:
    def __init__(self, api_key: str = None):
        """Initialize the validator with a Gemini API key."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"  # Using the flash model for quick evaluation
    
    def validate_problem(self, problem_statement: str) -> Dict[str, Any]:
        """
        Validate if a DSA problem is well-formed and solvable.
        
        Args:
            problem_statement: The full problem statement to validate
            
        Returns:
            Dictionary containing validation results
        """
        prompt = f"""
        Analyze the following Data Structures and Algorithms problem and determine if it's valid.
        A valid problem must:
        1. Have clear, unambiguous requirements
        2. Be free of logical contradictions or circular dependencies
        3. Have at least one valid solution
        4. Provide sufficient information to solve
        
        Problem Statement:
        {problem_statement}
        
        Please analyze the problem carefully and return a JSON with the following structure:
        {{
            "is_valid": true/false,
            "reason": "detailed explanation of validity or issues",
            "suggested_fixes": ["fix1", "fix2"] (only if invalid)
        }}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt],
            generation_config={
                "temperature": 0.1,  # Low temperature for more deterministic responses
                "max_output_tokens": 1024,
                "response_mime_type": "application/json"
            }
        )
        
        try:
            # Parse the JSON response
            validation_result = response.json()
            return validation_result
        except Exception as e:
            # Handle non-JSON responses
            return {
                "is_valid": False,
                "reason": f"Error processing response: {str(e)}",
                "raw_response": response.text
            }

class SolutionValidator:
    def __init__(self, api_key: str = None):
        """Initialize the solution validator with a Gemini API key."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"  # Using the flash model for quick evaluation
    
    def check_solution(self, problem_statement: str, solution_code: str, 
                      language: str = "python") -> Dict[str, Any]:
        """
        Check if a provided solution correctly solves the DSA problem.
        
        Args:
            problem_statement: The DSA problem statement
            solution_code: The code that attempts to solve the problem
            language: The programming language of the solution
            
        Returns:
            Dictionary containing solution evaluation results
        """
        prompt = f"""
        Evaluate if the following solution correctly solves the given DSA problem.
        
        Problem Statement:
        {problem_statement}
        
        Proposed Solution ({language}):
        ```{language}
        {solution_code}
        ```
        
        Please analyze the solution for:
        1. Correctness: Does it solve the problem as specified?
        2. Efficiency: What's the time and space complexity?
        3. Edge Cases: Does it handle all possible inputs?
        4. Code Quality: Is the implementation clean and maintainable?
        
        Return a JSON with the following structure:
        {{
            "is_correct": true/false,
            "correctness_explanation": "detailed analysis of correctness",
            "time_complexity": "e.g., O(n log n)",
            "space_complexity": "e.g., O(n)",
            "edge_cases_handled": true/false,
            "edge_cases_explanation": "analysis of edge case handling",
            "code_quality_score": 1-10,
            "improvement_suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt],
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 1500,
                "response_mime_type": "application/json"
            }
        )
        
        try:
            # Parse the JSON response
            evaluation_result = response.json()
            return evaluation_result
        except Exception as e:
            # Handle non-JSON responses
            return {
                "is_correct": False,
                "correctness_explanation": f"Error processing response: {str(e)}",
                "raw_response": response.text
            }
    
    def generate_test_cases(self, problem_statement: str, 
                           num_test_cases: int = 5) -> List[Dict[str, Any]]:
        """
        Generate test cases for a DSA problem.
        
        Args:
            problem_statement: The DSA problem statement
            num_test_cases: Number of test cases to generate
            
        Returns:
            List of test cases with inputs and expected outputs
        """
        prompt = f"""
        Generate {num_test_cases} diverse test cases for the following DSA problem:
        
        {problem_statement}
        
        Include normal cases, edge cases, and corner cases. For each test case, provide:
        1. Input values
        2. Expected output
        3. Brief explanation of what the test case is checking
        
        Return the test cases as a JSON array with the following structure:
        [
            {{
                "input": "description of input (in a format appropriate for the problem)",
                "expected_output": "expected output value",
                "explanation": "what this test case is checking"
            }},
            ...more test cases...
        ]
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt],
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2000,
                "response_mime_type": "application/json"
            }
        )
        
        try:
            # Parse the JSON response
            test_cases = response.json()
            return test_cases
        except Exception as e:
            # Handle non-JSON responses
            return [{
                "error": f"Failed to generate test cases: {str(e)}",
                "raw_response": response.text
            }]