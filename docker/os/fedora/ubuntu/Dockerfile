FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y && apt-get install -y wget djview-plugin browser-plugin-packagekit browser-plugin-spice browser-plugin-vlc gxineplugin kopete-plugin-thinklight kpartsplugin mozplugger rhythmbox-mozilla totem-mozilla x2goplugin xine-plugin gecko-mediaplayer gnupg2 sqlite3 libpango1.0-0 sudo python3 python3-numpy libnss3 \
        libgconf-2-4 libasound2  pulseaudio \
        python-software-properties software-properties-common \
        && add-apt-repository -y ppa:ubuntu-mozilla-security/ppa && apt-get update && apt-get upgrade -y && apt-get install -y flashplugin-nonfree && apt-get clean

RUN wget https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb
RUN dpkg -i google-talkplugin_current_amd64.deb
RUN sudo ln -sf /lib/x86_64-linux-gnu/libudev.so.1 /usr/lib/libudev.so.0
RUN rm -rf /usr/share/mozilla/extensions/*

RUN mkdir -p /home/blink/profile/
RUN mkdir /home/blink/ldpreload/
RUN mkdir /home/blink/.fonts/
RUN mkdir -p /home/blink/.mozilla/plugins/
RUN mkdir /home/blink/plugins/
RUN mv /usr/lib/mozilla/plugins/* /home/blink/plugins/ && mv /home/blink/plugins/flashplugin-alternative.so /usr/lib/mozilla/plugins

RUN wget http://amiunique.irisa.fr/fontsUbuntu.tar.gz && tar -C /usr/share/fonts/ -xf fontsUbuntu.tar.gz && rm fontsUbuntu.tar.gz
ADD scripts/* /home/blink/
ADD updateContainer.py /home/blink/

