import ast
import os

from rich import print


def highlight_level(level: str):
	if level == 'UNIMPORTANT':
		return f'[cyan][{level}][/cyan]'
	elif level == 'PLAIN' or level == 'NOTE':
		return f'[blue][{level}][/blue]'
	elif level == 'ERROR':
		return f'[red][{level}][/red]'
	elif level == 'WARNING':
		return f'[yellow][{level}][/yellow]'
	else:
		return f'[magenta][{level}][/magenta]'


class Linter:
	def __init__(self):
		self.checkers = set()
		self._count = 0

	@staticmethod
	def print_violations(checker, file_name):
		print(f"Filename: {file_name}\tChecker: {checker.__class__.__name__}\n")
		counts = 0
		for violation in checker.violations:
			print(
				f"{file_name}:{violation.node.lineno}:{violation.node.col_offset}:\n\t"
				f"{highlight_level(violation.level)} [bold]{checker.issue_code}[/bold]: {violation.message}"
			)
			counts += 1
			print()

		return counts

	def run(self, source_path):
		file_name = os.path.basename(source_path)

		with open(source_path) as source_file:
			source_code = source_file.read()

		tree = ast.parse(source_code)

		for checker in self.checkers:
			checker.visit(tree)
			self._count += self.print_violations(checker, file_name)

		print(f'Total Violations: {self._count}')
