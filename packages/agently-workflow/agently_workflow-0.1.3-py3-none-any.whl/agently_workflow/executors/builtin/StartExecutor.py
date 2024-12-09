from agently_workflow.lib.Store import Store
from agently_workflow.lib.constants import WORKFLOW_START_DATA_HANDLE_NAME

def start_executor(inputs, store: Store, **sys_info):
    return sys_info['sys_store'].get(WORKFLOW_START_DATA_HANDLE_NAME)
