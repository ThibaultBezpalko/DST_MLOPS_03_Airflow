from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import BranchPythonOperator
import random


def decide_branch(kwargs):
    condition = kwargs['condition']
    print(f"Branch condition: {condition}")
    if condition:
        print("Task_A chosen")
        return 'task_A'
    else:
        print("Task_B chosen")
        return 'task_B'


# Création du DAG
with DAG(
    dag_id="branching_dag",
    schedule_interval=None,
    tags=['tutorial', 'datascientest'],
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, 1)
    }
) as my_dag:

    task_A = DummyOperator(task_id="task_A")

    task_B = DummyOperator(task_id="task_B")

    branch_decider = BranchPythonOperator(
        task_id='branching',
        python_callable=decide_branch,
        op_args=[{'condition':bool(random.getrandbits(1))}]
    )

    with TaskGroup("group_C") as group_C:
        task_C1 = DummyOperator(task_id="task_C1", trigger_rule="all_done")
        task_C2 = DummyOperator(task_id="task_C2", trigger_rule="all_done")
        task_C3 = DummyOperator(task_id="task_C3", trigger_rule="all_done")

    # Définition de l'ordre des tâches
    start_task = DummyOperator(task_id='start_task')
    end_task = DummyOperator(task_id='end_task', trigger_rule="all_done")

    start_task >> branch_decider
    branch_decider >> [task_A, task_B]
    [task_A, task_B] >> group_C >> end_task 
