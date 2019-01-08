# This script will:
# highlight a particular line within a frame
# Output the contents of the pixels of that line to an array.

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

def highlight_line(core, clp, line_num):

   #clp1 = core.fmtc.resample(clip=clp, css="444")
   #clp1 = core.fmtc.matrix(clip=clp1, mat="601", col_fam=vs.RGB)
   clp1 = core.resize.Bicubic(clp, format=vs.RGB24)

   clpTop = core.std.CropAbs(clp1, top=0, height=line_num, width=clp.width)
   clpMid = core.std.CropAbs(clp1, top=line_num, height=1, width=clp.width)
   clpBtm = core.std.CropRel(clp1, top=line_num+1)
   
   clpMid = core.std.Levels(clpMid, gamma=1.5)

   clp1 = core.std.StackVertical(clips=[clpTop,clpMid,clpBtm])
   #return core.fmtc.matrix(clip=clp1, mat="601", col_fam=vs.YUV)
   return core.resize.Bicubic(clp1, format=vs.YUV420P8, matrix_s="709")

def examine_line(clp, frame_num, line_num):
   import time
   frame = clp.get_frame(frame_num)
   
   # 0 is for y, 1 for u, 2 for v.
   plane = frame.get_read_array(0)

   # myArray has 480 elements, one for each scanline
   # There are 704 values per each scanline 
   #plane_height = len(plane)
   plane_width = len(plane[0])
   

   filename = 'line-' + str(line_num) + '-' + time.strftime("%Y%m%d-%H%M%S")
   file = open(filename, 'w')

#   file.write(str(plane_width))
   
   for x in range(plane_width):
#      file.write(str(x))
#      file.write(',')
      file.write(str(plane[line_num, x]))
      file.write('\n')
   file.close
   
   return 0

   #highlight_line(clp, line_num)

clp = core.d2v.Source(input='./cal-edm-86-1/game1-disc1.d2v')
clp = core.std.Trim(clp, 14250, 28690)
clp = chromaAdjust(clp, 8, 4)
clp = hf.QTGMC(clp, TFF=True, Preset='Placebo')

#examine_line(clp, 0, 332)
clp = highlight_line(core, clp, 352)
#clp = core.std.Interleave(clips=[clp, clpNew])

clp.set_output()
