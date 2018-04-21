package prime;

import (
	"fmt";
);


func SieveOfEratosthenes(n int_t) {

	var integers [n+5] int_t;

	for i := 0; i < n+1; i++ {
		integers[i] = 1;
	};

	var totalprimes int_t;
	totalprimes=0;
	for p := 2; p*p <= n; p++ {
		totalprimes += 1;
		if integers[p] == 1 {
			for i := p * 2; i <= n; i += p {
				integers[i] = 0;
			};
		};
	};

	var primes [totalprimes+1] int_t;
	primes[0] = totalprimes;
	var i int_t = 1;
	for p := 2; p <= n; p++ {
		if integers[p] == 1 {
			print %d p;
			i++;
		};
	};

	return ;
};

func main() {
	var n int_t;
	scan n;
	SieveOfEratosthenes(n);
};

