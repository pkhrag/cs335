package types;

import (
	"fmt";
);

func main() {
	var a int_t;
	var b [2] int_t;
	var c *int_t;
	b[1] = 1;
	c = b+1;
	a=97;
	*c=a;
	print %d *c;
	return;
};
