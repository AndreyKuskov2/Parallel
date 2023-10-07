#include <iostream>
#include <omp.h>

int main()
{
    std::cout << omp_get_thread_limit() << std::endl;
    return 0;
}