#!/bin/bash
pip3 install setuptools setuptools_scm
#VER=$(python3 setup.py --version | sed 's/+/./g')
ACR_REGISTRY="http://acrarolibotnonprod.azurecr.io"
ACR_REPOSITORY="automation-server-test"
VER=15
echo $(date):automation-test:$VER

echo version=$VER>version.txt
echo version=$VER>>version_history.txt
echo $version
echo "::set-env name=TAG_NAME::$VER"

docker build --no-cache --network=host -t $ACR_REGISTRY/$ACR_REPOSITORY:$VER
docker push $ACR_REGISTRY/$ACR_REPOSITORY:$VER
