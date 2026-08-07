import csv
import os


def logSession(session):
    exists=os.path.exists("SAT Question Log Project/data/answer_log.csv")

    with open("SAT Question Log Project/data/answer_log.csv", "a") as file:
        writer=csv.DictWriter(file, fieldnames=["externalId", "date", "subject", "topic", "subtopic", "difficulty", "correctAnswer", "userAnswer", "correct", "timeSpent"])

        if not exists:
            writer.writeheader()

    for question in session.questions:

        sessionData=[
            session.answers[question.id],
            question.isCorrect(session.answers[question.id]),
            session.timeSpent[question.id]
        ]
        row=(question.getInfo()).insert(1, session.date)+sessionData

        writer.writerow(row)



def scoreSession(session):
    ...