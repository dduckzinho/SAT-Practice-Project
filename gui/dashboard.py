import customtkinter as ctk
from config import TOPICS, SUB_TOPICS
from gui.timer import Timer

import os

def startGUI():
    
    ctk.set_default_color_theme("SAT Question Log Project/gui/theme.json")

    root = ctk.CTk()
    root.title("SAT Practice")
    root.geometry("1200x800")
    
    outerTab = ctk.CTkTabview(root)
    outerTab.pack(fill="both", expand=True, padx=20, pady=20)

    
    outerTab.add("Custom Practice")
    outerTab.add("Full Test")

    
    cqTab = ctk.CTkTabview(outerTab.tab("Custom Practice"))
    cqTab.pack(fill="both", expand=True, padx=10, pady=10)

    customQuestionMode(cqTab)
    fullTestMode(outerTab.tab("Full Test"))

    root.mainloop()

def customQuestionMode(tabview):
    
    tabview.add("Filters")
    tabview.add("Settings")

    cqModeFilter = tabview.tab("Filters")
    cqModeSettings = tabview.tab("Settings")

    def updateTopicsFrame():
        if engSelected.get():
            engTopicsFrame.grid(row=0, column=0, padx=10, pady=10)
        else:
            engTopicsFrame.grid_remove()
            
        if mathSelected.get():
            mathTopicsFrame.grid(row=0, column=1, padx=10, pady=10)
        else:
            mathTopicsFrame.grid_remove()
    
    def updateSubtopicFrame():
        colIndex = 0
        for topic, isSelected in boolTopics.items():
            subFrame = topicFrameMap.get(topic)
            if subFrame:
                if isSelected.get():
                    subFrame.grid(row=0, column=colIndex, padx=10, pady=10, sticky="n")
                    colIndex += 1
                else:
                    subFrame.grid_remove()

    chooseSubject = ctk.CTkLabel(cqModeFilter, text="Choose Subject(s)", font=("Arial", 16, "bold"))
    chooseSubject.pack(pady=10)

    subjectFrame = ctk.CTkFrame(cqModeFilter, fg_color="transparent")
    subjectFrame.pack()

    outerTopicFrame = ctk.CTkFrame(cqModeFilter, fg_color="transparent")
    outerTopicFrame.pack()
    
    engTopicsFrame = ctk.CTkFrame(outerTopicFrame)
    mathTopicsFrame = ctk.CTkFrame(outerTopicFrame)

    engOuterSubTopicFrame = ctk.CTkFrame(cqModeFilter, fg_color="transparent")
    mathOuterSubTopicFrame = ctk.CTkFrame(cqModeFilter, fg_color="transparent")
    engOuterSubTopicFrame.pack(pady=10)
    mathOuterSubTopicFrame.pack(pady=10)

    info = ctk.CTkFrame(engOuterSubTopicFrame)
    structure = ctk.CTkFrame(engOuterSubTopicFrame)
    ideas = ctk.CTkFrame(engOuterSubTopicFrame)
    convention = ctk.CTkFrame(engOuterSubTopicFrame)

    alg = ctk.CTkFrame(mathOuterSubTopicFrame)
    adv = ctk.CTkFrame(mathOuterSubTopicFrame)
    data = ctk.CTkFrame(mathOuterSubTopicFrame)
    geo = ctk.CTkFrame(mathOuterSubTopicFrame)

    slidersFrame = ctk.CTkFrame(cqModeSettings, fg_color="transparent")
    ctk.CTkLabel(cqModeSettings, text="Select Amount of Questions", font=("Arial", 16, "bold")).pack(side="top", anchor="nw", padx=10, pady=10)
    slidersFrame.pack(fill="x", padx=20)
    
    topicFrameMap = {
        "Algebra": alg,
        "Advanced Math": adv,
        "Problem-Solving and Data Analysis": data,
        "Geometry & Trigonometry": geo,
        "Information and Ideas": info,
        "Craft and Structure": structure,
        "Expression of Ideas": ideas,
        "Standard English Conventions": convention
    }

    mathSelected = ctk.BooleanVar()
    engSelected = ctk.BooleanVar()

    ctk.CTkCheckBox(subjectFrame, text="English", variable=engSelected, command=updateTopicsFrame).pack(side="left", padx=10)
    ctk.CTkCheckBox(subjectFrame, text="Math", variable=mathSelected, command=updateTopicsFrame).pack(side="left", padx=10)

    boolTopics = {}
    for subject in TOPICS:
        frame = engTopicsFrame if subject == "English" else mathTopicsFrame
        ctk.CTkLabel(frame, text=f"{subject} Topics", font=("Arial", 14, "bold")).pack(side="top", anchor="nw", padx=10, pady=10)
        for topic in TOPICS[subject]:
            topicSelected = ctk.BooleanVar()
            ctk.CTkCheckBox(
                frame,
                text=topic,
                variable=topicSelected,
                command=updateSubtopicFrame
            ).pack(side="top", anchor="nw", padx=10, pady=5)
            boolTopics[topic] = topicSelected

    def updateSliders():
        for subtopic, isSelected in boolSubTopics.items():
            if isSelected.get():
                qAmtSliders[subtopic].pack(side="top", fill="x", padx=20, pady=10)
            else:
                qAmtSliders[subtopic].pack_forget()

    boolSubTopics = {}
    qAmtSliders = {}

    for topic in SUB_TOPICS:
        match topic:
            case "Algebra": subFrame = alg
            case "Advanced Math": subFrame = adv
            case "Problem-Solving and Data Analysis": subFrame = data
            case "Geometry & Trigonometry": subFrame = geo
            case "Information and Ideas": subFrame = info
            case "Craft and Structure": subFrame = structure
            case "Expression of Ideas": subFrame = ideas
            case "Standard English Conventions": subFrame = convention
            case _: subFrame = None

        if subFrame:
            ctk.CTkLabel(subFrame, text=f"{topic} Subtopics", font=("Arial", 12, "bold")).pack(side="top", anchor="nw", padx=10, pady=10)
            for subtopic in SUB_TOPICS[topic]:
                subTopicSelected = ctk.BooleanVar()
                ctk.CTkCheckBox(
                    subFrame,
                    text=subtopic,
                    variable=subTopicSelected,
                    command=updateSliders
                ).pack(side="top", anchor="nw", padx=10, pady=5)
                boolSubTopics[subtopic] = subTopicSelected


                sliderContainer = ctk.CTkFrame(slidersFrame, fg_color="transparent")
                ctk.CTkLabel(sliderContainer, text=subtopic).pack(side="left", padx=10)
                
                qAmtSlider = ctk.CTkSlider(
                    sliderContainer,
                    from_=1,
                    to=50,
                    number_of_steps=49,
                    width=250
                )
                qAmtSlider.pack(side="right", padx=10)
                qAmtSlider.set(10)
                
                qAmtSliders[subtopic] = sliderContainer

def fullTestMode(root):
    pass