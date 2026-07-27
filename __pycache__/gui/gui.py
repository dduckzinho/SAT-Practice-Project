import tkinter as tk
from tkinter import ttk
from config import TOPICS, SUB_TOPICS



def startGUI():
    root=tk.Tk()
    root.title("Question Entry")
    
    root.geometry("800x500")

    label=tk.Label(root, text="Question ID")
    label.pack()

    qID=tk.Entry(root, width=40)
    qID.pack()

    subject = tk.StringVar(value="Math")


    def updateTopics():
        topicsDD["values"] = TOPICS[subject.get()]
        topicsDD.current(0)
        updateSubTopics()

    def updateSubTopics(event=None):
        subTopicsDD["values"] = SUB_TOPICS[topicsDD.get()]
        subTopicsDD.current(0)

    tk.Radiobutton(
        root,
        text="Math",
        variable=subject,
        value="Math",
        command=updateTopics
        ).pack()

    tk.Radiobutton(
        root,
        text="English",
        variable=subject,
        value="English",
        command=updateTopics
        ).pack()


    topicsDD = ttk.Combobox(root, state="readonly")
    topicsDD.pack(pady=10)

    topicsDD.bind(
        "<<ComboboxSelected>>",
        updateSubTopics
    )

    subTopicsDD = ttk.Combobox(root, state="readonly")
    subTopicsDD.pack(pady=10)

    updateTopics()

    root.mainloop()


if __name__ == "__main__":
    startGUI()
