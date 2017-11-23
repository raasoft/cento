##############################################################################
# 
# @file            cento.py
# @author          Riccardo Ancona
# @date            20/11/2017
# @brief           Batch file to install all the necessary tools to compile
#
# @details         Batch file to install all the necessary tools to compile
##############################################################################

# -- Dependencies for this script --

# sudo apt-get install python-pip
# sudo pip --proxy http://username:pass@proxy:port install --upgrade pip
# sudo pip --proxy http://username:pass@proxy:port install urlgrabber
# sudo pip --proxy http://username:pass@proxy:port install patool
# sudo pip --proxy http://username:pass@proxy:port install pyunpack


# ----------------------------------

import os
import errno
import collections
import hashlib
import tarfile
import contextlib
from pyunpack import Archive

import urllib
import progressbar

import pyunpack
import json




## Tool Configuration

BatchScriptFolder = os.getcwd()
Dependency = collections.namedtuple('Dependency', 'name url md5 download_folder unzip_folder environment_variable environment_variable_path')
dependencyList = []

##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

proxy_json_file='./food.cento'
try:
    proxy_json_data=open(proxy_json_file)
    proxy_data = json.load(proxy_json_data)
    proxy_json_data.close()
    os.environ['http_proxy'] = proxy_data['http_proxy']['url']
    os.environ['https_proxy'] = proxy_data['https_proxy']['url']
except:
    os.environ['http_proxy'] = ""
    os.environ['https_proxy'] = ""

json_file='./litter.cento'
json_data=open(json_file)
data = json.load(json_data)
json_data.close()

for dep in data:
    dependencyList.append(Dependency(name=dep,
        url=data[dep]['url'], 
        md5=data[dep]['md5'], 
        download_folder=data[dep]['download_folder'], 
        unzip_folder=data[dep]['unzip_folder'],
        environment_variable=data[dep]['environment_variable'],
        environment_variable_path=data[dep]['environment_variable_path']))


##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def createMD5(fname):
    hash_md5 = md5(fname)
    with open(fname+".md5", "w") as f:
        f.write(hash_md5)

def untar(fname, outDir):
     tarfile.open(downloadPath).extractall(unzipOutFolder)

def untarzx(fname, outDir):
    with contextlib.closing(lzma.LZMAFile(fname)) as xz:
        with tarfile.open(fileobj=xz) as f:
            f.extractall(outDir)     

def deflate(fname, outDir):
    try:
        Archive(fname).extractall(outDir)
    except pyunpack.PatoolError: 
        print "        WARNING: Cannot unpack " + fname


pbar = None
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def UpdateDependency(dep):
    print "Collecting " + "'" + dep.name + "'"

    basename = os.path.basename(dep.url)
    downloadFolder = dep.download_folder
    downloadPath = downloadFolder +"/"+ basename
    basenameMD5 = os.path.basename(dep.md5)
    downloadMd5Path = downloadFolder +"/"+ basenameMD5
    unzipOutFolder = dep.unzip_folder
    unzipOutPath = ""

    ### Download
    
    # try to understand if we can create the download folder
    try: 
        os.makedirs(dep.download_folder)
        print "Created " + dep.download_folder
    except OSError:
        if not os.path.isdir(dep.download_folder):
            print "    ERROR: Cannot " + dep.download_folder
            raise

    md5IsAvaiable = True

    http_proxy = os.environ.get('http_proxy',"")
    https_proxy = os.environ.get('https_proxy',"")

    proxies = {'http': http_proxy, 'https': https_proxy}
    ug = urllib.FancyURLopener(proxies)

    try:
        f1 = ug.retrieve(dep.md5, downloadPath, show_progress)
        md5IsAvaiable = True
    except:
        print "    Cannot check if the dependency is already installed. Proceeding installing it from scratch."
        md5IsAvaiable = False


    if os.path.isfile(downloadMd5Path) == True and md5IsAvaiable == True:
        print "    The dependency is already installed. Skipping."
    else:

        f2 = ug.retrieve(dep.url, downloadPath, show_progress)
        print "    Saved in " + downloadPath

        ### Deflate

        # check if the unzip folder is specified
        # if no unzip folder specified, just use a default one
        if (unzipOutFolder == ""):
            unzipOutPath = BatchScriptFolder+"/"+ basename

        print "        Unpacking it in " + downloadPath
        deflate(downloadPath, unzipOutFolder)

        createMD5(downloadPath)
        
        ### Environment Vars

        if (dep.environment_variable_path != ""):
            os.environ[dep.environment_variable] = dep.environment_variable_path
        else:
            os.environ[dep.environment_variable] = unzipOutFolder

        print "    Setting envar "+dep.environment_variable+" = "+ \
        os.environ.get(dep.environment_variable, 'Not set')


    print "Done.\n"

#     echo -----------------------------------------------------
#     echo Check and Get %toolName% from artifactory...
#     echo -----------------------------------------------------
#     %wgetFolder%\bin\wget.exe %artifactoryLink%.md5 --user=lol_build --password=lol_build -O %workFolder%\%toolName%.zip.md5
#     CertUtil -hashfile %workFolder%\%toolName%.zip MD5 >test.md5
#     echo Check tools Match expected MD5 CRC
#     set "MD5Calc="
#     for /F "skip=1 delims=" %%i in (test.md5) do if not defined MD5Calc set "MD5Calc=%%i"
#     set MD5Calc=%MD5Calc: =%
#     echo %MD5Calc%
#     set /p MD5FromArt=<%workFolder%\%toolName%.zip.md5
#     echo %MD5FromArt%
#     if %MD5Calc%==%MD5FromArt% (
#     echo %toolName% is up to date
#     ) ELSE (
#          echo "%toolName% - get up to date tool"
#         RMDIR /S /Q %~1
#         %wgetFolder%\bin\wget.exe %artifactoryLink% --user=lol_build --password=lol_build -O %workFolder%\%toolName%.zip 
#         #move /Y %~1.zip 
#         %unzipFolder%\bin\unzip.exe -o %workFolder%\%toolName%.zip -d %unzipOutFolder%
#     )
#     echo.


print "### Cento ###\n\n"
print "Mheow! Cento is going out to catch some dependencies.\n\n"

for dep in dependencyList:
    UpdateDependency(dep)
    
print "Cento goes back to sleep. Meohw!"
