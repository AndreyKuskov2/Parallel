#include <stdio.h>
#include <omp.h>

int main() {
    int num_threads_outer = 2;
    int num_threads_middle = 2;
    int num_threads_inner = 2;

    // Вложенные параллельные области
#pragma omp parallel num_threads(num_threads_outer)
    {
        int thread_id_outer = omp_get_thread_num();
        printf("Outer thread %d\n", thread_id_outer);

#pragma omp parallel num_threads(num_threads_middle)
        {
            int thread_id_middle = omp_get_thread_num();
            printf("  1 thread %d\n", thread_id_middle);

#pragma omp parallel num_threads(num_threads_inner)
            {
                int thread_id_inner = omp_get_thread_num();
                printf("    2 thread %d\n", thread_id_inner);
            }
        }
    }

    printf("\n");

    // Запрет вложенных параллельных областей
    omp_set_max_active_levels(0);

#pragma omp parallel num_threads(num_threads_outer)
    {
        int thread_id_outer = omp_get_thread_num();
        printf("Outer thread %d\n", thread_id_outer);

#pragma omp parallel num_threads(num_threads_middle)
        {
            int thread_id_middle = omp_get_thread_num();
            printf("  Middle thread %d\n", thread_id_middle);

            // Вложенная параллельная область не будет создана из-за запрета
        }
    }

    return 0;
}