import click
from yggdrasilpylint.linter.basic import Linter
from yggdrasilpylint.linter.violations import SetDuplicateItemChecker


@click.group()
def cli():
	"""
	Simple, high-quality, beautiful linter and analyzer for Python
	"""
	pass


@cli.command()
@click.argument('source_file')
def lint(source_file: str):
	linter = Linter()
	linter.checkers.add(SetDuplicateItemChecker(issue_code="W001"))

	linter.run(source_file)


if __name__ == '__main__':
	cli()
