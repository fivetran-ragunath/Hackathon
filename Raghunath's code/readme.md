Convert Postman Collection to CCD :

This script allows you to convert a Postman Collection of API calls into a CCD (Coil Connector Definition) file. The CCD file contains the appropriate code for each endpoint in the Postman Collection.

Prerequisites :

Python 3.9 or later installed on your system.
Postman Collection file (`postman_collection.json`) containing API calls with examples for each endpoint. Ensure the file is stored in the same folder as this script.

Instructions :

1. Install the required Python libraries: sys, json, pandas.

`pip install pandas`

2. Open a terminal or command prompt and navigate to the folder containing the json_2_ccd.py file and the postman_collection.json file.

3. Run the script by executing the following command:

`python3.9 json_2_ccd.py`

This command will execute the script and generate the output.clj file with the appropriate CCD.

Find the generated output.clj file in the same folder. This file will contain the code for each endpoint in the Postman Collection.

Notes :
Ensure that the Postman Collection file (`postman_collection.json`) is correctly formatted and contains valid API calls with examples for each endpoint. Otherwise, the script may produce unexpected results.

If you encounter any errors or issues during the execution of the script, make sure that you have fulfilled all the prerequisites and that the required libraries are installed correctly.

