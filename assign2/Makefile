all:
	@mkdir -p bin
	@cp ./src/*.py ./bin/
	@chmod +x ./bin/codegen.py
	@cp ./bin/codegen.py ./bin/codegen
clean: ./bin
	@rm -rf bin
	@rm -f output.S 
	@rm -f output 
