#include <iostream>
#include <omp.h>

int main() {
    int n = 3; // Размер первого цикла
    int m = 4; // Размер второго цикла
    int i, j;
    int thread_id;
    
    #pragma omp parallel private(i, j, thread_id) shared(n, m)
    {
        thread_id = omp_get_thread_num();
        
        #pragma omp for collapse(2)
        for (i = 0; i < n; i++) {
            for (j = 0; j < m; j++) {
                std::cout << "Поток " << thread_id << ": Итерация (" << i << ", " << j << ")\n";
            }
        }
    }
    
    return 0;
}
