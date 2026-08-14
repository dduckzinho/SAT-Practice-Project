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
    
    # print(question.keys())
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
        question,
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

math={}
english={}

math={
    "Linear equations in one variable": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Linear functions": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Linear equations in two variables": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Systems of two linear equations in two variables": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Linear inequalities in one or two variables": {
        "E": 0,
        "M": 0,
        "H": 0
    },

    # --------------------------------------------------------------------------

    "Nonlinear functions": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Nonlinear equations in one variable and systems of equations in two variables": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Equivalent expressions": {
        "E": 0,
        "M": 0,
        "H": 0
    },

    # --------------------------------------------------------------------------

    "Ratios, rates, proportional relationships, and units": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Percentages": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "One-variable data: Distributions and measures of center and spread": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Two-variable data: Models and scatterplots": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Probability and conditional probability": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Inference from sample statistics and margin of error": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Evaluating statistical claims: Observational studies and experiments": {
        "E": 0,
        "M": 0,
        "H": 0
    },

    # --------------------------------------------------------------------------

    "Area and volume": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Lines, angles, and triangles": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Right triangles and trigonometry": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Circles": {
        "E": 0,
        "M": 0,
        "H": 0
    }
}

english={
    "Central Ideas and Details": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Inferences": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Command of Evidence": {
        "E": 0,
        "M": 0,
        "H": 0
    },

    # --------------------------------------------------------------------------

    "Words in Context": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Text Structure and Purpose": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Cross-Text Connections": {
        "E": 0,
        "M": 0,
        "H": 0
    },

    # --------------------------------------------------------------------------

    "Rhetorical Synthesis": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Transitions": {
        "E": 0,
        "M": 0,
        "H": 0
    },

    # --------------------------------------------------------------------------

    "Boundaries": {
        "E": 0,
        "M": 0,
        "H": 0
    },
    "Form, Structure, and Sense": {
        "E": 0,
        "M": 0,
        "H": 0
    }
}

with open("SAT Question Log Project/data/mathQuestionsMetadata.csv","r") as file:
    reader=csv.DictReader(file)
    for row in reader:
        math[row["subtopic"]][row["difficulty"]]+=1

with open("SAT Question Log Project/data/engQuestionsMetadata.csv","r") as file:
    reader=csv.DictReader(file)
    for row in reader:
        english[row["subtopic"]][row["difficulty"]]+=1


print(f"Math: {math}")
print()
print(f"English: {english}")
    
