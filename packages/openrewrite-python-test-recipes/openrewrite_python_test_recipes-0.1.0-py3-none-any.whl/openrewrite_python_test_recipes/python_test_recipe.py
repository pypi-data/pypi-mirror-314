from rewrite import ExecutionContext, Recipe, TreeVisitor
from rewrite.python import PythonVisitor
from rewrite.python.tree import Space, Block


class PythonTestRecipe(Recipe):
    """
    A recipe to test introspection of recipe module
    """

    def get_visitor(self) -> TreeVisitor:
        """
        Get the visitor for the recipe
        """

        class Visitor(PythonVisitor):
            """
            A visitor for the recipe
            """

            def visit_space(
                self, space: Space, loc: Space.Location, p: ExecutionContext
            ) -> Space:
                # If the space is empty (""), replace it with a single space (" ")
                if space and space.whitespace == "":
                    return Space(" ")
                return space

            def visit_block(self, block: Block, p: ExecutionContext) -> Block:
                # Visit the block normally first
                visited_block = super().visit_block(block, p)
                # If the block is not null, add a single space prefix
                if visited_block is not None:
                    return visited_block.with_prefix(Space(" "))
                return visited_block

        return Visitor()
