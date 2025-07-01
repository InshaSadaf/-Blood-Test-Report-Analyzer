# tools.py
from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re, os


#  Prebuilt search tool
search_tool = SerperDevTool()

# Custom blood test PDF reader tool
# Blood test reader with chunking
@tool("blood_report_reader")
def read_blood_report(path: str) -> str:
    """Reads and returns content from a blood test PDF, with chunking."""
    if not os.path.exists(path):
        raise ValueError(f"File path {path} is not a valid file or URL.")
    
    loader = PyPDFLoader(path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)
    return "\n\n".join(chunk.page_content for chunk in chunks)

#  Nutrition analysis tool
@tool("nutrition_analysis_tool")
def analyze_nutrition(blood_report_data: str) -> str:
    """Analyzes blood report and suggests nutrition recommendations."""
    suggestions = []
    processed = re.sub(r"\s+", " ", blood_report_data.lower())

    if "low iron" in processed or re.search(r"iron.*(low|decreased)", processed):
        suggestions.append("Increase iron intake: spinach, lentils, seeds, red meat.")
    if "high iron" in processed:
        suggestions.append("Reduce iron intake and consult a specialist.")
    if "low vitamin d" in processed:
        suggestions.append("Get sunlight daily and consider fortified milk/supplements.")
    if "b12" in processed and "low" in processed:
        suggestions.append("Eat eggs, dairy, fish. Consider B12 injections.")
    if "ldl" in processed and "high" in processed:
        suggestions.append("Avoid fried food, eat fiber, and use olive oil.")
    if "hdl" in processed and "low" in processed:
        suggestions.append("Eat fatty fish, avocado, nuts. Exercise regularly.")
    if "glucose" in processed and "high" in processed:
        suggestions.append("Reduce carbs and sugar; eat low-GI foods.")
    if "dehydration" in processed or "high sodium" in processed:
        suggestions.append("Drink 2.5–3L water daily, eat hydrating fruits.")
    if "protein" in processed and "low" in processed:
        suggestions.append("Increase protein: eggs, chicken, legumes, whey.")
    if not suggestions:
        suggestions = [
            "Maintain a balanced diet with vegetables, protein, and whole grains.",
            "Avoid processed food and sugar-laden drinks.",
            "Consult a registered dietitian for a personalized plan."
        ]
    return "Nutrition Recommendations:\n" + "\n".join(f"- {s}" for s in suggestions)

# Exercise plan tool
@tool("exercise_plan_tool")
def create_exercise_plan(blood_report_data: str) -> str:
    """Creates a personalized exercise plan from a blood report."""
    suggestions = []
    report = blood_report_data.lower()

    if "low hemoglobin" in report:
        suggestions.append("Start with light cardio and gradually increase intensity.")
    if "high blood pressure" in report:
        suggestions.append("Do walking, swimming, cycling; avoid heavy weightlifting.")
    if "glucose" in report and "high" in report:
        suggestions.append("Do moderate aerobic exercise for 30–45 mins, 5x a week.")
    if "high ldl" in report or "low hdl" in report:
        suggestions.append("Brisk walking, jogging, or Zumba — 150 mins per week.")
    if "low vitamin d" in report:
        suggestions.append("Try yoga or walking outdoors in sunlight.")
    suggestions += [
        "Warm-up: 5 mins dynamic stretching",
        "Cardio: 20 mins (running, HIIT, or cycling)",
        "Strength: 3 sets of push-ups, squats, lunges",
        "Core: Planks, mountain climbers, sit-ups",
        "Cool down: 5 mins yoga or deep breathing"
    ]

    return "Personalized Exercise Plan:\n" + "\n".join(f"- {s}" for s in suggestions)
