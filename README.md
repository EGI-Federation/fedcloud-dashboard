# FedCloud dashboard

Proof of concept to gather all OpenStack Horizon endpoints published in the EGI GOCDB.

## Installation

Clone this repository:
```shell
cd /path/to/working/directory
git clone https://github.com/EGI-Federation/fedcloud-dashboard.git
```

Create a conda environment with requirements:
```shell
# Download and install conda
cd /path/to/conda/install/folder
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh

# Create conda environment using the environment.yml file
cd /path/to/working/directory/fedcloud-dashboard/
conda env create -f environment.yml
conda activate horizon-aggregator
```

## Preview
Test whether the query script works:
```shell
cd /path/to/working/directory/fedcloud-dashboard/dashboard/
python find_endpoints.py
```

Test whether the flask app works:
```shell
cd /path/to/working/directory/fedcloud-dashboard/dashboard/
export FLASK_APP=main
flask run --host=0.0.0.0
```

## Use docker

Below are specific steps to make the flask app work using [Apache](https://hub.docker.com/r/ubuntu/apache2).

### Build image

Here are the steps:
```shell
git clone https://github.com/EGI-Federation/fedcloud-dashboard.git
cd fedcloud-dashboard
sudo docker build --no-cache -t dashboard:1.0.0 .
```

### Run container

Here are the steps:
```shell
git clone https://github.com/EGI-Federation/fedcloud-dashboard.git
cd fedcloud-dashboard/dashboard
sudo docker run \
  --name dashboard \
  --detach \
  --publish 80:80 \
  --volume "$(pwd)":/var/www/html \
  dashboard:1.0.0
```

The app should now return the list OpenStack Horizon endpoints published in the EGI GOCDB.

Make sure port 80 is open on the target system!
