import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///"
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DB"] = "test"

import asyncio
import pytest


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class FakeCache:
    def __init__(self):
        self._store: dict = {}

    async def get(self, key: str):
        return self._store.get(key)

    async def set(self, key: str, value, ttl=None):
        self._store[key] = value
        return True

    async def delete(self, *keys: str):
        deleted = 0
        for key in keys:
            if key in self._store:
                del self._store[key]
                deleted += 1
        return deleted

    async def delete_pattern(self, pattern: str):
        import fnmatch
        keys_to_delete = [k for k in self._store if fnmatch.fnmatch(k, pattern)]
        for key in keys_to_delete:
            del self._store[key]
        return len(keys_to_delete)


class FakeTaskQueue:
    def __init__(self):
        self.tasks: list = []
        self.results: dict = {}

    async def send_task(self, task_name: str, *args, **kwargs) -> str:
        import uuid
        task_id = str(uuid.uuid4())
        self.tasks.append({
            "id": task_id,
            "name": task_name,
            "args": args,
            "kwargs": kwargs,
        })
        return task_id

    async def get_result(self, task_id: str):
        return self.results.get(task_id)

    def set_result(self, task_id: str, result):
        self.results[task_id] = result


@pytest.fixture
def fake_cache():
    return FakeCache()


@pytest.fixture
def fake_task_queue():
    return FakeTaskQueue()
