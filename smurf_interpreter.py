from arpeggio.cleanpeg import ParserPEG
from arpeggio import ParserPython, visit_parse_tree
from arpeggio.export import PMDOTExporter, PTDOTExporter
import grammar as Grammar
import visitor as Visitor
from interpreter import Interpreter

debug=True

with open('01_variables.smu', 'r') as f:
    source = f.read()

parser = ParserPython(Grammar.program, Grammar.comment, debug=debug)

parse_tree = parser.parse("let a = 1, b = 5 print(b)")

tree = visit_parse_tree(parse_tree, Visitor.Visitor())

tree.accept(Interpreter())

