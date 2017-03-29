from PIL import Image
img = Image.open("set21_4.jpeg")
width,height = img.size
k = width/10
l = height/8
for i in range(0,height-l,l):
	for j in range(0,width-k,k):
		img2 = img.crop((i, j, i + l, j + k))
		img2.save("img"+str(int(i/l))+str(int(j/k))+".jpg")
