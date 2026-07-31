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
def getQuestion(extID):

    try:
        response = requests.get(QUESTION_URL)
        
        if response.status_code != 200: # it sent me an empty response once...
            print(f"Failed to get: {extID}. Status code: {response.status_code}")
            return None

        if not response.text.strip():
            print(f"Empty response: {extID}")
            return None
        
        return response.json()

    except requests.exceptions.JSONDecodeError:
        print(f"non-json text for ID: {extID}. {response.text[:100]}")
        return None
    except Exception as e:
        print(f"Error for ID {extID}: {e}")
        return None



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

    return ({"questionId":questionId,
             "externalId":externalId,
             "topic":topic,
             "subtopic":subTopic,
             "difficulty":difficulty})

