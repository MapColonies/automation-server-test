# Automation-server-test

This code provide tests that validate and testing entire tools provided for Map Colonies services: raster only [for current version]:

### Deploy:
#### Docker:
- Run build.sh script to generate docker image of this test suite.from project directory: [CMD]\
`` ./build.sh``
- Add DUMP_IMAGE=1 param to export .tar file of created image
- Output folder will be created with "generated_dockers.txt" that save current docker image name:tag

- current version include direct running for raster tests -> will be changed on future

#### Wheels and packages:
- This project can be installed as python's package:
    - Install cloned ropo into environment (recommended with virtual env)\
    ``pip install .``\
    It will install to environment all dependencies [On network]
    - To dump package as wheel [from rep root dir - where the setup.py located:\
    ``python3 setup.py sdist bdist_wheel``
*** 
### Raster
 - Exporter tools - server side epic:
   - Export data as valid geoPackages format
   - Export according restricted region size of geoPackage
   - Deletion of old packages after configurable time period -TBD [not implemented yet]
   - Package created on shared folder
   - Download locally package from shared storage
   
   ##### usage:
   1. To run functional testing on exporter tool:\
   ``pytest server_automation/tests/test_exporter_tools.py``
   2. To external debug mode logging run:\
   ``Add the variable <DEBUG_LOGS=True> before previous command``