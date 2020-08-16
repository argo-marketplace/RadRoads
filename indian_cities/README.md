**Delhi RadRoads**

_a. Circuity_:

I got the bearings for every edge. I am unsure how to interpret that.

Assuming 0 = North, 90 = East, 180 = South, 270 = West, the bearing values aren't making sense to me.

 
_b. Sinuosity:_

I went through the radroads.py file, and understood that sinuosity is being calculated as the ratio of street total length, and the gc distance between its two extreme points. I believe this is taken from the Sinuosity index for rivers:  _image taken from wikipedia_

 

I was able to get this calculation for all named roads. The main issue is figuring out the order in which the edges join to each other. Each edge has a 'from' and 'to' corresponding to the start and end node OSMID. However in the dataset they're all jumbled up. Plus, bidirectional roads have two parallel lines which seem to be causing some issues with this dimension.
