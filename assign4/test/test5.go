package madn;

import "fmt";

func gcd(a,b int_t) int_t{
	if b == 0{
		return a;
	};

	return gcd(b,a%b);
};


func main() {
	var a,b int_t;
	scan a;
	scan b;
	var c =gcd(a,b);
	print c;
	return;
};
