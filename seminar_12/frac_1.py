# Импортируем необходимые библиотеки
import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# Задаем параметры фрактала
width = 800 # Ширина изображения в пикселях
height = 600 # Высота изображения в пикселях
max_iter = 100 # Максимальное число итераций для каждой точки
x_min = -2.0 # Минимальное значение x на комплексной плоскости
x_max = 2.0 # Максимальное значение x на комплексной плоскости
y_min = -1.5 # Минимальное значение y на комплексной плоскости
y_max = 1.5 # Максимальное значение y на комплексной плоскости
c_re = -0.8 # Действительная часть константы c
c_im = 0.156 # Мнимая часть константы c

# Создаем массив для хранения результатов
output = np.empty((height, width), dtype=np.uint32)

# Создаем контекст и очередь OpenCL
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# Создаем буферы для передачи данных между хостом и устройством
output_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, output.nbytes)
prg = cl.Program(ctx, """
__kernel void julia(__global uint *output,
                    const uint width,
                    const uint height,
                    const uint max_iter,
                    const float x_min,
                    const float x_max,
                    const float y_min,
                    const float y_max,
                    const float c_re,
                    const float c_im)
{
    // Получаем индексы пикселя в двумерном массиве
    int i = get_global_id(0);
    int j = get_global_id(1);

    // Проверяем, что индексы не выходят за границы массива
    if (i >= width || j >= height) return;

    // Вычисляем координаты комплексного числа z, соответствующего пикселю
    float z_re = x_min + i * (x_max - x_min) / width;
    float z_im = y_max - j * (y_max - y_min) / height;

    // Инициализируем счетчик итераций нулем
    uint iter = 0;

    // Повторяем итерации до тех пор, пока модуль z не превысит 2 или не достигнем максимального числа итераций
    while (z_re * z_re + z_im * z_im < 4.0f && iter < max_iter)
    {
        // Выполняем итерацию z = z^2 + c
        float tmp_re = z_re * z_re - z_im * z_im + c_re;
        float tmp_im = 2.0f * z_re * z_im + c_im;
        z_re = tmp_re;
        z_im = tmp_im;

        // Увеличиваем счетчик итераций на единицу
        iter++;
    }

    // Записываем результат в выходной массив
    output[j * width + i] = iter;
}
""").build()

# Запускаем ядро на устройстве с заданными параметрами
prg.julia(queue, output.shape, None, output_buf,
          np.uint32(width), np.uint32(height), np.uint32(max_iter),
          np.float32(x_min), np.float32(x_max), np.float32(y_min), np.float32(y_max),
          np.float32(c_re), np.float32(c_im))

# Копируем результаты с устройства на хост
cl.enqueue_copy(queue, output, output_buf)

# Визуализируем результаты с помощью matplotlib
plt.imshow(output, cmap='inferno')
plt.show()