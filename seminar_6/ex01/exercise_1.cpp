#include <iostream>
#include <stdio.h>
#include <omp.h>
#include <locale>
#include <unistd.h>
using namespace std;
int main()
{
	setlocale(LC_ALL, "Russian");
	int i;
	double time = omp_get_wtime();
#pragma omp parallel private(i) num_threads(4)
	{
		// По очереди раскомментируем строчки ниже и пересобираем задание make run_exercise_1
#pragma omp for schedule (static, 6)
// #pragma omp for schedule (dynamic, 6)
// #pragma omp for schedule (guided, 6)
// #pragma omp for schedule (auto)
		for (i = 0; i<200; i++)
		{
			printf("Поток %d выполнила итерацию %d\n", omp_get_thread_num(), i);
			sleep(1); 
		}
	}
	cout << "Time = " << (omp_get_wtime() - time) << endl;
}
