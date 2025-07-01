# 🧬 Blood Test Report Analyzer

This project is an AI-powered blood report analysis system using CrewAI, Langchain, and Google Gemini 1.5 Flash (via Langchain's `langchain_google_genai`). It takes a blood report PDF as input, analyzes it using multiple agents (Doctor, Nutritionist, Verifier, Fitness Coach), and returns a comprehensive, entertaining, and medically exaggerated response.

---

## 📁 Project Structure

```bash
├── agents.py             # Defines the AI agents with Gemini LLM
├── tasks.py              # Defines their tasks/goals
├── tools.py              # Custom tools for PDF reading, chunking, etc.
├── main.py               # FastAPI server with file upload & agent execution
├── output/               # Stores generated output summaries
├── data/                 # Stores uploaded PDF reports temporarily
├── .env                  # API keys and environment config
├── requirements.txt      # All necessary dependencies
```

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/blood-report-analyzer.git
cd blood-report-analyzer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up `.env` File
```env
GEMINI_API_KEY=your_gemini_api_key
```

> 💡 You need to [enable the Gemini API](https://aistudio.google.com/app/apikey) and use `gemini-1.5-flash` model.

### 5. Start the Server
```bash
uvicorn main:app --reload
```

---

## 📥 API Usage

**POST** `/analyze`
- `file`: PDF blood report (Upload)
- `query`: Optional (default = "Summarise my Blood Test Report")

**Response:**
```json
{
  "status": "success",
  "query": "Summarise my Blood Test Report",
  "analysis": "Full agent output here",
  "file_processed": "your_report.pdf"
}
```

**Output is also saved in `output/report_summary_<uuid>.txt`**

---

## 🤖 Agents

| Agent               | Description |
|--------------------|-------------|
| Doctor             | Diagnoses everything dramatically, loves to panic users |
| Verifier           | Approves everything without thinking |
| Nutritionist       | Recommends expensive supplements, trendy diets |
| Exercise Coach     | Promotes intense workouts for everyone |

All powered by **Gemini 1.5 Flash**.

---

## 🧠 Tools
- `read_blood_report`: Reads + chunks PDF for token efficiency
- `analyze_nutrition`: Recommends food/supplements
- `create_exercise_plan`: Suggests (unsafe) workout plans
- `search_tool`: Optional search tool via Serper.dev

---

## 🛠️ Debugging & Evolution Journey (In-Depth)

### ✅ 1. **Dependency Compatibility Fixes**
- Locked `crewai` to `0.30.5`
- Fixed `pydantic`, `langchain`, `litellm` mismatches

### ✅ 2. **Import Structure Fixes**
- Split files into agents/tasks/tools
- Fixed import errors

### ✅ 3. **Missing LLM Integration**
- Initially no model was wired in
- Tried Groq, realized it needs LiteLLM
- Integrated `ChatLiteLLM` and later Gemini

### ✅ 4. **Integrated Gemini 1.5 Flash**
- Used `langchain_google_genai.ChatGoogleGenerativeAI`
- Model: `gemini-1.5-flash`
- Passed into agents using `llm=...`

### ✅ 5. **File Path Issues**
- Handled dynamic PDF upload
- Used `os.path.exists()` to validate

### ✅ 6. **Output Saving**
- Saved result to `output/report_summary_<uuid>.txt`
- Created `output/` folder if not present

### ✅ 7. **Token Limit Fix with Chunking**
- Used `RecursiveCharacterTextSplitter`
- Chunked large PDF into smaller LLM-readable pieces

### ✅ 8. **Agent Logic Implementation**
- Wrote goals, backstories, personalities per agent

### ✅ 9. **Task Logic**
- Defined tasks with `description`, `expected_output`, `agent`, `tools`

### ✅ 10. **Port Buffering Fix**
- Closed hanging Python tasks
- Restarted `uvicorn` cleanly

---

## 📦 Future Enhancements
- Add real medical diagnostics
- Add frontend UI for upload
- Send email summary to user

---

## 👨‍💻 Contributors
- Insha Sadaf

---

## 📄 License
MIT License
