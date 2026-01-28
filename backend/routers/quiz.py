import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

from rag_pipeline import get_relevant_docs
from chat_utils import local_llm_generate
from logger_utils import create_log_entry

router = APIRouter()


class QuizRequest(BaseModel):
    topic: Optional[str] = None


class QuizQuestion(BaseModel):
    question_number: int
    question_type: str
    question: str
    options: Optional[List[str]] = None
    answer: str


class QuizResponse(BaseModel):
    quiz_text: str
    sources: List[str]
    topic: str


@router.post("/generate")
def generate_quiz(request: QuizRequest):
    """Generate a quiz on a topic"""
    
    if request.topic and request.topic.strip():
        topic = request.topic.strip()
        docs = get_relevant_docs(topic)
        user_query = f"Generate quiz on topic: {topic}"
    else:
        general_topics = ["encryption", "network security", "cryptography", "authentication", "firewall"]
        topic = random.choice(general_topics)
        docs = get_relevant_docs(topic)
        user_query = "Generate random quiz from all PDFs"
    
    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")
    
    quiz_context = " ".join([doc.page_content for doc in docs])
    
    prompt = f"""
You are a professional Quiz Generator AI specializing in network security.
Based on the following study material, generate a 10-question quiz with mixed question types.

Question Types to Include:
- 2-3 True/False questions
- 3-4 Single Correct Answer (MCQ with 4 options)
- 2-3 Multiple Correct Answers (select all that apply)
- 2 Open-Ended Questions (no options, requires written answer)

Ensure questions are conceptually relevant, moderately challenging, and well-formatted.

Study Material:
{quiz_context[:3000]}

Format output exactly like this:

Q1. [TRUE/FALSE] <question text>
Answer: True/False

Q2. [SINGLE CORRECT] <question text>
A) <option 1>
B) <option 2>
C) <option 3>
D) <option 4>
Correct Answer: <letter>

Q3. [MULTIPLE CORRECT] <question text>
A) <option 1>
B) <option 2>
C) <option 3>
D) <option 4>
Correct Answers: <letters separated by comma, e.g., A, C>

Q4. [OPEN ENDED] <question text>
Sample Answer: <brief expected answer>

Generate all 10 questions following these formats strictly. Mix the question types randomly.
"""

    try:
        quiz_output = local_llm_generate(prompt)
        
        create_log_entry(user_query, docs, quiz_output, agent_type="quiz_generator")
        
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        
        return QuizResponse(
            quiz_text=quiz_output,
            sources=sources,
            topic=topic
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
