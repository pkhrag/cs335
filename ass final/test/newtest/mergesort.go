package mail;

import (
	"fmt";
);

func mergesort(numbers *int_t, n int_t) {
	if n <= 1 {
		return ;
	};

	var l,r,j int_t;
	l = n/2;
	r = n-l;

	var left [l] int_t;
	var right [r] int_t;

	j=0;
	for i := 0; i<l; i++ {
		left[i] = numbers[j];
		j++;
	};
	for i := 0; i<r; i++ {
		right[i] = numbers[j];
		j++;
	};
	mergesort(left, l);
	mergesort(right, r);

	var i int_t;
	i=0;
	j=0;
	for k := 0; k<n; k++ {
		if i==l {
			numbers[k] = right[j];
			j++;
		}
		else {
			if j==r {
				numbers[k] = left[i];
				i++;
			}
			else {
				if left[i] < right[j] {
					numbers[k] = left[i];
					i++;
				}
				else {
					numbers[k] = right[j];
					j++;
				};
			};
		};
	};
	return ;
};

func main() {
	var n int_t;
	scan n;
	var numbers [n] int_t;

	for i :=0; i<n; i++ {
		scan numbers[i];
	};
	mergesort(numbers, n);

	for i :=0; i<n; i++ {
		print %d numbers[i];
	};
};
