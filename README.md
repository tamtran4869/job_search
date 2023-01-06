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
Helping to search a specific job title and check it career site of company from ist of company name, city and type of visa.

For example, the published list company in government website is used:

<img src="https://user-images.githubusercontent.com/114192113/211102932-22cd38ed-4c3d-43eb-b900-5d4004349610.png" alt="drawing" width="700"/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Using library ddgr to search for websites and selenium for scraping data. These are 2 main steps.
* ddrg: https://github.com/jarun/ddgr
* selenium: https://pypi.org/project/selenium/

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


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

    --db or --file : get data from databse or local file and all data need to be lowercase (just use 1) (required)

    --job : job title for searching (required)

    --add_term : help ddgr can find the career page (example: career, vacancies, 'job opening', 'current opportunity')

    --city : search by city (if the list company file has this field)

    --rout : search by route (if the list company file has this field)

```sh
python3 job_search.py 
    --db 'name user password' # or --file '/data/2022-12-07_-_Worker_and_Temporary_Worker.csv' (get data from databse or local file and all data need to be lowercase.)
    --job 'analyst' 
    --add_term 'uk career vacancies' 
    --city 'London' #filter by city
    --rout 'Skilled Worker' #filter by type of visa
```
*** Due to the various structures of websites, the results may not be correct 100%, so you can check manually with the generated website list if you want.
*** 
<p align="right">(<a href="#readme-top">back to top</a>)</p>

