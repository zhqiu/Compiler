int main()
{
	int a[10];
	int i = 0, j = 10;
	int min = 0;
	int ti;
	while(i<j) {
		ti = (i+1) * (i+1) * (i+1);
		a[i] = ti - ti/j*j;
		i = i+1;
	}
	i = 0;
	while(i<j) {
		write(a[i]);
		i = i+1;
	}
	i = 1;
	while(i<j) {
		if(a[i] < a[min]) {
			min = i;
		}
		i = i+1;
	}
	write(a[min]);
	return 0;
}

