import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self):

        self.todolist = checklist()     #link to checklist

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

        self.progress_bar['value']=50
        #SET IT TO MATCH WHATS IN THE CHECKLIST CLASS-----------

        self.progress_label = tk.Label(self.progress_frame, text="x% complete", font=('Arial', 15))
        self.progress_label.pack()


        # put textbox inside frame- so the tectbox can stick to the left hand side
        self.frame= tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, anchor="nw")  #top corner of the frame
        # grid inside the frame
        self.add_textbox = tk.Text(self.frame, height=1, width=40, font= ('Arial', 13))
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
        self.taskframe = tk.Frame(self.canvas, background="white")
        self.canvas.create_window((0, 0), window=self.taskframe, anchor="nw")
        self.taskframe.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")) )    #updating the scroll


        #button frame
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(padx=300, anchor="nw")
        #buttons
        self.del_btn = tk.Button(self.btn_frame, text= "Delete", font=("Arial", 13))
        self.del_btn.grid(row=0, column=0, padx=10)
        self.clear_btn = tk.Button(self.btn_frame, text= "Clear", font=("Arial", 13))
        self.clear_btn.grid(row=0, column=1, padx=10)

        self.root.mainloop()

    def add_task_gui(self):
        self.task_name = self.add_textbox.get("1.0", tk.END).strip()    #read what the user types
        if not self.task_name:      #if textbox is empty
            return
        #add to checklist logic
        self.todolist.add_task(self.task_name)
        #create the checkbox
        self.is_ticked = tk.BooleanVar(value=False)
        self.checkbox= tk.Checkbutton(self.taskframe, text=self.task_name, font=('Arial', 15), background="white", variable=self.is_ticked)
        self.checkbox.pack(anchor="w")

        #store the references
        self.todolist.tasks[-1]["is_ticked"] = self.is_ticked       #item goes to end of the list to refer to the just added task
        self.todolist.tasks[-1]["widget"] = self.checkbox

        #clear textbox once button pressed
        self.add_textbox.delete("1.0", tk.END)

class checklist:
    def __init__(self):
        self.tasks = [{"task_name": "task1", "status": False}, 
                      {"task_name": "task2", "status": False}, 
                      {"task_name":"task3", "status": False}]        #all tasks start as false
                      

    def add_task(self, task_name):
        self.tasks.append({"task_name": task_name, "status": False})      #ensure new tasks are also started as false

    def del_task(self, index):
        self.removed_task = self.tasks.pop(index)
        print("Deleted:", self.removed_task["task_name"])

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
        print(f"{self.progress}%")

GUI()

