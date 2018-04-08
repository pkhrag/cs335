Instructions to run the code generator
--------------------------------------

* Go to the folder 'assign4'
* Type `make`
* Type `./bin/irgen ./test/testfile.go`. Replace `testfile` with any of the file present in test folder.
* Type `make clean` after successfully testing the parser.

## NOTE

* Type checking is to be done in the final submission.
* After every statement, semicolon need to be inserted.
* Package name can't be same as any identifier.
* Package and import statements are part of the syntax but play no role in code generation for now.
* Package and import statements are compulsion.
* Function with parameters and arrays are not supported by codegenerator but can be verified by generated IR code.
* Print and scan statements are included in the syntax for testing.
