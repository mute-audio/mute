![mute_top](https://github.com/mute-audio/mute/assets/120294905/8cfdd1db-430b-4641-8053-2148d7120e92)
# [ mute ] 
![Static Badge](https://img.shields.io/badge/-RaspberryPi-A22846?logo=raspberrypi&logoColor=white)
 ![Static Badge](https://img.shields.io/badge/-Raspi_Audio-red) ![Static Badge](https://img.shields.io/badge/-MPD-brightgreen)
 ![Static Badge](https://img.shields.io/badge/GNU_Bash-4EAA25?logo=gnubash&logoColor=white) ![Static Badge](https://img.shields.io/badge/-CSS-1572B6?logo=css3&logoColor=white) ![Static Badge](https://img.shields.io/badge/-HTML-E34F26?logo=html5&logoColor=white) ![Static Badge](https://img.shields.io/badge/license-MIT-blue) 


## Simple Raspi-Audio / MPD Dashboard
[ mute ] is a simple dashboard program for setting up a "RaspberryPi Audio Player" using [MPD (Music Player Daemon)](https://github.com/MusicPlayerDaemon/MPD) and a RaspberryPi.

This program is installed on your RaspberryPi and used as a web app that you control from a browser on a tablet or PC on the same network. The key feature is that this web app is "just" for RaspberryPi audio setup, and does not do any music browsing or playback control. This is a major difference from other raspberry audio distributions such as Volumio and moOde. For song browsing and playback control, you use a combination of MPD client apps installed on your mobile device or PC (e.g. [yaMPC for iOS](https://www.openaudiolab.com/yampc/)).

Why release such a half-baked product?

Because an all-in-one audio distribution does not always have the latest MPD available. Also, because we want to run the Raspi simply as a network audio server and enjoy music with the MPD client application.

If you try to install MPD manually and play sound, you will need a lot of knowledge and skills about Linux OS, commands, and various settings of MPD, and the hurdle of introduction will become higher at once. And you end up having to use the MPD client application to operate a multifunctional audio distribution that is supposed to be complete by itself...

So, let's make something that can easily build a "plain MPD audio server," and this is how [ mute ] was born.

## Install and Update [ mute ]

### Install [ mute ] 

Follow the steps below to install [ mute ].

Step 1 : Create RaspberryPi OS media (SD card)

Step 2 : Download the latest setting file "mute_setting_[DATE].zip"  (Check [here](https://github.com/mute-audio/mute/releases))

Step 3 : Unzip and copy the "mute_setting" folder under /boot of the OS media

Step 4 : Insert the OS media into RaspberryPi and boot.

Step 5 : Connect to RaspberryPi via SSH and type the installation command;
```
cd /boot/firmware/mute_setting && ./install_mute.sh
```
Or in case of installing on a legacy OS;
```
cd /boot/mute_setting && ./install_mute.sh
```
Step 6 : Access RaspberryPi with a browser on PC or tablet

### Update [ mute ] 
Follow the steps below to update [ mute ].

Step 1 : Connect to your [ mute ] via SSH

Step 2 : Download the latest setting file "mute_update_[VERSION].zip" in any directory (Check [here](https://github.com/mute-audio/mute/releases))
```
wget [DOWNLOAD LINK]
```

Step 3 : Unzip the downloaded zip file;
```
sudo unzip mute_update_[VERSION].zip
```
Step 4 : Type the installation command;
```
cd mute_update && ./update_mute.sh
```

### Further information
For more information, [visit [ mute ] site(https://kitamura-design.format.com/mute-en)](https://kitamura-design.format.com/mute-en).

©2024 kitamura_design
