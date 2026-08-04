class Session:
    def __init__(self, questions, timer):
        self.questions=questions
        self.timer=timer

        self.currentIndex=0
        self.answers={}

    def curQuestion(self):
        currentQuestion=self.questions[self.currentIndex]
        return{
            "type":currentQuestion.type,
            "stem":currentQuestion.stem,
            "options":currentQuestion.options,
            "rationale":currentQuestion.rationale,
            "correctAnswer":currentQuestion.correctAnswer,
            "resource":currentQuestion.resource
        }


    def nextQuestion(self):
        if self.currentIndex< len(self.questions)-1:
            self.currentIndex+=1

    def previousQuestion(self):
        if self.currentIndex!=0:
            self.currentIndex-=1

    def submitAnswer(self, answer):
        self.answers[self.currentIndex]=answer

    def inLastQuestion(self):
        return self.currentIndex==len(self.questions)-1
    
    def isFinished(self):
        return len(self.answers)==len(self.questions)
        