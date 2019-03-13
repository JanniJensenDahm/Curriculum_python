import sys
import os
import subprocess
import glob
import urllib.request
    
def getApi():
    #Get api-info
    api = urllib.request.urlopen("https://api.github.com/orgs/python-elective-2-spring-2019/repos?per_page=100").read()
    api = api.decode('utf-8')
    #Open api.txt, and write to the file. + create file if it does not exist
    file = open('api.txt', 'w+')
    file.write(api)
    file.close

def getUrls():
    #Open and read file
    apiFile = open('api.txt', 'r')
    #Array for api
    repoUrls = []
    for line in apiFile:
        apiPart = line.split('"')
        index = 0
        for part in apiPart:
            #if part == clone_url add the url to repoUrls[].
            if "clone_url" in part:
                repoUrls.append(apiPart[index +2])    
            index = index + 1
    return repoUrls

def pullRepos():
    #Get urls from api
    urls = getUrls()
    for repoUrl in urls:
        #path is name of repo
        path = repoUrl[49:-4]
        #if path exists pull repo
        if os.path.exists(path):
           os.chdir(path)
           subprocess.run('git pull ' + repoUrl)
           os.chdir('..')
        #else clone repo
        else:
            subprocess.run('git clone ' + repoUrl)

def getReqRead(readmeList):
    # Set() that holds required reading links
    reqReadingList = set()
    #Loop through all readme files
    for readme in readmeList:
        with open(readme) as file:
            for line in file:
                #If the line starts with Required reading add following links to reqReadingList
                if line.startswith("## Required reading"):
                    for line in file:
                        if line.startswith("\n" or "#"):
                            break
                        else:
                            reqReadingList.add(line)
    return reqReadingList

def createMdFile(links):
    #Sort links a-z and 1-9
    sortedList = sorted(links)
    #Open and write to file, + create file if it does not exist
    file = open('Curriculum_RequiredReading.md', 'w+')
    #Save every line in file
    for line in sortedList:
        file.write(line)

def pushMdFile(fileName):
    #If Curriculum_RequiredReading.md exists push to file
    if os.path.exists('.git'):
        subprocess.run('git add ./Curriculum_RequiredReading.md')
        subprocess.run('git commit -m "Updated"')
        subprocess.run('git push --force origin master')
    #Else create and push to file
    else:
        subprocess.run('git init')
        subprocess.run('git add ./Curriculum_RequiredReading.md')
        subprocess.run('git commit -m "Updated readme"')
        subprocess.run('git remote add origin https://github.com/JanniJensenDahm/Curriculum_RequiredReading.git')
        subprocess.run('git push --force -u origin master')

def main():
    #Get api file
    #getApi()
    #Get urls from api file
    getUrls()
    #Get repositories 
    pullRepos()
    #Get readme.md from all repositories
    #Return a list of path names that match '**/readme.md'
    #recursive = true the pattern ** will match any file or directory/subdirectory
    files = glob.glob('**/readme.md', recursive=True)
    #Get required_reading links from readme.md files
    links = getReqRead(files)
    #Create a readme.md with required_reading links
    createMdFile(links)
    #Push file to github
    pushMdFile('Curriculum_RequiredReading')


if __name__ == '__main__':
    main()