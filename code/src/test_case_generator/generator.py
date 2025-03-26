# test_case_generator/generator.py
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Union

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def save_test_cases(test_cases: List[Dict]) -> str:
    """Save test cases to a JSON file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"test_cases_{timestamp}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
    
    return output_file

def chunk_requirements(understanding_json: Union[List, Dict], max_chunk_size: int = 12000) -> List[Union[List, Dict]]:
    """Split requirements into manageable chunks while preserving feature context"""
    # Handle list input
    if isinstance(understanding_json, list):
        chunks = []
        current_chunk = []
        current_size = 0
        
        for item in understanding_json:
            item_size = len(str(item))
            
            # If adding this item would exceed chunk size, start a new chunk
            if current_size + item_size > max_chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_size = 0
            
            # Add item to current chunk
            current_chunk.append(item)
            current_size += item_size
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    # Handle dictionary input
    elif isinstance(understanding_json, dict):
        chunks = []
        current_chunk = {}
        current_size = 0
        
        for feature_id, feature_data in understanding_json.items():
            feature_size = len(str(feature_data))
            
            if current_size + feature_size > max_chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = {}
                current_size = 0
            
            current_chunk[feature_id] = feature_data
            current_size += feature_size
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    else:
        raise ValueError(f"Input must be list or dict, got {type(understanding_json)}")

def generate_test_cases_llm(understanding_json: Union[List, Dict]) -> str:
    """Generate test cases with support for large inputs while maintaining quality"""
    try:
        # Split requirements into chunks if they're too large
        requirement_chunks = chunk_requirements(understanding_json, max_chunk_size=6000)
        all_test_cases = []
        
        for chunk_index, chunk in enumerate(requirement_chunks, 1):
            print(f"\n📝 Processing requirement chunk {chunk_index}/{len(requirement_chunks)}...")
            
            prompt = f"""
You must generate multiple test cases (at least 5-10 test cases) for the given requirements.
As a QA expert, analyze these requirements and generate comprehensive test cases.

Each test case must include:
1. Unique ID (format: TC_XXX where XXX is a sequential number)
2. Clear title that summarizes the test objective
3. Detailed description explaining what is being tested
4. Preconditions (if any) that must be met before test execution
5. Test data structure must be a JSON object containing:
   - input_data: All input values
   - expected_data: Expected data values
   - api_endpoints: API endpoints if applicable
   - ui_elements: UI element identifiers if applicable
6. Step-by-step test steps (clear and actionable)
7. Expected results (specific and verifiable)
8. Test type (functional/negative/boundary/performance/security/usability)
9. Priority (high/medium/low)
10. Dependencies (IDs of other test cases that must be executed first)
11. Assumptions made for this test case
12. Test environment requirements (browser/OS/device if applicable)

Requirements to analyze:
{json.dumps(chunk, indent=2)}

Generate test cases covering:
1. Positive scenarios (happy path)
2. Negative scenarios (error handling)
3. Boundary conditions
4. Data validations
5. Business rule validations
6. Integration points
7. Error messages and notifications
8. Performance considerations
9. Security aspects
10. User experience flows

Return a JSON array of test cases. Each test case must follow this structure:
{{
    "id": "TC_001",
    "title": "Test case title",
    "description": "Detailed description",
    "preconditions": ["list", "of", "preconditions"],
    "test_data": {{
        "input_data": {{ "field1": "value1", "field2": "value2" }},
        "expected_data": {{ "expected1": "value1", "expected2": "value2" }},
        "api_endpoints": {{ "endpoint": "/api/path", "method": "POST" }},
        "ui_elements": {{ "element1": "id/xpath", "element2": "id/xpath" }}
    }},
    "steps": ["Step 1", "Step 2", "..."],
    "expected_result": "Expected outcome",
    "type": "functional/negative/boundary/performance/security/usability",
    "priority": "high/medium/low",
    "dependencies": ["TC_002", "TC_003"],
    "assumptions": ["Assumption 1", "Assumption 2"],
    "test_environment": {{
        "browser": ["Chrome", "Firefox"],
        "os": ["Windows", "MacOS"],
        "device": "Desktop/Mobile/Tablet"
    }}
}}

