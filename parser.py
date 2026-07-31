from collegeboard import getQuestion
import re
import models.question as q
from config import SUB_TOPICS, TOPICS
import sys


def makeQuestion(extID, subtopic, difficulty):

    typeDict={
        "Multiple Choice":"mcq",
        "SPR":"spr"
    }

    question=getQuestion(extID)

    if not question:
        sys.exit("Empty question")

    try:
        questionType=question["type"]
        stem=question["stem"]
        rationale=question["rationale"]
        correctAnswer=question["correct_answer"]
        try:
            answerOptions=question["answerOptions"]
        except KeyError:
            answerOptions=None
        
    except KeyError: #small id question
        answerData=question.get("answer", {})
        style=answerData.get("style", "Multiple Choice")
        
        questionType=typeDict.get(style, "mcq")
        stem=question.get("prompt", "")
        rationale=answerData.get("rationale", "")

        if questionType == "mcq":
            correctAnswer=answerData.get("correct_choice", None)
            answerOptions=answerData.get("choices", None)
        else:
            match=re.search(r"^<p>The correct answer is (.+?)\.", rationale)
            if match:
                correctAnswer=match.group(1)
            else:
                correctAnswer=rationale
        
    for topicName, subtopics in SUB_TOPICS.items():
        if subtopic in subtopics:
            topic=topicName
            break

    for subjectName, topics in TOPICS.items():
        if topic in topics:
            subject=subjectName
            break


    qObject=q.Question(
        questionType,
        subject,
        topic,
        subtopic,
        difficulty,
        stem,
        rationale,
        correctAnswer,
        answerOptions
    )
    return qObject