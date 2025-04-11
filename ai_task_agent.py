
import subprocess
import re
import os
import time

def run_command(command: str) -> tuple:
    """Execute a shell command and return the output and status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode == 0
    except Exception as e:
        return "", str(e), False

def query_ai(prompt: str) -> str:
    """Query the DeepSeek Coder model using Ollama."""
    try:
        # Craft a prompt that encourages detailed responses
        cmd = f'ollama run deepseek-coder:6.7b "{prompt}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return result.stdout
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def extract_code(text: str) -> str:
    """Extract code from text regardless of formatting."""
    # First, try to find code blocks with triple backticks
    code_block_pattern = r"```(?:python|bash|sh)?\s*([\s\S]*?)```"
    code_blocks = re.findall(code_block_pattern, text)
    
    if code_blocks:
        return code_blocks[0].strip()
    
    # If no code blocks found, extract anything that looks like code
    lines = text.split('\n')
    code_lines = []
    
    for line in lines:
        # Skip empty lines and lines that look like explanations
        if not line.strip() or line.strip().startswith(('#', '//', '/*', '*', '>')):
            continue
        
        # Lines with code-like patterns
        if re.search(r'[\w\d_]+\s*[=\(\[\{]|print|echo|import|def|class|function|mkdir|touch|cd', line):
            code_lines.append(line)
    
    return '\n'.join(code_lines)

def generate_plan(task: str) -> tuple:
    """Generate a plan for completing the task using AI."""
    system_prompt = (
        f"Generate a step-by-step plan to accomplish this programming task: '{task}'. "
        f"Include the shell commands or code needed for each step. Format your response as a numbered list."
    )
    
    print("\n🧠 Generating plan...")
    response = query_ai(system_prompt)
    
    # Extract the plan from the response
    plan_pattern = r"(\d+\.\s+.*(?:\n(?!\d+\.).*)*)+"
    plans = re.findall(plan_pattern, response)
    
    # If no structured plan was found, use the entire response
    final_plan = "\n".join(plans) if plans else response
    
    # Generate the execution code
    code_prompt = (
        f"Write code to accomplish this task: '{task}'. "
        f"Give me only the code with no explanations."
    )
    
    print("🧠 Generating code...")
    code_response = query_ai(code_prompt)
    code = extract_code(code_response)
    
    return final_plan, code

def save_and_run_code(code: str, task: str) -> tuple:
    """Save the extracted code to a file and run it."""
    # Determine file extension based on code content
    file_ext = '.py'  # Default to Python
    if 'echo' in code or 'mkdir' in code or 'cd' in code or 'bash' in code:
        file_ext = '.sh'
    
    # Create a safe filename from the task
    safe_filename = re.sub(r'[^\w]', '_', task.lower())
    filename = f"{safe_filename[:20]}{file_ext}"
    
    # Save the code to the file
    with open(filename, 'w') as f:
        f.write(code)
    
    print(f"\n✅ Code saved to {os.path.abspath(filename)}")
    
    # Run the code
    if file_ext == '.py':
        stdout, stderr, success = run_command(f"python {filename}")
    else:
        stdout, stderr, success = run_command(f"bash {filename}")
    
    return stdout, stderr, success, filename

def main():
    print("🤖 AI Task Agent")
    print("----------------")
    
    task = input("Enter the task you'd like me to perform: ")
    
    # Loop until task is successful
    task_successful = False
    feedback = ""
    
    while not task_successful:
        # If we have feedback, include it in the next iteration
        if feedback:
            plan_prompt = f"Task: {task}\nPrevious attempt feedback: {feedback}\nGenerate a new plan."
        else:
            plan_prompt = task
        
        # Generate plan and code
        plan, code = generate_plan(plan_prompt)
        
        # Display plan to user
        print("\n📋 Here's my plan:")
        print(plan)
        
        # Display code to user
        print("\n📝 Here's the code I'll execute:")
        print(code)
        
        # Ask for approval
        approval = input("\n⚠️ Approve execution? (yes/no): ").lower()
        
        if approval != 'yes' and approval != 'y':
            print("❌ Execution cancelled.")
            user_feedback = input("Would you like to provide feedback to refine the plan? (yes/no): ").lower()
            if user_feedback == 'yes' or user_feedback == 'y':
                feedback = input("Please provide your feedback: ")
                continue
            else:
                return
        
        # Execute the approved code
        print("\n🚀 Executing code...")
        stdout, stderr, success, filename = save_and_run_code(code, task)
        
        # Display results
        print("\n📊 Execution Results:")
        if stdout:
            print("Output:")
            print(stdout)
        if stderr:
            print("Errors:")
            print(stderr)
        
        # Check if task was successful
        success_response = input("\n✅ Was the task completed successfully? (yes/no): ").lower()
        
        if success_response == 'yes' or success_response == 'y':
            print("🎉 Great! Task completed successfully.")
            task_successful = True
        else:
            print("❌ Task was not successful.")
            feedback = input("Please explain what went wrong: ")
            print("\n🔄 I'll refine the solution based on your feedback...")
            time.sleep(1)  # Short pause for user experience

if __name__ == "__main__":
    main()