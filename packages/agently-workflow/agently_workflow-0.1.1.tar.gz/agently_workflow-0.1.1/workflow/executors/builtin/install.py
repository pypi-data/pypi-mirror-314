from workflow.executors.builtin.StartExecutor import start_executor
from workflow.executors.builtin.EndExecutor import end_executor
from workflow.executors.builtin.ConditionExecutor import condition_executor
from workflow.MainExecutor import MainExecutor
from workflow.lib.constants import EXECUTOR_TYPE_START, EXECUTOR_TYPE_END, EXECUTOR_TYPE_CONDITION

def mount_built_in_executors(main_executor: MainExecutor):
    """
    挂载内置的执行器
    """
    main_executor.regist_executor(EXECUTOR_TYPE_START, start_executor)
    main_executor.regist_executor(EXECUTOR_TYPE_END, end_executor)
    main_executor.regist_executor(EXECUTOR_TYPE_CONDITION, condition_executor)
