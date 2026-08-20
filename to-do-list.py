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


my_list = checklist()
print(my_list.tasks)
my_list.add_task("task4")
print(my_list.tasks)
my_list.del_task(2)
print(my_list.tasks)
my_list.toggle_task(0)
print(my_list.tasks)



