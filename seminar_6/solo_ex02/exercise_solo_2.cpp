#include <iostream>
#include <omp.h>

int main() {
    #pragma omp parallel
    {
        #pragma omp sections
        {
            #pragma omp section
            {
                // Задача 1: Выполнение первой задачи параллельно с другими
                std::cout << "Задача 1 выполняется\n";
            }
            
            #pragma omp section
            {
                // Задача 2: Выполнение второй задачи (сначала)
                std::cout << "Задача 2 выполняется\n";
            }
            
        }

        #pragma omp sections
        {
            #pragma omp section
            {
                // Задача 3: Выполнение третьей задачи (после второй)
                std::cout << "Задача 3 выполняется\n";
            }
            
            #pragma omp section
            {
                // Задача 4: Выполнение четвертой задачи параллельно с другими
                std::cout << "Задача 4 выполняется\n";
            }
        }
    }
    
    return 0;
}
