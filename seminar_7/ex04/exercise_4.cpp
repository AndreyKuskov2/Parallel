#include <stdio.h>
#include <omp.h>
#include <locale>

int main()
{
	setlocale(LC_ALL, "Russian");
	int count = 0;
#pragma omp parallel
	{
#pragma omp atomic // Указывает, что расположение памяти, которое будет обновляться атомарным образом.
		count++;
	}
	printf("Число потоков: %d\n", count);
}
