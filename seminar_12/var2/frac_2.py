import numpy as np
import pyopencl as cl
import matplotlib.pyplot as plt

def generate_cantor_set(width, height, x_min, x_max, y_min, y_max, max_depth=5):
    # Инициализация OpenCL
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    # Создание буфера для хранения данных
    output = np.empty((width, height), dtype=np.uint32)

    mf = cl.mem_flags
    output_buffer = cl.Buffer(context, mf.WRITE_ONLY, output.nbytes)

    # Компиляция ядра
    kernel_source = """
        int cantor_check(float2 point, float2 start, float2 end, int depth) {
            if (depth == 0) {
                return 1;
            }

            float2 middle1 = ((float2)2.0 * start + end) / (float2)3.0;
            float2 middle2 = (start + (float2)2.0 * end) / (float2)3.0;

            if (point.x >= middle1.x && point.x <= middle2.x) {
                return 0;
            }

            if (point.x < middle1.x) {
                return cantor_check(point, start, middle1, depth - 1);
            } else {
                return cantor_check(point, middle2, end, depth - 1);
            }
        }

        __kernel void cantor_set(__global uint *output, const int width, const int height,
                                  const float x_min, const float x_max, const float y_min, const float y_max,
                                  const int max_depth) {
            int gid_x = get_global_id(0);
            int gid_y = get_global_id(1);

            float x = x_min + (x_max - x_min) * gid_x / width;
            float y = y_min + (y_max - y_min) * gid_y / height;

            float2 point = (float2)(x, y);

            // Функция для проверки принадлежности к множеству Кантора
            int result = cantor_check(point, (float2)(0.0, 0.5), (float2)(1.0, 0.5), max_depth);

            output[gid_x + gid_y * width] = result;
        }
    """

    prg = cl.Program(context, kernel_source).build()

    # Запуск ядра
    global_size = (width, height)
    local_size = None

    prg.cantor_set(queue, global_size, local_size,
                   output_buffer, np.int32(width), np.int32(height),
                   np.float32(x_min), np.float32(x_max), np.float32(y_min), np.float32(y_max),
                   np.int32(max_depth))

    cl.enqueue_copy(queue, output, output_buffer).wait()

    return output

def plot_cantor_set(cantor_set):
    plt.imshow(cantor_set, cmap='binary', extent=(0, 1, 0, 1))
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    width = 800
    height = 400
    x_min, x_max = 0, 1
    y_min, y_max = 0, 1
    max_depth = 5

    cantor_set = generate_cantor_set(width, height, x_min, x_max, y_min, y_max, max_depth)
    plot_cantor_set(cantor_set)
