# Programming Languages: Final Project

Name: Jaymie Ruddock
SMU id: 47428255
feature based grading:
 -- variables row, interprets column 
 -- can also parse functions but I could not figure out how it was handling AST

This note describes the final project for the Programming Languages class.

The project involves implementing a small yet relatively powerful programming
language. The language you implement will support functions, closures,
recursion, bound variables, conditional logic, and integer arithmetic.

The language is called Smurf (because it is small, and if languages had colors,
it would be blue).

# Submission Checklist

[ ] everything I'll need to build a running version of your submission (source,
    dependency loading, etc)

[ ] a build file that will create an executable (if required)

[ ] a script that will run the tests.

[ ] packaged into a PR that MUST INCLUDE your SMU ID and name.

(see [Deliverables](#deliverables) for more details)

## Your Task

At the end of this document you'll find an EBNF grammar for Smurf, followed by a
description of the required semantics.

Your job will be to implement a Smurf interpreter that passes a set of included
tests. Your implementation will possibly contain a lexer, and definitely contain
a parser and an interpreter.

Your interpreter will be invoked from the command line. It takes a single
parameter: the name of a file containing Smurf code. It will then compile and
run that code, displaying any output.

The underlying goal is to show me that you understand the workings  of a
language (both the parsing at compile time and the execution at runtime).

### Implementation Language and Tools

You can implement this project in the language of your choice. You may use
lexing and parsing tools available for that language. For example, if you were
implementing in Python, you might choose to use a PEG parser library such as
Arpeggio. If instead you choose to implement Smurf in C++, you might choose a
C++ PEG parser, or you could go old-school and use `flex` for lexing and `byacc`
for parsing and AST generation. (FWIW, using `byacc` and `flex` will probably
increase the level of effort by a factor of two.)

### Deliverables

You'll deliver your work as a PR. Your commit should include all source
files—both program source and (if you used them) lexical
definitions or grammars used by any code generation tools.

If the programming language you used requires compilation and/or linking, you
will need to include a script or makefile that does this. If your code has
external dependencies, then you must include a separate script that will install
these.

I'll be running your code under Ubuntu inside a Docker container. If you wanted
to do the same, you could also manage your dependencies by including a
Dockerfile.

Finally, I'll need you to include a script that runs the tests: see the next
section.

To summarize, you'll deliver:

* everything I'll need to build a running version of your submission (source,
  dependency loading, etc)

* a build file that will create an executable (if required)

* a script that will run the tests.

These will be packaged into a PR that MUST INCLUDE your SMU ID and name.

### Testing

You'll find a set of files in the `test_cases` directory. The files whose names
end `.smu` are Smurf source files. These contain code to be executed by your
interpreter. They also contain the expected output (as comments). For example,
the start of the file `00_expr.smu` is:

~~~
print(1)            #=> 1
print(3 - 1)        #=> 2
print(2+1)          #=> 3
~~~

When you run this code using your interpreter, it should produce the output:

~~~
Print: 1
Print: 2
Print: 3
~~~

Rather than eyeballing the output, you should run these tests using
the supplied Python script `test_runner.py`.

The test_runner script takes a single parameter: the command needed to run your
interpreter. The test runner will automatically then invoke your interpreter on
each of the test programs and verify the output. For example, if your
interpreter is written in Python, and it lives in the directory `smu/`, then you
can start the tests using:

~~~ shell
$ python3 test_runner.py "/usr/local/bin/python3 smu/interpreter.py"
~~~

## Smurf Syntax

~~~ bnf
program = code EOF

comment  = "#" r'.*'

code = statement*

statement = "let" variable_declaration
          | assignment
          | expr

variable_declaration  = decl ("," decl)*

decl = identifier ("=" expr)?

identifier = [a-z][a-zA-Z_0-9]*

variable_reference = identifier

if_expression = expr brace_block ( "else" brace_block )?

assignment  = identifier "=" expr

expr  = "fn" function_definition
      | "if" if_expression
      | boolean_expression
      | arithmetic_expression

boolean_expression  = arithmetic_expression relop arithmetic_expression

arithmetic_expression  = mult_term addop arithmetic_expression
                       | mult_term

mult_term  = primary mulop mult_term
           | primary

primary  = integer
         | function_call
         | variable_reference
         | "(" arithmetic_expression ")"


integer = "-"? [0-9]+

addop   = '+' | '-'
mulop   = '*' | '/'
relop   = '==' | '!=' | '>=' | '>' | '<=' | '<'


function_call  = variable_reference "(" call_arguments ")"
               | "print" "(" call_arguments ")"

call_arguments = (expr ("," expr)*)?

function_definition = param_list brace_block

param_list =  "(" identifier ("," identifier)* ")"
           |  "(" ")"

brace_block = "{" code  "}"
~~~

### Notes:

#### Syntax
* The syntax does not show whitespace. It assumes that the lexing stage uses
  whitespace to separate tokens where needed, but that the whitespace is then
  ignored.

* Comments run from the `#` character to the end of the current line. They
  should be treated as whitespace and be ignored.

* Every statement in Smurf is an expression: they all return a value.

#### Variables

* Variables must be declared (using `let`) before being used.

* A single `let` can declare multiple variables.

* Variables may also be initialized in a `let` statement. If not initialized,
  they should have the value 0.

* Variable initializers may be expressions, and those expressions may reference
  previous variables in the same let (as well as any other already-declared
  variables.

  ~~~
  let a = 1,
      b = 2,
      c = a + b
  ~~~

* the syntax contains entries for both `identifier` and `variable_reference`.
  Although identical lexically, the syntax uses `identifier` when referring the
  the `name` of a variable, and `variable_reference` when referring to its
  value.

* There are only two things a variable can hold: integers and functions.

#### Booleans and If Expressions

* The six relational operators (`relop`) compare two integers, returning the
  value `1` if the relation is true and `0` otherwise.

* The `if` expression executes its `then` clause if its condition is nonzero.
  Otherwise, if the condition is zero and an `else` clause is specified, that
  `else` clauses is executed.

* The value of the `if` expression is the value of either the `then` or `else`
  clause.

#### Blocks of code

* Multiple expressions (statements) can be grouped inside braces.

* The value returned by a block is the value of the last expression it
  evaluates.

  ~~~
  max = if a > b { a } else { b }
  ~~~

#### Functions

* Functions are created using the `fn` expression.

* The value of an `fn` is something that you can subsequently call.

  ~~~
  adder = fn (a,b) { a + b }
  print(adder(2,3))           #=> 5
  ~~~

* A function stored in a variable `v` is called using `v(p1, p2...)`.

* As a special case, your interpreter must act as if there is a predefined
  function stored in the variable `print`. This function can be called with
  one or more arguments, and will write those arguments to standard output,
  preceded by "Print: ". If multiple arguments are given, their values should be
  displayed separated by a pipe character (and no spaces).

  ~~~
  print(1)
  print(2*3, 4+5)
  ~~~

  will output

  ~~~
  Print: 1
  Print: 6|9
  ~~~


#### Scope and Binding

* Variables are declared with `let`, and are available from that point to
  the end of the scope that declares them.

* Variables are associated with a current value. The list of variables and their
  values in the current scope is called a binding.

* When a function is defined, Smurf remembers the scope.

* When the function is
  subsequently run, smurf creates a new scope for it. That scope includes the
  binding for the scope where the function was declared, bindings for any
  function parameters and any variables declared inside the function.

  Here's an example from the test cases:

  ~~~
  let a = 99
  let f = fn(x) { x + a }
  print(f(1))     #=> 100
  a = 100
  print(f(1))     #=> 101
  ~~~

  Note that the function receives the _scope_ at its point of definition. If the
  variables in that scope change value, the function will see that new value.

  here's another example illustrating the nested scope created in a function.

  ~~~
  let add_n = fn (n) {
    fn (x) {
      x + n
    }
  }
  let add_2 = add_n(2)
  let add_3 = add_n(3)
  print(add_2(2))       #=> 4
  print(add_3(10))      #=> 13
  ~~~

  Note that the nested function has a reference the the variable `n` from the
  enclosing function, and that the value of `n` is specific to that outer
  function's execution.

## Suggestions

* This is going to be a fairly good sized program. Nicely formatted, my Python
  solution is about 500 lines long. START EARLY.

* It might be tempting to start with the lexer, then implement the parser, ands
  finally do the interpreter. I suggest it would be more instructive to instead
  implement this across these layers. When I first started, I wrote a parser
  that just handled integers, built an AST, then interpreted that.

  By doing so, I learned the tools I would be using (Arpeggio in my case), and
  made a number of structural mistakes, which were easy to fix because there was
  no code.

  I then implemented variables, then expressions, and so on.

* When you first start, it will feel like you're beating your head against a
  brick wall. Your parsing tools will generate strange errors, and there'll be
  interactions between parts of the syntax you aren't expecting.

  The trick, as always, is to take things step at a time, and verify as you go
  along. The supplied test cases are not good for this, so consider writing
  lower level unit tests of your own.

* See if your parsing library has a _debug mode_, which will trace what it is
  doing when analyzing your Smurf source. I found that to be a big help when
  trying to understand why it was interpreting syntax X as syntax Y.

* Because Smurf has closures, you're going to need to be careful when invoking
  functions. One approach is to generate a _thunk- for every execution that
  contains the bindings and code specific to that execution. we'll talk about
  this in class.

  I found it useful to add code to my runtime that would dump out the current
  scope, and to call that in situations where variables weren't what I expected
  them to be.

* Remember to use me as a resource.

* START EARLY.


## Grading

Your final PR to my repository must be submitted by December 4 at 23:59. Late
submissions will not be graded.

This project will count for 40% of the overall course grade.

Within the project, marks are given as follows:


| | |
|-|-|
| **Passes Tests** ||
| Passes all my tests (the `.smu` files in `test_cases/` along with others I have here. | 80% |
| Passes some of the tests | 80% -2 for each failing|
| Passes no tests | 0% |
|**Well coded** ||
| The code is easy to understand.†            | 12% |
| Clear division between parsing and runtime  | 4% |
| Makes good use of features of parsing tool chosen | 4% |

(†) _Easy to understand_ means:

* well laid out (indentation, short lines, blank lines, etc)
* short methods/functions
* meaningful names
* complex code broken into smaller less complex chunks
* consistency
* and other _I'll know it when I don't understand it_ stuff
