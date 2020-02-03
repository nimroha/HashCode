#! /bin/bash
####
# setup ubuntu environment
# (must have `sudo` installed on machine prior to running script)
####
set -e

export DEBIAN_FRONTEND=noninteractive

function title () {
    echo
    echo "--------------------------------------------------------------------"
    echo "$1"
    echo "--------------------------------------------------------------------"
    echo
}

title "starting setup script"
sudo apt -y upgrade && \
sudo apt -y dist-upgrade && \
sudo apt -y update

title "install some utilities"
sudo -E apt install -y \
    curl \
    desktop-file-utils \
    ecryptfs-utils \
    gdb \
    gedit \
    git \
    git-cola \
    gnupg \
    htop \
    kdiff3 \
    nano \
    openssh-server \
    openssl \
    software-properties-common \
    unzip \
    virtualenv \
    wget \
    xclip


title "install dependencies"
sudo -E apt install -y \
    binutils-arm-linux-gnueabi \
    build-essential \
    cmake \
    dkms \
    freeglut3 \
    freeglut3-dev \
    g++-arm-linux-gnueabi \
    gcc \
    gcc-6 \
    gcc-8 \
    gfortran \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libc6-armel-cross \
    libc6-dev-armel-cross \
    libgtk-3-dev \
    libjpeg-dev \
    libncurses5-dev \
    libpng-dev \
    libspdlog-dev \
    libswscale-dev \
    libtiff-dev \
    libv4l-dev \
    libx264-dev \
    libxmu-dev \
    libxvidcore-dev \
    linux-headers-$(uname -r) \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-pyqt5 \
    python3-tk

title "install python env and pacakges"
virtualenv -p `which python3.6` ~/venv3.6
source ~/venv3.6/bin/activate
pip install --upgrade pip
pip install numpy==1.16.4
if [[ -f requirements.txt ]]; then
    pip install -r requirements.txt
fi

echo '
alias hgrep="history | grep"
alias lgrep="ls | grep"
alias xclip="xclip -i -sel c -f | xclip -i -sel p"
alias cpwd="pwd | xclip"
alias venv="source ~/venv3.6/bin/activate"
' >> ~/.bash_aliases

echo venv >> ~/.bashrc
