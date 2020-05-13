class TreeNode:
    def __init__(self, experssion: str):
        self.expression = experssion
        self.left = None
        self.right = None

    def __str__(self):
        if self.left is None and self.right is None:
            return self.expression
        else:
            left_str = 'None' if self.left is None else str(self.left)
            right_str =  'None' if self.right is None else str(self.right)
            return f'{self.expression} ({left_str}, {right_str})'

    def add_left(self, node):
        self.left = node

    def add_right(self, node):
        self.right = node
