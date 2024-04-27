import PIL.Image
from ast import literal_eval
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

def main(TimeLapse = False):
    for i in range(1):
        EncodedFrame = f".\\input\\{i}.txt"
        with open(EncodedFrame, "r") as file:
            FrameSize = literal_eval(file.readline())
            DecodedFrame = PIL.Image.new(mode="RGB", size=FrameSize, color=(0,0,255))
            File = file.readlines()
            FinishedLines = []
            SinglePixels = {}
            Height = -1
            Step = 0
            Phase = 0
            while len(FinishedLines) < FrameSize[1]:
                Height += 1
                if Height == FrameSize[1]: 
                    Height = 0
                if Height not in FinishedLines:
                    try:
                        CurrentInterval = literal_eval(File[Height][File[Height].index(r"["):File[Height].index(r"]")+1])
                        Range = range(CurrentInterval[0], CurrentInterval[1]+1)
                        File[Height] = File[Height][File[Height].index(r"]")+1:]
                    except ValueError:
                        FinishedLines.append(Height)
                        continue
                    if len(Range) != 1:
                        for Width in Range:
                            DecodedFrame.putpixel((Width, Height), hex_to_rgb(CurrentInterval[2]))
                        Step += 1
                        print(f"Step {Step}-{Phase}")
                        if TimeLapse:
                            FrameForTimeLapse = DecodedFrame.copy()
                            PIL.ImageDraw.Draw(FrameForTimeLapse).text((0,0),f"Step {Step}-{Phase}", fill=(0,0,0), font=PIL.ImageFont.truetype('Monoid-Regular.ttf', 30))
                            FrameForTimeLapse.save(f".\\output\\{Step}.jpg")
                    else:
                        if CurrentInterval[2] not in SinglePixels.keys():
                            SinglePixels[CurrentInterval[2]] = [(CurrentInterval[0], Height)]
                        else:
                            SinglePixels[CurrentInterval[2]].append((CurrentInterval[0], Height))
            Phase = 1
            if SinglePixels != {}:
                PixelIndexes = SinglePixels.keys()
                for Color in PixelIndexes:
                    Step += 1
                    print(f"Step {Step}-{Phase}")
                    if TimeLapse:
                        FrameForTimeLapse = DecodedFrame.copy()
                        PIL.ImageDraw.Draw(FrameForTimeLapse).text((0,0),f"Step {Step}-{Phase}", fill=(0,0,0), font=PIL.ImageFont.truetype('Monoid-Regular.ttf', 0.01*(FrameSize[0]+FrameSize[1])))
                        FrameForTimeLapse.save(f".\\output\\{Step}.jpg")
                    for Coordinate in SinglePixels[Color]:
                        DecodedFrame.putpixel(Coordinate, hex_to_rgb(Color))

        DecodedFrame.save(f".\\output\\end.jpg")

if __name__ == "__main__":
    main(True)