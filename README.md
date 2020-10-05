Nikolai Kyrychenko Test Task DataForest

# LAUNCH
To launch parser you need:
  1. Install all packages via "pip install requirements.txt"
  2. Change your settings in config.py (chromedriver location, time delay, etc.)
  3. Run main.py

# COMPLETED MISSIONS
1. Scrape data from all regions of website (https://iwilltravelagain.com/):
    - Name (title)
    - Category
    - Location
    - Website

2. Implement multiprocessing or multithreading.

# HOW THE MISSION WAS COMPLETED
1. With the following steps:
    - First of all, scraper searches for the regions that are on the website with "region_extractor" function.
    - Function returns a list of links to each region.
    - For each region launches a funnel of steps.
    - First step is to open a page via selenium and through clicking on the "next page" button scrape all information through pages.
    NOTE: The first page scraped separately as "while loop" will search until the "next page" button becomes inactive. That means that each loop must start from clicking to a "next page" button, in this case, we will skip the first page before any info will be scrapped.
    - The next step will be extracting all information that we'll need from each activity article. That was implemented by "activity_info_extractor" function which scrapes this information (decodes it as there could be some symbols) and adds a dictionary to the SHARED_LIST of processes.
    - For each process will be created CSV file with the name of the region. Every loop finishes with writing the new scraped page into a row of CSV file via "save_csv" function.
    - After all processes will be finished all csv files will be merged into excel file "result.xlsx" via "csv_merger" function.

2. Scraping info from the region page starts in the separate process for the each region.

# OTHER FEATURES
1. Implemented "loguru" to save all logs into info.log file. File will be containing all exceptions if they will appear and information related to the scraped articles.
2. Delay between scraping pages in one process can be changed (default - 5 sec), not recommend to set delay lower than 3 seconds, as it might finish with an IP ban.

# THANKS FOR THE PROVIDED TEST TASK
