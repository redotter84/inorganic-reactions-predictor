import tkinter as tk
from tkinter import ttk

from compound import *
from reaction import *
import reacts

def preload():
    rs = reacts.reacts(["H2O"], True)
    for r in rs:
        pass

class App(tk.Frame):
    text = ("Arial", 13)
    form = ("Times New Roman", 14)
    entry = ('Helvetica')

    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=0)

        self.grid(sticky="nsew")
        self.interface()

    def interface(self):
        self.style = ttk.Style()
        self.style.configure("TButton", font=self.text)
        self.style.configure("TLabel", font=self.text)
        self.style.configure("Form.TLabel", font=self.form)

        self.l_comps = ttk.Label(self, text="Compounds", style="TLabel")
        self.l_comps.grid(row=0, column=0, columnspan=3, pady=10, sticky="s")

        self.t_comps = tk.Text(self, wrap="none", height=10, padx=5, pady=5,
          font=self.form)
        self.t_comps.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.sy_comps = ttk.Scrollbar(self, orient="vertical",
          command=self.t_comps.yview)
        self.t_comps["yscrollcommand"] = self.sy_comps.set
        self.sy_comps.grid(row=1, column=3, sticky="nsw")

        self.sx_comps = ttk.Scrollbar(self, orient="horizontal",
          command=self.t_comps.xview)
        self.t_comps["xscrollcommand"] = self.sx_comps.set
        self.sx_comps.grid(row=2, column=0, columnspan=3, sticky="nwe")

        self.b_submit = ttk.Button(self, text="Compute", style="TButton")
        self.b_submit.bind("<Button-1>", self.action)
        self.b_submit.grid(row=3, column=0, columnspan=3, pady=5, sticky="n")

        self.l_in = ttk.Label(self, text="As an input", style="TLabel")
        self.l_in.grid(row=4, column=0, pady=10, sticky="s")

        self.l_out = ttk.Label(self, text="As an output", style="TLabel")
        self.l_out.grid(row=4, column=2, pady=10, sticky="s")

        self.lb_in = tk.Listbox(self, font=self.form)
        self.lb_in.grid(row=5, column=0, sticky="nsew")
        self.lb_in.bind("<Double-Button-1>", self.lb_db_click)

        self.sy_in = ttk.Scrollbar(self, orient="vertical", command=self.lb_in.yview)
        self.lb_in["yscrollcommand"] = self.sy_in.set
        self.sy_in.grid(row=5, column=1, sticky="nsw")

        self.sx_in = ttk.Scrollbar(self, orient="horizontal", command=self.lb_in.xview)
        self.lb_in["xscrollcommand"] = self.sx_in.set
        self.sx_in.grid(row=6, column=0, sticky="nwe")

        self.lb_out = tk.Listbox(self, font=self.form)
        self.lb_out.grid(row=5, column=2, sticky="nsew")
        self.lb_out.bind("<Double-Button-1>", self.lb_db_click)

        self.sy_out = ttk.Scrollbar(self, orient="vertical", command=self.lb_out.yview)
        self.lb_out["yscrollcommand"] = self.sy_out.set
        self.sy_out.grid(row=5, column=3, sticky="nsw")

        self.sx_out = ttk.Scrollbar(self, orient="horizontal", command=self.lb_out.xview)
        self.lb_out["xscrollcommand"] = self.sx_out.set
        self.sx_out.grid(row=6, column=2, sticky="nwe")

        self.top = []

    def action(self, event):
        self.lb_in.delete(0, "end")
        self.lb_out.delete(0, "end")

        s = self.t_comps.get("1.0", "end")
        comps = s.split("\n")[0:-1]
        if len(comps) == 0 or comps[0] == "":
            return ""

        inp = reacts.reacts(comps, True)
        rs = set([])
        for r in inp:
            rs.add((r.value, r.cond))

        self.lb_in.reacts = []
        for r in rs:
            self.lb_in.insert(self.lb_in.size(), Reaction(r[0], r[1]))
            self.lb_in.reacts.append(r[0])

        outp = reacts.reacts(comps, False)
        rs = set([])
        for r in outp:
            rs.add((r.value, r.cond))

        self.lb_out.reacts = []
        for r in rs:
            self.lb_out.insert(self.lb_out.size(), Reaction(r[0], r[1]))
            self.lb_out.reacts.append(r[0])

    def lb_db_click(self, event):
        lb = event.widget
        sel = lb.curselection()[0]

        self.top.append(tk.Toplevel(self))
        tn = len(self.top) - 1
        self.top[tn].wm_title("Mass Calculating")

        self.top[tn].react = Reaction(lb.reacts[sel])
        comps = (self.top[tn].react.inp + self.top[tn].react.outp)
        self.top[tn].l_comps = []
        self.top[tn].e_mass = []
        self.top[tn].v_mass = []
        for i in range(len(comps)):
            self.top[tn].l_comps.append(ttk.Label(self.top[tn],
              style="Form.TLabel"))
            self.top[tn].l_comps[i]["text"] = repr(comps[i])
            self.top[tn].l_comps[i].grid(row=i, column=0, padx=(10, 20), pady=2,
              sticky="w")

            text = tk.StringVar()
            text.set("1 g")
            self.top[tn].v_mass.append(text)

            self.top[tn].e_mass.append(ttk.Entry(self.top[tn], font=self.entry,
              textvariable=self.top[tn].v_mass[i]))
            self.top[tn].e_mass[i].bind("<Return>",
                lambda ev, tn=tn, i=i: self.count_mass(tn, i, ev))
            self.top[tn].e_mass[i].grid(row=i, column=1)

        self.count_mass(tn, 0)

    def count_mass(self, tn, cn, event=0):
        comp = self.top[tn].l_comps[cn]["text"]
        for i in range(0, 10):
            comp = comp.replace(chr(0x2080 + i), f"{i}")
        comp = comp.replace("–", "-").replace("≡", "#")
        val = self.top[tn].v_mass[cn].get()
        react = self.top[tn].react
        _val = lambda val=val: val[0: -1] if val[-1] == 'g' else val
        mass = react.count_mass(comp, float(_val()))
        for i in range(len(mass)):
            self.top[tn].v_mass[i].set(repr(mass[i]) + " g")

if __name__ == "__main__":
    preload()

    root = tk.Tk()

    root.wm_state("zoomed")
    root.wm_title("Predicting the chemical properties of inorganic compounds")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.app = App(root)

    root.mainloop()
