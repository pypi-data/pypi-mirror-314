[![PyPI](https://img.shields.io/pypi/v/twist.svg)](https://pypi.python.org/pypi/twist/#history)

# 🌪️ Twist

Fast and reliable distributed systems in Python.

## Installation

```sh
pip install twist
```

## Example

This example runs the server and client in the same Python program using
subprocesses, but they could also be separate Python scripts running on
different machines.

```python
def server():
  import twist
  server = twist.Server(2222)
  server.bind('add', lambda x, y: x + y)
  server.bind('greet', lambda msg: print('Message from client:', msg))
  server.start()

def client():
  import twist
  client = twist.Client('localhost', 2222)
  future = client.add(12, 42)
  result = future.result()
  print(result)  # 54
  client.greet('Hello World')

if __name__ == '__main__':
  import twist
  server_proc = twist.Process(server, start=True)
  client_proc = twist.Process(client, start=True)
  client_proc.join()
  server_proc.kill()
  print('Done')
```
