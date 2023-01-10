# job_search


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Some companies did not post their opening roles on job boards and just put them on their website, which is hard to find; for those looking for sponsors, it is time-consuming to check manually. Therefore, this work helps search for a specific job title in the company's career site from a list of company names, cities and types of visas stored in a local machine or database (mySQL).

For example, the public list company on the government website is used:

<img src="https://user-images.githubusercontent.com/114192113/211102932-22cd38ed-4c3d-43eb-b900-5d4004349610.png" alt="drawing" width="700"/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Using ddgr library to search for websites and selenium for scraping data (included data in displayed iframe elements which often are used to list opening jobs). These are 2 main steps.
* ddrg: https://github.com/jarun/ddgr
* selenium: https://pypi.org/project/selenium/

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
### Installation

Clone the repo and go to the project directory
   ```sh
   git clone https://github.com/tamtran4869/job_search.git
   ```
   ```sh
   cd job_search
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage
To run the job_search file, there are 6 arguments need to be specified.

    --db or --file : get data from database (with table name company_list) or local file and all data need to be lowercase (just use 1) (required)

    --job : job title for searching (required)

    --add_term : help ddgr can find the career page (example: career, vacancies, 'job opening', 'current opportunity')

    --city : search by city (if the list company file has this field)

    --rout : search by route (if the list company file has this field)

```sh
python3 job_search.py 
    --file '/data/2022-12-07_-_Worker_and_Temporary_Worker.csv' # or --db 'dbname user password' 
    --job 'analyst' 
    --add_term 'uk career vacancies' 
    --city 'London' #filter by city
    --rout 'Skilled Worker' #filter by type of visa
```
*** Due to the various structures of websites, the results may not be correct 100%, so you can check manually with the generated website list if you want.

*** THANK YOU
<p align="right">(<a href="#readme-top">back to top</a>)</p>

