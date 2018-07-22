import sys
import os
import vapoursynth as vs
core = vs.get_core()
scriptPath = '/usr/share/vsscripts'
sys.path.append(os.path.abspath(scriptPath))
import havsfunc as hf

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
   inPlane = inFrame.get_read_array(0)
   outPlane = outFrame.get_write_array(0)

   height = len(inPlane)
   width = len(inPlane[0])
   w = 0
   
   invalidVal = 30
   recoveryVal = 35
   window = 6
   nextValue = 0
   startRange = 0 
   endLocation = 0
   endRange = 0
   
   #print(out_frame.props)
   for h in range(height):
      # use while loop rather than range as we need to jump
      # to particular spots after processing a sub-range.
      while w < width:
      
         # start of section that handles undershoot
         if inPlane[h, w] <= invalidVal:
            startRange = w

            if w + window >= width:
               endRange = width
            else:
               endRange = w + window
            
            # over the given range, look for a value above a threshold.
            # if you find it, assign it to a variable and tell us at what location
            # you found it, because we're going to use that location later.
            for tempW in range(startRange, endRange):
               if inPlane[h, tempW] >= recoveryVal:
                  nextValue = inPlane[h, tempW]
                  endLocation = tempW
                  break
            
            # if nextValue is still 0, then we haven't found a value
            # greater than the invalid value in our new range, so set
            # some default values.
            if nextValue == 0:
               nextValue = invalidVal
               endLocation = endRange
            
            # Now that we've determined the start and end places, and 
            # the value of the replacement value, write the replacement
            # value for all spots of our temporary array.
            for writeW in range(startRange, endLocation):
               outPlane[h, writeW] = nextValue

            # set the counter to the end of the write range, subtracting 1 to 
            # account for the increment that occurs at the end of this function.
            w = endLocation - 1
            
         # set this back to 0, so we can use it's value to detect if
         # it has been set by finding a recovery value.
         nextValue = 0
         endLocation = 0
         w += 1

   return outFrame
   

clp = core.d2v.Source(input='./video/game1-disc1.d2v')
clp = core.std.Trim(clp, 14250, 28690)
clp = chromaAdjust(clp, 8, 4)
clp = hf.QTGMC(clp, TFF=True, Preset='Placebo')

clpNew = core.std.ModifyFrame(clip=clp, clips=clp, selector=parseClip)
clp = core.std.Interleave(clips=[clp, clpNew])

clpNew.set_output()
