#Importing Maya commands 
import maya.cmds as cmd
#Importing a library needed to save/load python objects into/from a file
import pickle
#Importing os.path to check whether the folder entered exists or not
from pathlib import Path
#Importing RegEx, so that we can sort out possible name differences between the original and this file's lights' names
import re

#############################
### EXPORTING STARTS HERE ###
#############################

# Make a class consisting of a light.name and light.linkingInfo
class LightWithLinkingInfo:
    def __init__(self, name, linkingInfo):
        self.name = name
        self.linkingInfo = linkingInfo

def exportLLSettings(window): 

    # Close the dialog box
    cmd.deleteUI(window, window=True)
    
    # Get folder path (shows only folders)
    pathTo = cmd.fileDialog2(fileMode=3, dialogStyle=2)[0]
    print(pathTo)

    # Getting a list of all the light objects in the scene
    allLights = cmd.ls(type=["aiSkyDomeLight","areaLight","spotLight","aiAreaLight","aiLightPortal","aiPhotometricLight","ambientLight","directionalLight","pointLight","volumeLight"])

    # Getting light linking information for a light:
    # cmd.lightlink( query=True, light=allLights[1])

    # Storing light names and light linking info into a list

    allLightsAndLinkingInfo = []

    for x in allLights:
        llInfo = cmd.lightlink(query=True, light=x)
        allLightsAndLinkingInfo.append(LightWithLinkingInfo(x,llInfo))
    
    # Gwt current scene's name:
    sceneName = cmd.file(query=True, sceneName=True, shortName=True)[:-3]
    
    # Saving allLightsAndLinkingInfo into a file to be read later
    with open(f'{pathTo}/{sceneName}-lightLinkingData.pkl', 'wb') as outp:
        pickle.dump(allLightsAndLinkingInfo, outp, pickle.HIGHEST_PROTOCOL)
        
    print(f"########\nLight linking info saved to: (\"{pathTo}/lightLinkingData.pkl\").\nCopy the path between the \"s above and paste it somewhere, bc it will be needed in the second script\n########")


#############################
### IMPORTING STARTS HERE ###
#############################

def importLLSettings(window):

    # Close the dialog box
    cmd.deleteUI(window, window=True)
    
    # Get file path (shows .pkl files and folders)
    basicFilter = "*.pkl"
    pathTo = cmd.fileDialog2(fileFilter=basicFilter, fileMode=1, dialogStyle=2)[0]
        
    # Import light linking info from the exported file
    with open(pathTo, 'rb') as inp:
        allLightsAndLinkingInfoImported = pickle.load(inp)
    
     # Getting a list of all the light objects in the scene
    allLights = cmd.ls(type=["aiSkyDomeLight","areaLight","spotLight","aiAreaLight","aiLightPortal","aiPhotometricLight","ambientLight","directionalLight","pointLight","volumeLight"])
    allGeo = cmd.ls(transforms=True, geometry=True)
    
     # Storing light names and light linking info into a list

    newLightsAndLinkingInfo = []
    
    # Apply imported light linking info to the lights in the current scene
    for x in allLightsAndLinkingInfoImported:
        
        #RegEx expression used for getting new light names:
        thisRegEx = re.compile(f"(.*?:){x.name}")
        newName = list(filter(thisRegEx.match, allLights))
        newLLIlist = []       
        
        for y in x.linkingInfo:
            #RegEx expression used for getting new light linking info:
            thisRegEx = re.compile(f"(.*?:){y}")
            
            newLLI = list(filter(thisRegEx.match, allGeo))
            try:
                newLLIlist.append(newLLI[0])
            except:
                pass
        
        cmd.lightlink (b=True, light=newName, object=allGeo)
        cmd.lightlink (make=True, light=newName, object=newLLIlist)
        print("Light linking settings have been successfully imported!")


# Making a dialog popup prompting the user to choose between importing or exporting LLSettgins
# Then executing the selected export/import function

window = cmd.window( title="Please choose whether to export or import LLSettings?", iconName='Export or import?', widthHeight=(200, 50) )
cmd.columnLayout( adjustableColumn=True )
cmd.button( label='Export', command=("exportLLSettings(window)") )
cmd.button( label='Import', command=("importLLSettings(window)") )
cmd.setParent( '..' )
cmd.showWindow( window )