try:
        extID=question["externalid"]
        
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

    else:
        questionType=question["type"]
        stem=question["stem"]
        rationale=question["rationale"]
        correctAnswer=question["correct_answer"]
        try:
            answerOptions=question["answerOptions"]
        except KeyError:
            answerOptions=None


    subject=None
    topic=None
    subtopic=None
    difficulty=None


    qObject=q.Question(
        questionType,
        subject,
        topic,
        subtopic,
        difficulty,
        stem,
        rationale,
        correctAnswer,
        answerOptions
    )
    questions.append(qObject)