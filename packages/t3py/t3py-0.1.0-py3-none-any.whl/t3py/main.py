# cli_tool.py

import click  # Or argparse if preferred

@click.command()
@click.argument('name')
def greet(name):
    """Simple CLI that greets the user."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    greet()