Important:
1. Generate at least 5-10 test cases for comprehensive coverage
2. Each test case must have a unique ID
3. Steps must be clear, specific, and actionable
4. Expected results must be specific and verifiable
5. Dependencies must be correctly identified
6. Test data must be structured as JSON objects
7. Include environment requirements where applicable

Return only the JSON array without any additional text or markdown formatting.
"""
            
            start_id = len(all_test_cases) + 1
            prompt = prompt.replace("TC_001", f"TC_{start_id:03d}")
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a QA expert specializing in comprehensive test case design. You must generate multiple test cases (at least 5-10) for complete coverage. Always return pure JSON without any markdown formatting or explanation text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4096
            )

            output = response.choices[0].message.content.strip()
            
            # Remove any markdown formatting or explanation text
            if "```json" in output:
                output = output[output.find("["):output.rfind("]")+1]
            elif "```" in output:
                output = output[output.find("["):output.rfind("]")+1]
            
            try:
                chunk_test_cases = json.loads(output)
                
                # Ensure we got a list of test cases
                if isinstance(chunk_test_cases, dict) and 'test_cases' in chunk_test_cases:
                    chunk_test_cases = chunk_test_cases['test_cases']
                elif not isinstance(chunk_test_cases, list):
                    chunk_test_cases = [chunk_test_cases]
                
                # Validate and fix test cases
                for index, test_case in enumerate(chunk_test_cases):
                    # Fix ID - ensure it's unique and sequential
                    current_id = len(all_test_cases) + index + 1
                    test_case['id'] = f"TC_{current_id:03d}"
                    
                    # Ensure basic preconditions exist
                    if not test_case.get('preconditions'):
                        test_case['preconditions'] = ["Application is launched and in ready state"]
                    
                    # Validate dependencies - ensure they reference valid test cases
                    if 'dependencies' in test_case:
                        valid_deps = []
                        for dep in test_case['dependencies']:
                            # Only include dependencies for test cases that would exist
                            dep_num = int(dep.split('_')[1])
                            if dep_num < current_id:
                                valid_deps.append(dep)
                        test_case['dependencies'] = valid_deps
                    
                    # Validate required fields
                    required_fields = ['id', 'title', 'description', 'steps', 'expected_result', 'type', 'priority']
                    missing_fields = [field for field in required_fields if field not in test_case]
                    if missing_fields:
                        print(f"⚠️ Warning: Test case {test_case['id']} missing required fields: {missing_fields}")
                
                # Add validation for the new structure
                def validate_test_case(test_case: Dict) -> List[str]:
                    issues = []
                    if not isinstance(test_case.get('test_data'), dict):
                        issues.append("test_data must be a JSON object")
                    if 'input_data' not in test_case.get('test_data', {}):
                        issues.append("test_data must contain input_data")
                    if 'expected_data' not in test_case.get('test_data', {}):
                        issues.append("test_data must contain expected_data")
                    if not test_case.get('test_environment'):
                        issues.append("test_environment is required")
                    return issues

                # Update the test case processing
                for test_case in chunk_test_cases:
                    issues = validate_test_case(test_case)
                    if issues:
                        print(f"⚠️ Warning: Test case {test_case['id']} has issues: {', '.join(issues)}")
                
                all_test_cases.extend(chunk_test_cases)
                print(f"✅ Generated {len(chunk_test_cases)} test cases from chunk {chunk_index}")
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Error: Unable to parse LLM output as JSON: {str(e)}")
                print(f"Raw output: {output}")
                return [{"error": "Invalid JSON format", "raw_response": output}]
        
        # Save all test cases to file
        output_file = save_test_cases(all_test_cases)
        print(f"\n✅ Total test cases generated: {len(all_test_cases)}")
        print(f"✅ Test cases have been saved to: {output_file}\n")
        
        return output_file

    except Exception as e:
        print(f"⚠️ Error generating test cases: {str(e)}")
        return [{"error": str(e)}]
