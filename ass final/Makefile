all:
	@mkdir -p bin
	@cp ./src/* ./bin/
	@mv bin/parser.sh bin/irgen
	@chmod +x ./bin/irgen
	@cp testrun.sh GOtham 
	@chmod +x ./GOtham
clean:
	@rm -rf bin
	@rm -f output*
	@rm -f ./*.ir
