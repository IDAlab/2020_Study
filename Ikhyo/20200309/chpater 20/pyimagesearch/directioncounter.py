import  numpy as np

class DirectionCounter:
    def __init__ (self,dirctionMode, X,Y):
        self.X=X
        self.Y=Y
        self.directionMode =dirctionMode
        self.totalUp =0
        self.totalDown = 0
        self.totalRight = 0
        self.totalLeft = 0
        self.direction = ""
    def find_direction(self,to,centroid):
        if self.directionMode == "horizontal":
            x = [c[0] for c in to.centroids]
            delta = centroid[0] - np.mean(x)
            if delta < 0:
                self.direction = "left"
            elif delta > 0:
                self.direction = "right"
        elif self.directionMode =="vertical":
            y = [c[1] for c in to.centroids]
            delta = centroid[1] - np.mean(y)
            if delta < 0:
                self.direction ="up"
            elif delta > 0:
                self.direction = "down"

    def count_object(self, to,centroid):
        output = []
        if self.directionMode == "horizontal":
            leftofcenter = centroid[0] < self.x
            if self.direction == "left" and leftofcenter:
                self.totalLeft+=1
                to.counted = True
            elif self.direction == "right" and not leftofcenter:
                self.totalRight += 1
                to.counted = True
            output  = [("Left",self.totalLeft),("Right",self.totalRight)]
        elif self.directionMode == "vertical":
            aboveMiddle = centroid[1] < self.Y
            if self.direction == "up" and aboveMiddle:
                self.totalUp += 1
                to.counted = True
            elif self.direction == "down" and not aboveMiddle:
                self.totalDown += 1
                to.counted = True
            output = [("up",self.totalUp),("down",self.totalDown)]
        return output
