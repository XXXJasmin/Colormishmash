#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import HORIZONTAL, Scale


class Application(tk.Tk):
    name = "ColorMishMash"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        self.bind("<Escape>", self.quit)

        self.lbl1 = tk.Label(self, text="ColorMishMash")
        self.lbl1.pack(anchor="w")
        self.btnQ = tk.Button(self, text="Quit", command=self.quit)
        self.btnQ.pack(anchor="e")

        self.frameR = tk.Frame(self)
        self.frameR.pack()
        self.frameG = tk.Frame(self)
        self.frameG.pack()
        self.frameB = tk.Frame(self)
        self.frameB.pack()

        self.VarR = tk.IntVar(self, 0, "varR")
        self.VarR.trace('w', self.setcolor)
        self.VarG = tk.IntVar(self, 0, "varG")
        self.VarG.trace('w', self.setcolor)
        self.VarB = tk.IntVar(self, 0, "varB")
        self.VarB.trace('w', self.setcolor)

        self.lblR = tk.Label(self.frameR, text="R", fg="#ff0000")
        self.lblR.pack(side="left", anchor="s")
        self.scaleR = Scale(
            self.frameR,
            from_=0,
            to=0xFF,
            orient="horizontal",
            length=333,
            variable=self.VarR,
        )
        self.scaleR.pack(side="left", anchor="s")
        self.entryR = tk.Entry(self.frameR, width=4, textvariable=self.VarR)
        self.entryR.pack(side="left", anchor="s")


        self.lblG = tk.Label(self.frameG, text="G", fg="#00ff00")
        self.lblG.pack(side="left", anchor="s")
        self.scaleG = Scale(
            self.frameG,
            from_=0,
            to=0xFF,
            orient="horizontal",
            length=333,
            variable=self.VarG,
        )
        self.scaleG.pack(side="left", anchor="s")
        self.entryG = tk.Entry(self.frameG, width=4, textvariable=self.VarG)
        self.entryG.pack(side="left", anchor="s")

        self.lblB = tk.Label(self.frameB, text="B", fg="#0000ff")
        self.lblB.pack(side="left", anchor="s")
        self.scaleB = Scale(
            self.frameB,
            from_=0,
            to=0xFF,
            orient="horizontal",
            length=333,
            variable=self.VarB,
        )
        self.scaleB.pack(side="left", anchor="s")
        self.entryB = tk.Entry(self.frameB, width=4, textvariable=self.VarB)
        self.entryB.pack(side="left", anchor="s")

        self.canvasMain=tk.Canvas(self, width=333, height=222, bg="#FFFFFF")
        self.canvasMain.pack()

        self.VarP=tk.StringVar()
        self.entryP = tk.Entry(self, width=8, textvariable=self.VarP, state='readonly')
        self.entryP.pack(anchor='e')

        self.entryR.bind('<Key>', self.callback)
        self.entryG.bind('<Key>', self.callback)
        self.entryB.bind('<Key>', self.callback)
        with open("colors.txt", "r") as f:
            bg = f.readline()
            self.frameMemory=tk.Frame(self)
            self.frameMemory.pack()
            self.listMemory=[]
            for row in range(3):
                for column in range(7):
                    bg = str(f.readline())[0:7]
                    canvas=tk.Canvas(self.frameMemory, width=50, height=50, bg= bg)
                    canvas.grid(row=row, column=column)
                    self.listMemory.append(canvas)
                    canvas.bind('<Button-1>', self.clickHandler)
            self.canvasMain.bind('<Button-1>', self.clickHandler)

    def clickHandler(self, event:tk.Event):
        if self.cget('cursor') !='pencil':
            self.config(cursor='pencil')
            self.copycolor = event.widget.cget("bg")
        else:
            self.config(cursor='')
            if event.widget is self.canvasMain:
                r = int(self.copycolor[1:3], 16)
                g = int(self.copycolor[3:5], 16)
                b = int(self.copycolor[5:], 16)
                self.VarR.set(r)
                self.varG.set(g)
                self.VarB.set(b)
            else:    
                event.widget.config(bg=self.copycolor)
    def save(self):
        with open("colors.txt", "w") as f:
            f.write(self.canvasMain.cget("bg")+"\n")
            for canvas in self.listMemory:
                f.write(canvas.cget("bg")+"\n")

    def callback(self, event:tk.Event):
        print(event.keycode, event.keysym, event.keysym_num, event.x, event.y)
        

    def setcolor(self, variable, index, mode):
        r=self.VarR.get()
        g=self.VarG.get()
        b=self.VarB.get()

        self.canvasMain.config(bg=f'#{r:02X}{g:02X}{b:02X}')

        self.entryP.delete(0, 'end')
        self.entryP.insert(0, f'#{r:02X}{g:02X}{b:02X}' )


    def quit(self, event=None):
        self.save()
        super().quit()


app = Application()
app.mainloop()


