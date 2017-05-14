import os

for filename in os.listdir("./img"):
	print(os.path.join(".\img", filename))
