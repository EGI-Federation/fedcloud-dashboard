#!/var/www/common-dashboard/conda-install/envs/horizon-aggregator/bin/python
import sys
sys.path.insert(0, '/var/www/common-dashboard/conda-install/envs/horizon-aggregator/lib/python3.9/site-packages/')
sys.path.insert(0, '/var/www/common-dashboard/horizon-aggregator/')

from wsgi import app as application
