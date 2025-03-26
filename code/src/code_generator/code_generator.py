import json
import os
from openai import OpenAI
from typing import Dict, List

class LLMTestCodeGenerator:
    def __init__(self):
        self.client = OpenAI()

    def generate_test_code(self, test_cases: List[Dict]) -> Dict[str, str]:
        """Generate test code and required files using LLM"""
        try:
            prompt = f"""
Generate a complete pytest test suite for these test cases that can run in a Docker container.
Test Cases: {json.dumps(test_cases, indent=2)}

Return ONLY a JSON object with the following structure, no other text or explanation:
{{
    "test_generated.py": "<content>",
    "conftest.py": "<content>",
    "pytest.ini": "<content>",
    "requirements.txt": "<content>",
    "Dockerfile": "<content>"
}}
"""
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Python test automation expert. Return only JSON without any explanation or markdown."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            content = response.choices[0].message.content.strip()
            
            # Debug output
            print("\nRaw response from LLM:")
            print(content)
            
            try:
                # Try direct JSON parsing first
                return json.loads(content)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from markdown
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                # Debug output
                print("\nCleaned content:")
                print(content)
                
                return json.loads(content)

        except Exception as e:
            print(f"⚠️ Error generating test code: {str(e)}")
            print(f"Response content: {response.choices[0].message.content}")
            raise

    def save_test_files(self, generated_content: Dict[str, str], output_dir: str) -> None:
        """Save generated files to the output directory"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            for file_name, content in generated_content.items():
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"✅ Saved {file_name}")
                    
        except Exception as e:
            print(f"⚠️ Error saving files: {str(e)}")
            raise