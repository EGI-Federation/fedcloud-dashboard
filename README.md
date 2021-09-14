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
