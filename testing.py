from collegeboard import getQuestion
import random as r
import csv
from pathlib import Path
import models.question as q
import re
from bs4 import BeautifulSoup

BASE_DIR=Path(__file__).parent
metadata=BASE_DIR / "data" / "engQuestionsMetadata.csv"
#print(metadata)

with open("SAT Question Log Project/data/mathQuestionsMetadata.csv","r") as file:
        reader=csv.DictReader(file)
        rows=list(reader)

r.shuffle(rows)

i=0
questions=[]
for row in rows:
    i+=1
    if i>=10:
        break
    
    question=getQuestion(row["externalId"])
    
    print(question.keys())
    # print(question)
    #---------------------

    typeDict={
        "Multiple Choice":"mcq",
        "SPR":"spr"
    }

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
        questionType=typeDict[question["answer"]["style"]]
        stem=question["prompt"]
        rationale=question["answer"]["rationale"]

        if questionType=="mcq":
            try:
                correctAnswer=question["answer"]["correct_choice"]
            except KeyError:
                correctAnswer=None
            answerOptions=question["answer"]["choices"]
        else:
            match=re.search(r"^<p>The correct answer is (.+?)\.", question["answer"]["rationale"])
            try:
                correctAnswer=match.group(1)
            except AttributeError:
                correctAnswer=rationale
            answerOptions=[]


    subject=None
    topic=None
    subtopic=None
    difficulty=None

    soup=BeautifulSoup(stem, "html.parser")

    resource=None

    if "stimulus" in question and question["stimulus"]:
        resource=question["stimulus"]
    else:
        figure=soup.find("figure")

        if figure:
            svg=figure.find("svg")
            img=figure.find("img")

            if svg:
                resource=str(svg)
            elif img:
                resource=img.get("src")

            figure.decompose()

    stem=str(soup)

    qObject=q.Question(
        questionType,
        subject,
        topic,
        subtopic,
        difficulty,
        stem,
        rationale,
        correctAnswer,
        answerOptions,
        resource
    )
    questions.append(qObject)
    
for question in questions:
    print(question)

    
