from PIL import Image
from io import BytesIO
img = Image.new("RGB", (800,400), color="red")
img.save("back.png")
x,y = img.size
offset = x // 12, y // 5
img.paste(Image.open("flask.png"), offset)
from PIL import ImageFont
from PIL import ImageDraw
draw = ImageDraw.Draw(img)
fnt = ImageFont.truetype('arial.ttf', 48)
draw.text((x//8, 20),"FLASK & Python - part. 12",(255,255,255),font=fnt)
img.save('final.png')
img.show()