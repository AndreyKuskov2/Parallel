#include <iostream>
#include <omp.h>

int main() {
    int n = 10;
    int sum = 0; // Инициализируем переменную для накопления суммы
    int i;
    
    #pragma omp parallel for reduction(+:sum)
    for (i = 1; i <= n; i++) {
        sum += i; // Выполняем операцию накопления (суммирование)
    }
    
    std::cout << "Сумма значений от 1 до " << n << " равна " << sum << std::endl;
    
    return 0;
}
