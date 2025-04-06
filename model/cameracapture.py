import time
import cv2
import numpy as np

from model.camera import Camera

selector_list = [
    cv2.CAP_ANY,
    cv2.CAP_MSMF,
    cv2.CAP_DSHOW,
    cv2.CAP_V4L2
]

class CameraCapture():
	def __init__(self, fps=30, width=1600, height=1200, view_window=[1280, 720], index=0, focus=False, reStartTimes=5, videoCaptureAPI=0, exposure=-6):
		self.width = width
		self.height = height
		self.view_window = view_window
		self.index = index
		self.fps = fps
		self.focus = focus
		self.restart_times = reStartTimes
		self.selector = selector_list[videoCaptureAPI]

		self.cap = Camera(index, self.selector)
		self.cap.set_width(self.width)
		self.cap.set_height(self.height)
		self.cap.set_fps(self.fps)
		self.cap.set_exposure(self.exposure)
		
		self.data = []
	
	def open_camera(self):
		self.cap.open()
		
		if not self.cap.isOpened():
			print("Can't open camera")
			exit()
	
	def read_frame(self):
		ret, frame = self.cap.read()

		if not ret:
			if self.restart_times != 0:
				print("Unable to read video frame")
				success = False
				for i in range(1, self.restart_times + 1):
					print(f"reopen {i} times")
					try:
						self.cap.reStart()
						success = True
						break
					except:
						continue
				if not success:
					print("reopen failed")
					return
		
		self.data.append(frame)
		
		return frame
    
	def close_camera(self):
		self.cap.release()

	def collect_data(self, length):
		frames = 0
		
		self.open_camera()
		
		while frames < (length * self.fps):
			self.read_frame()
			
			frames += 1
		
		self.close_camera()

#camera = CameraCapture()
#camera.collect_data(5)
#print(len(camera.data))

#midFrame = len(camera.data) // 2

#cv2.imshow("Sample frame", np.array(camera.data[midFrame]))
#cv2.waitKey(0)

#cv2.destroyAllWindows()
	
	
