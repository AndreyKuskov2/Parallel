#include <stdio.h>
#include <omp.h>
#include <locale>

int main()
{
	setlocale(LC_ALL, "Russian");
	int i, n;
#pragma omp parallel private (i, n)
	{
		n = omp_get_thread_num();
#pragma omp for ordered // Требуется для параллельной инструкции, если в цикле будет использоваться упорядоченная директива.
		for (i = 0; i<5; i++)
		{
			printf("Поток %d, итерация %d\n", n, i);
#pragma omp ordered // выводит на экран ту же информацию, но в порядке, соответствующем порядку выполнения итераций.
			{
				printf("ordered: Поток %d, итерация %d\n", n, i);
			}
		}
	}
}
