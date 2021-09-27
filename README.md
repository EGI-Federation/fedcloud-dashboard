# horizon-aggregator
Proof of concept to gather all OpenStack Horizon endpoints published in the EGI GOCDB

## Installation

Clone this repository:
```
cd /path/to/working/directory
git clone https://github.com/sebastian-luna-valero/horizon-aggregator.git
```

Create a conda environment with requirements:
```
# Download and install conda
cd /path/to/conda/install/folder
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh

# Create conda environment using the environment.yml file
cd /path/to/working/directory/horizon-aggregator/
conda env create -f environment.yml
conda activate horizon-aggregator
```

## Preview
Test whether the query script works:
```
cd /path/to/working/directory/horizon-aggregator/
python find_endpoints.py
```

Test whether the flask app works:
```
cd /path/to/working/directory/horizon-aggregator/
flask run --host=0.0.0.0
```

## Set up with Apache on Ubuntu 20.04

Below are specific steps to make the flask app work behind Apache on Ubuntu 20.04.

First make sure you open port 80. Then install `mod_wsgi` with:
```
sudo apt-get install libapache2-mod-wsgi-py3 apache2
```

Create a dedicated folder for the app:
```
sudo mkdir -p /var/www/common-dashboard
sudo chown cloudadm.cloudadm -R /var/www/common-dashboard/
cd /var/www/common-dashboard/
git clone https://github.com/sebastian-luna-valero/horizon-aggregator.git
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh
cd horizon-aggregator/
conda env create -f environment.yml
```

Configure Apache:
```
sudo a2enmod wsgi
sudo cp apache/horizonaggregator.conf /etc/apache2/sites-available/horizonaggregator.conf
sudo a2ensite horizonaggregator
sudo a2dissite 000-default
sudo systemctl restart apache2
```

The app should now return the list OpenStack Horizon endpoints published in the EGI GOCDB via port `80`.
