import random
import re

def bnf_string_generator(bnf, symbol=None):
    """
    Generates a random string based on the provided BNF grammar, using an iterative approach.
    
    This function parses a Backus-Naur Form (BNF) grammar string and generates a random string by 
    iteratively expanding non-terminal symbols into their corresponding production rules, 
    until only terminal symbols remain. If no specific symbol is provided, the function 
    automatically uses the first defined non-terminal symbol as the starting point for string generation.
    
    Args:
        bnf (str): A string representation of the BNF grammar. Each production rule should be defined in the format: `<non-terminal> ::= <production1> | <production2> | ...`

        symbol (str, optional): A non-terminal symbol enclosed with angle brackets (e.g., `<greeting>`) to start generating the string from. If not provided, the function will automatically choose the first non-terminal defined in the grammar.

    Returns:
        str: A randomly generated string composed of terminal symbols.

    Raises:
        ValueError: If a non-terminal symbol is referenced but has no corresponding rule in the grammar, or if the grammar is improperly formatted.

    Example:
        Given the following BNF grammar:
        <greeting> ::= <salutation> | <salutation> <intro> <EOL> <reply>
        <reply> ::= <salutation>
        <salutation> ::= "Hello" | "Hi" | "Hey" | "Greetings"
        <intro> ::= ", I'm " <name>
        <name> ::= "Alice" | "Bob" | "Charlie" | "Sam" | "Emma" | "John"
        
        Calling `generate_random_string_from_bnf(bnf)` may return:
        'Hello' or 'Greetings, I'm Charlie\\nHello' depending on which production rule is randomly chosen for each non-terminal.

    Notes:
        - Literals are expected to be enclosed in quotes, either single or double. Non-terminals are enclosed 
          in angle brackets (`< >`).
        - May run a very long time if the input BNF includes too much recursion
    """
    
    def parse_bnf(bnf):
        """
        Parses a BNF (Backus-Naur Form) grammar string into a dictionary of production rules.
        
        Args:
            bnf (str): A string representation of the BNF grammar. Each rule should be in the format:
                       `<non-terminal> ::= <production1> | <production2> | ...`
        
        Returns:
            dict: A dictionary where each key is a non-terminal symbol and the value is a list of 
                  possible production options (strings).
        """
        grammar = {}
        lines = bnf.strip().splitlines()
        for line in lines:
            if "::=" in line:
                head, body = line.split("::=", 1)
                head = head.strip()
                options = [option.strip() for option in body.split("|")]
                grammar[head] = options
        return grammar
    
    # Parse the BNF grammar string
    rules = parse_bnf(bnf)
    
    if not symbol:
        # Automatically select the start symbol as the first non-terminal
        symbol = next(iter(rules))
    
    if symbol == "<EOL>":
        # Special case: return newline character for <EOL>
        return "\n"
    
    if symbol not in rules:
        # If the symbol is not in rules, check if it's a literal (surrounded by quotes)
        if (symbol.startswith("'") and symbol.endswith("'")) or (symbol.startswith('"') and symbol.endswith('"')):
            return symbol[1:-1]  # Remove the surrounding quotes
        else:
            raise ValueError(f"Missing definition for non-terminal: {symbol}")
    
    # Stack to hold the symbols to process
    stack = [symbol]
    result = []
    
    # Process the stack iteratively
    while stack:
        current_symbol = stack.pop()
        
        if current_symbol == "<EOL>":
            # Special case: end of line
            result.append("\n")
        elif (current_symbol.startswith("'") and current_symbol.endswith("'")) or (current_symbol.startswith('"') and current_symbol.endswith('"')):
            # Literal (terminal symbol)
            result.append(current_symbol[1:-1])  # Remove surrounding quotes
        elif current_symbol in rules:
            # Non-terminal, expand it
            production = random.choice(rules[current_symbol])
            # Add the symbols from the production to the stack in reverse order (to maintain the order of expansion)
            stack.extend(re.findall(r"<[^>]+>|'[^']*'|\"[^\"]*\"|[^<>\s]+", production)[::-1])
        else:
            raise ValueError(f"Missing definition for non-terminal: {current_symbol}")
    
    return ''.join(result)