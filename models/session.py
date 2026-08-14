from datetime import datetime
from answer_logger import generateSessionId

class Session:
    def __init__(self, questions, timer):
        self.id=generateSessionId()

        self.questions=questions
        self.timer=timer

        self.currentIndex=0
        self.currentModule=0

        self.answers={}
        self.timeSpent={}

        self.date=datetime.now().strftime("%Y-%m-%d")
        if self.questions:
            print(len(questions[0]))

    def curQuestion(self):
        currentQuestion=self.questions[self.currentModule][self.currentIndex]

        return {
            "id": currentQuestion.id,
            "type": currentQuestion.type,
            "stem": currentQuestion.stem,
            "options": currentQuestion.options,
            "rationale": currentQuestion.rationale,
            "correctAnswer": currentQuestion.correctAnswer,
            "resource": currentQuestion.resource,

            "isFirst": self.inFirstQuestion(),
            "isLast": self.inLastQuestion(),
            "isLastInModule": self.isLastInModule(),
            "currentModule": self.currentModule,
            "totalModules": len(self.questions),

            "userAnswer": self.answers.get(currentQuestion.id, "")
        }

    def nextQuestion(self):
        if self.currentIndex < len(self.questions[self.currentModule]) - 1:
            self.currentIndex += 1
        elif self.currentModule < len(self.questions) - 1:
            self.currentModule += 1
            self.currentIndex=0

    def nextModule(self):
        if self.currentModule < len(self.questions) - 1:
            self.currentModule += 1
            self.currentIndex=0

    def previousQuestion(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
        elif self.currentModule > 0:
            self.currentModule -= 1
            self.currentIndex=len(self.questions[self.currentModule]) - 1

    def submitAnswer(self, answer):
        question=self.questions[self.currentModule][self.currentIndex]
        self.answers[question.id]=answer.upper()

    def inFirstQuestion(self):
        return self.currentModule == 0 and self.currentIndex == 0

    def isLastInModule(self):
        return self.currentIndex == len(self.questions[self.currentModule]) - 1

    def inLastQuestion(self):
        return (
            self.currentModule == len(self.questions) - 1
            and self.currentIndex == len(self.questions[self.currentModule]) - 1
        )

    def isFinished(self):
        return self.inLastQuestion()

    def updateQuestionTime(self, ms):
        question=self.questions[self.currentModule][self.currentIndex]
        if question.id in self.timeSpent:
            self.timeSpent[question.id] += ms
        else:
            self.timeSpent[question.id]=ms