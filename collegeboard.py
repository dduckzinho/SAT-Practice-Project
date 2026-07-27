from config import QUESTION_URL, QUESTIONS_URL
import requests
import csv
import os

headers = {
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

    questions = requests.post(QUESTIONS_URL, json=payload, headers=headers).json()

    return questions

def getQuestion(externalID):

    question = requests.post(
        QUESTION_URL,
        json={"external_id": externalID}
    ).json()

    return question

def downloadMetadata():

    print("Downloading Questions Meta Data...")

    if not os.path.exists("data/engQuestionsMetadata.csv"):
        engQuestions=getQuestionMetadata("INI,CAS,EOI,SEC", 1)
        with open("data/engQuestionsMetadata.csv", "a", newline="") as file:
            writer=csv.DictWriter(file, fieldnames=["questionId", "externalId", "topic", "subTopic", "difficulty"])
            writer.writeheader()
            for question in engQuestions:
                writer.writerow(getImportantData(question))

    if not os.path.exists("data/mathQuestionsMetadata.csv"):
        mathQuestions=getQuestionMetadata("H,P,Q,S", 2)
        with open("data/mathQuestionsMetadata.csv", "a", newline="") as file:
            writer=csv.DictWriter(file, fieldnames=["questionId", "externalId", "topic", "subTopic", "difficulty"])
            writer.writeheader()
            for question in mathQuestions:
                writer.writerow(getImportantData(question))

    print("Finished downloading.")

def getImportantData(question):
    questionId=question["questionId"]

    externalId=question.get("external_id") or question.get("ibn")

    topic=question["primary_class_cd_desc"]
    subTopic=question["skill_desc"]
    difficulty=question["difficulty"]

    return ({"questionId":questionId,
             "externalId":externalId,
             "topic":topic,
             "subTopic":subTopic,
             "difficulty":difficulty})

