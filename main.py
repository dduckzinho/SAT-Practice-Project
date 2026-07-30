
from collegeboard import getQuestion
from gui.dashboard import startGUI
import csv
import models.question as q
import random as r
import copy

def makeQuestion(extID):
    ...

def startSession(settings):
    if "Math" in settings["subjects"]:
        mathExtIDs=collectExternalIDs("mathQuestionMetadata.csv", settings)
    if "English" in settings["subjects"]:
        engExtIDs=collectExternalIDs("engQuestionMetadata.csv", settings)

        
def collectExternalIDs(metaFile, settings):
    remainingQuestionCount= copy.deepcopy(settings)
    extIDs=[]

    with open(metaFile,"r") as file:
        reader=csv.DictReader(file)
        rows = list(reader)

    r.shuffle(rows)

    for row in rows:
        if row["subtopic"] in remainingQuestionCount["questionCount"]:
            if remainingQuestionCount["questionCount"][row["subtopic"]]>0:
                if row["difficulty"] in settings["difficulties"]:
                    remainingQuestionCount["questionCount"][row["subtopic"]]-=1
                    extIDs.append(row["externalId"])
    return extIDs

if (__name__=="__main__"):
    startGUI(startSession)