package main;
import "fmt";

func main() {
	var wflg, tflg int_t = 0, 0;
	var dflg int_t = 0;
	var c rune_t;
	switch (c)
	{
	case 'w':
	case 'W':
		wflg = 1;
		break;
	case 't':
	case 'T':
		tflg = 1;
		break;
	case 'd':
		dflg = 1;
		break;
	};
};
