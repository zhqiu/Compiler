int sort(int n)
{
	int t;
	int a[100], i = 0, j = 0;
	while (i < n)
	{

		a[i] = 100 - i * 2;
		i = i + 1;

	}
	i = 0;
	
	while (i < n)
	{

		write(a[i]);
		i = i + 1;

	}
	return 0;
}
int main()
{

	int m;
	m = read();
	if (m >= 100) write(-1);
	else sort(m);
	return 0;

}

