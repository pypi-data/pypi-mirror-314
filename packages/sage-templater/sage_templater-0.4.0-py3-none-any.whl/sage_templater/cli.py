"""Console script for sage_templater."""

import click


@click.command()
def main() -> None:
    """Main entrypoint."""
    click.echo("sage-templater")
    click.echo("=" * len("sage-templater"))
    click.echo("App to parse templates and create them as a Sage import files.")


if __name__ == "__main__":
    main()  # pragma: no cover
