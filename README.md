# Facial-Recogmition-Using-Raspi
This project delves into creating a Gate security system that utilizes Facial Recognition System based on Raspberry PI.
I used a Raspi 4B with 2GB of Ram for this project.  The facial recognition code requires a minimum of 1.4 when running, so it's better to have more ram especially if you are using VNC or other similar methods to control the raspi. This project also includes a 4x4 matrix keypad, a buzzer, an LCD display (LCD 1602) and also push buttons to separateoly access whehter to go through the facial recognition or pin access. You can also use push buttons to ring the buzzer. 
The system is also integrated to a Blynk Interface for controlling the system remotely. You can view the livestream from the camera and also open the gate.

I used a servo motor to act as the gate here. You can upgrade it to a large Stepper mototr for rela implentation. Remember the sky is the limit.

Ensure that the program codes are in the same folder when saving the codes.
The latest Raspian OS (Bookworm) requires virtual environments to execute the programs
Use " sudo apt install python3        #To install python
      python -m venv myenv            #To create virtual environment
      source myenv/bin/activate"      #To open the virtual environment. You can use this code to access the virtual environment when you shutdown the raspi in the future.
ALso you need to install the required libraries too.
You can do that by using the code " pip install ___________ " . (Add the name of the library in the dash. 
pip install opencv-python pigpio 

You also need to set the virtual enviroment in thonny idle.
Use image_capture to capture the images. Press space when the image window pops up and after sufficient photos have been taken, press Q to exit.
Use model training to train the model. Just run it in thonny it will create a encodings.pickle file. That is the product of image training. We mainly use HoG (Histogram of Oriented Gradients) to run tha facial recognition instead of CNN, as CNN is very hard on the processing and Ram requirements. 
The facial_recognition_combined2.py is the main code.
To adjust the pin use pin_lock.py
