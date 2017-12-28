#include <iostream>

enum RegNames {
	a = 0,
	b,
	c,
	d,
	e,
	f,
	g,
	h
};

using RegisterType = unsigned int;

void program(RegisterType* r)
{
	r[b] = 79;
	r[c] = r[b];
	if(r[a]!=0)
	{
		r[b] *= 100;
		r[b] += 100000;
		r[c] = r[b] + 17000;
	}

	meow:
	r[f] = 1;
	r[d] = 2;

	mooh:
	r[e] = 2;

	maeh:

	if(r[b]==r[d]*r[e])
		r[f] = 0;

	r[e] += 1;
	if(r[b] != r[e])
		goto maeh;

	r[d] += 1;
	if(r[b] != r[d])
		goto mooh;

	if(r[f]==0)
		r[h] += 1;

	if(r[b] == r[c])
		return;

	r[b] += 17;
	goto meow;
}

void printRegisters(RegisterType* r)
{
	std::cout << "R ";
	for(int i=0; i<8; ++i)
	{
		std::cout << r[i] << "\t";
	}
	std::cout << std::endl;
}

int main(int,char**)
{
	RegisterType r[8]={0,0,0,0,0,0,0,0};
	printRegisters(r);
	program(r);
	printRegisters(r);
	return 0;
}