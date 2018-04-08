import sys
import os
import vapoursynth as vs
core = vs.get_core()
scriptPath = '/usr/share/vsscripts'
sys.path.append(os.path.abspath(scriptPath))
import havsfunc as hf
from ctypes import *

def chromaAdjust(clp, pxlright, pxlup):
	clpChroma = core.std.CropRel(clp, left=0, right=pxlright, top=pxlup, bottom=0)
	clpChroma = core.std.AddBorders(clpChroma, left=pxlright, right=0, top=0, bottom=pxlup)
	return core.std.Merge(clipa=clp, clipb=clpChroma, weight=[0, 1])

def parse_clip(n, f):

   fout = f.copy()
   parse_frame(f, fout)

   return fout
   

def parse_frame(in_frame, out_frame):

#   import time
#   filename = 'frames-' + '-' + time.strftime("%Y%m%d-%H%M%S")
#   file = open(filename, 'w')
#   file.write(str(plane_width))
#   for x in range(plane_width):
#   file.write("howdy")
#   file.write(str(frame.readonly))
#   file.write(str(out_frame.readonly))
#   file.close   
   
   # 0 is for y, 1 for u, 2 for v.
   in_plane = in_frame.get_read_array(0)
   #out_plane = out_frame.get_write_array(0)

   height = len(in_plane)
   row_size = len(in_plane[0])
   
   stride = in_frame.get_stride(0)
   #dst_stride = out_frame.get_stride(0)
   
   srcp = in_frame.get_read_ptr(0)
   dstp = out_frame.get_write_ptr(0)
   
   vs_bitblt(dstp, stride, srcp, stride, row_size, height)
   #print(out_frame.props)
   #for x in range(plane_width):
      #out_plane[line_num, x] = in_plane[line_num, x] + 10

   return clp
   
def vs_bitblt(dstp, dst_stride, srcp, src_stride, row_size, height):
    if height > 0:
        if src_stride == dst_stride and src_stride == row_size:
            #ctypes.memmove(to_address, from_address, typesize*(size-i-1))
            memmove(dstp, srcp, row_size * height)
        else:
            for i in range(height):
                memmove(dstp, srcp, row_size)
                srcp += src_stride
                dstp += dst_stride

clp = core.d2v.Source(input='./video/game1-disc1.d2v')
clp = core.std.Trim(clp, 14250, 28690)
clp = chromaAdjust(clp, 8, 4)
clp = hf.QTGMC(clp, TFF=True, Preset='Placebo')

clpNew = core.std.ModifyFrame(clip=clp, clips=clp, selector=parse_clip)
clp = core.std.Interleave(clips=[clp, clpNew])

clp.set_output()
