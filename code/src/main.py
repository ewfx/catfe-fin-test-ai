import time
import json
import os
from datetime import datetime
from typing import Dict, List

from test_case_generator import generate_test_cases_llm
from code_generator import LLMTestCodeGenerator
# from code_executor import LLMTestExecutor

def print_step(step_name: str, start_time: float) -> None:
    """Print step completion with timing"""
    duration = time.time() - start_time
    print(f"\n⏱️ {step_name} completed in {duration:.2f} seconds")

def create_output_dirs() -> Dict[str, str]:
    """Create necessary output directories"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = f"output_{timestamp}"
    
    dirs = {
        'base': base_dir,
        'test_cases': os.path.join(base_dir, 'test_cases'),
        'test_code': os.path.join(base_dir, 'tests'),
        'reports': os.path.join(base_dir, 'reports'),
        'logs': os.path.join(base_dir, 'logs')
    }
    
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    
    return dirs

def main():
    try:
        total_start_time = time.time()
        output_dirs = create_output_dirs()
        
        print("\n🚀 Starting test automation process...")
        
        # Step 1: Read FRD file
        step_start = time.time()
        frd_file = "test_data/ecommerece.txt"  # Update path as needed
        with open(frd_file, 'r', encoding='utf-8') as f:
            frd_content = f.read()
        print(f"\n📄 Read FRD file: {frd_file}")
        print_step("FRD reading", step_start)

        # Step 2: Extract understanding blocks
        step_start = time.time()
        from extract_features import extract_understanding_blocks
        understanding_blocks = extract_understanding_blocks(frd_content)
        if isinstance(understanding_blocks, dict) and 'error' in understanding_blocks:
            raise Exception(f"Error extracting features: {understanding_blocks['error']}")
        print("\n🔍 Extracted understanding blocks")
        print_step("Feature extraction", step_start)

        # Step 3: Generate test cases
        step_start = time.time()
        print("\n📝 Generating test cases...")
        test_cases_file = generate_test_cases_llm(understanding_blocks)
        # test_cases_file = "test_outputs/test_cases_20250326_161348.json"
        
        if isinstance(test_cases_file, list) and test_cases_file and 'error' in test_cases_file[0]:
            error_msg = test_cases_file[0]['error']
            print(f"\n❌ Test case generation failed: {error_msg}")
            if 'context_length_exceeded' in error_msg:
                print("\n💡 Suggestions to fix token limit error:")
                print("1. Try reducing the size of the input FRD")
                print("2. Split the FRD into smaller sections")
                print("3. Use a model with larger context window")
            return
        
        # Read generated test cases
        with open(test_cases_file, 'r') as f:
            test_cases = json.load(f)
        print(f"\n✅ Generated {len(test_cases)} test cases")
        print_step("Test case generation", step_start)

        # Step 4: Generate test code and framework
        step_start = time.time()
        print("\n🔧 Generating test code and framework...")
        test_generator = LLMTestCodeGenerator()
        generated_content = test_generator.generate_test_code(test_cases)
        
        # Save all test files
        test_generator.save_test_files(generated_content, output_dirs['test_code'])
        print(f"\n💾 Test code and framework files saved to: {output_dirs['test_code']}")
        print("\nGenerated files:")
        for root, _, files in os.walk(output_dirs['test_code']):
            for file in files:
                print(f"  - {os.path.relpath(os.path.join(root, file), output_dirs['test_code'])}")
        print_step("Code generation", step_start)

        # # Step 5: Run tests
        # step_start = time.time()
        # print("\n🧪 Running tests...")
        # executor = LLMTestExecutor()
        # results = executor.run_tests(output_dirs['test_code'])
        
        # if results['success']:
        #     print("\n✅ Tests completed successfully!")
        #     print(f"📊 Test report available at: {results['report']}")
        #     if results.get('output'):
        #         print("\nTest Output Summary:")
        #         print(f"Total Tests: {results['total_tests']}")
        #         print(f"Passed: {results['passed_tests']}")
        #         print(f"Failed: {results['failed_tests']}")
        #         print(f"Skipped: {results['skipped_tests']}")
                
        #         if results['failed_tests'] > 0:
        #             print("\nFailed Tests:")
        #             for failure in results.get('failures', []):
        #                 print(f"  - {failure['test_name']}: {failure['error']}")
        # else:
        #     print("\n❌ Tests failed!")
        #     if results.get('error'):
        #         print("\nError Details:")
        #         print(results['error'])
        
        # print_step("Test execution", step_start)

        # # Final summary
        # total_time = time.time() - total_start_time
        # print("\n📊 Process Summary:")
        # print(f"Total processing time: {total_time:.2f} seconds")
        # print(f"Output directory: {output_dirs['base']}")
        print("Process completed!")

    except Exception as e:
        print(f"\n❌ Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()