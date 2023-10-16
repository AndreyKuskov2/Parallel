#include <stdio.h>
#include <locale>
#include <omp.h>

int main()
{
	setlocale(LC_ALL, "Russian");
	int n;
	// private - Указывает, что каждый поток должен иметь собственный экземпляр переменной.
#pragma omp parallel private(n) // Объявляем параллельную область, с приватной переменной n
	{
		n = 1;
#pragma omp master // Определяем, что поток главный
		{
			n = 2;
		}
		printf("Первое значение n потока %d: %d\n", omp_get_thread_num(),n);
#pragma omp barrier // синхронизируем все потоки
#pragma omp master
		{
			n = 3;
		}
		printf("Второе значение n потока %d: %d\n", omp_get_thread_num(),  n);
	}
	return 0;
}
