#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <omp.h>

int main() {
    // Задаем размер векторов
    int vector_size = 50000000;

    // Выделяем память для векторов
    std::vector<double> vector1(vector_size);
    std::vector<double> vector2(vector_size);
    std::vector<double> result_vector(vector_size);

    // Заполняем векторы случайными значениями
    srand(time(NULL));
    for (int i = 0; i < vector_size; i++) {
        vector1[i] = static_cast<double>(rand()) / RAND_MAX;
        vector2[i] = static_cast<double>(rand()) / RAND_MAX;
    }

    // Измеряем время выполнения
    double start_time = omp_get_wtime();

    // Выполняем сложение векторов с использованием OpenMP
#pragma omp parallel for shared(vector1, vector2, result_vector)
    for (int i = 0; i < vector_size; i++) {
        result_vector[i] = vector1[i] + vector2[i];
    }

    double end_time = omp_get_wtime();
    double execution_time = end_time - start_time;

    // Выводим время выполнения
    std::cout << "Время выполнения сложения векторов: " << execution_time << " секунд." << std::endl;

    // Выводим размер и любой элемент результирующего вектора
    std::cout << "Размер результирующего вектора: " << result_vector.size() << std::endl;
    std::cout << "Произвольный элемент результирующего вектора: " << result_vector[0] << std::endl;

    return 0;
}