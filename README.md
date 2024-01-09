# [ mute ] 

### Simple Raspi Audio / MPD Dashboard
[ mute ] is a simple dashboard program for setting up a "RaspberryPi Audio Player" using MPD (Music Player Daemon) and a RaspberryPi.

This program is installed on your RaspberryPi and used as a web app that you control from a browser on a tablet or PC on the same network. The key feature is that this web app is "just" for RaspberryPi audio setup, and does not do any music browsing or playback control. This is a major difference from other raspberry audio distributions such as Volumio and moOde. For song browsing and playback control, you use a combination of MPD client apps installed on your mobile device or PC (e.g. yaMPC for iOS).

Why release such a half-baked product?

Because an all-in-one audio distribution does not always have the latest MPD available. Also, because we want to run the Raspi simply as a network audio server and enjoy music with the MPD client application.

If you try to install MPD manually and play sound, you will need a lot of knowledge and skills about Linux OS, commands, and various settings of MPD, and the hurdle of introduction will become higher at once. And you end up having to use the MPD client application to operate a multifunctional audio distribution that is supposed to be complete by itself...

So, let's make something that can easily build a "plain MPD audio server," and this is how [ mute ] was born.

### Installing [ mute ] 
Follow the steps below to install [ mute ].

Step 1 : Create RaspberryPi OS media (SD card)

Step 2 : Copy the "mute_setting" folder under /boot of the OS media

Step 3 : Insert the OS media into RaspberryPi and boot.

Step 4 : Connect to RaspberryPi via SSH and type the installation command ;
cd /boot/firmware/mute_setting && . /install_mute.sh

Step 5 : Access RaspberryPi with a browser on PC or tablet