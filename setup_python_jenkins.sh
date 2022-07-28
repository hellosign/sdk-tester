#!/bin/bash

echo "***** Getting the external ipaddress"
curl https://ipinfo.io/ip

#####################################################
# Set up Python with packages
#####################################################
echo "***** Adding ppa:deadsnakes/ppa repostiory for Chrome"
sudo add-apt-repository ppa:deadsnakes/ppa
echo "***** Calling apt-get clean"
sudo apt-get clean

echo "***** Calling apt-get update"
PYTHON_VERSION=3.10
sudo apt-get update -y
sudo apt-get install python"$PYTHON_VERSION" -y

#####################################################
# Set up Python3 alternative for the binary
#####################################################
sudo update-alternatives --remove-all python3
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python"$PYTHON_VERSION" 2
sudo update-alternatives --set python3 /usr/bin/python"$PYTHON_VERSION"

echo "***** Python version"
python3 --version
# install pip this way so that we get the correct version and not an old, broken one
sudo apt-get autoremove -y
echo "***** Completed apt-get autoremove"
# need to update distutils to use get-pip
sudo apt-get install --reinstall python"$PYTHON_VERSION"-distutils -y
echo "***** Installed distutils"
# uninstall setuptools from apt-get so that we use the correct one when reinstalling
sudo apt-get remove python3-setuptools -y
echo "***** Uninstalled setuptools"
# install pip this way so that we get the correct version and not an old, broken one
curl -sS https://bootstrap.pypa.io/get-pip.py | python"$PYTHON_VERSION"
# add this to PATH
LOCAL_PATH="/home/ubuntu/.local"
export PATH="$LOCAL_BIN_PATH/bin":$PATH
python3 -m pip install pip -U
python3 -m pip install setuptools -U
which python3
which pip
echo "***** Installing python$PYTHON_VERSION-venv"
sudo apt-get install python"$PYTHON_VERSION"-dev python"$PYTHON_VERSION"-venv -y
echo "***** Creating virtualenv"
python3 -m venv env
echo "***** Activating virtualenv"
source env/bin/activate
python3 -m pip install pip -U
python3 -m pip install setuptools -U
which python3
# add to PYTHONPATH so that hellosign-python-sdk install doesn't fail
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
INSTALL_DIR="$SCRIPT_DIR/../env/lib/python$PYTHON_VERSION/site-packages/"
export PYTHONPATH="$INSTALL_DIR":$PYTHONPATH

#####################################################
# Install everything else
#####################################################

# specific installs for Linux. NOTE: oauth2client isn't installing properly from requirements.txt so explicitly installing
python3 -m pip install authenticator filelock oauth2client xlib unittest2 --ignore-installed six
python3 install_requirements.py install requirements.txt
# patch subunit to avoid buffer/broken runner error happening in Jenkins only.
# Should be safe as this module is not updated anymore.
sed -i 's/stream = stream.buffer/stream = sys.stdout/g' "$INSTALL_DIR/subunit/__init__.py"

# fix for slave going offline
sudo apt-get install -y ethtool
sudo ethtool -K ens3 sg off

sudo apt-get autoremove -y
### SDK ###
python3 -m pip uninstall argparse -y
echo "**** Cloning HelloSign/hellosign-python-sdk ********"
git clone https://github.com/HelloSign/hellosign-python-sdk.git
cd hellosign-python-sdk
echo "**** Checking out openapi ********"
git checkout openapi
git pull origin openapi
echo "**** Installing HelloSign Python SDK ********"
# need to wipe the build dir so that install can create it
sudo rm -rf ./build
cd ..
python3 -m pip uninstall hellosign-python-sdk -y
echo "**** Uninstall existing HelloSign Python SDK Completed ********"
python3 -m pip install ./hellosign-python-sdk

