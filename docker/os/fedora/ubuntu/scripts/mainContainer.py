#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import random
import subprocess
import numpy
import utils
import time
from chrome import Chrome
from firefox import Firefox
import signal

############### Container Class
class Container(object):

    ### Environment variables
    homeFolder = '/home/blink/'
    allPluginsFolder = homeFolder+'plugins/'
    allFontsFolder = homeFolder+'fonts/'
    allBrowsersFolder = homeFolder+'browsers/'

    profileFolder = homeFolder+'profile/'
    dataFile = profileFolder+'data.json'
    encryptedDataFile = dataFile+".gpg"
    updateFile = profileFolder+"update"

    destFontsFolder = '/home/blink/.fonts/'
    destPluginsFolder = '/home/blink/.mozilla/plugins/'

    averageNbFonts = 261.0094
    sdFonts = 91.45935
    averageNbPlugins = 12.6303
    sdPlugins = 5.7451

    ### Init
    def __init__(self):

        #List of plugins
        self.userP = []
        self.pluginsList = []
        self.userPlugins = []
        for root, dirs, files in os.walk(Container.allPluginsFolder):
            for file in files:
                self.pluginsList.append(os.path.abspath(os.path.join(root, file)))
                if file in self.userP :
                    self.userPlugins.append(os.path.abspath(os.path.join(root, file)))

        #List of fonts
        self.fontsList = []
        for root, dirs, files in os.walk(Container.allFontsFolder):
            for file in files:
                self.fontsList.append(os.path.abspath(os.path.join(root, file)))

    ### PLUGINS
    def selectPlugins(self):
        nbRandomPlugins = int(numpy.random.normal(loc=Container.averageNbPlugins,scale=Container.sdPlugins))
        while nbRandomPlugins < 1 :
            nbRandomPlugins = int(numpy.random.normal(loc=Container.averageNbPlugins,scale=Container.sdPlugins))

        randomPluginsList = [file for file in self.pluginsList if file not in self.userPlugins]
        finalPluginsList = list(self.userPlugins)
        if nbRandomPlugins > len(randomPluginsList):
            finalPluginsList = list(self.pluginsList)
        else :
            finalPluginsList.extend(random.sample(randomPluginsList,nbRandomPlugins))

        #We remove old mozilla files to be sure to correctly load plugins
        subprocess.call("find ~/.mozilla -name pluginreg.dat -type f -exec rm {} \;", shell=True)

        #We remove the old plugins and copy the new ones
        subprocess.call("rm -rf "+Container.destPluginsFolder+"*",shell=True)
        for plugin in finalPluginsList:
            subprocess.call(["cp",plugin,Container.destPluginsFolder])

    ### FONTS
    def selectFonts(self):
        nbRandomFonts = int(numpy.random.normal(loc=Container.averageNbFonts,scale=Container.sdFonts))
        while nbRandomFonts < 1:
            nbRandomFonts = int(numpy.random.normal(loc=Container.averageNbFonts,scale=Container.sdFonts))
        finalFontsList = random.sample(self.fontsList,nbRandomFonts)

        #We remove the old fonts, recreate the link to the user fonts and copy the new ones
        subprocess.call("rm -rf "+Container.destFontsFolder+"*",shell=True)
        for font in finalFontsList:
            subprocess.call(["cp",font,Container.destFontsFolder])

    ### BROWSERS
    @staticmethod
    def selectBrowser():
        browsersList = os.listdir(Container.allBrowsersFolder)
        browsersList.remove("extensions")
        return browsersList[random.randint(0,len(browsersList)-1)]

    ### Check existence of data file
    # If the file does not exist, it is created
    # If the file is encrypted, it will be unencrypted
    @staticmethod
    def checkDataFile():
        if os.path.isfile(Container.encryptedDataFile):
            #We decrypt it
            cancelled = False
            while not os.path.isfile(Container.dataFile) and not cancelled:
                res = subprocess.getstatusoutput("gpg2 -d -o "+Container.dataFile+" "+Container.encryptedDataFile)
                if res[0] != 0 and "cancelled" in res[1]:
                    cancelled = True
            subprocess.call("rm "+Container.encryptedDataFile,shell=True)
        elif not os.path.isfile(Container.dataFile):
            jsonData = {"bookmarks":
                            [{"name":"Bookmarks Toolbar","children":[],"type":"folder"},
                             {"name":"Bookmarks Menu","children":[],"type":"folder"},
                             {"name":"Unsorted Bookmarks","children":[],"type":"folder"}],
                        "openTabs":[],
                        "passwords":[],
                        "passwordStorage":"false",
                        "passwordEncryption":"false",
                        "browser":"Firefox"}
            utils.writeJSONDataFile(jsonData,Container.dataFile)

def sigint_handler(signum, frame):
    print("Waiting for data to be saved")

############### Main
def main():
    print("Blink Container Main script")

    #Change the working directory to the Shared folder
    os.chdir(Container.homeFolder)

    if os.path.isfile(Container.updateFile):
        #We update the container
        subprocess.call(["python3","/home/blink/updateContainer.py"])
    else :
        #We create an instance of Container
        blink = Container()

        #We check the Data file with the complete user profile
        blink.checkDataFile()

        #We chose the fonts and the plugins
        blink.selectFonts()
        blink.selectPlugins()

        if blink.selectBrowser() == 'chrome':
            browser = Chrome()
        else :
            browser = Firefox()
        #We import the user profile inside the browser
        browser.importData()

        #We initialise a boolean to indicate if the
        #VM must be shutdown
        shutdown = False

        while not shutdown :
            #We launch the browser
            browserProcess = browser.runBrowser()
            signal.signal(signal.SIGINT, sigint_handler)
            #We wait for either the browsing session to be finished
            while not isinstance(browserProcess.poll(),int):
                time.sleep(1)


            encryption = browser.exportData()

            #Encrypt file if the encryption is activated
            if encryption :
                done = False
                while not done :
                    res = subprocess.getstatusoutput("gpg2 -c --cipher-algo=AES256 "+Container.dataFile)
                    if res[0] == 0 :
                        #If the encryption went well, we removed the unencrypted file
                        subprocess.call("rm "+Container.dataFile,shell=True)
                        done = True
                    elif "cancelled" in res[1]:
                        #If the user cancelled the encryption operation, we do nothing
                        done = True

            #We finish the execution of the script
            shutdown = True

if __name__ == "__main__":
    main()