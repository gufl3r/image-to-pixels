import PIL.Image

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

for i in range(1):
    Frame = PIL.Image.open(f".\\input\\{i}.jpg")
    with open(f".\\output\\{i}.txt", "w") as file:
        file.write(f"{Frame.size}\n")
    with open(f".\\output\\{i}.txt", "a") as file:
        for Height in range(Frame.size[1]):
            ColorInterval = [0, -1, None]
            LastPixel = Frame.getpixel((0, Height))
            for Width in range(Frame.size[0]):
                FramePixel = Frame.getpixel((Width, Height))
                if FramePixel != LastPixel or Width == Frame.size[0]-1:
                    ColorInterval[1] = Width-1 if Width != Frame.size[0]-1 else Width
                    ColorInterval[2] = rgb_to_hex(LastPixel[0],LastPixel[1],LastPixel[2])
                    file.write(str(ColorInterval))
                    ColorInterval = [Width, -1, None]
                    LastPixel = FramePixel
            file.write("\n")