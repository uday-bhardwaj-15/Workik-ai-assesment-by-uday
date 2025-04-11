
```markdown
# 💻 AI Task Agent - Internship Assignment for Workik AI

## 🧠 Project Overview

This project is an **AI-powered task agent** that takes a programming task via command line and uses a free AI model (DeepSeek Coder V2 via Ollama) to:

1. Generate a step-by-step plan
2. Write the code or shell commands
3. Ask the user for approval
4. Execute the generated code locally
5. Ask if it succeeded, and if not — it asks for feedback and retries with a refined plan

All tasks and responses happen in the terminal, and execution is fully local.

---

## 🚀 How It Works

1. **Input** your task (e.g., _"Create a Python script to print prime numbers"_).
2. Agent generates a plan + code using DeepSeek Coder (run via `ollama run deepseek-coder:6.7b`)
3. You approve or reject the plan/code.
4. On approval, the code is saved to a `.py` or `.sh` file and executed.
5. If something fails, you're asked for feedback, and the agent retries.

---

## 🧪 Example Usage

```bash
$ python agent.py
🤖 AI Task Agent
----------------
Enter the task you'd like me to perform: create a python script to reverse a string

🧠 Generating plan...
🧠 Generating code...

📋 Here's my plan:
1. Take input from the user
2. Reverse the string using slicing
3. Print the reversed string

📝 Here's the code I'll execute:
input_str = input("Enter a string: ")
print("Reversed:", input_str[::-1])

⚠️ Approve execution? (yes/no): yes

🚀 Executing code...

📊 Execution Results:
Enter a string: hello
Reversed: olleh
```

---

## 🧰 Tech Stack

- **Python 3.8+**
- **DeepSeek Coder V2** (via Ollama)
- Regex for code extraction
- Subprocess for running commands
- CLI interaction for UX

---

## 📝 What I Learned

- Writing modular Python code
- Using `subprocess.run()` safely for executing shell commands
- Prompt engineering to get clean responses from an AI model
- Extracting meaningful code from raw AI responses using regex
- Creating an iterative agent that can self-correct using feedback

---

## 🔧 Improvements I’d Like to Make

- Add **VSCode extension** version using the same logic (bonus part of the task)
- Support for more languages (JavaScript, C++)
- Better error handling and smarter code extraction (with AI parsing)
- Integrate local LLMs like Mistral or Code Llama
- GUI wrapper for less technical users

---

## 📽️ Demo Video

➡️ [Click here to watch the screen recording](https://yourlink.com)  
_(Replace this with Google Drive or YouTube unlisted video link)_

---

## 📂 How to Run

1. Install [Ollama](https://ollama.com) and pull the DeepSeek model:
   ```bash
   ollama pull deepseek-coder:6.7b
   ```

2. Install Python dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```

---

## 👤 Author

- Name: Uday Bhardwaj
- Email: udaybhardwaj269@gmail.com
```
