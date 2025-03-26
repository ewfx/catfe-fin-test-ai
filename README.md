# 🚀 AI-Powered Test Automation Generator

## 📌 Table of Contents
- [Introduction](#introduction)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)

---

## 🎯 Introduction
An intelligent test automation framework that automatically generates comprehensive test suites from functional requirements documents (FRDs). It leverages GPT-4 to understand requirements, generate test cases, and create executable test code, making test automation more efficient and maintainable.

## 💡 Inspiration
Manual test case creation and automation is time-consuming and error-prone. We wanted to streamline this process by using AI to automatically understand requirements and generate high-quality test cases and automation code, reducing the time and effort needed for test automation while improving coverage.

## ⚙️ What It Does

- Extracts understanding blocks from FRD documents
- Generates comprehensive test cases covering functional, boundary, and negative scenarios
- Creates executable Selenium-based test code
- Generates necessary configuration files for test execution
- Supports Docker-based test execution
- Provides detailed execution reports

## 🛠️ How We Built It
The system is built with a modular architecture:
1. Feature Extractor: Analyzes FRD documents
2. Test Case Generator: Creates structured test cases
3. Code Generator: Produces executable test code
4. Test Executor: Runs tests in Docker environment

## 🚧 Challenges We Faced
1. Token limit management with large FRDs
2. Ensuring consistent test case structure
3. Generating maintainable test code
4. Handling complex test dependencies
5. Managing Docker environment setup

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/catfe-fin-test-ai.git
   cd catfe-fin-test-ai/code/src
   ```

2. Create and activate virtual environment  
   ```sh
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies  
   ```sh
   pip install -r requirements.txt
   ```

4. Create .env file  
   ```sh
   # Create .env file
   touch .env  # For macOS/Linux
   # or
   echo. > .env  # For Windows
   ```

5. Add your OpenAI API key to .env file:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

6. Run the project  
   ```sh
   python main.py
   ```

7. Deactivate virtual environment when done  
   ```sh
   deactivate
   ```

## 📁 Project Structure
```text
catfe-fin-test-ai/code/src/
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
├── test_data/
│   └── frd.txt
├── code_generator/
│   ├── __init__.py
│   └── code_generator.py
├── test_case_generator/
│   ├── __init__.py
│   └── generator.py
└── code_executor/
    ├── __init__.py
    └── executor.py
```

Contents of `.env.example`:
```env
# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here
```

Contents of `.gitignore`:
```gitignore
# Virtual Environment
venv/
env/

# Environment Variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class

# Output Directories
output*/
test_outputs/
tests/

# IDE
.vscode/
.idea/
```

## 🏗️ Tech Stack
- 🔹 Language: Python 3.9+
- 🔹 AI: OpenAI GPT-4 API
- 🔹 Testing: Pytest, Selenium WebDriver
- 🔹 Containerization: Docker
- 🔹 Other: PyYAML, Rich (for console output)

