from bs4 import BeautifulSoup
from zipfile import ZipFile
import requests
import getopt
import sys
import os

##                                                   ##
# Fetch all versions avilabvle for given spec number  #
##                                                   ##
def fetch_specs_versions(u,h):
    spec_archive = []
    response = requests.get(u,headers=h)
    if response.status_code == 200:
        html_data = response.text
        soup = BeautifulSoup(html_data, 'html.parser')
        soup.findAll('table')[0].tbody.findAll('tr')

        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            c1 = row.findAll('td')[1].find_all('a')[0].text
            c2 = row.findAll('td')[2].text.strip()
            c3 = row.findAll('td')[3].text.strip()
            if '.' in c1:
                spec_archive.append([c1,c2,c3])
    else:
        print("Error: No spec number found")
        exit()
    return spec_archive    

##                       ##
# List all specs version  #
##                       ##
def show_specs_versions(s_a):
    print("===========================================================")
    
    li = 0
    for li in range(len(s_a)):
        r=""
        r = s_a[len(s_a)-li-1]
    
        print('| ( {:3s})  {:18s}  {:15s}  {:10s} |'.format(str(li+1), r[1], r[0], r[2]))

    print("===========================================================")

def download_spec_file(file_name,url):
    print('Downloading spec : ', fname, " Please wait...")
    ftp_url = url+file_name
    r = requests.get(ftp_url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)
    print('Done')

#################
# MAIN          #
#################
try:
    argv = sys.argv[1:]
    if len(argv) == 0:
        raise Exception

    opts, args = getopt.getopt(argv, "hldn:v:")
    download_spec   = False
    list_specs      = False
    spec_name       = None
    spec_version    = None

    for opt, arg in opts:
        if opt in ['-n']:
            spec_number = arg
            spec_series=str(spec_number.split('.')[0])+'_series'
            
        elif opt in ['-v']:
            spec_version = arg
            
        elif opt in ['-l']:
            list_specs = True
            
        elif opt in ['-d']:
            download_spec = True
            list_specs = False

        elif opt in ['-h']:
            print("get3gppspec <options>")
            print("             -n <spec number>")
            print("             -v <spec version>")
            print("             -l list all versions of given spec number. Must be user with -n")
            print("             -d download spec")
            print("")
            print("Examples:")
            print("1 - To list all versions of a spec number")    
            print("    get3gppspec -l -n 29.503 to list all versions of spec 29.503")
            print("    No need to give version number. Note spec number must be in format xx.yyy means '.' must be there")
            print("")
            print("2 - To download specific version of spec")
            print("    get3gppspec -n 29.503 -v i00 ")
            print("    If no version is give, latest version will be downloaded")
            print("")
            
        else:    
            print("Error: Invalid arguments")
        
        
    
    url     = "https://www.3gpp.org/ftp/Specs/archive/" + spec_series + "/" + spec_number + "/"
    headers ={'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    
    s_archv = fetch_specs_versions(url,headers)
    
    if list_specs:
        show_specs_versions(s_archv)
        
    elif download_spec:
        if spec_version == None :
            print("No version is given so downloading latest one")
            fname=s_archv[len(s_archv)-1][0]
        else:   
            fname = spec_number.translate({ord('.'): None})+'-'+spec_version+'.zip'
        
        download_spec_file(fname, url)
        # Extract zip file and delete zip
        # in case there is problem in extracting, then dont delete zip file
        try:
            with ZipFile(fname, 'r') as zObject:
                zObject.extractall()
            zObject.close()
            os.remove(fname)
        except:
            pass
        
    else:
        pass
            
except:
    print("Please check if spec number is valid and given options are correct")
    print("usage: get3gppspec -h for list of supported option")