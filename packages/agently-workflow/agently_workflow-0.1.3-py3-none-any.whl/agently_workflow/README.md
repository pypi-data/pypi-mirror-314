A standalone workflow spun off from [Agently](https://github.com/Maplemx/Agently), featuring minimal third-party dependencies (e.g., json5).

The usage is consistent with the original **Agently** project(version 3.4.0.4). 

Simply change the import statement to `agently_workflow`:

```python
from agently_workflow import Workflow

workflow = Workflow()


@workflow.chunk()
def task_1(inputs, storage):
    return {"value": "1"}


@workflow.chunk()
def task_2(inputs, storage):
    return {"value": "2"}


@workflow.chunk()
def echo(inputs, storage):
    print("[Data Received]: ", str(inputs))
    return inputs


(
    workflow
    .connect_to(workflow.chunks["task_1"])
    .connect_to(workflow.chunks["echo"].handle("input_handle_a"))
)
(
    workflow
    .connect_to(workflow.chunks["task_2"])
    .connect_to(workflow.chunks["echo"].handle("input_handle_b"))
)
workflow.chunks["echo"].connect_to(workflow.chunks["END"])

result = workflow.start()
print(result)
```