int main()
{

	int a = 3, b = 4, c;
	c = a * a + b * b;
	write(c);
	c = (a + c) / b;
	write(c);
	c = a+b; // 7
	a = a + b; // 7
	b = a - b; // 3
	a = a - b; // 4
	c= a-b;    // 1
	b = ((a - b) * 2 - 1) + (a / b) * (2 * (3 + b));
	write(a);
	write(b);
	return 0;

}
