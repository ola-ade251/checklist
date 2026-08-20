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
            if task["status"]:
                self.box = "[x]"
            else:
                self.box = "[ ]"
            print(f"{self.box} {task["task_name"]}")



my_list = checklist()
my_list.print_tasks()
print("-----------")
my_list.add_task("task4")
my_list.print_tasks()
print("-----------")
my_list.del_task(2)
my_list.print_tasks()
print("-----------")
my_list.toggle_task(0)
my_list.print_tasks()



