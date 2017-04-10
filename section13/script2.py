from tkinter import *

window=Tk()

def convert_to():
    t1_val=float(e0_val.get())*1000
    t1.insert(END,t1_val)
    t2_val=float(e0_val.get())*2.20462
    t2.insert(END,t2_val)
    t3_val=float(e0_val.get())*35.274
    t3.insert(END,t3_val)


l0=Label(window, text="Kilo Grams")
l0.grid(row=0,column=0)

e0_val=StringVar()
e0=Entry(window, textvariable=e0_val)
e0.grid(row=0, column=1)

b0=Button(window, text="Convert", command=convert_to)
b0.grid(row=0,column=2)

t1=Text(window, height=1,width=10)
t1.grid(row=1,column=0)
l1=Label(window,text="Grams")
l1.grid(row=1,column=1)

t2=Text(window, height=1,width=10)
t2.grid(row=1,column=2)
l2=Label(window,text="Pounds")
l2.grid(row=1,column=3)

t3=Text(window, height=1,width=10)
t3.grid(row=1, column=4)
l3=Label(window,text="Ounces")
l3.grid(row=1,column=5)

window.mainloop()
