#open test1.txt
from PIL import Image
with open('para.txt', 'r') as f:
    lines = f.readlines()
line = lines[0].split(' ')
resx = int(line[1])
resy = int(line[0])
print(resx, resy)
im = Image.new('RGB', (resx, resy), (0,0,0))


for index,line in enumerate(lines[1:]):
    line = line.split(' ')
    #remove empty strings
    line = list(filter(None, line))
    #print(index/resx, line)
    if len(line) !=5:
        continue

    

    try:
        im.putpixel((int(line[-1]),int(line[-2])), (int(line[0]),int(line[1]),int(line[2])))
    except:
        print(line)
    
im.save('testPara.png')

