package mai;
import "fmt";
func main() {
	
	var h [3]rune_t;
	var k [4]rune_t;
	var t [7] rune_t;
	h[0]='a';
	h[1]='a';
	h[2]='a';
	k[0]='c';
	k[1]='c';
	k[2]='c';
	k[3]='c';
	t = h+k;
	print %s t;
	return;
};
