# Installation and Setup
1. Ensure Python3 is installed
2. Install PyQt6 with `pip3 install pyqt6`
3. Install pyqtgraph with `pip3 install pyqtgraph`
4. Install cv2 with `pip install opencv-python`
5. Install scipy with `pip install scipi`
6. Install requests with `pip install requests`
7. Install firebase with `pip install firebase_admin`

# Running the application
1. Run `python3 app.py` from the root folder of the project

# Code organization
- The project is set up in MVC (model view controller) design where
  - The view handles the UI display and elements
  - The model handles the data types and analysis of information for the application
- Code to run on the raspberry pi is in the /client folder