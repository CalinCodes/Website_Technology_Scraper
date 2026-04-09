**Website Technology Scraper**  
    The implementation uses an existing pip package for detecting website technologies(`builtwith`). This way the focus can be on implementing multi threading for processing multiple websites at once, error handling and outputting the reasoning for the choices taken.

*Debate Topics*
- What were the main issues with your current implementation and how would you tackle them?
    A lot of time is spent waiting for invalid domanins or websites that are down. A pre-processing phase where we first check if the website is up before trying to crawl it could improve this dead time. 
- How would you scale this solution for millions of domains crawled in a timely manner (1-2 months)?  
    I would think about a producer-consumer implementation, so a main server would contain a big list of domains, while other machines would run the algorithm on batches of websites requested from the main server and combine the results afterwards. This parallelization is crucial for a large database.    
- How would you discover new technologies in the future?
    While builtwith has a good base of knowledge on current technologies, it is crucial to monitor popular github repos and the top 1k-10k websites in order to have an idea on current technologies and frameworks. This way, new custom tests could be added acting separately to add to what builtwith provides.

*Usage*

- Make a new python virtual environment:  
    `python3 -m venv venv`  
    `source venv/bin/activate`
- Install the necesary pip packages:  
    `pip3 install -r requirements.txt`
- Convert the raw dataset to SQLite(Only for the first run):  
    `python3 process_dataset.py`
- Run the main script:  
    `python3 main.py`

*Output*

A file called `results.json` will be created with technologies found for every website and the reasoning. If an error occurs it states the type of error.