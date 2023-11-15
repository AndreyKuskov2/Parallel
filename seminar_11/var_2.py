import numpy as np
import pyopencl as cl

# Определение функции ядра
kernel_code = """
__kernel void monte_carlo_pi(__global float* result, __global float* random_numbers) {
    int id = get_global_id(0);
    float x = random_numbers[id * 2];
    float y = random_numbers[id * 2 + 1];
    if (x*x + y*y <= 1.0) {
        result[id] = 1.0;
    } else {
        result[id] = 0.0;
    }
}
"""

# Параметры задачи
n = 1000000  # Количество случайных точек

# Генерация случайных чисел с помощью numpy
random_numbers = np.random.rand(n * 2).astype(np.float32)

# Инициализация OpenCL контекста и очереди команд
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Создание буфера данных для результатов и случайных чисел
result = np.zeros(n, dtype=np.float32)
result_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, result.nbytes)
random_numbers_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=random_numbers)

# Компиляция и запуск программы OpenCL
prg = cl.Program(ctx, kernel_code).build()
prg.monte_carlo_pi(queue, (n,), None, result_buf, random_numbers_buf)

# Чтение результатов обратно на хост
cl.enqueue_copy(queue, result, result_buf)

# Вычисление числа Пи
inside_circle = np.sum(result)
pi_approx = 4 * inside_circle / n
print("Approximated value of Pi:", pi_approx)
