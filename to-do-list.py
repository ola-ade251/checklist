import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self):

        self.todolist = checklist()     #link to checklist class

        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("checklist")

        self.label = tk.Label(self.root, text="To Do List", font =('Arial', 20))
        self.label.pack(padx=20, pady=20)


        #progress bar
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Thick.Vertical.TProgressbar", thickness= 50)       #bar width

        # proress bar frame
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.place(relx=0.75, rely=0.5, anchor="center")
        self.progress_frame.pack_propagate(True)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="vertical", length=150, mode="determinate", style="Thick.Vertical.TProgressbar")
        self.progress_bar.pack(pady=20)

        #self.progress_bar['value']=50
        #SET IT TO MATCH WHATS IN THE CHECKLIST CLASS-----------

        self.progress_label = tk.Label(self.progress_frame, text="0% complete", font=('Arial', 15))
        self.progress_label.pack()


        # put textbox inside frame- so the textbox can stick to the left hand side
        self.frame= tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, anchor="nw")  #top corner of the frame

        # grid inside the frame
        self.add_textbox = tk.Text(self.frame, height=1, width=40, font= ('Arial', 13))
        #self.add_textbox.bind("<KeyPress>", self.check)
        self.add_textbox.grid(row=0, column=0, sticky="w")

        # button also inside frame on the ride side of the textbox
        self.add_btn = tk.Button(self.frame, text= "Add Task", font=('Arial', 13), command =self.add_task_gui)
        self.add_btn.grid(row=0, column=1, sticky="w")


        # another frame for the canvas the checklists will be on
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(padx=20, pady=20, anchor="w")

        # create canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=230, background="white", highlightbackground="black", highlightthickness=1)
        self.canvas.pack(side="left", padx=10)

        # scrolling
        self.scroll = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll.pack(side="left", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        # task frame inside the canvas
        self.task_frame = tk.Frame(self.canvas, background="white")
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        #update scrolling
        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")) )    #updating the scroll


        #button frame
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(padx=300, anchor="nw")
        #buttons
        self.del_btn = tk.Button(self.btn_frame, text= "Delete", font=("Arial", 13), command=self.del_task_gui)
        self.del_btn.grid(row=0, column=0, padx=10)
        self.clear_btn = tk.Button(self.btn_frame, text= "Clear", font=("Arial", 13), command=self.clear_tasks_gui)
        self.clear_btn.grid(row=0, column=1, padx=10)


        # store task the user clicked
        self.selected_task_idx= None

        self.root.mainloop()


    def add_task_gui(self):
        self.task_name = self.add_textbox.get("1.0", tk.END).strip()    #read what the user types
        if not self.task_name:      #if textbox is empty
            return
        
        # add to the checklist logic
        self.todolist.add_task(self.task_name)

        # one frame per task
        self.task_row = tk.Frame(self.task_frame, background="white")
        self.task_row.pack(anchor="w")
        # click row to call selecting function, and update the index of the tasks
        self.task_row.bind("<Button-1>", lambda e, idx=len(self.todolist.tasks)-1:self.select_task(idx))
        #add checkbox
        self.is_ticked = tk.BooleanVar(value=False)
        self.checkbox= tk.Checkbutton(self.task_row, variable=self.is_ticked, background="white", command=lambda idx=len(self.todolist.tasks)-1: self.toggle_task_gui(idx))
        self.checkbox.pack(side="left")
        #add the label for the task
        self.task_label= tk.Label(self.task_row, text=self.task_name, font=('Arial', 14), background="white", wraplength=400, justify="left")
        self.task_label.pack(side="left")
        self.task_label.bind("<Button-1>", lambda e, idx=len(self.todolist.tasks)-1:self.select_task(idx))

        #store the references
        self.todolist.tasks[-1]["is_ticked"] = self.is_ticked       #item goes to end of the list to refer to the just added task
        self.todolist.tasks[-1]["row"] = self.task_row
        self.todolist.tasks[-1]["checkbox"] = self.checkbox
        self.todolist.tasks[-1]["label"] = self.task_label


        #clear textbox once button pressed
        self.add_textbox.delete("1.0", tk.END)
        #update the progress bar
        self.upgrade_progress()


    def select_task(self, index):
        #select/deselect
        if self.selected_task_idx == index:
            self.selected_task_idx= None
        else:
            self.selected_task_idx = index

        #highlight the selected task/row
        for i, task in enumerate(self.todolist.tasks):
            self.task_row = task.get("row")
            self.checkbox = task.get("checkbox")
            self.task_label = task.get("label")

            if self.selected_task_idx == i:
                self.task_row.config(background="light blue")
                self.checkbox.config(background="light blue")
                self.task_label.config(background="light blue")
            else:
                self.task_row.config(background="white")
                self.checkbox.config(background="white")
                self.task_label.config(background="white")


    def del_task_gui(self):
        if self.selected_task_idx is None:
            return
        
        self.idx = self.selected_task_idx


        #remove widgets
        self.task= self.todolist.tasks[self.idx]
        self.task["row"].destroy()

        #remove task from list
        self.todolist.del_task(self.idx)
        #reset the selection
        self.selected_task_idx = None

        #rebind for other tasks
        for i, task in enumerate(self.todolist.tasks):
            self.task_row = task["row"]
            self.task_label = task["label"]
            #take away old binds, and rebind with new indexes
            self.task_row.unbind("<Button-1>")
            self.task_label.unbind("<Button-1>")
            self.task_row.bind("<Button-1>", lambda e, idx=i: self.select_task(idx))
            self.task_label.bind("<Button-1>", lambda e, idx=i: self.select_task(idx))

        #update progress
        self.upgrade_progress()



    def clear_tasks_gui(self):
        #remove all rows
        for self.task in self.todolist.tasks:
            self.task["row"].destroy()
        self.todolist.clear_tasks()
        #reset
        self.selected_task_idx=None

        self.upgrade_progress()


    def toggle_task_gui(self, index):
        self.todolist.toggle_task(index)
        self.upgrade_progress()


    def upgrade_progress(self):
        self.percent = self.todolist.progress_bar()
        self.progress_bar['value'] = self.percent
        self.progress_label.config(text = f"{self.percent:.0f}% complete")


    #def check(self,event):
        #print(event.keysym)
        #print(event.state)

class checklist:
    def __init__(self):
        self.tasks = []        
                      

    def add_task(self, task_name):
        self.tasks.append({"task_name": task_name, "status": False})      #ensure new tasks are also started as false

    def del_task(self, index):
        self.removed_task = self.tasks.pop(index)
        print("Deleted:", self.removed_task["task_name"])

    def clear_tasks(self):
        self.tasks.clear()

    def toggle_task(self, index):      #ticking and unticking off tasks
        self.tasks[index]["status"] = not self.tasks[index]["status"]    #task you have selected to mark done, its status will change to the opposite

    def print_tasks(self):
        for task in self.tasks:
            if task["status"]==True:
                self.box = "[x]"
            else:
                self.box = "[ ]"
            print(f"{self.box} {task["task_name"]}")

    def progress_bar(self):
        if len(self.tasks) == 0:
            return 0
        
        self.done = 0
        self.total = len(self.tasks)
        for task in self.tasks:
            if task["status"] == True:
                self.done += 1
        self.progress = (self.done/self.total)*100
        return self.progress

GUI()

