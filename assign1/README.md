Instructions to run the lexer
------------------------------

* Go to the folder 'asgn1'
* Type `make`
* Type `bin/lexer test/testx.go`. Replace `x` with any number from 1 to 5
* Type `make clean` after successfully testeing the lexer.


## NOTE

* Note that TYPES like _int, float, bool, complex etc_ are **predefined** identifiers and the lexer categorises them as identifiers. It will be the job of the parser to identify the identifier as a type or not. That is how *GOLANG* is implemented.
