# Automation-server-test

This code provide tests that validate and testing entire tools provided for raster services:

## Deploy:
Run build.sh script to generate docker image of this test suite.

- current version include direct running for raster tests -> will be changed on future

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