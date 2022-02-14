sudo apt install ffmpeg libsdl2-2.0-0 adb wget \
                 gcc git pkg-config meson ninja-build libsdl2-dev \
                 libavcodec-dev libavdevice-dev libavformat-dev libavutil-dev \
                 libusb-1.0-0 libusb-1.0-0-dev
git clone https://github.com/Genymobile/scrcpy
cd scrcpy
./install_release.sh

# v4l2loopback
sudo apt install v4l2loopback-dkms
sudo modprobe v4l2loopback  # To create a v4l2 device:

# To start scrcpy using a v4l2 sink:
scrcpy --v4l2-sink=/dev/video2 --no-display