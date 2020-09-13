import requests
import re 
from bs4 import BeautifulSoup
import datetime
import julian
from colorama import init
from termcolor import colored

def convert_to_jd(datetime_tuple):
    # time = (2019, 12, 31, 0, 0, 0)
    d = datetime.datetime(*datetime_tuple)
    return julian.to_jd(d)

def get_planet_data(toi_names): 
    url = "https://exofop.ipac.caltech.edu/tess/gototoitid.php"
    payload = 'toi='
    headers = {
    'Origin': 'https://exofop.ipac.caltech.edu',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    data = []
    
    for name in toi_names:
        try:
            response = requests.request("POST", url, headers=headers, data = payload+name)
            # save_response(response,name)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find("tbody")
            tr = table.find_all("tr")[1]
            td = table.find_all("td")

            response = response.text
            ra = re.search("\d+\.\d+&deg",response).group(0)[:-4]
            dec = re.search("[+|-]\d+\.\d+&deg",response).group(0)[:-4]
            tyc_name = re.search("TYC\s.+\-\d,",response).group(0)[:-1]
            print(dec)
            planet = []
            planet.extend([name.upper(), ra, dec, tyc_name])
            tmp = [td[3].text, td[4].text, td[7].text]  # epoch,period,duration
            tmp = [ i[:i.find(" ")-1] for i in tmp]
            planet.extend(tmp)

            data.append(planet)
            print("   TOI",name,"=",planet)

        except Exception as e:
            print(e)
            print("Failed for: ",name)

    #             0    1   2       3       4       5       6
    # data  = [ name, ra, dec, tyc_name, epoch, period, duration]
    print()
    return data

if __name__ == "__main__":
    print(get_planet_data(["toi1005"]))