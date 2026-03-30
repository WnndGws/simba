#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import time
from multiprocessing import Process, Queue
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import shared_variables
from utils import process_data, udp_processor, udp_receiver

### ------- ###
### Globals ###
### ------- ###
app = FastAPI()

src_path = Path(__file__).resolve().parents[1]
templates_dir = src_path / "templates"
shared_dir = src_path / "templates" / "shared"
static_dir = src_path / "templates" / "static"

templates = Jinja2Templates(directory=templates_dir.as_posix())
app.mount("/static", StaticFiles(directory=static_dir.as_posix()), name="static")
app.mount("/shared", StaticFiles(directory=shared_dir.as_posix()), name="shared")
router = APIRouter()

receiver_process = Process(
    target=udp_receiver.udp_receiver,
    daemon=False,
)
receiver_process.start()

# Queue for raw decoded data from udp_processor
raw_data_queue = Queue()
# Queue for tasks (prettify functions) from process_data
task_queue = Queue()

processor_thread = Process(
    target=udp_processor.process_named_shared_memory,
    args=(raw_data_queue,),
    daemon=False,
)
processor_thread.start()


### --------------- ###
### FastAPI Helpers ###
### --------------- ###
@app.on_event("shutdown")
def app_shutdown():
    global processor_thread, receiver_process, raw_data_queue, task_queue
    if processor_thread is not None:
        processor_thread.join(timeout=5)
        if processor_thread.is_alive():
            processor_thread.terminate()
            processor_thread.join()

    if receiver_process is not None:
        receiver_process.join(timeout=5)
        if receiver_process.is_alive():
            receiver_process.terminate()
            receiver_process.join()

    try:
        if raw_data_queue is not None:
            raw_data_queue.close()
            raw_data_queue.join_thread()
    except Exception as e:
        print("raw_data_queue cleanup error:", e)

    try:
        if task_queue is not None:
            task_queue.close()
            task_queue.join_thread()
    except Exception as e:
        print("task_queue cleanup error:", e)


### ------------------ ###
### Server Sent Events ###
### ------------------ ###
@app.get("/stream", response_class=EventSourceResponse)
async def stream_data():
    while True:
        ## This will block until data is available
        header, values = raw_data_queue.get()

        # Process the data (updates shared_variables and populates task_queue)
        process_data.process_data(header, values, shared_variables, task_queue)

        # Execute Prettification Tasks
        # Collect results from tasks placed in the queue by process_data
        prettified_results = []
        try:
            while not task_queue.empty():
                task_func = task_queue.get_nowait()
                if callable(task_func):
                    result = task_func()
                    if result is not None:
                        prettified_results.append(result)
        except Queue.Empty:
            pass

        if prettified_results:
            for item in prettified_results:
                if isinstance(item, list):
                    for sub_item in item:
                        if isinstance(sub_item, tuple) and len(sub_item) == 2:
                            key, value = sub_item
                            yield ServerSentEvent(event=key, data=value)
                elif isinstance(item, tuple) and len(item) == 2:
                    key, value = item
                    yield ServerSentEvent(event=key, data=value)


### --------- ###
### Endpoints ###
### --------- ###
@app.get("/test")
def index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
