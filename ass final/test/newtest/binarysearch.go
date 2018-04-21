package binsearch;

import (
	"fmt";
);


func binarysearch(numbers *int_t, n int_t, l int_t, r int_t, a int_t) int_t {
	if r>=l {
		var mid int_t = l + (r-l)/2;
		if numbers[mid] == a {
			return mid+1;
		};
		if numbers[mid] > a {
			var temp int_t = binarysearch(numbers, n, l, mid-1, a);
			return temp;
		};

		return binarysearch(numbers, n, mid+1, r, a);
	};
	return -1;
};


func main() {
	var n,a,result int_t;
	scan n;
	var numbers [n] int_t;

	for i := 0; i < n; i++ {
		scan a;
		numbers[i] = a;
	};
	scan a;

	result = binarysearch(numbers, n, 0, n-1, a);
	print %d result;
	return ;
};
