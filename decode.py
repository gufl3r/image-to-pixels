import yaml
import glob
import sys
import PIL.Image
from ast import literal_eval

import PIL.ImageDraw
import PIL.ImageFont


def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return (r, g, b)


def main(
    Directory,
    OutputDirectory,
    Timelapse,
    TimelapseInterval,
    ShowProgress,
    SaveEnd,
    Show,
):
    for PixelSequenceFile in glob.glob(f"{Directory}\\*.imgps"):
        EncodedFrame = PixelSequenceFile
        PixelSequenceFile = PixelSequenceFile[PixelSequenceFile.rindex("\\") + 1 :]
        with open(EncodedFrame, "r") as File:
            FrameSize = literal_eval(File.readline())
            DecodedFrame = PIL.Image.new(mode="RGB", size=FrameSize, color=(0, 0, 255))
            FileLines = File.readlines()
            FinishedLines = []
            SinglePixels = {}
            Height = -1
            Step = 0
            TimelapseStep = 0
            Phase = 0
            NextLine = True

            while len(FinishedLines) != FrameSize[1]:
                if NextLine:
                    NextLine = False
                    Height += 1
                    if Height == FrameSize[1]:
                        Height = 0
                        if SinglePixels != {}:
                            Color = list(SinglePixels.keys())[0]
                            for Coordinate in SinglePixels[Color]:
                                DecodedFrame.putpixel(Coordinate, hex_to_rgb(Color))
                            SinglePixels.pop(Color)

                if Height not in FinishedLines:
                    try:
                        CurrentInterval = literal_eval(
                            FileLines[Height][
                                FileLines[Height].index("[") : FileLines[Height].index("]") + 1
                            ]
                        )
                        Range = range(CurrentInterval[0], CurrentInterval[1] + 1)
                        FileLines[Height] = FileLines[Height][
                            FileLines[Height].index(";") + 1 :
                        ]
                    except ValueError:
                        FinishedLines.append(Height)
                        NextLine = True
                        continue

                    if len(Range) != 1:
                        for Width in Range:
                            DecodedFrame.putpixel(
                                (Width, Height), hex_to_rgb(CurrentInterval[2])
                            )
                        NextLine = True
                        Step += 1

                        if ShowProgress:
                            print(f"Step {Step}-{Phase}")

                        if Timelapse:
                            FrameForTimeLapse = DecodedFrame.copy()
                            PIL.ImageDraw.Draw(FrameForTimeLapse).text(
                                (0, 0),
                                f"Step {Step}-{Phase}",
                                fill=(0, 0, 0),
                                font=PIL.ImageFont.truetype(
                                    "Monoid-Regular.ttf",
                                    int(0.013 * (FrameSize[0] + FrameSize[1])),
                                ),
                            )
                            if Step % TimelapseInterval == 0:
                                FrameForTimeLapse.save(
                                    f"{OutputDirectory}\\{PixelSequenceFile} {TimelapseStep}.jpg"
                                )
                                TimelapseStep += 1
                    else:
                        if CurrentInterval[2] not in SinglePixels:
                            SinglePixels[CurrentInterval[2]] = [
                                (CurrentInterval[0], Height)
                            ]
                        else:
                            SinglePixels[CurrentInterval[2]].append(
                                (CurrentInterval[0], Height)
                            )
                else:
                    NextLine = True

            Phase = 1
            if SinglePixels != {}:
                for Color in reversed(list(SinglePixels.keys())):
                    for Coordinate in SinglePixels[Color]:
                        DecodedFrame.putpixel(Coordinate, hex_to_rgb(Color))
                    Step += 1

                    if ShowProgress:
                        print(f"Step {Step}-{Phase}")

                    if Timelapse:
                        FrameForTimeLapse = DecodedFrame.copy()
                        PIL.ImageDraw.Draw(FrameForTimeLapse).text(
                            (0, 0),
                            f"Step {Step}-{Phase}",
                            fill=(0, 0, 0),
                            font=PIL.ImageFont.truetype(
                                "Monoid-Regular.ttf",
                                int(0.013 * (FrameSize[0] + FrameSize[1])),
                            ),
                        )
                        if Step % TimelapseInterval == 0:
                            FrameForTimeLapse.save(
                                f"{OutputDirectory}\\{PixelSequenceFile} {TimelapseStep}.jpg"
                            )
                            TimelapseStep += 1

        print(f"Decoded {PixelSequenceFile} in {Step} steps")

        if SaveEnd:
            DecodedFrame.save(
                f"{OutputDirectory}\\{PixelSequenceFile[:PixelSequenceFile.index('.')]} .jpg"
            )

        if Show:
            DecodedFrame.show()


if __name__ == "__main__":
    MainArgs = {
        "DirectoryArg": ".\\input",
        "OutputDirectoryArg": ".\\output",
        "TimelapseArg": True,
        "TimelapseIntervalArg": 1,
        "ShowProgressArg": True,
        "SaveEndArg": False,
        "ShowArg": True,
    }

    for Index, Argument in enumerate(sys.argv):
        if Argument in ["-d", "--directory"]:
            MainArgs["DirectoryArg"] = sys.argv[Index + 1]
        if Argument in ["-od", "--outputdirectory"]:
            MainArgs["OutputDirectoryArg"] = sys.argv[Index + 1]
        if Argument in ["-t", "--timelapse"]:
            MainArgs["TimelapseArg"] = sys.argv[Index + 1].lower() in ["true", "yes", "y", "1"]
        if Argument in ["-ti", "--timelapseinterval"]:
            MainArgs["TimelapseIntervalArg"] = int(sys.argv[Index + 1])
        if Argument in ["-sp", "--showprogress"]:
            MainArgs["ShowProgressArg"] = sys.argv[Index + 1].lower() in ["true", "yes", "y", "1"]
        if Argument in ["-se", "--saveend"]:
            MainArgs["SaveEndArg"] = sys.argv[Index + 1].lower() in ["true", "yes", "y", "1"]
        if Argument in ["-s", "--show"]:
            MainArgs["ShowArg"] = sys.argv[Index + 1].lower() in ["true", "yes", "y", "1"]

    print(f"Executing with:\n{yaml.dump(MainArgs, default_flow_style=False)}")

    main(
        Directory=MainArgs["DirectoryArg"],
        OutputDirectory=MainArgs["OutputDirectoryArg"],
        Timelapse=bool(MainArgs["TimelapseArg"]),
        TimelapseInterval=int(MainArgs["TimelapseIntervalArg"]),
        ShowProgress=bool(MainArgs["ShowProgressArg"]),
        SaveEnd=bool(MainArgs["SaveEndArg"]),
        Show=bool(MainArgs["ShowArg"]),
    )
