package main;
import "fmt";
type T struct{
	a rune_t;
	b int_t ;
	c rune_t;
	d int_t;
	e float_t;
	name[10] rune_t;
	f rune_t;
};

func f(x type T) {
	x.a = 'a';
	x.b = 47114711;
	x.c = 'c';
	x.d = 1234;
	x.e = 3.141592897932;
  	x.f = '*';
  	x.name[0] = 'a';
	x.name[1] = 'b';
	x.name[2] = 'c';
};

func main() {
	var k type T;
	f(k);
};
