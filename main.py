
from collegeboard import downloadMetadata
from gui.dashboard.db import startGUI
import csv
import random as r
from copy import deepcopy
from models.session import Session
from parser import makeQuestion
from config import FULL_EM1, FULL_EM2, FULL_MM1, FULL_MM2

def startSession(settings):

    print(settings)

    if settings["mode"]=="full_test":

        modules=[]

        if settings["subjects"]["English"]:

            if not settings["skipModuleOne"]["English"]:
                modules.append(FULL_EM1)

            modules.append(FULL_EM2)

        if settings["subjects"]["Math"]:

            if not settings["skipModuleOne"]["Math"]:
                modules.append(FULL_MM1)

            modules.append(FULL_MM2)

        time=sum(module["timer"] for module in modules)
        time+=settings["extraTime"]*60

        print("full test")
        print("Modules:", modules)
        print("Time:", time)

        moduleIDs=[]

        for module in modules:
            moduleIDs.append(getIDs(module))

        questions=[]

        for IDs in moduleIDs:
            moduleQuestions=[]

            for id in IDs:
                moduleQuestions.append(
                    makeQuestion(
                        id,
                        IDs[id]["subtopic"],
                        IDs[id]["difficulty"]
                    )
                )

            questions.append(moduleQuestions)

        session=Session(questions, time)
        return session

    else:

        IDs=getIDs(settings)
        questions=[]

        for id in IDs:
            questions.append(
                makeQuestion(
                    id,
                    IDs[id]["subtopic"],
                    IDs[id]["difficulty"]
                )
            )

        session=Session([questions], settings["timer"])
        return session

def getIDs(settings):
    mathExtIDs={}
    engExtIDs={}

    if "Math" in settings["subjects"]:
        mathExtIDs=collectExternalIDs(
            "SAT Question Log Project/data/mathQuestionsMetadata.csv",
            settings
        )

    if "English" in settings["subjects"]:
        engExtIDs=collectExternalIDs(
            "SAT Question Log Project/data/engQuestionsMetadata.csv",
            settings
        )

    return mathExtIDs|engExtIDs

def collectExternalIDs(metaFile, settings):
    remainingQuestionCount=deepcopy(settings)
    extIDs={}

    with open(metaFile,"r") as file:
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

    orderedIDs={}

    for subtopic in settings["questionCount"]:
        for extID, info in extIDs.items():
            if info["subtopic"] == subtopic:
                orderedIDs[extID]=info

    print("Requested:", settings["questionCount"])
    print("Remaining:", remainingQuestionCount["questionCount"])
    print("Collected:", len(extIDs))

    return orderedIDs

if (__name__=="__main__"):
    downloadMetadata()
    startGUI(startSession)