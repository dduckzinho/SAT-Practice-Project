from collegeboard import getQuestion
import re
import models.question as q
from config import SUB_TOPICS, TOPICS
import sys
from bs4 import BeautifulSoup
from PIL import Image
import base64
import io


def cropEmbeddedPNGs(html):
    if not html:
        return html

    soup=BeautifulSoup(html, "html.parser")

    for img in soup.find_all("img"):
        src=img.get("src", "")

        if src.startswith("data:image/png;base64,"):
            img["src"]=cropTransparentPNG(src)

    return str(soup)


def cropTransparentPNG(uri):
    if not uri.startswith("data:image/png;base64,"):
        return uri

    prefix, b64=uri.split(",", 1)

    try:
        image_data=base64.b64decode(b64)
        img=Image.open(io.BytesIO(image_data)).convert("RGBA")
    except Exception:
        return uri

    alpha=img.getchannel("A")
    bbox=alpha.getbbox()

    if bbox is None:
        return uri

    img=img.crop(bbox)

    output=io.BytesIO()
    img.save(output, format="PNG")

    encoded=base64.b64encode(output.getvalue()).decode()

    return prefix + "," + encoded


def findTopicAndSubject(subtopic):
    topic=None

    for topicName, subtopics in SUB_TOPICS.items():
        if subtopic in subtopics:
            topic=topicName
            break

    if topic is None:
        raise ValueError(f"Unknown subtopic: {repr(subtopic)}")

    subject=None

    for subjectName, topics in TOPICS.items():
        if topic in topics:
            subject=subjectName
            break

    if subject is None:
        raise ValueError(f"Unknown topic: {repr(topic)}")

    return topic, subject


def extractResource(soup, question):
    if question.get("stimulus"):
        stimulus=question["stimulus"]

        if isinstance(stimulus, str):
            return cropEmbeddedPNGs(stimulus)

        return stimulus

    figure=soup.find("figure")

    if figure is None:
        return None

    svg=figure.find("svg")
    img=figure.find("img")

    resource=None

    if svg:
        resource=str(svg)

    elif img:
        resource=img.get("src")

        if resource and resource.startswith("data:image/png;base64,"):
            resource=cropTransparentPNG(resource)

    figure.decompose()

    return resource


def normalizeCorrectAnswer(correctAnswer, extID):
    if correctAnswer is None:
        return None

    if not isinstance(correctAnswer, list):
        correctAnswer=[correctAnswer]

    normalized=[]

    for answer in correctAnswer:
        if answer is None:
            raise ValueError(
                f"Question {extID} contains None as a correct answer"
            )

        normalized.append(str(answer).upper())

    return normalized


def processAnswerOptions(answerOptions):
    if not answerOptions:
        return answerOptions

    if isinstance(answerOptions, list):
        options=answerOptions

    elif isinstance(answerOptions, dict):
        options=answerOptions.values()

    else:
        return answerOptions

    for option in options:
        if not isinstance(option, dict):
            continue

        if "body" in option and option["body"]:
            option["body"]=cropEmbeddedPNGs(option["body"])

        if "content" in option and option["content"]:
            option["content"]=cropEmbeddedPNGs(option["content"])

    return answerOptions


def makeQuestion(extID, subtopic, difficulty):

    typeDict={
        "Multiple Choice": "mcq",
        "SPR": "spr"
    }

    question=getQuestion(extID)

    if not question:
        sys.exit(f"Empty question: {extID}")

    try:
        questionType=question["type"]
        stem=question["stem"]
        rationale=question["rationale"]
        correctAnswer=question["correct_answer"]
        answerOptions=question.get("answerOptions")

    except KeyError:
        answerData=question.get("answer", {})

        style=answerData.get("style", "Multiple Choice")
        questionType=typeDict.get(style, "mcq")

        stem=question.get("prompt", "")
        rationale=answerData.get("rationale", "")

        if questionType == "mcq":
            correctAnswer=answerData.get("correct_choice")
            answerOptions=answerData.get("choices")

        else:
            match=re.search(
                r"^<p>The correct answer is (.+?)\.",
                rationale
            )

            if match:
                correctAnswer=match.group(1)
            else:
                correctAnswer=rationale

            answerOptions=None

    topic, subject=findTopicAndSubject(subtopic)

    soup=BeautifulSoup(stem or "", "html.parser")
    resource=extractResource(soup, question)

    for img in soup.find_all("img"):
        src=img.get("src", "")

        if src.startswith("data:image/png;base64,"):
            img["src"]=cropTransparentPNG(src)

    stem=str(soup)

    correctAnswer=normalizeCorrectAnswer(
        correctAnswer,
        extID
    )

    answerOptions=processAnswerOptions(answerOptions)

    rationale=cropEmbeddedPNGs(rationale)

    if isinstance(resource, str):
        if resource.startswith("data:image/png;base64,"):
            resource=cropTransparentPNG(resource)

        elif "<" in resource:
            resource=cropEmbeddedPNGs(resource)


    qObject=q.Question(
        extID,
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

    return qObject