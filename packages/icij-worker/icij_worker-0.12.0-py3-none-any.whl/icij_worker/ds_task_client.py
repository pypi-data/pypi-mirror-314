import uuid
from typing import Any, Dict, Optional

from icij_common.pydantic_utils import jsonable_encoder
from icij_worker import Task, TaskState
from icij_worker.exceptions import UnknownTask
from icij_worker.utils.http import AiohttpClient

# TODO: we shouldn't have DS dependent class in here, move this util in its own repo

# TODO: maxRetries is not supported by java, it's automatically set to 3
_TASK_UNSUPPORTED = {"max_retries"}


class DatashareTaskClient(AiohttpClient):
    def __init__(self, datashare_url: str):
        super().__init__(datashare_url)

    async def create_task(
        self,
        name: str,
        args: Dict[str, Any],
        *,
        id_: Optional[str] = None,
        group: Optional[str] = None,
    ) -> str:
        if id_ is None:
            id_ = _generate_task_id(name)
        task = Task.create(task_id=id_, task_name=name, args=args)
        task = jsonable_encoder(task, exclude=_TASK_UNSUPPORTED, exclude_unset=True)
        task.pop("createdAt")
        url = f"/api/task/{id_}"
        if group is not None:
            if not isinstance(group, str):
                raise TypeError(f"expected group to be a string found {group}")
            url += f"?group={group}"
        async with self._put(url, json=task) as res:
            task_res = await res.json()
        return task_res["taskId"]

    async def get_task(self, id_: str) -> Task:
        url = f"/api/task/{id_}"
        async with self._get(url) as res:
            task = await res.json()
        if task is None:
            raise UnknownTask(id_)
        # TODO: align Java on Python here... it's not a good idea to store results
        #  inside tasks since result can be quite large and we may want to get the task
        #  metadata without having to deal with the large task results...
        task = _ds_to_icij_worker_task(task)
        task = Task(**task)
        return task

    async def get_tasks(self) -> list[Task]:
        url = "/api/task/all"
        async with self._get(url) as res:
            tasks = await res.json()
        # TODO: align Java on Python here... it's not a good idea to store results
        #  inside tasks since result can be quite large and we may want to get the task
        #  metadata without having to deal with the large task results...
        tasks = (_ds_to_icij_worker_task(t) for t in tasks)
        tasks = [Task(**task) for task in tasks]
        return tasks

    async def get_task_state(self, id_: str) -> TaskState:
        return (await self.get_task(id_)).state

    async def get_task_result(self, id_: str) -> Any:
        # TODO: we probably want to use /api/task/:id/results instead but it's
        #  restricted, we might need an API key or some auth
        url = f"/api/task/{id_}"
        async with self._get(url) as res:
            task = await res.json()
        if task is None:
            raise UnknownTask(id_)
        if "result" not in task:
            msg = (
                f"task {id_} doesn't have a result yet, "
                f"it's probably not {TaskState.DONE}"
            )
            raise ValueError(msg)
        task_res = task["result"]
        return task_res

    async def delete(self, id_: str):
        url = f"/api/task/{id_}"
        async with self._delete(url):
            pass

    async def delete_all_tasks(self):
        for t in await self.get_tasks():
            await self.delete(t.id)


def _generate_task_id(task_name: str) -> str:
    return f"{task_name}-{uuid.uuid4()}"


_JAVA_TASK_ATTRIBUTES = ["result", "error"]


def _ds_to_icij_worker_task(task: dict) -> dict:
    for k in _JAVA_TASK_ATTRIBUTES:
        task.pop(k, None)
    return task
