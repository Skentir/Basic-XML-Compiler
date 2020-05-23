# -*- coding: utf-8 -*-
"""
STALGCM Machine Project
S15

Deticio, Christine
Gaw, Sharmaine
Sison, Kirsten
"""

import re

f = open("sample.txt", "r")
if f.mode == "r":
    input = f.read()


input = re.sub(r"[\t\n]*", "", input)
input = re.sub(' +', " ", input)
print(input)

#input = "<?XML version=\"1.0\" viewport=\"sedekd\"?><hello> <con/> <a> Love </a> </hello>"

tokens = []


class Token:
    def __init__(self, symbol, attr):
        self.symbol = symbol
        self.attr = attr

def LexiAnalyzer(input):
    word = ""
    for c in input:
        #if word starts with "
        if word and word[0] == '"':
            if c != '"':
                word = word + c
            else:
                if word[-1:] != '\\':
                    tokens.append(Token(word + c, "Attribute Value"))
                    word = ""
        else:
            opr = recognize(c)

            # if
            if tokens and tokens[-1].attr == "CloseTag" and c != "<":
                word = word + c
            
            #if the character is recognized as an operator
            elif (opr): 
                if word:
                    storeWord(word)
                    word = ""
                tokens.append(opr)
            elif c == " ":
                if word:
                    storeWord(word)
                    word = ""
            else:
                word = word + c
    if word:
        storeWord(word)
        word = ""

def storeWord(word):
    switcher = {
        "Escape": Token(word, "Tag"),
        "OpenTag": Token(word, "Tag"),
        "Header": Token(word, "Tag"),
        "Tag": Token(word, "Attribute"),
        "Attribute Value": Token(word, "Attribute")
    }
    
    tempToken = switcher.get(tokens[-1].attr, False)
    
    if word != " ":
        if (valid(word)):
            if tempToken:
                tokens.append(tempToken)
            else:
                tokens.append(Token(word, "Value"))
    
        else:
            tokens.append(Token(word, "Value"))
  
    
def recognize(c): 
    switcher = { 
        "<": Token(c, "OpenTag"),
        ">": Token(c, "CloseTag"),
        "/": Token(c, "Escape"),
        "?": Token(c, "Header"),
        "=": Token(c, "Assignment")
    }
    return switcher.get(c, False) 

class State:
    def __init__(self, switcher, accepting):
        self.switcher = switcher
        self.accepting = accepting

states = []
stack = []

def SyntaxAnalysis(tokens):
    # state a 0
    states.append(State({"OpenTag": 1}, False))
    # state b 1
    states.append(State({"Header": 2}, False))
    # state c 2
    states.append(State({"Tag": 3}, False))
    # state d 3
    states.append(State({"Attribute": 5, "Header": 4}, False))
    # state e 4
    states.append(State({"CloseTag": 8}, False))
    # state f 5
    states.append(State({"Assignment": 6}, False))
    # state g 6
    states.append(State({"Attribute Value": 7}, False))
    # state h 7
    states.append(State({"Attribute": 5, "Header": 4}, False))
    # state 0 8
    states.append(State({"OpenTag": 9, "Value": 8}, True))
    # state 1 9
    states.append(State({"Escape": 10, "Tag": 12}, False))
    # state 2 10
    states.append(State({"Tag": 11}, False))
    # state 3 11
    states.append(State({"CloseTag": 8}, False))
    # state 4 12
    states.append(State({"Escape": 15, "CloseTag": 16, "Attribute": 13}, False))
    # state 5 13
    states.append(State({"Assignment": 14}, False))
    # state 6 14
    states.append(State({"Attribute Value": 12}, False))
    # state 7 15
    states.append(State({"CloseTag": 8}, False))
    # state 8 16
    states.append(State({"Value": 8}, False))
    
    # initialize nextstate with using first token
    if tokens:
        nextstate = states[0].switcher.get(tokens[0].attr, states[0].accepting)
        answer = True
    else:
        answer = False
        nextstate = False  

    # if header is valid
    # if first token is valid
    if nextstate:
        for token in tokens[1:]:    
            if (nextstate == 3 and token.symbol.upper().lower() == "xml"):
                break
            elif nextstate == 16 and token.attr == "OpenTag":
                nextstate = 9
                
            else: nextstate = states[nextstate].switcher.get(token.attr, False)
            
            if nextstate is not False:
                # pop self-closing tag
                if nextstate == 15:
                    print("POPPED " + stack.pop())
                    
                # pop using tagname
                elif nextstate == 11: 
                    if stack[-1] == token.symbol:
                        print("POPPED " + stack.pop())
                    else:
                        print("ERROR")
                        answer = False
                        break
                # push tagname
                elif nextstate == 12 and token.attr == "Tag":
                    print("PUSHED " + token.symbol)
                    stack.append(token.symbol)
            # no state exists
            else:
                answer = False
                break
    
    # if entire input has been read,
    # check if current state is an accepting state
    if nextstate is not False:
        answer = states[nextstate].accepting
    
    print("\n")
    
    if (not stack) and answer:
        print("YES")
    else:
        print("NO")


def valid(word):
    return (word.replace("_", '')).isalnum()
    
LexiAnalyzer(input)
for token in tokens:
    print(token.symbol + "\t\t" + token.attr)
SyntaxAnalysis(tokens)
