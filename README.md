# AppleStoreTop100Chart

Python application which send request to url found in input/chart_url.txt file,
performs web scraping for received page and output the data into json file into output/ directory.
The url which is scraped is Top 100 free apple store applications.
The url should be one of 'apps.apple.com/us/charts' Apple Store charts urls.

You can run the program by running next script by the Python:

    python src/web_scraping.py
    
You can run the program in Docker container:

1. Building the image from Dockerfile
   Run this command from the main directory of the repository where Dockerfile is found:
   
        docker build -t top100 .
        
2. Run the container from this image (top100):
   instead of d:\tmp - you can choose any directory where output json file will be stored on host 
   machine where docker is running:
   
        docker run -d  -v d:\tmp:/usr/apple_store_top_chart/output  --name=top100 top100
        
Structure of the project:
--------------------------
input - directory for input file
output - directory for output files
src - src python scripts of the project
docs - html documentation describing the source files
Dockerfile - docker file for building the docker container image
requirements.txt - file used for Dockerfile with required modeles which should be installed in Docker container 
