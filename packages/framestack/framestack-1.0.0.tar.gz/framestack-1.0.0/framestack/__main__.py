import pathlib
import re
import subprocess
import sys

import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont


"""
Example instructions.txt:
canvas w=500 h=300 d=100
text message=Hello_World font=font.ttf size=20 x=100 y=100 ax=center
video path=acro.gif t=000 x=000 y=000 w=030 h=050 d=030 st=020
video path=walk.gif t=020 x=400 y=000 w=040 h=040 d=080
save path=out.gif lossy=80
"""


def shell(cmd):
  # print('  shell:', cmd)
  return subprocess.check_output(cmd, shell=True).decode('utf-8')


def canvas(canvas, w=800, h=600, d=100):
  return 255 * np.ones((d, w, h, 3), np.uint8)


def save(canvas, path='out.gif', lossy=None, fps=20, pt=0, pr=0, pb=0, pl=0):
  path = pathlib.Path(path)
  if pt or pr or pb or pl:
    d, w, h, c = canvas.shape
    container = 255 * np.ones((d, w + pl + pr, h + pt + pb, c), np.uint8)
    container[:, pl: pl + w, pt: pt + h, :] = canvas
    canvas = container
  imageio.mimsave(path, canvas.transpose((0, 2, 1, 3)), fps=fps)
  print(f'Written {path} ({path.stat().st_size/1024/1024:.2f} MB)')
  if lossy:
    out = path.with_suffix('.lossy.gif')
    shell(f'gifsicle -O3 --lossy={lossy} --colors 256 {path} > {out}')
    print(f'Written {out} ({out.stat().st_size/1024/1024:.2f} MB)')
  return canvas


def video(
    canvas,
    path,     # Filename of the input video.
    t=0,      # Start time on the canvas.
    x=0,      # Horizontal position on the canvas.
    y=0,      # Vertical position on the canvas.
    d=None,   # Duration in the input and canvas.
    w=None,   # Width on the canvas.
    h=None,   # Height on the canvas.
    br=0,     # Border radius.
    st=0,     # Start time in the input.
    sx=0,     # Vertical start pixel in the input.
    sy=0,     # Horizontal start pixel in the input.
    sw=None,  # Used width of the input.
    sh=None,  # Used height of the input.
    sat=None,  # TODO: Saturation.
):
  if d:
    assert d <= canvas.shape[0], 'too long duration'
    assert st >= 0 or d <= abs(st), 'not enough frames'
  if any([sx, sy, sw, sh]):
    assert sw and sh, 'need to specify crop width and height'
    sw, sh = int(sw), int(sh)
  e = d and st + d - 1 or ''
  video = imageio.mimread(path, memtest='1GiB')
  if path.endswith('.gif'):
    length = len(video)
    print(f'Loading {path} with {length} frames.')
    shell(' '.join(['gifsicle --colors=255', path, '> tmp.gif']))
    shell(' '.join([
        'gifsicle --unoptimize',
        f'--crop {sx},{sy}-{sx+sw},{sy+sh}' if any([sx, sy, sw, sh]) else '',
        f'--resize {w}x{h} --resize-method sample' if w or h else '',
        'tmp.gif',
        f"'#{st}-{e}'" if st or e else '',
        '> tmp2.gif',
    ]))
    # video = imageio.mimread('tmp2.gif', playback=True)
    video = imageio.mimread('tmp2.gif')
  else:
    if any([sx, sy, sw, sh]):
      video = np.array(video)[st:, sy: sy + sh, sx: sx + sw]
    if d:
      video = video[:d]
  video = np.array(video)
  video = video[..., :3].transpose((0, 2, 1, 3))
  t, x, y, d, w, h, video = _clip(canvas, video, t, x, y)
  if sat is not None:
    gray = (video * np.array([0.299, 0.587, 0.114])).sum(-1)
    video = sat * video + (1 - sat) * gray[..., None]
  orig = canvas.copy()
  canvas[t: t + d, x: x + w, y: y + h] = video
  if br:
    def restore(i, j):
      canvas[t: t + d, i, j] = orig[t: t + d, i, j]
    for i in range(0, br):
      for j in range(0, br):
        if (i - br) ** 2 + (j - br) ** 2 > br ** 2:
          restore(x + i, y + j)
          restore(x + w - i - 1, y + j)
          restore(x + i, y + h - j - 1)
          restore(x + w - i - 1, y + h - j - 1)
  return canvas


def image(
    canvas,
    path,     # Filename of the input image.
    x=0,      # Horizontal position on the canvas.
    y=0,      # Vertical position on the canvas.
    w=None,   # Width on the canvas.
    h=None,   # Height on the canvas.
):
  # TODO
  image = imageio.imread(path)
  image = image[..., :3].transpose((1, 0, 2))
  if w or h:
    h = h or image.shape[0]
    w = w or image.shape[1]
    if image.shape[:2] != (w, h):
      from PIL import Image
      print(image.shape)
      image = Image.fromarray(image)
      image = image.resize((h, w))
      image = np.array(image)
      print(image.shape)
  # t, x, y, d, w, h, video = _clip(canvas, video, t, x, y)
  canvas[:, x: x + w, y: y + h] = image
  return canvas


