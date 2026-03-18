import os
from core.file_manager import FileManager
from core.code_generator import CodeGenerator
from core.code_executor import CodeExecutor
from core.debugger import Debugger

class Agent:
    """The main intelligent agent orchestrator."""
    def __init__(self, project_name="my_project"):
        self.project_path = os.path.join("projects", project_name)
        self.file_manager = FileManager(self.project_path)
        self.code_generator = CodeGenerator()
        self.code_executor = CodeExecutor()
        self.debugger = Debugger()
        self.max_retries = 3

    def run(self, request, language, entry_file):
        """The main method to run the entire agent workflow."""
        print(f"🤖 Agent is starting a new task: '{request}' in {language}")

        # Step 1: Generate initial code
        print("💡 Step 1: Generating initial code...")
        initial_code = self.code_generator.generate_code(request, language)

        # Handle single vs. multi-file projects
        if isinstance(initial_code, dict):
            for filename, content in initial_code.items():
                self.file_manager.write_file(filename, content)
        else:
            self.file_manager.write_file(entry_file, initial_code)

        # Step 2: Iteratively execute and debug
        for attempt in range(self.max_retries):
            print(f"\n⚙️ Step 2 (Attempt {attempt + 1}/{self.max_retries}): Executing code...")
            exit_code, stdout, stderr = self.code_executor.run_code(
                self.project_path, language, entry_file
            )

            is_success, feedback = self.debugger.analyze_output(exit_code, stdout, stderr)

            if is_success:
                print("\n✅ Task completed successfully!")
                print("Final Output:")
                print("---")
                print(stdout)
                print("---")
                return True
            else:
                print(f"\n❌ Code failed. Feedback from execution: {feedback}")

                # Step 3: Debug and fix the code
                print("🐛 Step 3: Debugging and generating a fix...")
                current_files_content = self.file_manager.get_all_files()
                fixed_code = self.code_generator.fix_code(current_files_content, feedback, language)

                # Update only the files that need fixing
                if isinstance(fixed_code, dict):
                    for filename, content in fixed_code.items():
                        self.file_manager.write_file(filename, content)
                else:
                    self.file_manager.write_file(entry_file, fixed_code)


        print("\n❌ Task failed after multiple attempts.")
        print("Final files in the project:")
        print(self.file_manager.get_all_files())
        return False

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Simple Python multi-file task
    python_agent = Agent(project_name="python_project")
    request_py = "Create a two-file Python program. 'main.py' should import a function from 'utils.py' that returns the string 'Hello from a separate file!' and then print it."
    python_agent.run(request_py, "python", "main.py")

    # Example 2: Simple JavaScript single-file task
    js_agent = Agent(project_name="javascript_project")
    request_js = "Create a single-file JavaScript program that prints 'Hello, world!' to the console."
    js_agent.run(request_js, "javascript", "index.js")