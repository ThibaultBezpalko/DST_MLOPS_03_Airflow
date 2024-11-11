from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='sensor_dag',
    schedule_interval=None,
    tags=['tutorial', 'datascientest'],
    start_date=days_ago(0)
) as dag:

    my_sensor = FileSensor(
        task_id="check_file",
        fs_conn_id="my_filesystem_connection",
        filepath="/tmp/my_file.txt",
        poke_interval=15,
        timeout=4 * 15,
        mode='reschedule'
    )

    my_task = BashOperator(
        task_id="print_file_content",
        bash_command="cat /tmp/my_file.txt",
    )

    my_sensor >> my_task
