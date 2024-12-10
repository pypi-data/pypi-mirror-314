# Lesty

A CLI tool to execute AWS Lambda handlers with a JSON event file.

## Installation

Install as a development dependency in your Python project:


```sh
poetry add --group=dev lesty
```

or 

```sh
uv add --dev lesty
```

## Usage
```sh
uv run lesty /path/to/lambda_handler.py /path/to/event.json
```
