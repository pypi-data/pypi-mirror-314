import atexit
import os

import psutil

from .cli import nrp_command


def kill_process(process):
    if not process.is_running():
        return
    try:
        process.kill()
        try:
            process.wait(1)
        except psutil.TimeoutExpired:
            print(f"Can not kill process {process.pid} in time")
    except psutil.NoSuchProcess:
        pass
    except:
        print(f"Can not kill process {process.pid}, got an exception")


def kill_process_tree(process, except_process):
    try:
        sub_processes = process.children()
        for sub_process in sub_processes:
            kill_process_tree(sub_process, except_process)
        if process != except_process:
            kill_process(process)
    except:
        print(f"Can not kill process tree of {process.pid}, got an exception")


def exit_handler(*args, **kwargs):
    this_process = psutil.Process(os.getpid())
    kill_process_tree(this_process, except_process=this_process)


atexit.register(exit_handler)


if __name__ == "__main__":
    nrp_command()
