class Question:
    def __init__(
        self,
        id,
        type,
        subject,
        topic,
        subtopic,
        difficulty,
        stem,
        rationale,
        correctAnswer,
        options,
        resource
    ):
        self.id=id
        self.type=type #mcq or spr
        self.subject=subject
        self.topic=topic
        self.subtopic=subtopic
        self.difficulty=difficulty

        self.stem=stem
        self.options=options

        self.correctAnswer=correctAnswer
        self.rationale=rationale
        self.resource=resource

    def isCorrect(self, userAnswer):
        return str(userAnswer).strip()==str(self.correctAnswer)

    def getChoices(self):
        return self.options

    def isMultipleChoice(self):
        return self.type=="mcq"

    def isStudentResponse(self):
        return self.type=="spr"


    def __str__(self):
        return f"""
            External ID: {self.id}
            Question type: {self.type}
            Subject: {self.subject}
            Topic: {self.topic}
            Subtopic: {self.subtopic}
            Difficulty: {self.difficulty}
            Question: {shorten(self.stem)}
            Question length: {len(self.stem)}
            Rationale: {shorten(self.rationale)}
            Correct answer: {self.correctAnswer}
            Answer options: {shorten(self.options)}
            Resource: {shorten(self.resource)}
            """

def shorten(text):
    if not text:
        return None
    
    if isinstance(text, str):
        
        if len(text)<=100:
            return text
        
        return text[:100]+"..."
    
    if isinstance(text, list) or isinstance(text, dict):
        return f"Dictionary or list of length {len(text)}"