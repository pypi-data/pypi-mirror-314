import sys
from pathlib import Path
from typing import Optional

import click
import pyperclip

from .parser import parse_xml_string
from .apply import apply_file_changes, ChangeApplicationError
from .config import get_default_directory, set_default_directory, get_config


@click.group()
def cli() -> None:
    """XML file change application tool"""
    pass


@cli.command()
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="XML file to read changes from (defaults to clipboard)",
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Target project directory (defaults to configured directory)",
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Preview changes without applying them",
)
def apply(file: Optional[Path], directory: Optional[Path], dry_run: bool) -> None:
    """Apply XML-defined changes to a project directory"""
    try:
        # Get directory
        if not directory:
            directory = get_default_directory()
            if not directory.exists():
                raise click.ClickException(
                    f"Default directory {directory} does not exist."
                )

        # Get XML content
        if file:
            xml_content = file.read_text()
        else:
            xml_content = pyperclip.paste()
            if not xml_content.strip():
                raise click.ClickException("No content found in clipboard!")

        changes = parse_xml_string(xml_content)

        if not changes:
            raise click.ClickException("No valid file changes found in XML")

        # Preview or apply changes
        for change in changes:
            msg = f"{'Would apply' if dry_run else 'Applying'} {change.file_operation} to {change.file_path}..."
            click.echo(msg)
            if not dry_run:
                try:
                    apply_file_changes(change, directory)
                except ChangeApplicationError as e:
                    raise click.ClickException(str(e))

        if dry_run:
            click.echo("\nDry run completed. No changes were made.")
        else:
            click.echo("\nAll changes applied successfully!")

    except click.ClickException:
        raise
    except ValueError as e:
        raise click.ClickException(f"Error parsing XML: {str(e)}")
    except Exception as e:
        raise click.ClickException(f"Unexpected error: {str(e)}")


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
def set_dir(directory: Path) -> None:
    """Set the default project directory"""
    try:
        set_default_directory(directory)
        click.echo(f"Default directory set to: {directory}")
    except Exception as e:
        raise click.ClickException(f"Error setting default directory: {str(e)}")


@cli.command()
def show_config() -> None:
    """Show current configuration"""
    config = get_config()
    click.echo("\nCurrent Configuration:")
    click.echo(f"Default Directory: {config['default_directory']}")


def main():
    """Entry point for the CLI"""
    cli(prog_name="xmlapply")


if __name__ == "__main__":
    main()
