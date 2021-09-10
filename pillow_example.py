from PIL import Image

# image = Image.open('nature.png')
# px = image.load()

# image2 = Image.new('RGB', image.size)

# print(px, type(px))
# print(image.size)

# for x in range(image.size[0]):
# 	for y in range(image.size[1]):
# 		mean = (px[x, y][0] + px[x, y][1] + px[x, y][2]) // 3
# 		image2.putpixel((x, y), (mean, mean, mean))

# image.save('nature.png')

# weather_image_0 = Image.open('weather_icon_0.png')
# weather_image_12 = Image.open('weather_icon_12.png')
image_background = Image.new('RGB', (500, 500), (255, 255, 255))
for i in range(7):
	weather_image = Image.open(f'weather_icon_{i+16}.png')
	image_background.paste(weather_image, (weather_image.size[0] * i, 0), weather_image.split()[-1])
# image_background.paste(weather_image_0, weather_image_0.split()[-1])
# image_background.paste(weather_image_12, (weather_image_12.size[0], 0), weather_image_12.split()[-1])
image_background.save('weather_background.png')