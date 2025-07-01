🧬 Blood Test Report Analyzer with Multi-Agent AI System
A fast, smart, and highly configurable AI-driven PDF blood test analyzer that simulates expert consultations from doctors, nutritionists, and fitness coaches using LangChain, CrewAI, and Google Gemini 1.5 Flash LLMs.

Key Features
✅ Upload and analyze any blood test PDF
✅ Interact with humorous and specialized agents
✅ Nutrition + Exercise + Diagnosis from PDF
✅ Supports large files using chunking
✅ Output saved as .txt report
✅ Powered by Gemini via LangChain
✅ Built with FastAPI & CrewAI framework


🛠️ Tech Stack
Layer	Tools / Libraries
Backend API	FastAPI
Orchestration	CrewAI
LLM	Gemini 1.5 Flash via langchain-google-genai
PDF Parsing	LangChain PDFLoader
Chunking	RecursiveCharacterTextSplitter
Tooling	CrewAI Tools + Custom Python Functions
Output	Auto-saved in /output folder


🚀 How It Works
User uploads a blood report in .pdf

System reads it and chunks long content for token safety

AI agents take over:

Doctor: Diagnoses in dramatic style

Verifier: Pretends to verify blood report

Nutritionist: Gives (wild) food advice

Fitness Coach: Suggests intense workouts

Each agent runs their task sequentially via CrewAI

Final response is returned as JSON and saved to /output/


📁 Project Structure
bash
Copy
Edit
blood-test-analyser/
├── main.py                  # FastAPI entry point
├── agents.py                # All AI agents
├── tasks.py                 # Agent task definitions
├── tools.py                 # Blood report tools
├── requirements.txt
├── data/                    # Uploaded PDFs
├── output/                  # Processed result summaries
├── .env                     # GEMINI_API_KEY here



⚙️ Setup & Installation
# 1. Clone project
git clone https://github.com/your-repo/blood-test-analyser
cd blood-test-analyser

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
echo "GEMINI_API_KEY=your_actual_key_here" > .env

# 5. Run the app
uvicorn main:app --reload
📡 API Endpoint
POST /analyze

Form Parameters:

file: PDF file upload

query: Optional (e.g., "Summarise my Blood Report")

Response:

json
Copy
Edit
{
  "status": "success",
  "query": "Summarise my Blood Test Report",
  "analysis": "Final output from agents...",
  "file_processed": "blood_test_report_xyz.pdf"
}


🛠️ Debugging & Evolution Journey (In-Depth)
This section tracks our real-world debugging journey — how we started from a broken codebase, identified and fixed every critical error, added missing functionality, and ultimately delivered a complete AI-powered blood report analyzer.

✅ 1. Dependency Compatibility Fixes
Problem:

The codebase had mismatched or outdated dependencies (crewai==0.130.0, langchain, litellm, langchain_groq, etc.).

crewai was breaking with newer langchain and litellm versions.

What We Did:

We locked the crewai version to a working version (0.30.5 or stable).

Matched all dependencies:

langchain with crewai

pydantic v1.x to prevent breaking changes with v2

Re-installed all packages in a clean venv.

How:

bash
Copy
Edit
pip install crewai==0.30.5 langchain==0.1.13 pydantic==1.10.13
✅ 2. Import Structure Fixes
Problem:

Many ImportError and ModuleNotFoundError due to circular references and missing tools.

What We Did:

Separated agents.py, tools.py, and tasks.py cleanly.

Used proper relative imports and top-level function placements.

✅ 3. Missing LLM Integration
Problem:

The agents had no language model (LLM) wired in. llm=None.

What We Did:

At first, tried using Groq model (LLAMA 3 via langchain_groq) but faced errors.

Realized CrewAI internally expects LLMs compatible with LiteLLM.

Switched to using ChatLiteLLM from langchain.chat_models with OpenAI-style config.

✅ 4. Integrated Gemini 1.5 Flash (Google Generative AI)
Problem:

LLAMA or OpenAI-based models exceeded token limits.

What We Did:

Switched to Gemini 1.5 Flash, a fast, high-context model.

Integrated it using:

langchain_google_genai.ChatGoogleGenerativeAI

Gemini API Key in .env

Custom llm = ChatGoogleGenerativeAI(...) object passed into agents

How:

python
Copy
Edit
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
  model="gemini-1.5-flash",
  temperature=0.7,
  google_api_key=os.getenv("GEMINI_API_KEY")
)
✅ 5. File Path Issues
Problem:

File path is not a valid file or URL errors when reading PDF.

The read_blood_report() function always assumed sample.pdf and ignored uploaded files.

What We Did:

Ensured uploaded file is saved with a UUID name inside data/

Passed the correct path to read_blood_report(path)

Added validation using os.path.exists(path)

Code Fix:

python
Copy
Edit
file_id = str(uuid.uuid4())
file_path = f"data/blood_test_report_{file_id}.pdf"
with open(file_path, "wb") as f:
    f.write(await file.read())
✅ 6. Added Output File Saving
Problem:

No way to save generated analysis summary.

What We Did:

Saved all agent outputs to /output/report_summary_<uuid>.txt

Ensured output/ directory exists

Code Fix:

python
Copy
Edit
output_filename = f"output/report_summary_{file_id}.txt"
os.makedirs("output", exist_ok=True)
with open(output_filename, "w", encoding="utf-8") as out_file:
    out_file.write(str(response))
✅ 7. Token Limit Exceeded — Solved via Chunking
Problem:

Models like LLAMA, GPT-3.5 crashed with large PDFs.

What We Did:

Added chunking using RecursiveCharacterTextSplitter in tools.py

Each chunk is analyzed individually and concatenated

Code Snippet:

python
Copy
Edit
from langchain.text_splitter import RecursiveCharacterTextSplitter

def read_blood_report(path: str) -> str:
    loader = PyPDFLoader(path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    return "\n".join([chunk.page_content for chunk in chunks])
✅ 8. Agent Logic Implementation
Problem:

Default Agent roles were missing or blank.

What We Did:

Created rich, role-specific agents:

doctor: dramatic, humorous diagnosis

nutritionist: promotes supplements/diets

verifier: rubber-stamps everything

exercise_specialist: intense workout pusher

Integration:
Each Agent() received:

Custom role, goal, backstory

Specific tools (read_blood_report, analyze_nutrition, etc.)

Gemini LLM

✅ 9. Task Definitions
Problem:

Tasks were too generic or undefined.

What We Did:

Defined clear tasks with:

description

expected_output

tools used

agent assigned

Example:

python
Copy
Edit
help_patients = Task(
  description="Analyze blood report and return scary medical insight...",
  expected_output="Add scary-sounding jargon, URLs, contradicting advice",
  agent=doctor,
  tools=[read_blood_report]
)
✅ 10. Port Buffering or Hanging
Problem:

Uvicorn kept buffering, never launched.

What We Did:

Killed Python background processes

Restarted VSCode terminal or used taskkill in CMD

Ensured uvicorn main:app --reload is clean


🙋 FAQ
Does it support image-based PDFs?
No, only text-based PDFs currently supported.

Can I use OpenAI instead of Gemini?
Yes, but token limits and costs vary.

Is this production-ready?
It's a prototype. Improve agent logic + add authentication to deploy for real.

✨ Future Improvements
Add summarization agent back if needed

Improve report parsing with OCR

Export result in structured JSON / PDF

Add frontend interface with file drag/drop