class Question:
    def __init__(
        self,
        questionType,
        subject,
        topic,
        subtopic,
        difficulty,
        stem,
        rationale,
        correctAnswer,
        answerOptions=None,
        image=None
    ):
        self.question_type=questionType # "mcq" and "spr"
        self.subject=subject
        self.topic=topic
        self.subtopic=subtopic
        self.difficulty=difficulty

        self.stem=stem
        self.answer_options=answerOptions

        self.correct_answer=correctAnswer
        self.rationale=rationale

        self.image=image