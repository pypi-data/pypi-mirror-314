import os
import shutil
from pathlib import Path
import click

@click.group()
def main():
    """AI Castle CLI"""
    pass

def copy_if_not_exists(src: Path, dst: Path):
    """
    Copy files and directories from src to dst, skipping existing files.
    """
    if src.is_dir():
        # Ensure destination directory exists
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            copy_if_not_exists(item, dst / item.name)
    else:
        if not dst.exists():
            shutil.copy2(src, dst)


# `chat` 명령 그룹
@main.group(invoke_without_command=True)
@click.pass_context
def chat(ctx):
    """Commands related to AI Castle Chat"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(init)
        ctx.invoke(run)

# `chat init` 하위 명령
@chat.command()
def init():
    """Initialize the AI Castle Chat project."""
    source_folder = Path(__file__).parent / "package_data" / ".aicastle" / "chat"
    target_folder = Path.cwd() / ".aicastle" / "chat"  # 현재 작업 디렉터리의 .aicastle/chat

    if target_folder.exists():
        click.echo(f"Directory {target_folder} already exists! Only new files will be copied.")
    else:
        click.echo(f"Initializing AI Castle Chat at {target_folder}")

    copy_if_not_exists(source_folder, target_folder)
    click.echo(f"AI Castle Chat initialized at {target_folder}")

# `chat` 명령
@chat.command(name="run")
def run():
    """Run the AI Castle Chat application."""
    app_path = Path(__file__).parent / "chat" / "app.py"
    os.system(f"streamlit run {app_path}")

# `dev` 명령
@main.command()
def dev():
    """Copy devcontainer.json from package data."""
    source_file = Path(__file__).parent / "package_data" / ".devcontainer" / "devcontainer.json"
    target_file = Path.cwd() / ".devcontainer" / "devcontainer.json"

    if target_file.exists():
        click.echo(f"File {target_file} already exists!")
    else:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        click.echo(f"Copied devcontainer.json to {target_file}")