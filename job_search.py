
'''
JOB_SEARCH
Check whether the company recruits for the specific job title from a list of companies (with name, city, and type of visa)

"python3 job_search.py 
    --db 'name user password' or --file '/data/2022-12-07_-_Worker_and_Temporary_Worker.csv' #get data from databse or local file and all data need to be lowercase.
    --job 'analyst' --add_term 'uk career vacancies' 
    --city 'London' #filter by city
    --rout 'Skilled Worker' #filter by type of visa"

*** Due to the various structures of websites, the results may not be correct 100%, so you can check manually with the generated website list if you want.
'''

# Import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse
import sys
import time
import mysql.connector
from mysql.connector import Error
import numpy as np
cwd = os.getcwd()
sys.path.append(cwd)

#Get arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='file', type=str, help='Add file of companies')
    parser.add_argument('--db', dest='db', type=str, help='Add database "name user password" to connect data from database', default= None)
    parser.add_argument('--job', dest='job', type=str, help='Add job names')
    parser.add_argument('--city', dest='city', type=str, help='Add city names where you want to search')
    parser.add_argument('--rout', dest='rout', type=str, help='Add type of vise you want to search')
    parser.add_argument('--add_term', dest='add_term', type=str, help='Add additional term for searching more accurate')
    args = parser.parse_args()
    return args

# Get website by company name using ddgr (https://github.com/jarun/ddgr.git)
# Return link website
def get_web(company_name,add_term):
    name = str.lower(company_name.strip().replace("'",""))
    cmd = "python3 "+cwd+"/ddgr "+ "-j '" + name + " " + add_term + "' > " + cwd +"/url.txt"
    os.system(cmd)
    url = open(cwd+"/url.txt")
    web= url.read()
    if web.find("ERROR") != -1:
        web = None
    os.remove(cwd+"/url.txt")
    return web

# Get dataframe of compnay from sql database  (if the company list is stored in database)
# Return dataframe
def get_df_from_db(db,user,password,args):
    company_name, city, county, type_rating, rout= [],[],[],[],[]
    _city = str.lower(args.city)
    _rout= str.lower(args.rout)
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database=db,
                                            user= user,
                                            password= password)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

        if _city and _rout:
            sql_select_Query = 'select * from company_list where lower(rout)="'+_rout+'" and lower(city)="'+_city+'" limit 3'
        elif _city and not _rout:
            sql_select_Query = 'select * from company_list where lower(city)="'+_city+'" limit 3'
        elif not _city and _rout:
            sql_select_Query = 'select * from company_list where lower(rout)="'+_rout+'" limit 3'
        else:
            sql_select_Query = 'select * from company_list limit 3'
 
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            company_name.append(row[0])
            city.append(row[1])
            county.append(row[2])
            type_rating.append(row[3])
            rout.append(row[4])

        df = pd.DataFrame(np.column_stack([company_name, city, county, type_rating, rout]), 
                                columns=['company_name', 'city', 'county', 'type_rating', 'rout'])
        return df
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Check whether the job title is in the content of the website.
# Save file with weblink and checking results in folder results.
def find_term(web, job):
    link = cwd+"/chromedriver_linux64/chromedriver"
    driver = webdriver.Chrome(executable_path= link) #Place save the file
    driver.get(web)

    time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    data_bs4 = soup.find_all("p")
    data = []
    for x in data_bs4:
        data.append(str(x))

    iframes = driver.find_elements_by_tag_name("iframe")
    if iframes:
        for i in iframes:
            try:
                driver.switch_to.frame(i)
            except:
                continue   
            textElements = driver.find_elements_by_xpath("/html/body/div") #Gets all text elements
            for i in textElements:
                data.append(i.text)
                data.append(i.location)
    data = [d for d in data if type(d) is str]
    find_term = str.lower("".join(data)).find(job)
    driver.close()
    if find_term !=-1:
        return True
    else:
        return False

def main():
    count = 0
    #Get arguments from parse
    args= parse_args()
    city = str.lower(args.city)
    rout = str.lower(args.rout)
    add_term = str.lower(args.add_term)

    # Get dataframe list of company from file path
    if args.file !=None:
        file = args.file
        df = pd.read_csv(file)
        df.columns = ['company_name', 'city', 'county', 'type_rating', 'rout']
        df["website"] =0
        df["check_job"]=0

        if city and rout:
            df = df[(df["city"]==city) & (df["rout"]==rout)]
        elif city and not rout:
            df = df[df["city"]==city]
        elif not city and rout:
            df = df[df["rout"]==rout]

    # Get dataframe list of company from database
    if args.db !=None:
        lst = args.db.split(" ")
        db = lst[0]
        user = lst[1]
        password = lst[2]
        df = get_df_from_db(db,user,password,args)
        df["website"] =0
        df["check_job"]=0

    # Get web and search job title
    try:
        for i in range(0,len(df)):
            print(i)
            web=get_web(df.iat[i,0],args.add_term)
            if web.find("indeed.com/cmp/") !=-1:
                web= web + "/jobs"
            if web.find("linkedin.com/")!=-1:
                web = web+"jobs/"

            print ("-----------------------------------------")
            df.iloc[i,df.columns.get_loc('website')]=web
            if web == None:
                df.at[i,"check_job"]=False
                print("Not found any website")
            else:
                print(web)
                check = find_term(web,args.job)
                if check==True:
                    count +=1
                    df.at[i,"check_job"]= True
                    print ("***An %s job found ***" % (args.job))
                else:
                    df.at[i,"check_job"]= False
                    print ("NO %s job found" % (args.job))
                

        #Save resulst
        timestr = time.strftime("%Y%m%d_%H%M%S")
        df.to_csv(cwd + "/result/done_detailed_"+timestr+"_"+args.job+"_"+"_".join(add_term.split(" "))+".csv", index=False)
        print ("******************")
        print("Finishing the list")
        print("%s jobs found" % (count))
        print("Detailed file is saved at %s" % (cwd + "/result/done_detailed_"+timestr+"_"+args.job+"_"+"_".join(add_term.split(" "))+".csv"))
    except(Exception, KeyboardInterrupt):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        df.to_csv(cwd + "/result/stop_detailed_"+timestr+"_"+args.job+"_"+"_".join(add_term.split(" "))+".csv", index=False)
        print ("******************")
        print("Error or KeyboardInterrupt while running")
        print("%s jobs found" % (count))
        print("Detailed file is saved at %s" % (cwd + "/result/stop_detailed_"+timestr+"_"+args.job+"_"+"_".join(add_term.split(" "))+".csv"))
        

if __name__ == "__main__":
    main()
