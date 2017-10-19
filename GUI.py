import tkinter as tk
import pandas
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob.classifiers import *

class UI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Menu, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Welcome!!!", font = ("Verdana", 12))
        label.pack(pady=10, padx=10)

        btn1 = tk.Button(self, text="Start",
                         command=lambda: controller.show_frame(PageOne))
        btn1.pack(fill=tk.BOTH, expand=tk.YES)

        btn2 = tk.Button(self, text="Exit", command=controller.destroy)
        btn2.pack(fill=tk.BOTH, expand=tk.YES)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # configure column
        self.columnconfigure(1, weight=1)

        btn1 = tk.Button(self, text="Algorithm Performance",
                         command=lambda: controller.show_frame(PageTwo))
        btn1.pack(fill=tk.BOTH, expand=tk.YES)

        btn2 = tk.Button(self, text="Message Check",
                         command=lambda: controller.show_frame(PageThree))
        btn2.pack(fill=tk.BOTH, expand=tk.YES)

        backbutton = tk.Button(self, text="Back",
                               command=lambda: controller.show_frame(Menu))
        backbutton.pack(fill=tk.BOTH, expand=tk.YES)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Decision Tree Accuracy: " + str(a1))
        label1.pack()
        label2 = tk.Label(self, text="Naive Bayes Accuracy: " + str(a2))
        label2.pack()
        # performance check button
        graphbtn = tk.Button(self, text="Plot", command=self.plotgraph)
        graphbtn.pack()
        backbutton = tk.Button(self, text="Back",
                               command=lambda: controller.show_frame(PageOne))
        backbutton.pack()

    def plotgraph(self):
        model = ('Decision Tree', 'Naive Bayes')
        y_pos = np.arange(len(model))
        accuracy = [a1, a2]
        error = [1-a1, 1-a2]
        plt.bar(y_pos-0.2, accuracy, color='b', width=0.2, align='center')
        plt.bar(y_pos, error, color='r', width=0.2, align='center')
        plt.xticks(y_pos, model)
        plt.title('Accuracy Performance')
        plt.xlabel('Models')
        plt.ylabel('Accuracy')
        plt.show()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # configure row and column
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(3, pad = 7)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(5, pad = 7)

        # title label of the current window
        label = tk.Label(self, text = "Message check", font = ("Verdana", 12))
        label.grid(row = 0, column = 0, pady = 5, sticky = tk.W)

        # button return to the menu
        backbutton = tk.Button(self, text = "Back", command = lambda: controller.show_frame(PageOne))
        backbutton.grid(row = 0, column = 3, sticky = tk.E)

        # small title
        label2 = tk.Label(self, text = "Message:")
        label2.grid(row = 1, column = 0, sticky = tk.W)

        # message entry area
        area = tk.Text(self)
        area.grid(row = 2, column = 0, columnspan = 2, rowspan = 4,
                  padx=5,sticky = tk.E + tk.W + tk.S + tk.N)

        def msg_window():
            keywords = ["suicidal", "suicide", "kill myself", "my suicide note", "my suicide letter", "end my life",
                        "never wake up", "can't go on", "not worth living", "ready to jump", "sleep forever",
                        "want to die", "be dead", "better off without me", "better off dead", "suicide plan",
                        "suicide pact", "tired of living", "don't want to be here", "die alone",
                        "go to sleep forever"]
            vctr = TfidfVectorizer(ngram_range=(1,4))
            analyze = vctr.build_analyzer()(area.get('1.0', tk.END))
            i = 0
            found = False
            while i < len(analyze):
                if analyze[i] in keywords:
                    found = True
                    break
                i += 1
            if area.get('1.0', tk.END) == "\n":
                pop = tk.Toplevel(self)
                msglabel = tk.Label(pop, text="Nothing entered!!!")
                msglabel.pack(side="top", fill="both", expand=True, padx=20, pady=20)
                btn = tk.Button(pop, text="Close", command=lambda win=pop: win.destroy())
                btn.pack(side="bottom")
            elif found:
                pop = tk.Toplevel(self)
                msglabel = tk.Label(pop, text="Suicide related keyword(s) have been found within the message!!!")
                msglabel.pack(side="top", fill="both", expand=True, padx=20, pady=20)
                btn = tk.Button(pop, text="Close", command=lambda win=pop: win.destroy())
                btn.pack(side="bottom")
            else:
                pop = tk.Toplevel(self)
                msglabel = tk.Label(pop, text="Congratulation!!! The message doesn't contain any suicide related keywords!!!")
                msglabel.pack(side="top", fill="both", expand=True, padx=20, pady=20)
                btn = tk.Button(pop, text="Close", command=lambda win=pop: win.destroy())
                btn.pack(side="bottom")

        # message check button
        checkbtn = tk.Button(self, text = "Check", command = msg_window)
        checkbtn.grid(row=2, column=3, sticky=tk.E)

        tk.Label(self).grid(row=6)

def accuracy_calculate():
    dataset = pandas.read_csv("smallcomments.csv")
    keywords = ["suicidal", "suicide", "kill myself", "my suicide note", "my suicide letter", "end my life",
                "never wake up", "can't go on", "not worth living", "ready to jump", "sleep forever",
                "want to die", "be dead", "better off without me", "better off dead", "suicide plan",
                "suicide pact", "tired of living", "don't want to be here", "die alone", "go to sleep forever"]
    array = []
    for m in dataset.message:
        c = 0
        for k in keywords:
            if type(m) is not str:
                c = 2
            elif k in m:
                c = 1
        if c == 0:
            array.append((m, "neg"))
        elif c == 1:
            array.append((m, "pos"))
    split = int(0.8 * (len(array)))
    train = array[0:split]
    test = array[split:]
    cl1 = DecisionTreeClassifier(train)
    a1 = cl1.accuracy(test)
    cl2 = NaiveBayesClassifier(train)
    a2 = cl2.accuracy(test)
    return a1, a2


if __name__ == "__main__":
    a1, a2 = accuracy_calculate()
    # create window
    window = UI()
    # set the title and the size of root window
    window.title("User Interface")
    window.geometry("350x300")
    window.mainloop()