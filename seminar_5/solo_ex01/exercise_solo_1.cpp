#include <stdio.h>
#include <iostream>
#include <omp.h>

using namespace std;

int main() {
    int n = 10;
    int i;
    int thread_id;
    
    #pragma omp parallel private(i, thread_id) shared(n)
    {
        thread_id = omp_get_thread_num();
        
        #pragma omp for nowait
        for (i = 0; i < n; i++)
            cout << "Поток " << thread_id << ": Итерация " << i << endl;
        cout << "Поток " << thread_id << " завершил работу." << endl;
    }
    cout << "Все потоки завершили работу" << endl;    
    return 0;
}