def text(
    canvas,
    message,       # Text to render using use underscores as spaces.
    font,          # Filename of the font file.
    size=20,       # Font size.
    ax='center',   # Horizontal alignment to the position point.
    ay='center',   # Vertical alignment to the position point.
    t=0,           # Start time on the canvas.
    x=0,           # Horizontal position on the canvas.
    y=0,           # Vertical position on the canvas.
    d=None,        # Duration in the input and canvas.
    r=0,           # Degrees to rotate text on the canvas.
):
  message = message.replace('_', ' ')
  d = d or len(canvas) - t
  font = ImageFont.truetype(font, size)
  w, h = font.getsize(message)
  image = Image.new('RGB', (w, h), (255, 255, 255))
  draw = ImageDraw.Draw(image)
  draw.text((0, 0), message, (0, 0, 0), font=font)
  text = np.array(image).transpose((1, 0, 2))[None]
  w, h, text = _rotate(text, r)
  x = dict(left=x, right=x - w, center=x - w // 2)[ax]
  y = dict(top=y, bottom=y - h, center=y - h // 2)[ay]
  t, x, y, _, w, h, text = _clip(canvas, text, t, x, y)
  canvas[t:t + d, x:x + w, y:y + h] = text
  return canvas


def rectangle(
    canvas,
    t=0,          # Start time on the canvas.
    x=0,          # Horizontal position on the canvas.
    y=0,          # Vertical position on the canvas.
    d=None,       # Duration in the input and canvas.
    w=None,       # Width on the canvas.
    h=None,       # Height on the canvas.
    c='#000000',  # Color of the rectangle.
    br=0,         # Border radius.
):
  assert w and h
  d = d or canvas.shape[0]
  assert c.startswith('#') and len(c) == 7
  video = np.zeros((d, w, h, 3))
  video[..., 0] = int(c[1:3], 16)
  video[..., 1] = int(c[3:5], 16)
  video[..., 2] = int(c[5:7], 16)
  t, x, y, d, w, h, video = _clip(canvas, video, t, x, y)
  orig = canvas.copy()
  canvas[t: t + d, x: x + w, y: y + h] = video
  if br:
    def restore(i, j):
      canvas[t: t + d, i, j] = orig[t: t + d, i, j]
    for i in range(br):
      for j in range(br):
        if (i - br) ** 2 + (j - br) ** 2 > br ** 2:
          restore(x + i, y + j)
          restore(x + w - i - 1, y + j)
          restore(x + i, y + h - j - 1)
          restore(x + w - i - 1, y + h - j - 1)
  return canvas


def _main():
  canvas_ = None
  instructions = pathlib.Path(sys.argv[1]).read_text()
  for line in instructions.split('\n'):
    line = line.strip()
    if not line or line.startswith('#'):
      continue
    try:
      command, kwargs = _parse(line)
    except Exception:
      print('Error parsing line:', line)
      raise
    print(command.__name__, ' '.join(f'{k}={v}' for k, v in kwargs.items()))
    canvas_ = command(canvas_, **kwargs)


def _clip(canvas, source, t, x, y):
  d, w, h, _ = source.shape
  if t < 0:
    source = source[abs(t):]
    t = 0
  if x < 0:
    source = source[:, abs(x):]
    x = 0
  if y < 0:
    source = source[:, :, abs(y):]
    y = 0
  if t + d > canvas.shape[0]:
    source = source[:canvas.shape[0] - t]
  if x + w > canvas.shape[1]:
    source = source[:, :canvas.shape[1] - x]
  if y + h > canvas.shape[2]:
    source = source[:, :, :canvas.shape[2] - y]
  d, w, h, _ = source.shape
  return t, x, y, d, w, h, source


def _rotate(source, r):
  source = {
      0: source,
      90: source.transpose((0, 2, 1, 3))[:, ::-1],
      180: source[:, ::-1, ::-1],
      270: source.transpose((0, 2, 1, 3))[:, :, ::-1],
  }[r]
  _, w, h, _ = source.shape
  return w, h, source


def _parse(line):
  try:
    line = re.sub(r'\s+', ' ', line)
    command, remaining = line.split(' ', 1)
    command = globals()[command]
    kwargs = {}
    for pair in remaining.split(' '):
      key, value = pair.split('=')
      try:
        value = int(value)
      except ValueError:
        try:
          value = float(value)
        except ValueError:
          value = str(value)
      kwargs[key] = value
    return command, kwargs
  except Exception:
    print(f"Could not _parse line '{line}':")
    raise


if __name__ == '__main__':
  _main()
