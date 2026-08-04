
from collegeboard import downloadMetadata
from gui.dashboard.db import startGUI
import csv
import models.question as q
import random as r
from copy import deepcopy
from models.session import Session
from parser import makeQuestion


def startSession(settings):
    
    mathExtIDs={}
    engExtIDs={}

    if "Math" in settings["subjects"]:
        mathExtIDs=collectExternalIDs("SAT Question Log Project/data/mathQuestionsMetadata.csv", settings)
    if "English" in settings["subjects"]:
        engExtIDs=collectExternalIDs("SAT Question Log Project/data/engQuestionsMetadata.csv", settings)
    IDs=mathExtIDs|engExtIDs

    questions=[]
    for id in IDs:
        questions.append(makeQuestion(id, IDs[id]["subtopic"], IDs[id]["difficulty"]))

    session=Session(questions, settings["timer"])
    return session



        
def collectExternalIDs(metaFile, settings):
    remainingQuestionCount=deepcopy(settings)
    extIDs={}

    with open(metaFile,"r", encoding="utf-8-sig") as file:
        reader=csv.DictReader(file)
        print(f"Headers for {metaFile}:", reader.fieldnames)
        rows=list(reader)

    r.shuffle(rows)

    for row in rows:
        if row["subtopic"] in remainingQuestionCount["questionCount"]:
            if remainingQuestionCount["questionCount"][row["subtopic"]]>0:
                if row["difficulty"] in settings["difficulties"]:
                    remainingQuestionCount["questionCount"][row["subtopic"]]-=1
                    extIDs[row["externalId"]]={
                        "difficulty":row["difficulty"],
                        "subtopic":row["subtopic"]
                    }
    return extIDs

if (__name__=="__main__"):
    downloadMetadata()
    startGUI(startSession)