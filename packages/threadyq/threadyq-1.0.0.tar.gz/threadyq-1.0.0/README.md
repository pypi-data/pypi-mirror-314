# ThreadyQ
`ThreadyQ` is a Python library designed to simplify and extend the capabilities of threading and queue management. This package provides an abstraction layer over Python's built-in threading and queue modules, enabling developers to create, manage, and synchronize tasks efficiently in multi-threaded applications.

`ThreadyQ` is a simple Python utility that provides a thread-safe task queue managed by a background worker thread. It enables asynchronous execution of tasks with minimal setup.

## Features
- **Thread-safe task queue**
- **Asynchronous task execution**
- **Graceful shutdown and completion handling**
- **Colored console output for responses**

---

## Requirements

This utility works with:
- Python 3.6+

---

## Installation

Copy the `ThreadyQ` class code into your project or save it as `threadyq.py`. Import it wherever needed.

---

## Usage

### Importing ThreadyQ
```python
from threadyq import ThreadyQ
```

### Creating a Task Queue
```python
# Create an instance of ThreadyQ
tq = ThreadyQ()
```

### Adding Tasks
You can add tasks to the queue using the `put_the_task` method. Each task must be a callable function.

```python
# Define a sample task
def sample_task(arg1, arg2):
    print(f"Task executed with arguments: {arg1}, {arg2}")

# Add the task to the queue
tq.put_the_task(sample_task, "Hello", "World")
```

### Monitoring Tasks
You can get the number of pending tasks in the queue:
```python
print(f"Pending tasks: {tq.get_task_count()}")
```

### Waiting for All Tasks to Complete
To block the main thread until all tasks in the queue are completed:
```python
tq.join()
```

### Example
Here is a complete example:
```python
from threadyq import ThreadyQ

def sample_task(arg1, arg2):
    print(f"Task executed with arguments: {arg1}, {arg2}")

# Initialize ThreadyQ
tq = ThreadyQ()

# Add tasks to the queue
tq.put_the_task(sample_task, "Hello", "World")
tq.put_the_task(sample_task, "Foo", "Bar")

# Wait for all tasks to complete
tq.join()
```

### Output
```plaintext
Task sample_task added. Current task count: 1
Task sample_task added. Current task count: 2
Task executed with arguments: Hello, World
Task executed with arguments: Foo, Bar
All tasks completed.
```

---

## Customization
### Print Colored Messages
You can customize the output of `print_response` to provide color-coded messages for success or error logs.

### Worker Daemon Mode
By default, the worker thread runs as a daemon. You can change this behavior by passing `daemon=False` while initializing `ThreadyQ`:
```python
tq = ThreadyQ(daemon=False)
```

---

## Limitations
- The worker thread doesn’t have a direct shutdown mechanism in this version. To improve it, you can implement a stop signal as shown in enhanced versions.
- It’s best suited for lightweight task management. For large-scale or complex systems, consider frameworks like Celery.

---

## Contributing
Feel free to contribute to `ThreadyQ` by submitting pull requests or reporting issues.

---

## License
This utility is open-source and free to use. Licensed under the MIT License.

