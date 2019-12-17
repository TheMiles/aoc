import numpy as np



class Field(object):

    def __init__(self):
        self.c      = np.array([[2]])
        self.offset = np.array([0,0])
        self.track  = {}

    def setTrackedPosition(self, name, pos):
        self.track[name] = pos+self.offset

    def getTrackedPosition(self, name):
        return self.track[name]

    def getStringList(self):
        l = []
        for y in range(self.c.shape[0]):
            c = []
            for x in range(self.c.shape[1]):
                p = np.array([y,x])
                c.append(self.getContent(p-self.offset))
            l.append(c)
        return l

    def getAdjacentValues(self, pos):
        adj = [
            np.array([-1, 0]),
            np.array([ 1, 0]),
            np.array([ 0,-1]),
            np.array([ 0, 1])
        ]

        result = []
        for a in adj:
            nextPos = pos+a
            result.append((nextPos, self.getValue(nextPos)))

        return result

    def getContent(self, pos):
        return self.getValue(pos)

    def getValue(self, pos):
        p = pos+self.offset
        if np.less(p,0).any() or np.greater_equal(p,self.c.shape).any(): return 0
        return self.c[tuple(p)]

    def setValue(self, pos, value):
        p = pos+self.offset

        # print("setValue",p,pos,self.offset,self.c.shape)
        if np.less(p,0).any() or np.greater_equal(p,self.c.shape).any:
            self.growField(p)
            p = pos+self.offset
            # print("afterGrow",p,pos,self.offset,self.c.shape)

        self.c[tuple(p)] = value
        # print("field now",self.c)

    def growField(self,pos):

        height, width = self.c.shape
        if pos[1]<0:
            d = abs(pos[1])
            self.c = np.concatenate((np.zeros(d*height,dtype=np.uint8).reshape(height,d),self.c),axis=1)
            width += d
            self.offset[1] += d
            for t in self.track.values():
                t[1] += d
        elif pos[1]>=width:
            d = pos[1]-width+1
            self.c = np.concatenate((self.c,np.zeros(d*height,dtype=np.uint8).reshape(height,d)),axis=1)
            width += d

        if pos[0]<0:
            d = abs(pos[0])
            self.c = np.concatenate((np.zeros(d*width,dtype=np.uint8).reshape(d,width),self.c),axis=0)
            height += d
            self.offset[0] += d
            for t in self.track.values():
                t[0] += d
        elif pos[0]>=height:
            d = pos[0]-height+1
            self.c = np.concatenate((self.c,np.zeros(d*width,dtype=np.uint8).reshape(d,width)),axis=0)
            height += d


class ContentField(Field):
        def __init__(self,content):
            Field.__init__(self)
            self.content = content

        def convertContentToValue(self, c):
            value = None
            if c in self.content:
                value = self.content.index(c)
            return value

        def countContent(self, c):
            v = self.convertContentToValue(c)
            return len(list(filter(lambda x:v==x, self.c.flatten())))


        def getContent(self, pos):
            return self.content[self.getValue(pos)]

        def setContent(self, pos, content):
            v = self.convertContentToValue(content)
            if v is not None:
                self.setValue(pos,v)

        def getAdjacentContent(self, pos):
            return [ (v[0],self.content[v[1]]) for v in self.getAdjacentValues(pos) ]

