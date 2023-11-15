import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

sierpinski_fractal_kernel = """
__kernel void sierpinski_fractal_kernel(__global int *fractal,
                                        const int width,
                                        const int height,
                                        const int maxiter,
                                        const float xmin,
                                        const float ymin,
                                        const float dx,
                                        const float dy)
{
    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);

    float x = xmin + gid_x * dx;
    float y = ymin + gid_y * dy;

    float2 z = (float2)(x, y);
    float2 c = (float2)(x, y);

    int i;
    for (i = 0; i < maxiter; i++)
    {
        z = (float2)(z.x * z.x - z.y * z.y, 2 * z.x * z.y) + c;
        if (z.x * z.x + z.y * z.y > 4.f)
            break;
    }

    fractal[gid_y * width + gid_x] = i;
}
"""

prg = cl.Program(ctx, sierpinski_fractal_kernel).build()

def sierpinski_fractal(xmin, xmax, ymin, ymax, width, height, maxiter):
    x = np.linspace(xmin, xmax, width).astype(np.float32)
    y = np.linspace(ymin, ymax, height).astype(np.float32)
    c = x + y[:, None] * 1j
    fractal = np.zeros(c.shape, dtype=np.int32)

    dx = (xmax - xmin) / width
    dy = (ymax - ymin) / height

    fractal_buf = cl.Buffer(ctx,
                            cl.mem_flags.WRITE_ONLY,
                            fractal.nbytes)

    prg.sierpinski_fractal_kernel(queue,
                                  fractal.shape,
                                  None,
                                  fractal_buf,
                                  np.int32(width),
                                  np.int32(height),
                                  np.int32(maxiter),
                                  np.float32(xmin),
                                  np.float32(ymin),
                                  np.float32(dx),
                                  np.float32(dy))

    cl.enqueue_copy(queue, fractal, fractal_buf)

    return fractal

xmin, xmax, ymin, ymax = -2.0, 2.0, -2.0, 2.0
width, height = 1024, 1024
maxiter = 100

fractal = sierpinski_fractal(xmin, xmax, ymin, ymax,
                          width=width,
                          height=height,
                          maxiter=maxiter)

plt.imshow(fractal.T[::-1], cmap='gray', extent=(xmin,xmax,ymin,ymax))
plt.show()
