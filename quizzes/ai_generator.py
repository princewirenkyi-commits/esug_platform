
import json
import anthropic
from django.conf import settings
from .models import Quiz, Question, Option
 
 
def generate_quiz_with_ai(course, difficulty="medium", num_questions=10):
    """
    Call Anthropic Claude API to generate quiz questions for a given course.
    Returns the created Quiz instance.
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
 
    prompt = f"""
You are an expert university professor in engineering.
Generate a quiz for the course: "{course.name}"
Department: {course.department.name if course.department else "General Engineering"}
Level: {course.level.number} (Year {course.level.number // 100})
Difficulty: {difficulty}
Number of questions: {num_questions}
 
Return ONLY a valid JSON object in this exact format:
{{
  "quiz_title": "Quiz title here",
  "quiz_description": "Brief description",
  "questions": [
    {{
      "text": "Question text?",
      "explanation": "Why the correct answer is correct",
      "options": [
        {{"text": "Option A", "is_correct": true}},
        {{"text": "Option B", "is_correct": false}},
        {{"text": "Option C", "is_correct": false}},
        {{"text": "Option D", "is_correct": false}}
      ]
    }}
  ]
}}
Each question must have exactly 4 options and exactly 1 correct answer.
Do not include any text outside the JSON object.
    """
 
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
 
    raw_text = message.content[0].text.strip()
 
    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
 
    data = json.loads(raw_text)
 
    # Create Quiz object
    quiz = Quiz.objects.create(
        course=course,
        title=data["quiz_title"],
        description=data.get("quiz_description", ""),
        difficulty=difficulty,
        is_ai_generated=True,
        ai_prompt_used=prompt,
        is_published=False,
    )
 
    # Create Questions and Options
    for i, q_data in enumerate(data["questions"], start=1):
        question = Question.objects.create(
            quiz=quiz,
            text=q_data["text"],
            explanation=q_data.get("explanation", ""),
            order=i,
        )
        for opt in q_data["options"]:
            Option.objects.create(
                question=question,
                text=opt["text"],
                is_correct=opt["is_correct"],
            )
 
    return quiz

