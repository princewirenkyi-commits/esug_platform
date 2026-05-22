
import json
import anthropic
from django.conf import settings
from .models import Recommendation
 
 
def generate_recommendation(attempt):
    """
    Given a submitted QuizAttempt, call Anthropic Claude to analyse
    the student's performance and produce a personalised study plan.
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
 
    answers = attempt.answers.select_related(
        "question", "selected_option", "question__options"
    )
 
    # Build a summary of the student's answers
    answer_summary = []
    for ans in answers:
        correct_option = ans.question.options.filter(is_correct=True).first()
        answer_summary.append({
            "question": ans.question.text,
            "student_answer": ans.selected_option.text if ans.selected_option else "Not answered",
            "correct_answer": correct_option.text if correct_option else "N/A",
            "is_correct": ans.selected_option.is_correct if ans.selected_option else False,
            "explanation": ans.question.explanation,
        })
 
    prompt = f"""
You are an expert academic advisor for engineering students.
 
Student: {attempt.student.get_full_name()}
Course: {attempt.quiz.course.name}
Quiz: {attempt.quiz.title}
Score: {attempt.score}% ({attempt.earned_marks}/{attempt.total_marks} marks)
Passed: {"Yes" if attempt.passed else "No"}
 
Question-by-question breakdown:
{json.dumps(answer_summary, indent=2)}
 
Return ONLY a valid JSON object with these exact keys:
{{
  "overall_feedback": "Encouraging overall assessment (2-3 sentences)",
  "strengths": "Topics the student answered well (bullet points as plain text)",
  "weaknesses": "Topics needing improvement (bullet points as plain text)",
  "study_plan": "Specific week-by-week or day-by-day study plan",
  "resources_suggested": "Specific textbook chapters, YouTube channels, or online resources"
}}
Do not include markdown or text outside the JSON.
    """
 
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
 
    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
 
    data = json.loads(raw)
 
    rec = Recommendation.objects.create(
        attempt=attempt,
        overall_feedback=data["overall_feedback"],
        strengths=data["strengths"],
        weaknesses=data["weaknesses"],
        study_plan=data["study_plan"],
        resources_suggested=data["resources_suggested"],
        ai_raw_response=raw,
    )
    attempt.status = "analysed"
    attempt.save()
    return rec