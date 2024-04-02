import os
import sys
import platform
from enum import Enum
from typing import NamedTuple
import color


def to_string(string:str) -> str:
    if not '"' in string:
        return f'"{string}"'
    elif not "'" in string:
        return f"'{string}'"
    else:
        return f'"""{string}"""'

class TokenType(Enum):
    keyword = 1
    varname = 2
    varvalue = 3
    string = 4
    semi = 5
    _if = 6
    _else = 7
    _while = 9
    _for = 10
    start = 15
    end = 16
    vardef = 17
    func = 18
    assignment = 19
    relational = 20
    arithethic = 21
    _range = 22
    number = 23
    colon = 24
    unknow = 25
    exit = 26
    



class Token(NamedTuple):
    tokentype: TokenType
    value: str | tuple = None
    line: int = None
    column: int = None


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens:list[Token] = tokens
    
    
    def parse(self):
        self.python_code:str = ""
        indent:int = 0
        self.__index:int = 0
        last_line:int = 0
        last_token:Token = None
        
        while self.__get_token():
            
            token = self.__get_token()
            if token == last_token:
                self.__consume()
                continue
            last_token = token
            
            if self.__get_token().line != last_line:
                
                last_line = self.__get_token().line
                self.python_code += "\n"
            
                self.python_code += " " * (4*indent)
            
            if self.__get_token().tokentype == TokenType.start:
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType.end:
                indent -= 1
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType._if:
                self.python_code += "if "
                self.__consume()
                
                while self.__get_token() and self.__get_token().tokentype != TokenType.colon:
                    self.python_code += self.__get_token().value
                    self.__consume()
                
                self.python_code += ":\n"
                indent += 1
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType._else:
                self.python_code += "else"
                indent += 1
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType._while:
                
                self.python_code += "while "
                self.__consume()
                
                while self.__get_token() and self.__get_token().tokentype != TokenType.colon:
                    self.python_code += self.__get_token().value
                    self.__consume()
                
                self.python_code += ":\n"
                indent += 1
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType._for:
                self.python_code += "for "
                indent += 1
                self.__consume()
            
            
            elif self.__get_token().tokentype == TokenType.exit:
                self.__consume()
                if self.__get_token():
                    self.python_code += f"exit({self.__consume().value or ''})"
                else:
                    self.python_code += f"exit()"

            
            elif self.__get_token().tokentype == TokenType.func:
                self.python_code += "def "
                self.__consume()
                self.python_code += f"{self.__consume().value}("
    

                
                if self.__get_token() and self.__get_token().value == ":":
                    self.__consume()
                    
                if self.__get_token() and self.__get_token().tokentype == TokenType.vardef:
                    self.__consume()
                    if self.__get_token() and self.__get_token().tokentype == TokenType.colon:
                        self.__consume()

                    
                args = []
                while self.__get_token() and not self.__get_token().value.lower() == "finvariables":
                    args.append(self.__consume().value)
                self.__consume()
                
                self.python_code += ','.join(args)
                    
                self.python_code += "):"
                    
                if self.__get_token() and self.__get_token().value.lower() == "algo":
                    self.__consume()
                    self.__consume()
                    indent += 1


            
            
            elif self.__get_token().tokentype == TokenType.keyword:
                if self.__get_token().value == "afficher":
                    printline = self.__get_token().line
                    self.python_code += "print("
                    self.__consume()
                    
                    to_print = []
                    
                    while self.__get_token() and self.__get_token().line == printline:
                        to_print.append(self.__consume().value)
                    
                    self.python_code += ", ".join(to_print)
                        
                    
                    self.python_code += ")"
                
                elif self.__get_token().value == "lire":
                    self.__consume()
                    self.python_code += f"{self.__consume().value} = input()"
                
                elif self.__get_token().value.lower() == "entier":
                    self.__consume()
                    
                    self.python_code += f"int({self.__consume().value})"     
                    
                elif self.__get_token().value.lower() == "executer":
                    self.__consume()
                    
                    funcname = self.__consume().value or ""
                    self.python_code += f"{funcname}("
                    
                    line = self.__get_token(-1).line
                    while self.__get_token() and self.__get_token().line == line:
                        self.python_code += self.__consume().value
                        
                    self.python_code += ")"         

                elif self.__get_token().value.lower() == "dans":
                    self.python_code += " in "
                    self.__consume()
                
                elif self.__get_token().value.lower() == "retourner":
                    self.python_code += "return "
                    self.__consume()
                    
            elif self.__get_token().tokentype == TokenType.varname:
                if self.__get_token(1) and self.__get_token(1).tokentype == TokenType.assignment:
                    self.python_code += self.__consume().value + " = " + " "
                    self.__consume()
                
                else:
                    self.python_code += self.__consume().value
                    self.python_code += " "

            elif self.__get_token().tokentype == TokenType.number:
                self.python_code += self.__get_token().value
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType.string:
                self.python_code += self.__get_token().value
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType.arithethic:
                self.python_code += self.__get_token().value
                self.__consume()
            
            elif self.__get_token().tokentype == TokenType.relational:
                self.python_code += self.__get_token().value
                self.__consume()
                
            elif self.__get_token().tokentype == TokenType._range:
                self.python_code += f" in range({self.__get_token().value[0]}, {self.__get_token().value[1]})"
                self.__consume()
                
            elif self.__get_token().tokentype == TokenType.colon:
                
                self.python_code += self.__consume().value
            
            else:
                self.python_code += self.__consume().value
                continue
                print(f"{color.red}Error: Unexpected token {self.__consume().value} at line {self.__get_token().line} column {self.__get_token().column}{color.reset}")
                
            
        return self.python_code
                
    
    def __get_token(self, offset: int = 0) -> Token | None:
        if self.__index + offset <= (len(self.tokens) - 1):
            return self.tokens[self.__index + offset]
        return None
    
    def __consume(self) -> Token | None:
        if self.__index <= (len(self.tokens) - 1):
            toretrun = self.tokens[self.__index]
            self.__index += 1
            return toretrun
        return None
        
        


