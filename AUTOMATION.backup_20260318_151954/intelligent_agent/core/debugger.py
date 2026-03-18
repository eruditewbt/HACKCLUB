
class Debugger:
    """Analyzes execution results and decides on the next step."""

    def analyze_output(self, exit_code, stdout, stderr):
        """
        Analyzes the output of a code execution.

        Returns a tuple: (is_success, feedback).
        """
        if exit_code == 0 and not stderr:
            print("Code executed successfully.")
            return True, stdout
        elif stderr:
            print("Code execution failed with an error.")
            return False, stderr
        else:
            print("Code executed with a non-zero exit code but no stderr.")
            return False, f"Non-zero exit code: {exit_code}"