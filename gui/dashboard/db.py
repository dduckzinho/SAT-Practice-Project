import webview
import os
from config import TOPICS, SUB_TOPICS, SUB_TOPIC_TIME, DIFFICULTY, MATH_SUB_TOPICS

class DashboardAPI:
    def __init__(self, callback):
        self.callback=callback
        self.session=None

    def getConfig(self):
        return {
            "TOPICS": TOPICS,
            "SUB_TOPICS": SUB_TOPICS,
            "SUB_TOPIC_TIME": SUB_TOPIC_TIME,
            "DIFFICULTY": DIFFICULTY
        }

    def submitSettings(self, payload):

        subjects=[]
        questionCount=payload["questionCount"]
        difficulties=[]
        
        for diff in payload["difficulties"]:
            difficulties.append(DIFFICULTY[diff])

        seconds=0
        for subtopic, qAmount in questionCount.items():
            seconds+=(SUB_TOPIC_TIME[subtopic] * qAmount)
        totalSeconds=(seconds * 1.05) + (payload["extraTime"] * 60)
        timer=int(totalSeconds)

        for subtopic in questionCount.keys():
            if any(subtopic in listSub for listSub in MATH_SUB_TOPICS.values()):
                if "Math" not in subjects:
                    subjects.append("Math")
            else:
                if "English" not in subjects:
                    subjects.append("English")

        settings={
            "subjects": subjects,
            "questionCount": questionCount,
            "difficulties": difficulties,
            "timer": timer
        }
        self.session=self.callback(settings) 

        return True
    
    def getCurrentQuestion(self):
        if self.session:
            return self.session.curQuestion()
        return None

    def nextQuestion(self):
        if self.session:
            self.session.nextQuestion()
            return self.session.curQuestion()
        return None

    def previousQuestion(self):
        if self.session:
            self.session.previousQuestion()
            return self.session.curQuestion()
        return None

    def submitAnswer(self, answer):
        if self.session:
            self.session.submitAnswer(answer)
            return {
                "inLast": self.session.inLastQuestion(),
                "isFinished": self.session.isFinished()
            }
        return None

    def getSessionTimer(self):
        if self.session:
            return self.session.timer
        return 0
        
    def getCurrentQuestion(self):
        if self.session:
            data=self.session.curQuestion() | {"is_first":self.session.inFirstQuestion(), "is_last":self.session.inLastQuestion()}
            print("--- DEBUG CURQUESTION SENT TO JS ---")
            print(data)
            print("------------------------------------")
            return data
        return None

    def debug(self, object):
        print(object)

    def updateQuestionTime(self, ms):
        self.session.updateQuestionTime(ms)

    def finalizeSession(self):
        score=self.session.finalizeSession()
        

        return {
            "status":"success",
            "score":score
        }


def startGUI(startSessionCallback):
    api=DashboardAPI(startSessionCallback)
    
    curDir=os.path.dirname(os.path.abspath(__file__))
    gui_dir=os.path.dirname(curDir)
    htmlFilePath=os.path.join(gui_dir, 'db_window.html')

    webview.create_window(
        title="SAT Practice Dashboard", 
        url=htmlFilePath,   
        js_api=api,      
        width=1200, 
        height=800
    )
    
    webview.start()