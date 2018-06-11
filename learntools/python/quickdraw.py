import numpy as np
import pandas as pd
import os
from glob import glob
import random

qd_path = ['..', 'input', 'quickdraw_simplified']
base_dir = os.path.join(*qd_path)
obj_files = glob(os.path.join(base_dir, '*.ndjson'))
if not obj_files:
    qd_path.insert(2, 'tinyquickdraw')
    base_dir = os.path.join(*qd_path)
    obj_files = glob(os.path.join(base_dir, '*.ndjson'))
if not obj_files:
    print("WARNING: it doesn't look like the quickdraw dataset is available in this context")
top_row_dict = lambda in_df: list(in_df.head(1).T.to_dict().values())[0]
getcat = lambda path: path.split('/')[-1].split('.')[0]


plot_kwargs = dict(
    marker='.',
    ms=2,
    linestyle='-',
    color='black',
)
# Adapted from Kevin Mader's "QuickDraw Overview" kernel here: https://www.kaggle.com/kmader/quickdraw-overview
def draw_dict(in_dict, in_ax):
    for i, (x_coord, y_coord) in enumerate(in_dict['drawing']):
        # upside-down!
        y_coord = [255-y for y in y_coord]
        in_ax.plot(x_coord, y_coord, **plot_kwargs)
    in_ax.axis('equal')
    in_ax.xaxis.set_ticks([])
    in_ax.yaxis.set_ticks([])

def random_category():
    return random.choice(obj_files)

def sample_images_of_category(n, cat):
    with open(cat) as f:
        to_skip = random.randint(0, 500)
        for _ in range(to_skip):
            next(f)
        cj = pd.read_json(f, lines=True, chunksize=1)
        dicts = []
        while len(dicts) < n:
            d = top_row_dict(next(cj))
            if d['recognized']:
                dicts.append(d)
    return dicts

def draw_images_on_subplots(dicts, figax):
    fig, axes = figax
    if not hasattr(axes, 'shape'):
        rows = cols = 1
    elif len(axes.shape) == 2:
        rows, cols = axes.shape
    elif len(axes.shape) == 1:
        rows = 1
        cols = axes.shape[0]
    else:
        assert False, 'Unrecognized axes shape: {}'.format(axes.shape)

    n = len(dicts)
    extra_cols = max(0, cols - n)
    extra_rows = max(0, rows - ( (n+cols-1)//cols ))
    if extra_cols:
        print("WARNING: {} empty column{}".format(extra_cols, 
            's' if extra_cols > 1 else ''))
    if extra_rows:
        print("WARNING: {} empty row{}".format(extra_rows, 
            's' if extra_rows > 1 else ''))
    w = fig.get_figwidth()
    h = fig.get_figheight()
    subplot_size = [round(dim, 1) for dim in [w/cols, h/rows]]
    if subplot_size != [2.0, 2.0]:
        print("WARNING: Expected image size to be 2 x 2. Actual size = {} x {}".format(
            *subplot_size))
    if w > 16.0:
        print("WARNING: Total width, {}, is greater than limit of 16".format(
            w))
    naxes = np.product(axes.shape)
    n = len(dicts)
    if naxes < n:
        print("WARNING: Only have room to draw {} out of {} images. Skipping the rest.".format(naxes, n))
    catname = dicts[0]['word']
    fig.suptitle('{} Sketches of category "{}"'.format(len(dicts), catname))
    fig.set_facecolor( (.93, .97, .99) )
    for d, ax in zip(dicts, axes.flatten()):
        draw_dict(d, ax)
    leftover_idxs = range(len(dicts), naxes)
    for i in leftover_idxs:
        axes.flatten()[i].axis('off')
