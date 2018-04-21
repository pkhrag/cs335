###############################################################################
A GOlang Compiler written in Python (for x86) 
Authors: Akash Kumar Dutta, Prakhar Agarwal, Swarnadeep Mandal 
Group 11
###############################################################################

# Language Features:
    a.  Data Types - int, rune, pointers and multi dimensional arrays of int, rune 
    b.  Operators
            int:
                - Unary
                - Relational 
                - Arithmetic
                - Bitwise 
                - Logical 
                - Assignment 
            bool (realized as int 0 and 1):
                - Unary 
                - Logical 
                - Assignment

    c.  Loops -> for
    d.  Selection Statements  if, switch
    e.  Multiple Declarations and Sequential Assignments
        - Multiple Declarations  -> a,b,c int_t = 3,4,5 ;
    f.  Arrays  n-D arrays of types - {int,rune,bool}
    g.  Functions
        - Allowed return types -> int, rune, pointer
        - Allowed argument types -> int, rune, and pointers
    h.  Scoping
    	- Imlemented as a tree of symbol tables
    i.  boolean expressions realized as integer 0 and 1 with relational operators
    j.	pre increment/decrement
    k.	RECURSION
    l.  struct
    m.  type checking
    n.  string concatenation
    o.  print string
    p.  type checking

###############################################################################


USAGE:
> make
> ./GOtham test

To Clean:
> make clean
