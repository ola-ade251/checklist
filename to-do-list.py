class checklist:
    def __init__(self):
        self.tasks = ["task1", "task2", "task3"]
        self.status = [False, False, False] #all tasks start as false

    def add_task(self, name):
        self.tasks.append(name)
        self.status.append(False)       #ensure new tasks are also started as false

    def del_task(self, index):
        self.removed_task = self.tasks.pop(index)
        self.status.pop(index)
        print("Deleted task: " + self.removed_task)

    def toggle_task(self, index):      #ticking and unticking off tasks
        self.status[index] = not self.status[index]    #task you have selected to mark done, its status will change to the opposite


my_list = checklist()
print(my_list.tasks)
my_list.add_task("task4")
print(my_list.tasks)
print(my_list.status)
my_list.del_task(2)
print(my_list.tasks)
print(my_list.status)
my_list.toggle_task(0)
print(my_list.status)
my_list.toggle_task(0)
print(my_list.status)


