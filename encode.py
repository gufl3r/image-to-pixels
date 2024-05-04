import glob
import PIL.Image


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def main(Directory, OutputDirectory):
    for ImageFile in glob.glob(f"{Directory}\\*.jpg"):
        Step = 0
        ImageFile = f"{ImageFile[ImageFile.rindex("\\")+1:]}"
        Frame = PIL.Image.open(f"{Directory}\\{ImageFile}")
        with open(
            f"{OutputDirectory}\\{ImageFile[:ImageFile.index(".")]}.imgps", "w"
        ) as File:
            File.write(f"{Frame.size}\n")
        with open(
            f"{OutputDirectory}\\{ImageFile[:ImageFile.index(".")]}.imgps", "a"
        ) as File:
            for Height in range(Frame.size[1]):
                ColorInterval = [0, -1, None]
                LastPixel = Frame.getpixel((0, Height))
                for Width in range(Frame.size[0]):
                    FramePixel = Frame.getpixel((Width, Height))
                    if FramePixel != LastPixel or Width == Frame.size[0] - 1:
                        ColorInterval[1] = (
                            Width - 1 if Width != Frame.size[0] - 1 else Width
                        )
                        ColorInterval[2] = rgb_to_hex(
                            LastPixel[0], LastPixel[1], LastPixel[2]
                        )
                        File.write(f"{str(ColorInterval).replace(" ", "")};")
                        Step += 1
                        ColorInterval = [Width, -1, None]
                        LastPixel = FramePixel
                File.write("\n")
        print(f"Encoded {ImageFile} in {Step} steps")


if __name__ == "__main__":
    main(Directory=".\\input", OutputDirectory=".\\output")
