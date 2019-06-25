from modules.rgb_camera.module.pi_cam import PiCam
from time import sleep

""" This is only here for legacy reasons, deleting it will be discussed.
if __name__ == "__main__":
	print("[+] Pi Camera test")

	test_cam = PiCamera()
	
	user_width = int(input("set width: "))
	user_height = int(input("set height: "))
	user_framerate = int(input("set framerate: "))
	user_time = int(input("set time to capture for: "))
	

	# configure camera settings
	test_cam.resolution = (user_width, user_height)
	test_cam.framerate = user_framerate

	# capture video
	print("[+] start recording...")
	test_cam.start_recording("test_video.h264")
	test_cam.wait_recording(user_time)
	test_cam.stop_recording()

	print("[!] done...")
"""
