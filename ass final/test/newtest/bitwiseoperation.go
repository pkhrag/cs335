package bitwise;

import (
	"fmt";
);

func main() {
	var q,w,e,r,t,y int_t;
	q = 1;
	w=2;
	e=4;
	r=8;
	t=16;
	y=32;
	print %d y>>q<<w>>e<<r%(q|w|e|r);
	print %d y>>q<<w>>e<<r%15;
	print %d q|w|e|r;
	return;
};
