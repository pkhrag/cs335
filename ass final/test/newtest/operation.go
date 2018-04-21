package operation;

import (
	"fmt";
);

func main() {
	var q,w,e,r,t,y,u int_t;
	q = 1;
	w = 2;
	e = 4;
	r = 8;
	t=16;
	y=32;
	u=64;
	var result int_t = (q*w*e*r)/t%y|q;
	//var result int_t = (u)/t|q;
	print %d result;
	return;
};
