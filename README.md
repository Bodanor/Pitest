To create a binary follow those steps bellow :
1) Git clone this repo with this command < git clone https://github.com/Bodanor/Pitest/ >
2) Install Py2app with the following command < pip3 install -U py2app >
3) Install Virtualenv with the following command < pip3 install virtualenv >
4) While beeing in your home directory, run the following command < virtualenv venv --system-site-packages > then < source ven/bin/activate >
5) Go to the folder where the project is located < cd ~/Pitest >
6) Create a setup.py file with the following command < py2applet --make-setup Pitest.py >
7) Finally run this command to create a binary < python setup.py py2app -A >

Note : The binary should be in the same folder as the one you cloned before and the binary is located under the "Dist" folder that was created by Py2app.
