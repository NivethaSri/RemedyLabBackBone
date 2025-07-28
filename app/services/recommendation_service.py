from sqlalchemy.orm import Session
from ..models.health_report import Report
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Load environment variables


def build_prompt(metrics):
    """Builds a well-structured prompt for AI based on lab metrics."""
    lines = [
        "You are an expert AI assistant specialized in functional and integrative medicine.",
        "Analyze the following lab test results and provide a structured response with:",
        "1️⃣ Key abnormal findings",
        "2️⃣ Suggested medical treatments (general guidance, avoid drug names)",
        "3️⃣ Personalized lifestyle and diet recommendations",
        "4️⃣ Stress management and wellness strategies",
        "5️⃣ Follow-up notes for a doctor",
        "",
        "### Lab Test Results:",
    ]

    for entry in metrics or []:
        line = f"- {entry.get('test_name', 'Unknown Test')}: {entry.get('value', '?')} {entry.get('unit', '')}"
        if entry.get("normal_range"):
            line += f" (Normal: {entry['normal_range']})"
        lines.append(line)

    return "\n".join(lines)


def generate_ai_recommendation_service(report_id: str, db: Session):
    """Generates AI recommendations for a given report and saves it to DB."""
    # 1️⃣ Fetch report from DB
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        print(f"❌ Report with ID {report_id} not found.")
        return None, "Report not found"

    # 2️⃣ Build AI prompt
    prompt = build_prompt(report.metrics)
    print(f"📝 Generated prompt for AI:\n{prompt}")

    try:
        # 3️⃣ Call OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a trusted AI health assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=1500,
        )

        ai_recommendation = completion.choices[0].message.content
        print(f"✅ AI Recommendation:\n{ai_recommendation}")

        # 4️⃣ Save to DB
        report.ai_recommendation = ai_recommendation
        db.commit()
        db.refresh(report)

        return report, None

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        return None, str(e)


def save_doctor_recommendation(report_id: str, recommendation: str, db: Session):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        return None, "Report not found"

    report.doctor_recommendation = recommendation  # ✅ Save doctor's recommendation
    db.commit()
    db.refresh(report)

    return report, None


def get_doctor_recommendation(report_id: str, db: Session):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        return None, "Report not found"

    return {
        "report_id": str(report.id),  # ✅ Convert UUID to string
        "doctor_recommendation": report.doctor_recommendation,
        "patient_id": str(report.patient_id) if report.patient_id else None,
    }, None
