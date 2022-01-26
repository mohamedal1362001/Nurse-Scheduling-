from tkinter import *
from tkinter import ttk
import _tkinter
from tkinter import messagebox
from populations import Populations

from Solution  import Solution
Nurse=0
populations=0
generations=0
Mutation=0
Select_random=0
Select_best=0

data=""
root=Tk()
root.title("Nurse Schedule")
root.minsize(800, 600)
root.resizable(True,True)


style=ttk.Style()
style.configure('TButton',foreground='black',font=('Arial',18,'bold'))
style.configure('TLabel',background="#073763",font=('Courier',20,'bold'),fg='#ffffff')
f1=ttk.Frame(root)
f1.grid()
f1.configure(relief='raised')#flat groove raised ridge solid   sunken
f1.config(padding=(0,0),borderwidth=10)
style.configure('TFrame',background="#000000")

lap1=ttk.Label(f1, text="Nurse",foreground="#ffffff")
lap1.grid(row=1,column=0,padx=5,pady=5)
entry1=ttk.Entry(f1,width=20,font=('Courier',12))
entry1.grid(row=2,column=0,padx=5,pady=5)

lap2=ttk.Label(f1, text="populations",foreground="#ffffff")
lap2.grid(row=3,column=0,padx=5,pady=5)
entry2=ttk.Entry(f1,width=20,font=('Courier',12))
entry2.grid(row=4,column=0,padx=5,pady=5)

lap3=ttk.Label(f1, text="generations",foreground="#ffffff")
lap3.grid(row=5,column=0,padx=5,pady=5)
entry3=ttk.Entry(f1,width=20,font=('Courier',12))
entry3.grid(row=6,column=0,padx=5,pady=5)
titlelable=ttk.Label(f1,text="NURSE\nSCHEDULING",foreground="#990000",background='black',font=('Roman',30,'bold'))
titlelable.grid(row=2,rowspan=2,column=1)
lap4=ttk.Label(f1, text="Mutation",foreground="#ffffff")
lap4.grid(row=1,column=2,padx=0,pady=5)
entry4=ttk.Entry(f1,width=20,font=('Courier',12))
entry4.grid(row=2,column=2,padx=0,pady=5)

lap5=ttk.Label(f1, text="Select random",foreground="#ffffff")
lap5.grid(row=3,column=2,padx=0,pady=5)
entry5=ttk.Entry(f1,width=20,font=('Courier',12))
entry5.grid(row=4,column=2,padx=0,pady=5)

lap6=ttk.Label(f1, text="Select best",foreground="#ffffff")
lap6.grid(row=5,column=2,padx=0,pady=5)
entry6=ttk.Entry(f1,width=20,font=('Courier',12))
entry6.grid(row=6,column=2,padx=0,pady=5)
text = Text(f1)
text.grid(row=0, column=0, padx=100, pady=0, columnspan=3)


def but1Click():
    try:
        text = Text(f1)
        text.grid(row=0, column=0, padx=100, pady=0, columnspan=3)
        Nurse = int(entry1.get())
        populations = int(entry2.get())
        generations = int(entry3.get())
        Mutation =int(entry4.get())
        Select_random = int(entry5.get())
        Select_best = int(entry6.get())
        p1 = Populations(Nurse, populations)
        s = Solution(p1, Nurse, 7, generations, Select_random, Select_best, Mutation)
        s.find_best_solution()
        data = s.displaytTable()
        print(data)
        s.save_data_in_file("tabel_for_week", data)
        text.insert(END, data)



    except:
     messagebox.showerror(title="ERROR",message="PLEASE INPUT FULL DATA")
but1=ttk.Button(f1,text="Print",command=but1Click)
but1.grid(row=13,column=1,padx=5,pady=10 )


root.mainloop()