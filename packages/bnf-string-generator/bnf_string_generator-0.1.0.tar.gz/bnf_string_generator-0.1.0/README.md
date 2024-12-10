# BNF String Generator

## Description

This is a tool for generating random strings from grammars defined in Backus-Naur Form (BNF). It operates by iteratively expanding non-terminal symbols into their corresponding production rules until only terminal symbols remain.

### Install from PyPI:

```bash
pip install bnf-string-generator
```

### Install from Source:

Clone the repository and install:

```bash
git clone https://github.com/yourusername/bnf-string-generator.git
cd bnf-string-generator
pip install .
```

## Usage

You can generate random strings by providing a BNF grammar. Here’s an example:

### Example:

```python
from bnf_string_generator import bnf_string_generator

bnf_grammar = """
<greeting> ::= <salutation> | <salutation> <intro> <EOL> <reply>
<reply> ::= <salutation>
<salutation> ::= "Hello" | "Hi" | "Hey" | "Greetings"
<intro> ::= ", I'm " <name>
<name> ::= "Alice" | "Bob" | "Charlie" | "Sam" | "Emma" | "John"
"""

random_string = bnf_string_generator(bnf_grammar)
print(random_string)
```

This will generate a random greeting like:

```
Hello, I'm Bob
```