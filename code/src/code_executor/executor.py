from typing import Dict
import json
from openai import OpenAI
import docker
import os
import subprocess

class LLMTestExecutor:
    def __init__(self):
        self.client = OpenAI()
        self.docker_client = docker.from_env()

    def run_tests(self, test_dir: str) -> Dict:
        """Run pytest files in Docker container"""
        try:
            # Step 1: Generate Docker configuration
            docker_config = self._generate_docker_config(test_dir)
            print("✅ Generated Docker configuration")

            # Step 2: Create Docker environment
            self._setup_docker_environment(test_dir, docker_config)
            print("✅ Set up Docker environment")

            # Step 3: Run tests in Docker
            result = self._run_tests_in_docker(test_dir)
            print("✅ Completed test execution")

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _generate_docker_config(self, test_dir: str) -> Dict:
        """Generate Docker configuration for running pytest"""
        # Read the test file to analyze requirements
        with open(os.path.join(test_dir, "test_generated.py"), 'r') as f:
            test_code = f.read()

        prompt = f"""
Analyze this Python test code and generate Docker configuration for running pytest.
The configuration should include:
1. Appropriate Python base image
2. Required system dependencies
3. Python package requirements
4. Volume mappings for test files and reports
5. Environment variables if needed

Test code:
{test_code}

Return a JSON object with:
1. dockerfile: Content of Dockerfile
2. requirements: Python package requirements
3. docker_command: Docker run command with all necessary options

Example Response:
{{
    "dockerfile": "FROM python:3.9-slim\\nWORKDIR /tests\\nCOPY requirements.txt .\\nRUN pip install -r requirements.txt",
    "requirements": "pytest>=7.0.0\\npytest-html>=4.1.0\\nrequests>=2.31.0",
    "docker_command": "docker run -v $(pwd):/tests -w /tests python-tests pytest -v --html=report.html"
}}
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a DevOps expert specializing in Python testing environments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={ "type": "json_object" }
        )

        return json.loads(response.choices[0].message.content)

    def _setup_docker_environment(self, test_dir: str, docker_config: Dict) -> None:
        """Set up Docker environment for running tests"""
        # Create requirements.txt
        with open(os.path.join(test_dir, "requirements.txt"), 'w') as f:
            f.write(docker_config['requirements'])

        # Create Dockerfile
        with open(os.path.join(test_dir, "Dockerfile"), 'w') as f:
            f.write(docker_config['dockerfile'])

        # Build Docker image
        try:
            subprocess.run(
                ['docker', 'build', '-t', 'python-tests', '.'],
                check=True,
                cwd=test_dir,
                capture_output=True,
                text=True
            )
            print("✅ Built Docker image")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Docker build failed: {e.stderr}")
            raise

    def _run_tests_in_docker(self, test_dir: str) -> Dict:
        """Run tests in Docker container"""
        try:
            # Run tests in Docker
            result = subprocess.run(
                ['docker', 'run', 
                 '-v', f"{os.path.abspath(test_dir)}:/tests",
                 '-w', '/tests',
                 'python-tests',
                 'pytest', '-v', '--html=report.html', '--self-contained-html'],
                capture_output=True,
                text=True,
                cwd=test_dir
            )

            success = result.returncode == 0
            report_path = os.path.join(test_dir, "report.html")

            return {
                'success': success,
                'output': result.stdout,
                'error': result.stderr if not success else None,
                'report': report_path if os.path.exists(report_path) else None
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 