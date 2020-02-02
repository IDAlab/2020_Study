from imutils.video import VideoStream
from itertools import cycle
from pprint import pprint
import time
import cv2

global vs
 
def get_picam_setting(output=False):
	global picamSettings
	global vs
	currentPicamSetting ={}

	if output:
		print("[INFO] reading from settings...")
	for attr in picamSettings.keys():
		currentPicamSetting[attr] = getattr(vs.camera,attr)
	if output :
		pprint(currentPicamSettings)
	picamSettings=currentPicamSettings
	return currentPicamSettings


def get_single_picam_setting(setting):
	currentPicamSettings = get_picam_setting()
	return currentPicamsettings[setting]


def _set_picam_setting(**kwargs):
	global vs
	vs.stop()
	time.sleep(0.25)
	vs =Videostream(usePicamer=True,**kwargs).start()
	time.sleep(1.5)
	print("[INFO] success")

def set_picam_setting(**kwargs):
	global picamSettings
	global vs
	print("[INFO] reading settings...")
	currentPicamSettings = get_picam_setting()
	for (attr,value) in kwargs.items():
		print("[INFO] changing {} from {} to {} ".format(attr,currentPicamSettings[attr],value))
		currentPicamSettings[attr]=value
	attrsToDel = []

	for attr in currentPicamSEttings.keys():
		if currentPIcamSettings[attr]==None:
			attrsToDel.append(attr)
	for attr in attrsToDel:
		currentPicamSettings.pop(attr)
	kwargs=currentPicamSettings
	_set_picam_setting(**kwargs)


vs = VideoStream(usePicamera = True).start()
time.sleep(2.0)
awbModes=["off","auto","sunlight","cloudy","shade","tungsten","fluorescent","flash","horizon"]
isoModes=[0,100,200,320,400,500,640,800,1600]

isoModesPool = cycle(isoModes)
awbModesPool = cycle(awbModes)
picamSettings = {
	"awb_mode" : None,
	"awb_gains": None,
	"brightness": None,
	"color_effects": None,
	"contrast": None,
	"drc_strength": None,
	"exposure_compensation": None,
	"exposure mode": None,
	"flash_mode" : None,
	"hflip": None,
	"image_denoise": None,
	"image_effect": None,
	"image_effect_params": None,
	"iso": None,
	"meter_mode" : None,
	"rotation": None,
	"saturation": None,
	"sensor_mode" : None,
	"sharpness": None,
	"shutter_speed" : None,
	"vflip": None,
	"video_denoise": None,
	"video_stabilization": None,
	"zoom": None
}
while True :
	frame = vs.read()
	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1)
	if key ==ord("q"):
		break
	elif key == ord("w"):
		awbMode = get_single_picam_setting("awb_mode")
		set_picam_setting(awb_mode=next(awbModesPool))
	elif key == ord("i"):
		iso = get_single_picam_setting("iso")
		set_picam_setting(iso=next(isoModesPool))

	elif key == ord("b"):
		brightness = get_single_picam_setting("brightness")
		brightness += 1
		set_picam_setting(brightness=brightness)
	elif key == ord("d"):
		brightness = get_single_picam_setting("brightness")
		brightness -= 1
		set_picam_setting(brightness=brightness)
	elif key == ord("r"):
		get_picam_settings(output=True)
	elif key == ord("c"):
		set_picam_setting(brightness=30,iso=800,awb_mode="cloudy",vflip=True)

vs.stop()
cv2.destroyAllWindows()