class TokenisationError(Exception):
    ...


def to_python(algo: str) -> str:
    ...

    
    

class Tokenizer:
    def __init__(self, code: str) -> None:
        self.code = code
        self.__char = 0
    
    
    def Tokenize(self) -> list:
        buffer:str = ""
        tokens: list = []
        self.line:int = 1
        self.column: int = 1
        
        while (self.__get_char()):
            if self.__get_char().isalpha():
                buffer = self.__consume()
                while (self.__get_char() and (self.__get_char().isalnum() or self.__is_spaced_keword(buffer + self.__get_char()))):
                    buffer += self.__consume()
                
                if buffer.lower() in ["début", "debut"]:
                    tokens.append(
                        Token(TokenType.start, buffer, self.line, self.column))
                
                elif buffer.lower() == "fin":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))
                
                elif buffer.lower() == "tant que":
                    tokens.append(Token(TokenType._while, buffer, self.line, self.column))
                
                elif buffer.lower() == "fintantque":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))

                elif buffer.lower() == "si":
                    tokens.append(Token(TokenType._if, buffer, self.line, self.column))
                    
                elif buffer.lower() == "finsi":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))
                    
                elif buffer.lower() == "sinon":
                    tokens.append(Token(TokenType._else, buffer, self.line, self.column))
                
                elif buffer.lower() == "finsinon":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))
                
                elif buffer.lower() == "afficher":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                    
                elif buffer.lower() == "lire":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                
                elif buffer.lower() == "entier":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                
                elif buffer.lower() == "pour":
                    tokens.append(Token(TokenType._for, buffer, self.line, self.column))
                
                elif buffer.lower() == "finpour":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))
                
                elif buffer.lower() == "quitter":
                    tokens.append(Token(TokenType.exit, buffer, self.line, self.column))
                
                elif buffer.lower() == "fonction":
                    tokens.append(Token(TokenType.func, buffer, self.line, self.column))
                
                elif buffer.lower() == "variables":
                    tokens.append(Token(TokenType.vardef, buffer, self.line, self.column))
                
                elif buffer.lower() == "finvariables":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))
                
                elif buffer.lower() == "algo":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                
                elif buffer.lower() == "finalgo":
                    tokens.append(Token(TokenType.end, buffer, self.line, self.column))
                
                elif buffer.lower() == "executer":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                
                elif buffer.lower() == "dans":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                
                elif buffer.lower() == "retourner":
                    tokens.append(Token(TokenType.keyword, buffer, self.line, self.column))
                    
                elif buffer.lower() == "utiliser":
                    modules = ""
                    while self.__get_char() and self.__get_char() != "\n":
                        modules += self.__consume() or ""
                    
                    modules = modules.split(" ")
                    for module in modules:
                        if os.path.exists(module+".algo"):
                            with open(module+".algo", "r", encoding="utf-8") as file:
                                content = file.read()
                            
                            tokenizer = Tokenizer(content)
                            
                            tokens.extend(tokenizer.Tokenize())
                    
                
                elif buffer.lower() == "de":
                    
                    while self.__get_char() and self.__get_char() == " ":
                        self.__consume()
                    
                    start:str = ""
                    while (self.__get_char() and self.__get_char()not in [" ", "\n", ":"]):
                        start += self.__consume()
                    
                    while self.__get_char() and self.__get_char() == " ":
                        self.__consume()
                        
                    if self.__get_char().lower() in ["a", "à"]:
                        self.__consume()
                    
                    while self.__get_char() and self.__get_char() == " ":
                        self.__consume()
                    
                    end:str = ""
                    while (self.__get_char() and self.__get_char()not in [" ", "\n", ":"]):
                        end += self.__consume()
                    
                    tokens.append(Token(TokenType._range, (start, end), self.line, self.column))
                    
                
                else:
                    tokens.append(Token(TokenType.varname, buffer, self.line, self.column))
                
                buffer = ""
                
            
            
            elif self.__get_char().isdecimal() or (self.__get_char() == "." and (self.__get_char(1) and self.__get_char(1).isdecimal())):
                number = ""
                if self.__get_char() == ".":
                    number += "0."
                    self.__consume()
                
                number += self.__consume()
                
                while(self.__get_char() and self.__get_char().isdecimal() or self.__get_char() == "_"):
                    number += self.__consume()
                
                tokens.append(Token(TokenType.number, number, self.line, self.column))
                
                
                
            
            
            elif self.__get_char() in ['"', "'"]:
                quotesymbole = self.__consume()
                textvar = quotesymbole
                while (self.__get_char() and self.__get_char() != quotesymbole):
                    textvar += self.__consume()
                textvar += self.__consume()
                tokens.append(Token(TokenType.string, textvar, self.line, self.column))
            
            elif self.__get_char() == "←" or (self.__get_char(1) and self.__get_char()+self.__get_char(1) == "<-"):
                if self.__get_char() == "<":
                    self.__consume()
                    asign = "<-"
                else:
                    asign = "←"
                self.__consume()
                tokens.append(Token(TokenType.assignment, value=asign,  line=self.line, column=self.column))
                
            
            elif self.__get_char() in ["+", "-", "*", "/"]:
                tokens.append(Token(TokenType.arithethic, self.__consume(), self.line, self.column))
                
            elif self.__get_char() in ["<", ">"] or (self.__get_char(1) and self.__get_char()+self.__get_char(1) in ["<=", ">=", "=="]):
                if (self.__get_char(1) and self.__get_char()+self.__get_char(1) in ["<=", ">=", "=="]):
                    relational_op = self.__consume()+self.__consume()
                else:
                    relational_op = self.__consume()
                
                tokens.append(Token(TokenType.relational, relational_op, self.line, self.column))
                
                
                

            elif self.__get_char() == "\n":
                column = 0
                self.__consume()
            
            
            elif self.__get_char() == "#" or (self.__get_char(1) and self.__get_char()+self.__get_char(1) == "//"):
                while self.__get_char() and self.__get_char() != "\n":
                    self.__consume()
            
            elif self.__get_char() == ":":
                tokens.append(Token(TokenType.colon, self.__consume(), self.line, self.column))

            
            elif self.__get_char() == " ":
                self.__consume()
                
            else:
                
                tokens.append(Token(TokenType.unknow, self.__consume(), self.line, self.column))
                
                continue
                columnstart = self.column
                columncount = 0
                
                errorchars = ""
                
                while (self.__get_char() and not self.__get_char().isalpha() and not self.__get_char().isdecimal() and self.__get_char() not in ['"', "'", " ", "\n", "#", "//", "←", "<", ">", "+", "-", "*", "/", ":", "<", ">"]):
                    errorchars += self.__consume()
                    columncount += 1
                print(f'{color.red}Error at line {self.line} column {columnstart}{color.reset}: Unexpected token "{errorchars}" in')
                print(self.code.split("\n")[self.line-1])
                print(" "*(columnstart-1) + "^"*columncount)


        return tokens
            

    
    def __get_char(self, offset: int = 0) -> str | None:
        if self.__char + offset <= (len(self.code) - 1):
            return self.code[self.__char + offset]
        return None
    
    def __consume(self) -> str | None:
        if self.__char <= (len(self.code) - 1):
            toretrun = self.code[self.__char]
            self.__char += 1
            self.column += 1
            if toretrun == "\n":
                self.line += 1
                self.column = 0
            
            return toretrun
        return None

    def __is_spaced_keword(self, keword: str) -> bool:
        isin = False
        for kw in ["tant que"]:
            if kw.startswith(keword.lower()):
                isin = True
                break
        return isin
    


