import sys
import os
import numpy as np
import vapoursynth as vs
core = vs.get_core()
scriptPath = '/usr/share/vsscripts'
sys.path.append(os.path.abspath(scriptPath))
import havsfunc as hf

import logging
logger = logging.getLogger('undershootFiller')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('processing.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def chromaAdjust(clp, pxlright, pxlup):
	clpChroma = core.std.CropRel(clp, left=0, right=pxlright, top=pxlup, bottom=0)
	clpChroma = core.std.AddBorders(clpChroma, left=pxlright, right=0, top=0, bottom=pxlup)
	return core.std.Merge(clipa=clp, clipb=clpChroma, weight=[0, 1])
	
def parseClip(n, f):

   fout = f.copy()
   fnew = parse_frame(f, fout)
   #fnew = fout

   return fnew

def parse_frame(in_frame, out_frame):

   # 0 is for y, 1 for u, 2 for v.
   in_array = np.asarray(in_frame.get_read_array(0))
   out_array = np.asarray(out_frame.get_write_array(0))

   f = np.fft.fft2(in_array)
   fshift = np.fft.fftshift(f)
   
   rows, cols = in_array.shape
   crow,ccol = rows/2 , cols/2
   crow = int(crow)
   ccol = int(ccol)
   
   #logger.debug('in_array shape: ' + str(in_array.shape))   
   #logger.debug('crow dtype: ' + str(np.dtype(crow)))
   #logger.debug('crow value: ' + str(crow))   
      
   fshift[crow-30:crow+30, ccol-30:ccol+30] = 0   
   #fshift[210:270, 322:382] = 0   
   #fshift[0:80, 0:704] = 0   
   #fshift[400:480, 0:704] = 0  
   #fshift[0:480, 0:120] = 0   
   #fshift[0:480, 584:704] = 0   
   
   f_ishift = np.fft.ifftshift(fshift)
   img_back = np.fft.ifft2(f_ishift)
   img_back = np.abs(img_back)
   img_back = img_back.astype(np.uint8)

   #logger.debug('img_back shape: ' + str(img_back.shape))
   #logger.debug('img_back details: ' + str(np.dtype(img_back)))

   np.copyto(out_array, img_back)
   #np.copyto(out_array, in_array)
   
   return out_frame
   

clp = core.d2v.Source(input='../video/1.d2v')
clp = core.std.Trim(clp, 12900, 17169)
clp = chromaAdjust(clp, 8, 4)
#clp = core.std.ModifyFrame(clip=clp, clips=clp, selector=parseClip)
clp = hf.QTGMC(clp, TFF=True, Preset='Placebo')

clp_new = core.std.ModifyFrame(clip=clp, clips=clp, selector=parseClip)

clp_new1 = core.std.Merge(clp_new, clp)

clp_diff = core.std.MakeDiff(clp_new1, clp)
clp_diff = core.std.Levels(clp_diff, min_in=127, max_in=129, min_out=0, max_out=255)

clp = core.std.Interleave(clips= [clp, clp_new, clp_new1])
#clp = core.std.Interleave(clips=[clp, clpNew])

clp.set_output()
