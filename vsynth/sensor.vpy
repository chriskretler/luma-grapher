# The point of this script is to open a video clip, identify a particular
# line for which you want the luma values via highlight_line, and print
# out those luma values via examine_line.
import sys
import os
import vapoursynth as vs
core = vs.get_core()
scriptPath = '/usr/share/vsscripts'
sys.path.append(os.path.abspath(scriptPath))


# highlight individual lines, useful for identifying the line 
# you want values for.
def highlight_line(core, clp, line_num):

   clp1 = core.fmtc.resample(clip=clp, css="444")
   clp1 = core.fmtc.matrix(clip=clp1, mat="601", col_fam=vs.RGB)

   clpTop = core.std.CropAbs(clp1, top=0, height=line_num-1, width=clp.width)
   clpMid = core.std.CropAbs(clp1, top=line_num, height=1, width=clp.width)
   clpBtm = core.std.CropRel(clp1, top=line_num+1)
   
   clpMid = core.std.Levels(clpMid, gamma=1.5)

   clp1 = core.std.StackVertical(clips=[clpTop,clpMid,clpBtm])
   return core.fmtc.matrix(clip=clp1, mat="601", col_fam=vs.YUV)

# print out values from a particular line.
def examine_line(clp, frame_num, line_num):
   import time
   frame = clp.get_frame(frame_num)
   
   # file where we will store values.
   filename = 'line-' + str(line_num) + '-' + time.strftime("%Y%m%d-%H%M%S")
   file = open(filename, 'w')

   # in yuv colorimetry: 0 is for y, 1 for u, 2 for v.
   plane = frame.get_read_array(0)

   # Width of the luma plane. Chroma planes maybe shorter
   # depending on the sampling of your video.
   plane_width = len(plane[0])
   
   for x in range(plane_width):
      file.write(str(plane[line_num, x]))
      file.write('\n')
   file.close
   
   return 0


clp = core.d2v.Source(input='./cal-edm-86-7-dvd/dvd1.d2v')

# Here we are examining line 332 for frame 0).
examine_line(clp, 0, 332)
clp = highlight_line(core, clp, 332)

clp.set_output()