class Preprocessor:
    def __init__(self, code:str) -> None:
        self.code:str = code
    
    def preporcess(self):
        for line in self.code.split('\n'):
            if line.startswith('$'):
                command = line.split(' ')[0][1::].lower()
                args = line.split(' ')[1::]
                
                if command == "define":
                    self.code.replace(args[0], args[1])
            
            self.code.replace(line, "")
        return self.code



if __name__ == "__main__":
    
    color.clear()
    
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
        prepocessor = Preprocessor(content)
        tokenizer = Tokenizer(prepocessor.preporcess())
        tokens = tokenizer.Tokenize()
        parser = Parser(tokens)
        
        
        # print(parser.parse())
        
        pycode = parser.parse()
        
        if len(sys.argv) == 2 or "-r" in sys.argv or "-run" in sys.argv:
            try:
                exec(pycode)
            except KeyboardInterrupt:
                print(f"{color.red}KeyboardInterrupt{color.reset}")
                exit()
            except Exception as e:
                print(f"{color.red}Error in {color.green}{path}{color.reset}: {str(e)} ")
        if "-s" in sys.argv or "-save" in sys.argv:
            if "-o" in sys.argv:
                index = sys.argv.index("-o") + 1
                if index > len(sys.argv) - 1:
                    print(f"{color.red}Error: No path supplied{color.reset}")
                    exit(1)
                else:
                    savepaht = sys.argv[index]
                
            else:
                savepaht = path + ".py"
                
            print(f"{color.blue}Saving to {color.green}{savepaht}{color.reset}")
            with open(savepaht, "w", encoding="utf-8") as file:
                file.write(pycode)
                
        if '--' in sys.argv:
            print(f"{color.blue}Tokens:{color.reset}")
            print(tokens)
        
    else:
        

        print(f'{color.blue}Algorama{color.reset} v0.0.1')
        print(f"Running on{color.blue}", platform.platform(), color.reset)
        print()
        
        while True:
            try:
                command = input(">>>")
                tokenizer = Tokenizer(command)
                
                tokenized = tokenizer.Tokenize()
                
                multiline = False
                
                if not "utiliser" in command:
                
                    for token in tokenized:
                        if token.tokentype in [TokenType._else, TokenType._for, TokenType._while]:
                            multiline = True
                            break
                
                
                if multiline:
                    code = command+"\n"
                    while command != "\n":
                        command = input("...") + "\n"
                        code += command
                        tokenized = Tokenizer(code).Tokenize()
                
                
                
                parser = Parser(tokenized)
                
                exec(parser.parse())
            except KeyboardInterrupt:
                print(f"\n{color.blue}KeyboardInterrupt{color.reset}")
                break
            
            except Exception as e:
                print(f"{color.red}Error: {str(e)}{color.reset}")