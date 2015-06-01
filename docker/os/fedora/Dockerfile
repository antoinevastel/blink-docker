FROM fedora:21

RUN yum localinstall -y --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
RUN yum update -y && yum install -y alsa-plugins-pulseaudio pavucontrol pulseaudio pulseaudio-libs pulseaudio-libs pulseaudio-module-gconf pulseaudio-module-x11 pulseaudio-module-zeroconf pulseaudio-utils \
    PackageKit-browser-plugin djview4-plugin esteid-browser-plugin freewrl-plugin gnome-chemistry-utils-mozplugin gnome-shell gxine-mozplugin kopete kpartsplugin mozplugger npapi-vlc npapi-vlc-gtk nspluginwrapper rhythmbox spice-xpi x2goplugin xine-plugin gecko-mediaplayer gnupg2 pinentry-gtk sudo python3 python3-numpy \
    flash-plugin && yum clean all
RUN wget http://dl.google.com/linux/direct/google-talkplugin_current_x86_64.rpm
RUN yum install -y google-talkplugin_current_x86_64.rpm --nogpgcheck
RUN ln -sf /usr/lib64/libudev.so.1 /usr/lib64/libudev.so.0

RUN mkdir -p /home/blink/profile/
RUN mkdir /home/blink/ldpreload/
RUN mkdir /home/blink/.fonts/
RUN mkdir -p /home/blink/.mozilla/plugins/
RUN mkdir /home/blink/plugins
RUN mv /usr/lib64/mozilla/plugins/* /home/blink/plugins/

RUN yum install -y tar && wget http://amiunique.irisa.fr/fontsFedora.tar.gz && tar -C /usr/share/fonts/ -xf fontsFedora.tar.gz && rm fontsFedora.tar.gz
ADD ubuntu/scripts/*.py /home/blink/
ADD updateContainer.py /home/blink/
