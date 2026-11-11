# Concurrent and Multi-Threaded Progress

When tasks run across multiple threads, processes, or asynchronous coroutines, coordinate progress bars safely through a single `rich.progress.Progress` instance.

## 1. Multi-Threaded Workers (`ThreadPoolExecutor`)

```python
import concurrent.futures
import time
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

def worker_task(progress: Progress, task_id: int, total_steps: int) -> str:
    for _ in range(total_steps):
        time.sleep(0.05)  # Simulate real work
        progress.advance(task_id, advance=1)
    return "done"

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    console=console,
) as progress:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i in range(4):
            task_id = progress.add_task(f"Worker {i+1}", total=20)
            futures.append(executor.submit(worker_task, progress, task_id, 20))
        
        # Wait for all workers to complete
        for future in concurrent.futures.as_completed(futures):
            _ = future.result()
```

## 2. Asyncio Workers

```python
import asyncio
from rich.progress import Progress

async def async_worker(progress: Progress, task_id: int, count: int):
    for _ in range(count):
        await asyncio.sleep(0.1)
        progress.advance(task_id)

async def main():
    with Progress(console=console) as progress:
        tasks = [
            async_worker(progress, progress.add_task(f"Stream {i}", total=15), 15)
            for i in range(3)
        ]
        await asyncio.gather(*tasks)

asyncio.run(main())
```

## 3. Important Rules
- **Never call `print()` inside workers**: Interleaved output will break the progress bar rendering lines. Use `progress.console.log()` or `progress.console.print()` if log output is required.
- **One `Progress` per console**: Do not create multiple active `Progress` context managers at the same time.
- **Update descriptions dynamically**: Use `progress.update(task_id, description="...")` to communicate changing sub-phases.
