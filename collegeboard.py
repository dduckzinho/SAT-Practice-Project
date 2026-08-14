from config import QUESTION_URL, QUESTIONS_URL
import requests
import csv
import os

headers={
    "Content-Type": "application/json",
    "Origin": "https://satsuiteeducatorquestionbank.collegeboard.org",
    "Referer": "https://satsuiteeducatorquestionbank.collegeboard.org/"
}

def getQuestionMetadata(domains, test):

    payload={
        "asmtEventId":99,
        "domain":domains,
        "test":test
    }

    questions=requests.post(QUESTIONS_URL, json=payload, headers=headers).json()

    return questions

def getQuestion(externalID):

    question=requests.post(
        QUESTION_URL,
        json={
            "external_id": externalID
        },
        headers={
            "Content-Type": "application/json",
            "Origin": "https://satsuiteeducatorquestionbank.collegeboard.org",
            "Referer": "https://satsuiteeducatorquestionbank.collegeboard.org/",
        }
    )
    return question.json()



def downloadMetadata():

    if not os.path.exists("SAT Question Log Project/data/engQuestionsMetadata.csv"):
        engQuestions=getQuestionMetadata("INI,CAS,EOI,SEC", 1)
        with open("SAT Question Log Project/data/engQuestionsMetadata.csv", "a", newline="") as file:
            writer=csv.DictWriter(file, fieldnames=["questionId", "externalId", "topic", "subtopic", "difficulty"])
            writer.writeheader()
            for question in engQuestions:
                writer.writerow(getImportantData(question))

    if not os.path.exists("SAT Question Log Project/data/mathQuestionsMetadata.csv"):
        mathQuestions=getQuestionMetadata("H,P,Q,S", 2)
        with open("SAT Question Log Project/data/mathQuestionsMetadata.csv", "a", newline="") as file:
            writer=csv.DictWriter(file, fieldnames=["questionId", "externalId", "topic", "subtopic", "difficulty"])
            writer.writeheader()
            for question in mathQuestions:
                writer.writerow(getImportantData(question))


def getImportantData(question):
    questionId=question["questionId"]

    externalId=question.get("external_id") or question.get("ibn")

    topic=question["primary_class_cd_desc"]
    subTopic=question["skill_desc"]
    difficulty=question["difficulty"]

    
    if subTopic=="Cross-text Connections":
        subTopic="Cross-Text Connections"

    return ({"questionId":questionId.strip(),
             "externalId":externalId.strip(),
             "topic":topic.strip(),
             "subtopic":subTopic.strip(),
             "difficulty":difficulty.strip()})

