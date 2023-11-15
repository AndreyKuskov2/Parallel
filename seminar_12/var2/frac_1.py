import numpy as np
import pyopencl as cl
import matplotlib.pyplot as plt

def generate_lambertw_fractal(width, height, x_min, x_max, y_min, y_max, max_iter=100):
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
        __kernel void lambertw_fractal(__global uint *output, const int width, const int height,
                                       const float x_min, const float x_max, const float y_min, const float y_max,
                                       const int max_iter) {
            int gid_x = get_global_id(0);
            int gid_y = get_global_id(1);

            float x = x_min + (x_max - x_min) * gid_x / width;
            float y = y_min + (y_max - y_min) * gid_y / height;

            float2 z = (float2)(x, y);
            float2 zn = z;

            int iter;
            for(iter = 0; iter < max_iter; iter++) {
                float2 w = zn - (exp(zn) - z) / (exp(zn) + (float2)1.0);

                if (length(w - zn) < 1e-6) {
                    break;
                }

                zn = w;
            }

            output[gid_x + gid_y * width] = iter;
        }
    """

    prg = cl.Program(context, kernel_source).build()

    # Запуск ядра
    global_size = (width, height)
    local_size = None

    prg.lambertw_fractal(queue, global_size, local_size,
                         output_buffer, np.int32(width), np.int32(height),
                         np.float32(x_min), np.float32(x_max), np.float32(y_min), np.float32(y_max),
                         np.int32(max_iter))

    cl.enqueue_copy(queue, output, output_buffer).wait()

    return output

def plot_lambertw_fractal(fractal):
    plt.imshow(fractal, cmap='viridis', extent=(-5, 5, -5, 5))
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    width = 800
    height = 800
    x_min, x_max = -5, 5
    y_min, y_max = -5, 5

    lambertw_fractal = generate_lambertw_fractal(width, height, x_min, x_max, y_min, y_max)
    plot_lambertw_fractal(lambertw_fractal)
