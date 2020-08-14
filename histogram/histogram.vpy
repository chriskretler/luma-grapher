from collections import OrderedDict
import logging
import havsfunc as hf
import vapoursynth as vs

core = vs.get_core()

logger = logging.getLogger('undershootFiller')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('processing.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)


def deint(clp):
   clp = core.std.Trim(clp, 12950, length=3600)
   return hf.QTGMC(clp, TFF=True, Preset='Fast')


def get_pixel_dist(pixels):
  dist = {}
  for i in pixels:
    if(i in dist.keys()):
      dist[i] = dist[i] + 1
    else:
      dist[i] = 1
  return dist

def equalize_hist(dist, num_pixels):
  dist_sorted = OrderedDict(sorted(dist.items()))
  cumulative_value = 0
  bitdepth = 255
  #min_value = dist_sorted.get(0)
  min_value = 0
  transform_table = {}

  # This part is dubious
  num_pixels = num_pixels - min_value

  for key in dist_sorted.keys():
    cumulative_value = cumulative_value + dist_sorted.get(key) - min_value
    transform_table[key] = int((cumulative_value / num_pixels) * bitdepth)

  #logger.info('{}'.format(transform_table))
  return transform_table


def get_pixel_values(in_plane):
  height = len(in_plane)
  width = len(in_plane[0])

  pixels = []

  for h in range(height):
     for w in range(width):
        pixels.append(in_plane[h, w])
  return pixels


def write_new_plane(in_plane, out_plane, transform_table):
  height = len(in_plane)
  width = len(in_plane[0])

  for h in range(height):
    for w in range(width):
      out_plane[h, w] = transform_table.get(in_plane[h, w])
  return out_plane


def parseFrame(inFrame, outFrame):
   # 0 is for y, 1 for u, 2 for v.
   in_plane = inFrame.get_read_array(0)
   out_plane = outFrame.get_write_array(0)

   pixels = get_pixel_values(in_plane)
   dist = get_pixel_dist(pixels)
   num_pixels = len(pixels)
   transform_table = equalize_hist(dist, num_pixels)
   out_plane = write_new_plane(in_plane, out_plane, transform_table)

   return outFrame


def parseClip(n, f):
   fout = f.copy()
   fnew = parseFrame(f, fout)
   return fnew


clp = deint(core.d2v.Source(input='../video/1.d2v'))

clp_new = core.std.ModifyFrame(clip=clp, clips=clp, selector=parseClip)

#clp = core.std.Interleave(clips=[clp, clp_new])
clp_new.set_output()
