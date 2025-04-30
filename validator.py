from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

GEMINI_API_KEY= os.environ.get("GEMINI_API_KEY")

def validate_Ques(ques: str ):
    prompt = f"""
        Analyze the following Data Structures and Algorithms problem and determine if it's valid.
        A valid problem must:
        1. Have clear, unambiguous requirements
        2. Be free of logical contradictions or circular dependencies
        3. Have at least one valid solution
        4. Provide sufficient information to solve
        
        Problem Statement:
        {ques}
        
        Please analyze the problem carefully and return only a JSON with the following structure and strictly nothing else:
        {{
            "is_valid": true/false,
            "reason": "detailed explanation of validity or issues",
            "suggested_fixes": ["fix1", "fix2"] (only if invalid)
        }}
        """

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
    )
    cleaned = response.text.replace("```json\n", "").replace("\n```", "")
    return json.loads(cleaned)
    



# result1 = validate_Ques("Given an array of integers, find the maximum sum of a contiguous subarray.")
# print("Question Validation Result:")
# print(json.dumps(result1, indent=2))


def validate_Solution(ques: str, solution_code : str ):
    prompt = f"""
        Evaluate if the following solution correctly solves the given DSA problem.
        
        Problem Statement:
        {ques}
        
        Proposed Solution:
        ```{solution_code}
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

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
    )
    print(response.text)
    cleaned = response.text.replace("```json\n", "").replace("\n```", "")
    return json.loads(cleaned)


# result2 = validate_Solution(
#     "Given an array of integers, find the maximum sum of a contiguous subarray.",
#     """def max_subarray(nums):
#     if not nums:
#         return 0
#     max_sum = current_sum = nums[0]
#     for num in nums[1:]:
#         current_sum = max(num, current_sum + num)
#         max_sum = max(max_sum, current_sum)
#     return max_sum"""
# )
# print("\nSolution Validation Result:")
# print(json.dumps(result2, indent=2))