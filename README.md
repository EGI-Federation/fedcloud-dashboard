# FedCloud dashboard

A web dashboard which shows all OpenStack Horizon endpoints published in
[EGI GOCDB](https://goc.egi.eu/)

## Installation

This code relies on docker-compose to run 3 containers:

- [traefik](https://traefik.io/traefik/) to provide HTTP proxy and cert
  management
- [homer](https://homer-demo.netlify.app/) for generating the dashboard
- some python code to generate the list of endpoints

The existing docker-compose file assumes you will run the code on a publicly
accessible host with a valid name:

```shell
cd /path/to/working/directory
git clone https://github.com/EGI-Federation/fedcloud-dashboard.git
cd fedcloud-dashboard
docker-compose up --build
```

This will build the container that generates the list of endpoints and start all
the process to make the dashboard available.

## Running locally

If you don't have a publicly accessible host, the easiest is to manually run
dashy and the code to generate the list of endpoints:

First clone the repository:

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

Test whether the query script works:

```shell
cd /path/to/working/directory/fedcloud-dashboard/
python dashboard/update_config.py > assets/config.yml
```

Use the generated `conf.yml` with dashy:

```shell
cd /path/to/working/directory/fedcloud-dashboard/
docker run  \
       -p 8080:8080 \
       -v $PWD/assets:/www/assets/ \
       b4bz/homer:v24.05.1
```

And point your browser to `http://localhost:8080` to see your dashboard running
