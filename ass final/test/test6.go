package mai;
import "fmt";


func goo(c, d, e int_t) {
	print c+d;
	print e;
	print d;
	return;
};

func foo(a,b int_t)
{
	print a;
	print b;
	goo(1, 2, 3);
	return;
};


func main() {
	var i,j int_t = 3,4;
	foo(i,j);
	return;
};
