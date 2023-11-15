import numpy as np
import pyopencl as cl
import matplotlib.pyplot as plt

# НЕ ЗАПУСКАЕТСЯ НА CUDA

# Определение функции ядра
kernel_code = """
__kernel void burn_ship_fractal(__global float2* output, const int max_iter, const float escape_radius, const int width, const int height) {
    int x = get_global_id(0);
    int y = get_global_id(1);
    
    float2 z = 0;
    float2 c = (float2) (2.0 * x / width - 1.5, 2.0 * y / height - 1.0);
    int iter = 0;

    while (z.x * z.x + z.y * z.y < escape_radius && iter < max_iter) {
        float temp = z.x * z.x - z.y * z.y + c.x;
        z.y = fabs(2.0 * z.x * z.y) + c.y;
        z.x = temp;
        iter++;
    }

    if (iter == max_iter) {
        output[y * width + x] = (float2) 0.0f;
    } else {
        output[y * width + x] = (float2) ((float)iter / (float)max_iter);
    }
}
"""

# Параметры задачи
width = 800
height = 600
max_iter = 256
escape_radius = 100.0

# Инициализация OpenCL контекста и очереди команд
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Создание буфера данных для результатов
output = np.empty((height, width), dtype=np.float32)
output_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, output.nbytes)

# Компиляция и запуск программы OpenCL
prg = cl.Program(ctx, kernel_code).build()
prg.burn_ship_fractal(queue, (width, height), None, output_buf, np.int32(max_iter), np.float32(escape_radius), np.int32(width), np.int32(height))

# Чтение результатов обратно на хост
cl.enqueue_copy(queue, output, output_buf)

# Отображение фрактала
plt.imshow(output, cmap='hot', extent=(-2.0, 1.0, -1.5, 1.5))
plt.show()
