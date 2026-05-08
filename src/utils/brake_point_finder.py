#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from multiprocessing import Process, Queue, shared_memory

from loguru import logger

from utils import udp_processor, udp_receiver, udp_simulator

if __name__ == "__main__":
    # receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver = Process(target=udp_simulator.udp_receiver, daemon=True)
    receiver.start()

    queue = Queue()
    udp_processor.process_named_shared_memory(
        output_queue=queue, decode_list=["lapdata"]
    )
