# py-fpng-nb

Very fast .PNG image(24/32bpp) writer for Python.

Compared to typical PNG libraries, its compression is about 10-20x faster, while producing 10-50% larger files.

- Homepage: https://github.com/dofuuz/py-fpng-nb
- PyPI: https://pypi.org/project/fpng/

py-fpng-nb is a Python wrapper of [fpng](https://github.com/richgel999/fpng)


## Installation

```sh
pip install fpng
```

If installation fails, upgrade pip with `python -m pip install --upgrade pip` and try again.


## Usage

### with PIL

```python
import fpng
from PIL import Image

# ...

img.save('file_path.png', 'FPNG')
```

### with NDarray

n-dimensional arrays of NumPy, PyTorch, TensorFlow, JAX, and CuPy.

Must have 3 dimensions [height, width, channels] with RGB or RGBA format.

```python
import fpng

# ...

png_bytes = fpng.from_ndarray(img_ndarray)

with open('file_path.png', 'wb') as f:
    f.write(png_bytes)
```


### with OpenCV

```python
import cv2
import fpng

# ...

png_bytes = fpng.from_cv2(img_mat)

with open('file_path.png', 'wb') as f:
    f.write(png_bytes)
```


## Benchmark

Comparison with Pillow 11.0.0

### Compressing photo

![Photo x86_64](img/bench_photo_amd64.png) | ![Photo x86_64](img/bench_photo_aarch64.png)
:---: | :---:
x86_64 | AArch64(ARM64)

### Compressing screenshot

[Screenshot](tests/wikipedia.png) of Wikipedia

![Screenshot x86_64](img/bench_screenshot_amd64.png) | ![Screenshot x86_64](img/bench_screenshot_aarch64.png)
:---: | :---:
x86_64 | AArch64(ARM64)
