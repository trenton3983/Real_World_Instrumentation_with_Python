#-------------------------------------------------------------------------------
# docstrings.py
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

""" Module level docstring.

    This describes the overall purpose and features of the module.
    It should not go into detail about each function or class as
    each of those objects has its own docstring.
"""

def Function1():
    """ A function docstring.

        Describes the purpose of the function, its inputs (if any)
        and what it will return (if anyting).
    """
    pass

class Class1:
    """ Top-level class docstring.

        Like the module docstring this is a general high-level
        description of the class. The methods and variable
        attributes are not described here.
    """

    def Method1():
        """ A method docstring.

            Similar to a function docstring.
        """
        pass

    def Method2():
        """ A method docstring.

            Similar to a function docstring.
        """
        pass
