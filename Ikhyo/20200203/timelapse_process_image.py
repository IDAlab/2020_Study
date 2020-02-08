from imutils.video import VideoStream
from imutils import paths
import progressbar
import argparse
import cv2
import os

def get_number(imagePath):
        return int(imagePath.split(os.path.sep)[-1][:-4])
ap = argparse.ArgumentParser()
ap.add_argument("-i","--input",required=True,help="Path to the input directory of image files")
ap.add_argument("-o","--output",required=True,help="Path to the output video directory")
ap.add_argument("-f","--fps",type=int,default=30,help="Frames per second of the output video")
args = vars(ap.parse_args())
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
writer = None
imagePaths = list(paths.list_images(args["input"]))
outputFile = "{}.avi".format(args["input"].split(os.path.sep)[2])
outputPath = os.path.join(args["output"],outputFile)
print("[INFO] building {}...".format(outputPath))
widgets = ["Building Video: ", progressbar.Percentage()," ",progressbar.Bar()," ",progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(imagePaths),widgets=widgets).start()
for (i,imagePath) in enumerate(sorted(imagePaths,key=get_number)):
        image = cv2.imread(imagePath)
        if writer is None:
                (H,W) = image.shape[:2]
                writer = cv2.VideoWriter(outputPath,fourcc,args["fps"],(W,H),True)
        writer.write(image)
        pbar.update(i)
print("[INFO] cleaning up...")
pbar.finish()
writer.release()
