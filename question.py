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
        answerOptions
    ):
        self.questionType=questionType #mcq or spr
        self.subject=subject
        self.topic=topic
        self.subtopic=subtopic
        self.difficulty=difficulty

        self.stem=stem
        self.answerOptions=answerOptions

        self.correctAnswer=correctAnswer
        self.rationale=rationale

    def isCorrect(self, userAnswer):
        return str(userAnswer).strip()==str(self.correctAnswer)

    def getChoices(self):
        return self.answerOptions

    def isMultipleChoice(self):
        return self.questionType=="mcq"

    def isStudentResponse(self):
        return self.questionType=="spr"


    def __str__(self):
        return f"""
            Question type: {self.questionType}
            Subject: {self.subject}
            Topic: {self.topic}
            Subtopic: {self.subtopic}
            Difficulty: {self.difficulty}
            Question: {shorten(self.stem)}
            Question length: {len(self.stem)}
            Rationale: {shorten(self.rationale)}
            Correct answer: {self.correctAnswer}
            Answer options: {(self.answerOptions)}
            """

def shorten(text):
    if not text:
        return None
    
    if isinstance(text, str):
        
        if len(text)<=40:
            return text
        
        return text[:40]+"..."
    
    if isinstance(text, list) or isinstance(text, dict):
        return f"Dictionary or list of length {len(text)}"