#include <iostream>
#include <cmath>

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

bool isPrime(RegisterType n)
{
	if (n <= 1) return false;
	if (n <= 3) return true;
	if (n % 2 == 0 || n % 3 == 0) return false;
	// if (static_cast<RegisterType>(std::pow(2.f,static_cast<float>(n-1))) % n != 1) return false;

	RegisterType i = 5;

	while (i * i <= n)
	{
		if (n % i == 0 || n % (i+2) == 0) return false;
		i += 6;
	}

	return true;
}

RegisterType countNotPrimes(RegisterType begin, RegisterType end)
{
	RegisterType count = 0;
	for(RegisterType n=begin; n <= end; n += 17)
	{
		if(!isPrime(n))
			++count;
	}
	return count;
}


void program(RegisterType* r)
{
	r[b] = 79;
	r[c] = r[b];
	if(r[a]!=0)
	{
		r[b] = 107900;
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

	if(r[b] != ++r[e])
		goto maeh;

	if(r[b] != ++r[d])
		goto mooh;

	if(r[f]==0)
		++r[h];

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
	RegisterType r[8]={1,0,0,0,0,0,0,0};
	// printRegisters(r);
	// program(r);
	// printRegisters(r);
	RegisterType h = countNotPrimes(107900,124900);
	std::cout << "register H has entry " << h << std::endl;
	return 0;
}