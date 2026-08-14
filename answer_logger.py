import csv
import os

FILE_PATH="SAT Question Log Project/data/answer_log.csv"

def logSession(session):

    exists=os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a", newline="") as file:
        writer=csv.DictWriter(file, fieldnames=["sessionId", "date", "module", "questionEId", "subject", "topic", "subtopic", "difficulty", "userAnswer", "correctAnswer", "correct", "timeSpent"])

        if not exists:
            writer.writeheader()

        for moduleIndex, module in enumerate(session.questions):
            for question in module:

                userAnswer=session.answers.get(question.id, "")
                timeSpent=session.timeSpent.get(question.id, 0)
                isCorrect=question.isCorrect(userAnswer) if userAnswer else False

                row={
                    "sessionId":session.id,
                    "date":session.date,
                    "module":moduleIndex+1,
                    "questionEId":question.id,
                    "subject":question.subject,
                    "topic":question.topic,
                    "subtopic":question.subtopic,
                    "difficulty":question.difficulty,
                    "userAnswer":userAnswer,
                    "correctAnswer":question.correctAnswer,
                    "correct":isCorrect,
                    "timeSpent":timeSpent
                }
                writer.writerow(row)

def generateSessionId():

    if not os.path.exists(FILE_PATH):
        return 1

    sid=0

    with open(FILE_PATH, "r") as file:
        reader=csv.DictReader(file)
        for row in reader:
            sid=max(sid, int(row["sessionId"]))

    return (sid+1)
            

def scoreSession(session): 

    if not os.path.exists(FILE_PATH):
        return

    total=0
    correct=0

    with open(FILE_PATH, "r") as file:
        reader=csv.DictReader(file)
        for row in reader:
            if int(row["sessionId"])==session.id:
                total+=1
                if row["correct"]=="True":
                    correct+=1
    return {
        "correct":correct,
        "total":total
    }

def getLog(sessionId=None):
    
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as file:
        reader=csv.DictReader(file)
        
        if not sessionId:
            return list(reader)

        
        return [row for row in reader if row["sessionId"]==str(sessionId)]