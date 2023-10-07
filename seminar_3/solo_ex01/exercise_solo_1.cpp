#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    const int VECTOR_SIZE = 50000000;
    double *vector1 = (double *)malloc(VECTOR_SIZE * sizeof(double));
    double *vector2 = (double *)malloc(VECTOR_SIZE * sizeof(double));
    double *result_vector = (double *)malloc(VECTOR_SIZE * sizeof(double));

    // Заполнение векторов случайными значениями
    srand(time(NULL));
    for (int i = 0; i < VECTOR_SIZE; i++) {
        vector1[i] = (double)rand() / RAND_MAX;
        vector2[i] = (double)rand() / RAND_MAX;
    }

    // Вычисление и вывод времени выполнения
    clock_t start_time = clock();

    for (int i = 0; i < VECTOR_SIZE; i++) {
        result_vector[i] = vector1[i] + vector2[i];
    }

    clock_t end_time = clock();
    double execution_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Время выполнения: %.2f секунд\n", execution_time);

    // Вывод размера и одного элемента результирующего вектора
    printf("Размер результирующего вектора: %d\n", VECTOR_SIZE);
    printf("Один элемент результирующего вектора: %.4f\n", result_vector[0]);

    // Освобождение памяти
    free(vector1);
    free(vector2);
    free(result_vector);

    return 0;
}