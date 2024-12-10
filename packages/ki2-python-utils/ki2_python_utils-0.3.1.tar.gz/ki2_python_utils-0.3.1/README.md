# ki2 - Python Utility Elements

## Installation

To install using pip:

```
pip install ki2-python-utils
```

Or, if you're using Poetry:

```
poetry add ki2-python-utils
```

## Usage

### Lists

#### `UniqueList`

A list that cannot contain duplicate elements.

```python
from ki2_python_utils import UniqueList

x = UniqueList()
x.append(1)
x.append(2)
x.append(1)
print(x)  # [1, 2]
```

`UniqueList` can be typed to enforce the type of its elements:

```python
x = UniqueList[int]()  # Restrict elements to type `int`
```

#### `CallbackList`

A list of callback functions that can be invoked all at once.

```python
from ki2_python_utils import CallbackList

def cb1():
    print("cb1")

def cb2():
    print("cb2")

x = CallbackList()
x.append(cb1)
x.append(cb2)
x()  # Prints "cb1" then "cb2"
```

Callbacks are called sequentially, and the order of addition matters:

```python
x = CallbackList()
x.append(cb2)
x.append(cb1)
x()  # Prints "cb2" then "cb1"
```

By default, the `CallbackList` type assumes callbacks take no parameters. However, you can specify the parameter types for the callbacks in the list.

Example with a single parameter:

```python
def cb1(x: int):
    print(f"cb1({x})")

def cb2(x: int):
    print(f"cb2({x})")

x = CallbackList[int]()
x.append(cb1)
x.append(cb2)
x(1)  # Prints "cb1(1)" then "cb2(1)"
```

Example with two parameters:

```python
def cb1(x: int, y: str):
    print(f"cb1({x}, {y})")

def cb2(x: int, y: str):
    print(f"cb2({x}, {y})")

x = CallbackList[int, str]()
x.append(cb1)
x.append(cb2)
x(1, "test")  # Prints "cb1(1, test)" then "cb2(1, test)"
```

If the same callback function is added multiple times, only the first occurrence is kept. Subsequent additions are ignored.

The `CallbackList` class is an alias for `UniqueCallbackList`, which uses `UniqueList` to store callbacks and ensures that the same callback cannot be added more than once. If you need a callback list that allows duplicates, you can use `MultipleCallbackList` instead.

The `UniqueCallbackList` (or `CallbackList`) and `MultipleCallbackList` classes work with synchronous functions. If you need to work with asynchronous functions, you can use `AsyncUniqueCallbackList` (or `AsyncCallbackList`) and `AsyncMultipleCallbackList` instead.

### JSON

The `Json` submodule provides utility functions for working with JSON data. It includes specific type definitions for JSON objects and functions to validate their types.

- **`Number` Type**: Represents a JSON number, as defined in JavaScript, which can be either an `int` or a `float`. The `is_number` validator checks if a value is a valid JSON number. Unlike Python's behavior, `is_number` returns `False` for boolean values.

- **`Json` Type**: Allows typing or casting a value as a JSON object. The `is_json` validator can be used to check whether a value is a valid JSON object.

This submodule helps ensure consistency when handling JSON data in Python, aligning behavior more closely with JSON standards.

### Exist

The `exist` submodule provides utilities to validate whether an optional object exists or not—specifically, whether it is `None`.

#### `exist`

The `exist` function takes an optional object as input and returns `True` if the object is not `None`, and `False` otherwise. This function supports type-checking and serves as a compact alternative to the test `x is not None`.

Example usage:

```python
from ki2_python_utils import exist

# Assume x is of type int | None

if exist(x):
    ...  # Here, x is of type int
else:
    ...  # Here, x is of type None
```

#### `count_exist`

Counts the number of elements in a list that are not `None`.

#### `count_none`

Counts the number of elements in a list that are `None`.

#### `exist_all`

Ensures that all elements in a list are not `None`. This function also supports type narrowing:

