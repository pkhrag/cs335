Instructions to run the code generator
------------------------------

* Go to the folder 'asgn2'
* Type `make`
* Type `./bin/codegen ./test/testfile.ir`. Replace `testfile` with any of the file present in test folder.
* Type `gcc -m32 -o output output.S` to create the executable from the generated assembly code.
* Type `make clean` after successfully testing the codegen.


## NOTE

* Nothing to note this time :)
