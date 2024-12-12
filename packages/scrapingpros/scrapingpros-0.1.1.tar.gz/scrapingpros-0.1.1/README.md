# **ScrapingPros' client for Python**

The **ScrapingPros' API Client for Python** is the official library to access the ScrapingPros' API from your Python applications. It provides useful features like jobs running retries and convenience functions to improve your experience with the ScrapingPros' API.


## **Installation**
Requires **Python 3.6+**
You can install the package from its [PyPI listing](https://test.pypi.org/project/scrapingpros/). Just by running `pip install scrapingpros` in your terminal. You may need to install requests package too. `pip install requests`

## **Usage**
For usage instructions, check the [documentation on ScrapingPros' Docs](https://console.sprosdata.com/docs).

## **Quick Start**
```python
from scraping_pros import Batch, Project, Job

# Considering we want to work on the project with the ID 64.
PROJECT_ID = 64 # 
# Project must be previously created.
API_KEY = "your-api-key"
 # We create the batch that will hold all the jobs we want to run.
project = Project(api_key=API_KEY, project_id=PROJECT_ID, verbose=True)
first_batch = project.create_batch("first_batch")


# We create a job and append it to the batch, selecting the scrap mode.
url_to_scrape = ["url"]
first_batch.append_jobs(url_to_scrape, ScrapMode.PUPPETEER)

# Puts this job to run.
first_batch.run()

# Retrieves html for all jobs in that batch whenever it finishes running.
data = first_batch.get_data()
```

The package provides tools to manage every aspect of running jobs and retrieving data. It includes functions to easily execute and access data for `Batches` and `Jobs`.

## Automatic Retries
The package automatically retries any operation—such as `run()` or `get_data()`—to handle intermittent issues and improve reliability.

