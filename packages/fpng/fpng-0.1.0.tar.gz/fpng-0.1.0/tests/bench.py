# py-fpng-nb
# https://github.com/dofuuz/py-fpng-nb
#
# SPDX-FileCopyrightText: (c) 2024 KEUM Myungchul
# SPDX-License-Identifier: MIT
#
# Fast PNG writer for Python.
# py-fpng-nb is a Python wrapper of fpng(https://github.com/richgel999/fpng).

import os
import os.path as osp
import timeit

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import fpng


REPEAT = 10


img = Image.open('fpng/example.png')
# img = Image.open('tests/wikipedia.png')
img.load()


fp = open(os.devnull, "wb")


# Pillow PNG
times = []
for comp_lv in range(0, 10):
    t = timeit.timeit(lambda: img.save(fp, format='png', compress_level=comp_lv), number=REPEAT)
    times.append(t)
    print(f'on-memory PNG (comp level={comp_lv}): {t:f} sec')

t = timeit.timeit(lambda: img.save(fp, format='fpng'), number=REPEAT)
print(f'on-memory fpng: {t:f} sec')


# fpng
sizes = []
for comp_lv in range(0, 10):
    t = timeit.timeit(lambda: img.save('img/pil_png.png', format='png', compress_level=comp_lv), number=REPEAT)
    sz = osp.getsize("img/pil_png.png")
    sizes.append(sz)
    print(f'write PNG (comp level={comp_lv}): {t:f} sec; {sz:,} bytes')

t_f = timeit.timeit(lambda: img.save('img/pil_fpng.png', format='fpng'), number=REPEAT)
sz_f = osp.getsize("img/pil_fpng.png")
print(f'write fpng: {t_f:f} sec; {sz_f:,} bytes')


# plot
times = np.asarray(times) / REPEAT * 1000
sizes = np.asarray(sizes) / 1024
t_f = t_f / REPEAT * 1000
sz_f /= 1024
plt.figure()
plt.plot(times, sizes, marker='o', label='Pillow')
plt.plot([t_f], [sz_f], marker='o', label='fpng')
for i, (x, y) in enumerate(zip(times, sizes)):
    if i % 2 == 0:
        plt.text(x, y, str(i), fontsize=9, ha='left', va='top')
    else:
        plt.text(x, y, str(i), fontsize=9, ha='right', va='top')
plt.xlabel("Compression time (ms)")
plt.ylabel("Size (KB)")
# plt.ylim([min(sizes)*0.9, sz_f*1.1])
plt.legend()
plt.savefig('img/bench.png')
