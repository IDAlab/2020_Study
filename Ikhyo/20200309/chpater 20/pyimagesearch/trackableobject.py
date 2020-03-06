class TrackableObject:
    def __init__(self,objectID,centriod):
        self.objectID = objectID
        self.centroids = [centriod]
        self.counted = False