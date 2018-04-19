package math;
import "fmt";

var bar int_t = 50;

func foo() int_t{
    return bar;
};

func main()
{
	var a int_t = 0;
	a = foo();
	print a;
	return;
};