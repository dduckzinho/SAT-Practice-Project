from collegeboard import getQuestion
import re
import models.question as q
from config import SUB_TOPICS, TOPICS
import sys


def makeQuestion(extID, subtopic, difficulty):

    typeDict={
        "Multiple Choice":"mcq",
        "SPR":"spr"
    }

    question=getQuestion(extID)

    if not question:
        sys.exit("Empty question")

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
        answerData=question.get("answer", {})
        style=answerData.get("style", "Multiple Choice")
        
        questionType=typeDict.get(style, "mcq")
        stem=question.get("prompt", "")
        rationale=answerData.get("rationale", "")

        if questionType == "mcq":
            correctAnswer=answerData.get("correct_choice", None)
            answerOptions=answerData.get("choices", None)
        else:
            match=re.search(r"^<p>The correct answer is (.+?)\.", rationale)
            if match:
                correctAnswer=match.group(1)
            else:
                correctAnswer=rationale
            answerOptions=None
        
    for topicName, subtopics in SUB_TOPICS.items():
        if subtopic in subtopics:
            topic=topicName
            break

    for subjectName, topics in TOPICS.items():
        if topic in topics:
            subject=subjectName
            break

    if subject=="Math":
        match=re.search(r"src=\\\"(.+?)\\\"", stem)
        try:
            resource=match.group(1)
        except (AttributeError):
            match=re.search()

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
    return qObject


"""<p class=\"stem_paragraph \">The equation <span class=\"math_expression \"><span class=\"math-container\"><img align=\"middle\" role=
\"math\" class=\"math-img\" src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJ8AAAAeCAYAAAAy98ydAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAABGJ
hU0UAAAAPUJuPDwAAAAFzUkdCAK7OHOkAAAAEZ0FNQQAAsY8L/GEFAAADUUlEQVR4Xu2YAXaDIAxAPdXO4IE8jnfpVXoTRghBFhOM1sK25r/Hm20phE+CdtNfIzyWAH+wLeERAl
x/FO5gAOG5hnmaw/pE2WkT5jXElx8j3x0MIoleHkVyiDW/fFjl/1sHvKpGEWIdr/MUouNmHO+oencwAKygvtJxo+nZJbZdRevx4OfHm3OGEQ4eS7V+NvcIBxyIb44B5JcFKg64p
Cb1I7RxEs0P30Cq2PiHxJHIOgatqilp75be2wEm3nbLRCcsATs7qKE94k62xOOxy/5an+WF3PPcYKlGCp4H81zn+LpaUO5XjyVtUAvr6dDdgZA8kpc7HFwB90I+0TD2/fx8/4DW
OInUIa4uv0ykqmQVh5XaXrRdvE1eEp1jO/M9wpp8koP0HnNQqp71rbHOydHGftXBWbbkxnWISSOA3+On4cE4kFRcFBeIGXy8aFPylSCxL7wFTQoOZeOC6iraWvu0siaC6IDJBDa
hr8/J0RxfcUAxwGWrNfcpj2FNPunAAtRxsNpkmWWwtHhbEBbxuIGw+G1eFLyfA8c7TnoNUzyKA4ypitFw6gGWOWvqhJK+86qDq9A6TPue91SPX0w+fWGUEHCpCaeB4bLV6qAoUB
4MbgI7aRrFIXEpHsUBjUV9pZMQuDKnRPHNXJ91cBe0rqPkK4cJi5tQx9HEE/ictxeuwTdMQqsSfP9nLK+KN8WjOKCTDqTV1/ljFcucGtKt94oDigEuW+3YS3vN5dSOA+E7e9RxN
PHAdjuwL9winiqc95GTT4/PgimexhxQfCn5lFNPwjKnxjscXIXWoSUfHkzHBamOQxUtJwJ+IU0SO+AnbSzitWDk2y70tZ+8HFs8sgMgxbSs5lMPMM2Z/fI+73BwFW2fADqYLE5a
45Tqzi9LZ0o4qRo1LOIBLl/9wQH9hF9QVqzxcAcExXn7o0dO+HptNNfdDq6iJY22VxraOIl6cdSxll1E5WS8i21jsUnBaUlxN9oGnxV9huI1XlKTEraXA46WNNvjmNT2RdpOviz
h6HToDQbd51lHcyDdBnvS08EwRh3tLWDje1Y8d0AVO7IoezsYBlb5+CqTnod6gQ6+8P9tsY3a+JEOHMdxHMdxHMdxHMdxHMdxHMdxHMf5ZUzTNy2DP9AGZxRnAAAAAElFTkSuQm
CC\" alt=\"open parenthesis, x plus 6, close parenthesis, squared, plus, open parenthesis, y plus 3, close parenthesis, squared, equals
121 \"></span></span> defines a circle in the <span class=\"italic \">xy</span>&#8209;plane. What is the radius of the circle?</p>\n"""