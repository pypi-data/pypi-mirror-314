import queue
import threading
from typing import Callable, Any


def print_response(prefix: str, msg: str, color: str = "success"):
    """
    Prints a response message with colored output.

    :param prefix: The prefix for the message (e.g., 'success', 'error').
    :param msg: The message content.
    :param color: The message color ('success' for green, 'error' for red).
    """
    colors = {
        "success": '\033[92m',  # Green
        "error": '\033[91m',    # Red
    }
    color_code = colors.get(color)
    end_color = '\033[0m'
    print(f"{color_code}{prefix} : {msg}{end_color}")



class ThreadyQ:

    def __init__(self, deamon:bool = True):
        """Initialize the task queue and worker thread."""
        self.task_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=deamon)
        self.worker_thread.start()


    def _worker(self):
        """Worker function to process tasks from the queue."""
        while True:
            task, args = self.task_queue.get()  # Get the next task and its arguments
            if task is None:  # Exit signal
                break
            try:
                task(*args)  # Execute the task with unpacked arguments
            except Exception as e:
                print_response(prefix="error", msg = f"Error processing task: {e}",color="error")
            finally:
                self.task_queue.task_done()  # Mark the task as done


    def put_the_task(self, task: Callable, *args: Any):
        """
        Add a task to the queue with optional arguments.
        
        :param task: The task function to be executed.
        :param args: The arguments to pass to the task.
        """
        if not callable(task):
            raise ValueError("The task must be a callable function or method.")
        
        self.task_queue.put((task, args))  # Put the task and its args in the queue
        print(f"Task {task.__name__} added. Current task count: {self.get_task_count()}")


    def get_task_count(self) -> int:
        """
        Get the approximate number of tasks in the queue.
        
        :return: Number of tasks in the queue.
        """
        return self.task_queue.qsize()
    

    def join(self):
        """
        Wait for all tasks to complete 
        """
        self.task_queue.join()
        print_response(prefix="", msg="All tasks completed.", color="success")
