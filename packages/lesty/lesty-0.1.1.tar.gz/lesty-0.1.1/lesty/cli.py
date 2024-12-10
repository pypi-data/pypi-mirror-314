# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
# ]
# ///

import typer
import json
import importlib.util
from types import SimpleNamespace

app = typer.Typer()


def import_lambda_handler(handler_file_path: str):
    spec = importlib.util.spec_from_file_location(
        "lambda_handler_module", handler_file_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "lambda_handler"):
        raise ValueError(
            "The specified file does not contain a `lambda_handler` function."
        )
    return module.lambda_handler


@app.command()
def execute_lambda(handler_path: str, event_path: str):
    """
    Executes a Lambda handler with the given event JSON file.

    Args:
    handler_path: Path to the Python file containing the lambda_handler function.
    event_path: Path to the JSON file containing the event data.
    """
    try:
        # Import the lambda_handler function
        lambda_handler = import_lambda_handler(handler_path)

        # Read and parse the JSON event file
        with open(event_path, "r") as event_file:
            event = json.load(event_file)

        # Simulate a simple context object
        context = SimpleNamespace(function_name="mock_function", memory_limit_in_mb=128)

        # Execute the lambda_handler
        result = lambda_handler(event, context)
        typer.echo(f"Lambda Execution Result: {result}")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    app()

