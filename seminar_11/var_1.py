"""
создать программу для решения простых дифференциальных уравнений 
с помощью функции ядра, используйте метод Эйлера или метод Рунге-Кутты .
"""


import numpy as np
import pyopencl as cl
import pyopencl.array
import matplotlib.pyplot as plt

# Определение функции ядра
kernel_code = """
__kernel void euler_method(__global float* t, __global float* y, float h, int n) {
    int i = get_global_id(0);
    if (i < n) {
        t[i+1] = t[i] + h;
        y[i+1] = y[i] + h*t[i]*y[i];
    }
}
"""

# Параметры задачи
t0 = 0
y0 = 1
h = 0.1
n = 100

# Инициализация OpenCL контекста и очереди команд
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Создание буферов данных для t и y
t = np.zeros(n+1, dtype=np.float32)
y = np.zeros(n+1, dtype=np.float32)
t[0] = t0
y[0] = y0
t_buf = cl.Buffer(ctx, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=t)
y_buf = cl.Buffer(ctx, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=y)

# Компиляция и запуск программы OpenCL
prg = cl.Program(ctx, kernel_code).build()
prg.euler_method(queue, (n,), None, t_buf, y_buf, np.float32(h), np.int32(n))

# Чтение результатов обратно на хост
cl.enqueue_copy(queue, t, t_buf)
cl.enqueue_copy(queue, y, y_buf)

# Визуализация результатов
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('y')
plt.title('Solution of the differential equation using Euler method with pyopencl')
plt.show()
