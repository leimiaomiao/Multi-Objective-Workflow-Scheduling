from model.WorkFlow import WorkFlow

if __name__ == "__main__":
    workflow = WorkFlow()
    workflow.create(10)
    for task in workflow.task_list:
        print(task.pre_task_id_list, task.task_id, task.suc_task_id_list)
