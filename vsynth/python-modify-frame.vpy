import sys
import os
import vapoursynth as vs
core = vs.get_core()
scriptPath = '/usr/share/vsscripts'
sys.path.append(os.path.abspath(scriptPath))
import havsfunc as hf

#import logging
#logger = logging.getLogger('undershootFiller')
#logger.setLevel(logging.INFO)
#fh = logging.FileHandler('processing.log')
#fh.setLevel(logging.INFO)
#logger.addHandler(fh)


def chromaAdjust(clp, pxlright, pxlup):
	clpChroma = core.std.CropRel(clp, left=0, right=pxlright, top=pxlup, bottom=0)
	clpChroma = core.std.AddBorders(clpChroma, left=pxlright, right=0, top=0, bottom=pxlup)
	return core.std.Merge(clipa=clp, clipb=clpChroma, weight=[0, 1])
	
def parseClip(n, f):

   fout = f.copy()
   fnew = parseFrame(f, fout)
   #fnew = fout

   return fnew

def parseFrame(inFrame, outFrame):

   # 0 is for y, 1 for u, 2 for v.
   in_plane = inFrame.get_read_array(0)
   out_plane = outFrame.get_write_array(0)

   height = len(in_plane)
   width = len(in_plane[0])
   
   window = 5
   fill_range = 16
   drop = 45
   recover = 35
         
   for h in range(height):

      #logger.info('h: ' + str(h))  
      # use while loop rather than range as we need to jump
      # to particular spots after processing a sub-range.
      w = 0
      while w + fill_range < width:
      
         my_array = [in_plane[h, w+i] for i in range(window)]
         
         if my_array[0] - min(my_array) > drop:
         
            # 4/19: smear val is not responsive enough.  What is a better formula?
            smear_val = int((my_array[0] + recover) / 2)
            
            for wo in range(fill_range):
               if my_array[0] - in_plane[h, w+wo] > recover:
                  out_plane[h, w + wo] = smear_val
         
         w += 1

   return outFrame

clp = core.d2v.Source(input='./cal-edm-86-1/game1-disc1.d2v')
clp = core.std.Trim(clp, 14250, 28690)
clp = chromaAdjust(clp, 8, 4)

clp = hf.QTGMC(clp, TFF=True, Preset='Placebo')

clpNew = core.std.ModifyFrame(clip=clp, clips=clp, selector=parseClip)
clp = core.std.Interleave(clips=[clp, clpNew])

clp.set_output()
