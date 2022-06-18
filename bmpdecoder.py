#Mod by Killo
class bmpData:
    def __init__(self,w,h,array):
        self.w = w
        self.h = h
        self.data = array
    def render(self,display,pos):
        pos = list(pos)
        if (pos[0]+self.w > display._size[0]):  pos[0] = display._size[0] -self.w
        if (pos[1]+self.h > display._size[1]):  pos[1] = display._size[1] -self.h 
        display._setwindowloc((pos[0],pos[1]),(pos[0]+self.w - 1,pos[1]+self.h - 1))
        display._writedata(self.data)
    @staticmethod
    def decode(filename,screenSize = (160,80)):
        f=open(filename, 'rb')
        if f.read(2) == b'BM':  #header
            dummy = f.read(8) #file size(4), creator bytes(4)
            offset = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
                depth = int.from_bytes(f.read(2), 'little')
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                    #print("Image size:", width, "x", height)
                    rowsize = (width * 3 + 3) & ~3
                    if height < 0:
                        height = -height
                        flip = False
                    else:
                        flip = True
                    if width > screenSize[0]: width = screenSize[0]
                    if height > screenSize[1]: height = screenSize[1]
                    #display._setwindowloc((posX,posY),(posX+w - 1,posY+h - 1))
                    row = 0
                    buff = bytearray(width*2*height)
                    while row < height:
                        if flip:
                            pos = offset + (height - 1 - row) * rowsize
                        else:
                            pos = offset + row * rowsize
                        if f.tell() != pos:
                            dummy = f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            temp = col*2+row*width*2
                            buff[temp]=(bgr[0]&0xf8|(bgr[1]&0xfc)>>5)
                            buff[temp+1]=((bgr[1]&0x1C)<<3|bgr[2]>>3)
                            col += 1
                        #display._writedata(buff)
                        row += 1
            return bmpData(width,height,buff)
class bmpFileData:
    def __init__(self,w,h,file):
        self.w = w
        self.h = h
        self.data = file
    @staticmethod
    def load(filename):
        f = open(filename+'.rgb565','rb')
        w = int.from_bytes(f.read(2),'big')
        h = int.from_bytes(f.read(2),'big')
        return bmpFileData(w,h,f)
    def render(self,display,pos):
        pos = list(pos)
        if (pos[0]+self.w > display._size[0]):  pos[0] = display._size[0] -self.w
        if (pos[1]+self.h > display._size[1]):  pos[1] = display._size[1] -self.h
        display._setwindowloc((pos[0],pos[1]),(pos[0]+self.w - 1,pos[1]+self.h - 1))
        i = 0
        self.data.seek(4)
        while i<self.h:
            display._writedata(self.data.read(self.w*2))
            i+=1
    def __del__(self):
        self.data.close()
        del self
    @staticmethod
    def decode(filename,newname = None,screenSize = (160,80),biasY = 0):
        f=open(filename, 'rb')
        if f.read(2) == b'BM':  #header
            dummy = f.read(8) #file size(4), creator bytes(4)
            offset = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
                depth = int.from_bytes(f.read(2), 'little')
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                    print("Image size:", width, "x", height)
                    rowsize = (width * 3 + 3) & ~3
                    if height < 0:
                        height = -height
                        flip = False
                    else:
                        flip = True
                    if width > screenSize[0]: width = screenSize[0]
                    if height > screenSize[1]: height = screenSize[1]
                    #display._setwindowloc((posX,posY),(posX+w - 1,posY+h - 1))
                    row = 0
                    if newname == None:
                        buff = open(filename[:-4]+'.rgb565','wb+')#bytearray(width*2*height)
                    else:
                        buff = open(newname+'.rgb565','wb+')#bytearray(width*2*height)
                    buff.write(width.to_bytes(2,'big'))
                    buff.write(height.to_bytes(2,'big'))
                    
                    while row < height:
                        if flip:
                            pos = offset + (height - 1 - row + biasY) * rowsize
                        else:
                            pos = offset + (row + biasY)* rowsize
                        if f.tell() != pos:
                            dummy = f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            buff.write((bgr[0]&0xf8|(bgr[1]&0xfc)>>5).to_bytes(1,'big'))
                            buff.write(((bgr[1]&0x1C)<<3|bgr[2]>>3).to_bytes(1,'big'))
                            col += 1
                        #display._writedata(buff)
                        row += 1
            return bmpFileData(width,height,buff)

