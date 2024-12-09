from agently_workflow.executors.builtin.StartExecutor import start_executor
from agently_workflow.executors.builtin.EndExecutor import end_executor
from agently_workflow.executors.builtin.ConditionExecutor import condition_executor
from agently_workflow.MainExecutor import MainExecutor
from agently_workflow.lib.constants import EXECUTOR_TYPE_START, EXECUTOR_TYPE_END, EXECUTOR_TYPE_CONDITION

def mount_built_in_executors(main_executor: MainExecutor):
    """
    挂载内置的执行器
    """
    main_executor.regist_executor(EXECUTOR_TYPE_START, start_executor)
    main_executor.regist_executor(EXECUTOR_TYPE_END, end_executor)
    main_executor.regist_executor(EXECUTOR_TYPE_CONDITION, condition_executor)
