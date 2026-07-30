class Session:
    def __init__(self, questions, timer):
        self.questions=questions
        self.timer=timer

        self.curIndex=0
        self.answers={}

    def curQuestion(self):
        return self.questions[self.curIndex]

    def nextQuestion(self):
        if self.curIndex< len(self.questions)-1:
            self.curIndex+=1

    def previousQuestion(self):
        if self.curIndex!=0:
            self.curIndex-=1

    def submitAnswer(self, answer):
        self.answers[self.curIndex]=answer

    def inLastQuestion(self):
        return self.curIndex==len(self.questions)-1
    
    def isFinished(self):
        return len(self.answers)==len(self.questions)
        