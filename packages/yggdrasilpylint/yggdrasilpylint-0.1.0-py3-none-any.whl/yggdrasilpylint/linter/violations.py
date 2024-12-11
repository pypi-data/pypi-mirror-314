import ast
from dataclasses import dataclass


@dataclass
class Violation:
	node: ast.AST
	message: str
	level: str = "PLAIN"


class Checker(ast.NodeVisitor):
	def __init__(self, issue_code):
		self.issue_code = issue_code
		self.violations = []


class SetDuplicateItemChecker(Checker):
	def visit_Set(self, node):
		seen_values = set()

		for element in node.elts:
			if not isinstance(element, ast.Constant):
				continue

			value = element.value
			if value in seen_values:
				violation = Violation(
					node=element,
					message=f"Set contains duplicate item: {value!r}",
					level="UNIMPORTANT",
				)
				self.violations.append(violation)
			else:
				seen_values.add(element.value)
