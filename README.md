# AppleStoreTop100Chart

Description:
--------------
Python application which send request to url found in input/chart_url.txt file,\
performs web scraping for received page and output the data into json file into output/ directory.\
The url which is scraped is Top 100 free apple store applications.\
The url should be one of 'apps.apple.com/us/charts' Apple Store charts urls.

You can run the program by running next script by the Python:

    python ./src/web_scraping.py .\input\chart_url.txt
    
  Note: you can define other path found below the project directory as input file and pass it as argument to python application.
  
You can run the program in Docker container:

1. Building the image from Dockerfile\
   Run this command from the main directory of the repository where Dockerfile is found:
   
        docker build -t top100 .
        
2. Run the container from this image (top100):\
   instead of d:\tmp - you can choose any directory where output json file will be stored on host \
   machine where docker is running:
   
        docker run -d  -v d:\tmp:/usr/apple_store_top_chart/output  --name=top100 top100
        
Structure of the project:
--------------------------
input - directory for input file\
output - directory for output files\
src - src python scripts of the project\
docs - html documentation describing the source files and tests files\
Dockerfile - docker file for building the docker container image\
requirements.txt - file used for Dockerfile with required modeles which should be installed in Docker container\
test - directory for tests performed by Pytest

The structure of output json file:
-----------------------------------
This is the list of data about of top 100 applications scraped from the input url. The data per application consists of:
- ApplicationName
- ageLimit
- aggregateRating with ratingValue and reviewCount fields
- applicationCategory
- applicationId
- appType : one of "Game App"/"Music App"/"TV App"/"Other" should be "Yes". If it's "Other App" that type field should be updated too
- author
- category
- datePublished
- description
- kidsFriendly : if ageLimit is "4+" then it is kids friendly
- name
- operatingSystem
- rank
