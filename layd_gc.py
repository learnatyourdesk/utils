## Learnatyourdesk

import getopt
import subprocess
import sys
import time

import requests
from bs4 import BeautifulSoup

##                                                   ##
# Prepare a list of all urls for a given user         #
##                                                   ##
def _extract_repos(git_user):

    page_counter = 1
    git_url_list = []    
    eof_page = False

    while not eof_page:

        temp_l = []
        
        print('\nExtrating repositories urls from page ', page_counter, ', ', end=' ')
        git_url = 'https://github.com/'+git_user+'?page='+str(page_counter)+'&tab=repositories'

        page = requests.get(git_url)
        soup = BeautifulSoup(page.content, "html.parser")

        for h in soup.find_all('h3' , {'class':'wb-break-all'} ):

            gr_url = 'https://github.com/'+str(list(h)[1]).split()[1].split('"')[1]
            temp_l.append(gr_url)
            
        if len(temp_l) == 0:
            print('End of page or no repository found')
            eof_page = True
            
        else:
            print('Total repositories found ', str(len(temp_l)))
            git_url_list.extend(temp_l)
            page_counter = page_counter +1

    return git_url_list


##                                                     ##
# Function to clone all git repositories based on list  #
# prepared by function _extract_repos(repo_name)
##                                                     ##
def _clone_repos(l_uris):
        
    for gr in l_uris:
        cmd = 'git clone '+gr
        print(cmd)
        print('')
        print('(',l_uris.index(gr)+1,')','-' * 100)
        print('Cloning repo : ', gr)
        returned_value = subprocess.call(cmd, shell=True)  
        if returned_value == 0:
            print('Cloning Status: SUCCESS')
        else:
            print('Cloning Status: FAILED')

    
##                                                   ##
# Function to display usage of tools                  #
##                                                   ##
def usage():
    
    print('')
    print('Usage:')
    print('To list all repositories')
    print('  python layd_gc.py -l <git user name without quite>')
    print('  For example to list all repositories under learnatyourdesk')
    print('  python layd_gc.py -l learnatyourdesk')
    print('')
    print('To clone all repositories')
    print('  python layd_gc.py -c <git user name without quite>')
    print('  For example to clone all repositories under learnatyourdesk')
    print('  python layd_gc.py -c learnatyourdesk')
    print('')
    print('Note: Repositories will be cloned under same directory where command is executed')
          
##                                                   ##
## Comman Message                                     #
##                                                   ##
def copyright_msg():
    print('\nCopyright (C) 2023 LearnAtYourDesk')
    print('Free to use and distribute')
    


##                                                   ##
# Main function                                       #
##                                                   ##                
def main():
    
    copyright_msg()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:l:d:")

    except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            usage()
            sys.exit(2)
        
    rn=None          # Setting variable rn, repo name as None
    list_repo=False  # Setting list repos flag to False
    clone_repo=False # Clone all repose
    delete_repo=False# Delete all downloaded reposes for a user
    
    for opt, arg in opts:
        if opt == '-l':
            list_repo = True
            rn = arg
            
        elif opt == '-c':
            clone_repo = True
            rn = arg
            
        else:
            usage()
        
    if list_repo:   
        
        l_repo = _extract_repos(rn)
        print('\nRepositories under ', rn)
      
        if len(l_repo) == 0:
            print('None')
            print('Look like there is no git user like ',rn)
        else:
            for gr in l_repo:
                print('(',l_repo.index(gr)+1,') -> ',gr)    
            
            print('Total ',len(l_repo),' repositories to clone' )
        
    if clone_repo:    
        l_repo = _extract_repos(rn)
        if len(l_repo) == 0:
            print('\nLook like there is no git user like ',rn)
        else:
            print('Total ',len(l_repo),' repositories to clone' )
            _clone_repos(l_repo)

    if not list_repo and not clone_repo:
        usage()

##                                                   ##
# Calling MAIN function                               #
##                                                   ##
if __name__ == "__main__":
    main() 