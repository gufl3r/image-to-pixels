import PIL.Image
from ast import literal_eval as make_tuple
import re
import time

import PIL.ImageDraw
import PIL.ImageFont

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return (r, g, b)

for i in range(1):
    EncodedFrame = f".\\input\\{i}.txt"
    with open(EncodedFrame) as file:
        FrameSize = make_tuple(file.readline())
        ConvertedFrame = PIL.Image.new(mode="RGB", size=FrameSize, color=(0,0,255))
        File = file.readlines()
        FinishedLines = []
        Height = -1
        This = 0
        Offset = 0
        while len(FinishedLines) < FrameSize[1]:
            Height += 1
            if Height == FrameSize[1]: 
                Height = 0
                Offset += 1
            if Height not in FinishedLines:
                try:
                    CurrentInterval = [
                        [SubFinder.start() for SubFinder in re.finditer("\\[", File[Height])][Offset], 
                        [SubFinder.start() for SubFinder in re.finditer("\\]", File[Height])][Offset]+1,
                        None
                    ]
                    CurrentInterval[2] = make_tuple(File[Height][CurrentInterval[0]:CurrentInterval[1]])
                except IndexError:
                    FinishedLines.append(Height)
                    continue
                for Width in range(CurrentInterval[2][0], CurrentInterval[2][1]+1):
                    ConvertedFrame.putpixel((Width, Height), hex_to_rgb(CurrentInterval[2][2]))
                This += 1
                #print(This)
                #PIL.ImageDraw.Draw(ConvertedFrame).text((0,0),f"Step {This}", fill=(0,0,0), font=PIL.ImageFont.truetype('Monoid-Regular.ttf', 30))
                #ConvertedFrame.save(f".\\output\\badapple steps\\{This}.jpg")
                #PIL.ImageDraw.Draw(ConvertedFrame).text((0,0),f"Step {This}", fill=(255,255,255), font=PIL.ImageFont.truetype('Monoid-Regular.ttf', 30))
    ConvertedFrame.save(f".\\output\\badapple steps\\end.jpg")