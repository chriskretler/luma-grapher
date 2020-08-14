The idea is to patch the relative mins with the value of the rational value for all values either
under or over the the rational value--depending on the max or min--for pixels both to the left and 
the right of the min and max.

If the next pixel to be patched is within the range of what has already been patched, then skip it.
