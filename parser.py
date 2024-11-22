
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
class Parser(object):
    def __init__(self,tokens):
        self.tokens=tokens
        print(f"test{self.tokens}")
        self.index=0
    def advance(self):
        self.token_index +=1

        if self.index < len(self.tokens):
            self.current_tok=self.tokens[self.index]
        return self.current_tok
            
        

    def parse(self):
        return self.parse_expression()
    def parse_expression(self):
        print(f"test{self.tokens}")
        # if self.index < len(self.tokens) and self.tokens[self.index][0] == "SUM_OF":
        #     self.index += 1  # Consume SUM OF
        #     left = self.parse_expression()  # Parse left operand
        #     if self.index < len(self.tokens) and self.tokens[self.index][0] == "AN":
        #         self.index += 1  # Consume AN
        #         right = self.parse_expression()  # Parse right operand
        #         return Node("SUM_OF", left, right)
        # elif self.index < len(self.tokens) and self.tokens[self.index][0] == "NUMBER":
        #     node = Node(int(self.tokens[self.index][1]))
        #     self.index += 1  # Consume NUMBER
        #     return node
        # elif self.index < len(self.tokens) and self.tokens[self.index][0] == "VISIBLE":
        #     node = Node()
        # raise ValueError("Invalid syntax")