```python
from ki2_python_utils import exist_all

# Assume x is of type list[int | None]

if exist_all(x):
    ...  # Here, x is of type list[int]
else:
    ...  # Here, x is of type list[int | None]
```

If `exist_all` is called with an empty list, it returns `True`.

#### `exist_some`

Checks whether at least one element in a list is not `None`. If the function is called with an empty list, it also returns `True`.

### Filter

The `filter` submodule provides utilities for filtering elements in lists or dictionaries.

#### `filter_exist`

Removes `None` values from a list or keys with `None` values from dictionaries.

Example:

```python
from ki2_python_utils import filter_exist

x = [1, None, 2, None, 3]
y = filter_exist(x)  # y = [1, 2, 3]
```

```python
from ki2_python_utils import filter_exist

x = {"a": 1, "b": None, "c": 2}
y = filter_exist(x)  # y = {"a": 1, "c": 2}
```

#### `first_exist`

Returns the first non-`None` element from a list.

Example:

```python
from ki2_python_utils import first_exist

x = [None, None, 2, None, 3]
y = first_exist(x)  # y = 2
```

#### `last_exist`

Returns the last non-`None` element from a list.

Example:

```python
from ki2_python_utils import last_exist

x = [2, None, 3, None, None]
y = last_exist(x)  # y = 3
```

### Async Utils

The `async_utils` submodule offers utilities to simplify working with asynchronous functions.

#### `apply_parallel`

Executes an asynchronous function on a list of arguments in parallel using `asyncio.gather`.

**Example**:

```python
from ki2_python_utils import apply_parallel

async def add_one(x: int) -> int:
    return x + 1

x = [1, 2, 3]
y = await apply_parallel(add_one, x)  # y = [2, 3, 4]
```

#### `run_parallel`

Executes a list of coroutines concurrently using `asyncio.gather`. This function is ideal for running multiple asynchronous tasks that do not require arguments.

**Example**:

```python
from ki2_python_utils import run_parallel

async def func_1():
    print("func_1")

async def func_2():
    print("func_2")

await run_parallel(func_1, func_2)
```

### FlowBuffer

The `FlowBuffer` submodule provides a `FlowBuffer` class designed to manage a sliding window buffer where elements are continuously added.

#### `FlowBuffer`

The `FlowBuffer` class accepts an integer parameter `max_length`, which defines the maximum size of the buffer.

It offers the following methods:

- **`append(item)`**: Adds an element to the buffer. If the buffer is full, the oldest element is removed to make room for the new one.
- **`extend(items)`**: Adds multiple elements to the buffer. If the total number of elements exceeds the buffer's maximum size, only the most recent elements are retained.
- **`clear()`**: Empties the buffer.
- **`get(index)`**: Retrieves the element at the specified index in reverse order. Index 0 corresponds to the most recently added element, index 1 to the second most recent, and so on.
- **`get_raw(index)`**: Retrieves the element at the specified index in insertion order. Index 0 corresponds to the first element added, index 1 to the second element, and so forth.

It also provides the following properties:

- **`is_full`** (`bool`): Indicates whether the buffer is completely filled.
- **`last_item`**: Returns the most recently added element in the buffer.

#### `IndexedFlowBuffer`

Unlike `FlowBuffer`, which retrieves elements in reverse order, `IndexedFlowBuffer` assigns an incrementing index to each element as it is added. Elements are accessed using this index.

**Example**:

```python
from ki2_python_utils import IndexedFlowBuffer

buffer = IndexedFlowBuffer(max_length=3)
buffer.append(1)
buffer.append(2)
buffer.append(3)
print(buffer.get(0))  # Output: 1
print(buffer.get(1))  # Output: 2
print(buffer.get(2))  # Output: 3
buffer.append(4)
# buffer.get(0) is no longer accessible
print(buffer.get(1))  # Output: 2
print(buffer.get(2))  # Output: 3
print(buffer.get(3))  # Output: 4
```
