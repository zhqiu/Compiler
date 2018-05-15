int main()
{
	int n = read();
	int i = 2;
	int r, half, isPrime, remainr;
	while(i<=n) {
		r = 2;
		half = i / 2;
		isPrime = 1;
		while(r <= half) {
			remainr = i - i / r * r;
			if(remainr == 0)
				isPrime = 0;
			r = r + 1;
		}
		if(isPrime == 1)
			write(i);
		i = i+1;
	}
	return 0;
}
