####
import clr
import os
import sys
clr.AddReference('System')
clr.AddReference('UI.Scripting')
clr.AddReference('UI.BusinessLogic')
clr.AddReference('UI.Interfaces')
clr.AddReference('UI.Settings')
clr.AddReference('IN_UserScripts')
from System import *
from System.Collections.Generic import *
from UI.Scripting import *
from IN_UserScripts import *
from IN_UserScripts.Actions import *
from IN_UserScripts.Actions.Base import *
from IN_UserScripts.Actions.Alignments import *
from IN_UserScripts.Actions.Features import *
from IN_UserScripts.Actions.Instruments import *
from IN_UserScripts.Actions.PlayActions import *
from IN_UserScripts.Actions.Reporting import *
from IN_UserScripts.Actions.Graphics import *
from IN_UserScripts.Actions.Analysis import *
from IN_UserScripts.Actions.CAD import *
from IN_UserScripts.Actions.ImportExport import *
from IN_UserScripts.Actions.EditOperations import *
from IN_UserScripts.Actions.FileOperations import *
from IN_UserScripts.Actions.TreeOperations import *
from IN_UserScripts.Data import *
from IN_UserScripts.Data.Base import *

IN_SetScriptUnits()

def AL0GEOM0(HightolPar, LowtolPar):
    HightolPar = HightolPar
    LowtolPar = LowtolPar
    #Generate User Frame on First Roller With Primary Axis As Base Line, secondary as lvl frame, origin as ref cyl cardinal point
    #GET ALL OBJECTS IN JOB TREE AND ADD ONLY GEOMETRY FEATURES TO LIST
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    #CONSTRUCT REFRENCE FRAME WITH Z LEVEL, Z AONG BASE REF LINE, ORIGIN AT FIRST ROLLER CENTER
    Cylinders =[]
    Lines = []
    Cardinals = []
    for feature in objectlist:
        if "Ref" in feature.GetActualPath() and "Cylinder" in feature.GetActualPath() and not "Points" in feature.GetActualPath():
            RefCylinderName = IN_Cylinder(feature.GetActualPath())
            Cylinders.append(RefCylinderName)
        if "Ref" in feature.GetActualPath() and "Cylinder" in feature.GetActualPath() and "Points" in feature.GetActualPath():
            CardinalPointName = IN_Point(feature.GetActualPath())
            Cardinals.append(CardinalPointName)
        if "Ref" in feature.GetActualPath() and "Line" in feature.GetActualPath():
            RefLineName = IN_Line(feature.GetActualPath())
            Lines.append(RefLineName)
    #COUNT NUMBER OF ROLLERS IN JOB FOR GRAPHICS ON REPORT PAGE
    global Num_Rollers
    Num_Rollers = len(Cylinders)
    #CREATE COORDINATE FRAME
    RefCyl = str(Cylinders[0])
    RefCylsplit = RefCyl.split('/')
    RefCylName = Cylinders[0]
    RefLine = str(Lines[0])
    RefLinesplit = RefLine.split('/')
    RefLineName = Lines[0]
    RefCard = str(Cardinals[0])
    RefCardplit = RefCard.split('/')
    RefCardName = Cardinals[0]
    cmd0 = IN_AddCoordinateFrame(None,None,"RefrenceRollerFrame",False,False,None,None,None)
    cmd0.Run()
    cmd1 = IN_Copy(List[str](["Level Frame"]),"RefrenceRollerFrame/Input/Secondary Axis",False,-1)
    cmd1.Run()  
    cmd2 = IN_Copy(List[str]([str(RefLineName)]),"RefrenceRollerFrame/Input/Primary Axis",False,-1)
    cmd2.Run()
    cmd3 = IN_Copy(List[str]([str(RefCardName)]),"RefrenceRollerFrame/Input/Origin",False,-1)
    cmd3.Run()
    cmd4 = IN_SetWorkingFrame("RefrenceRollerFrame/RefrenceRollerFrame Actual")
    cmd4.Run()
    #CHECK ALL ROLLERS FOR SQUARNESS TO BASE LINE (X AXIS OF FRAME)
    counter = 2
    axiscounter = 1
    #CONSTRUCT AXIS LINE OBJECTS IN TREE FOR EACH ROLLER
    for feature in objectlist:
        if "Cylinder" in feature.GetActualPath() and not "Points" in feature.GetActualPath():
            #CONSTRUCT A CYLINDER SCRIPT OBJECT TO USE
            path = feature.GetActualPath()
            cylindername = IN_Cylinder(feature.GetActualPath())
            #CREATE ALL CYLINDER AXIS' 
            linename = "CylinderAxis_" + str(axiscounter)
            axiscounter +=1 
            #ADD AXISLINE ELEMENT
            cmd6 = IN_AddLineFeature(None,None,linename,True,True)
            cmd6.Run()
            holder = linename + "/Input"
            #ADD CYLINDER AS INPUT TO AXIS LINE
            cmd7 = IN_Copy(List[str]([str(cylindername)]),holder,False,-1)
            cmd7.Run()

    #GET BEGIN AND END OF EACH AXIS AND FIND DIFFERENCE FOR END POINT TO MOVE
    #GET RX AND RZ FROM EACH CYLINDER MEASURED
    namelist =[]
    BeginList=[]
    EndList=[]
    BeginX =[]
    BeginY=[]
    BeginZ=[]
    EndX=[]
    EndY=[]
    EndZ=[]
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    i = int(0)
    counter = int(2)
    for feature in objectlist:
            if "CylinderAxis" in feature.GetActualPath():
               namelist.append(feature.GetActualPath())
               #CONSTRUCT A Line SCRIPT OBJECT TO USE
               Axisname = IN_Line(feature.GetActualPath())
               #BEGIN COORD
               Begin = Axisname.BeginCoordinate
               BeginList.append(Begin)
               BeginStr = str(BeginList[i])
               BeginStr2 = BeginStr.split(',')
               x = BeginStr2[0]
               BeginX.append(x)
               y = BeginStr2[1]
               BeginY.append(y)
               z = BeginStr2[2]
               BeginZ.append(z)
               #END COORD
               End = Axisname.EndCoordinate
               EndList.append(End)
               EndStr = str(EndList[i])
               EndStr2 = EndStr.split(' ')
               x = EndStr2[0]
               EndX.append(x)
               y = EndStr2[1]
               EndY.append(y)
               z = EndStr2[2]
               EndZ.append(z)
               #INC i
               i+=1
    
    #X CHANGE
    i=0
    changex = []
    for coord in BeginX:
        BX = BeginX[i]
        BXClean = float(BX[0:12])
        EX = EndX[i]
        EXClean = float(EX[0:12])
        CHANGEX = EXClean - BXClean
        changex.append(CHANGEX)
        i+=1

    #Y CHANGE
    i=0
    changey = []
    for coord in BeginY:
        BY = BeginY[i]
        BYClean = float(BY[0:12])
        EY = EndY[i]
        EYClean = float(EY[0:12])
        CHANGEY = EYClean - BYClean
        changey.append(CHANGEY)
        i+=1

    #Z CHANGE
    i=0
    changez = []
    for coord in BeginZ:
        BZ = BeginZ[i]
        BZClean = float(BZ[0:12])
        EZ = EndZ[i]
        EZClean = float(EZ[0:12])
        CHANGEZ = EZClean - BZClean
        changez.append(CHANGEZ)
        i+=1

    #NEED ADJUSTMENTS BEFORE FINAL REPORTING??????
    Flagx = 0
    Flagy = 0
    Flagz = 0
    for entry in changex:
        if float(entry) > float(HightolPar) or float(entry) < float(LowtolPar):
            Flagx +=1
    for entry in changez:
        if float(entry) > float(HightolPar) or float(entry) < float(LowtolPar):
            Flagz +=1

    #IF RETURN ADJUSTMENTS NEEDED BACK TO MAIN PY
    global return_dict
    return_dict = {}
    #if Flagx >0 or Flagz>0:
    counter = 3
    i=0
        #NOTE FOR SARAH LATER I PUT THE LABEL OF THE DIRECTION AS -X ON PURPOSE
        #ANY DIRCTION TRANSFORMATIONS WILL BE DONE IN THE BACKROUND DON'T FIGHT WITH INSPIRE TO TRANSFORM FRAMES AROUND TO MATCH EACHOTHER
    for entry in changex:
        return_dict[i] = (str(namelist[i]), str(changez[i]), str(changey[i]), str(changex[i]))
        i+=1
        counter+=1
    return(Flagx, Flagy, Flagz, return_dict,Num_Rollers)

#REF ROLLER SQUARE TO BASE OTHER ROLLERS PARALLEL TO REF ROLLER
def AL1GEOM0(HightolPar, LowtolPar):
    HightolPar = float(HightolPar)
    LowtolPar = float(LowtolPar)
    print("Running AL1GEOM0")
    #Generate User Frame on First Roller With Primary Axis As LEVEL FRAME, secondary as BASE LINE, origin as ref cyl cardinal point TO CHECK FIRST ROLLER SQUARENESS
    #GET ALL OBJECTS IN JOB TREE AND ADD ONLY GEOMETRY FEATURES TO LIST
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    #CONSTRUCT REFRENCE FRAME WITH Z LEVEL, X AONG BASE REF LINE, ORIGIN AT FIRST ROLLER CENTER
    Cylinders =[]
    Lines = []
    Cardinals = []
    for feature in objectlist:
        if "Ref" in feature.GetActualPath() and "Cylinder" in feature.GetActualPath() and not "Points" in feature.GetActualPath():
            RefCylinderName = IN_Cylinder(feature.GetActualPath())
            Cylinders.append(RefCylinderName)
        if "Ref" in feature.GetActualPath() and "Cylinder" in feature.GetActualPath() and "Points" in feature.GetActualPath():
            CardinalPointName = IN_Point(feature.GetActualPath())
            Cardinals.append(CardinalPointName)
        if "Ref" in feature.GetActualPath() and "Line" in feature.GetActualPath():
            RefLineName = IN_Line(feature.GetActualPath())
            Lines.append(RefLineName)
    RefCyl = str(Cylinders[0])
    RefCylsplit = RefCyl.split('/')
    RefCylName = Cylinders[0]
    RefLine = str(Lines[0])
    RefLinesplit = RefLine.split('/')
    RefLineName = Lines[0]
    RefCard = str(Cardinals[0])
    RefCardplit = RefCard.split('/')
    RefCardName = Cardinals[0]
    cmd0 = IN_AddCoordinateFrame(None,None,"RefrenceRollerFrame",False,False,None,None,None)
    cmd0.Run()
    cmd1 = IN_Copy(List[str](["Level Frame"]),"RefrenceRollerFrame/Input/Secondary Axis",False,-1)
    cmd1.Run()  
    cmd2 = IN_Copy(List[str]([str(RefLineName)]),"RefrenceRollerFrame/Input/Primary Axis",False,-1)
    cmd2.Run()
    cmd3 = IN_Copy(List[str]([str(RefCardName)]),"RefrenceRollerFrame/Input/Origin",False,-1)
    cmd3.Run()
    cmd4 = IN_SetWorkingFrame("RefrenceRollerFrame/RefrenceRollerFrame Actual")
    cmd4.Run()

    #REF ROLLER SQUARE TO BASE LINE??????
    #CONSTRUCT AXIS LINE FOR REF CYLINDER
    for feature in objectlist:
        if "Cylinder" in feature.GetActualPath() and "Ref" in feature.GetActualPath() and not "Points" in feature.GetActualPath():
            #CONSTRUCT A CYLINDER SCRIPT OBJECT TO USE
            path = feature.GetActualPath()
            cylindername = IN_Cylinder(feature.GetActualPath())
            #CREATE ALL CYLINDER AXIS' 
            linename = "Ref Axis" 
            #ADD AXISLINE ELEMENT
            cmd6 = IN_AddLineFeature(None,None,linename,True,True)
            cmd6.Run()
            holder = linename + "/Input"
            #ADD CYLINDER AS INPUT TO AXIS LINE
            cmd7 = IN_Copy(List[str]([str(cylindername)]),holder,False,-1)
            cmd7.Run()

    #GET BEGIN AND END OF REF AXIS AND FIND DIFFERENCE FOR END POINT TO MOVE
    namelist =[]
    BeginList=[]
    EndList=[]
    BeginX =[]
    BeginY=[]
    BeginZ=[]
    EndX=[]
    EndY=[]
    EndZ=[]
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    i = int(0)
    counter = int(2)
    for feature in objectlist:
            if "Ref Axis" in feature.GetActualPath():
               global Axisname
               namelist.append(feature.GetActualPath())
               #CONSTRUCT A Line SCRIPT OBJECT TO USE
               Axisname = IN_Line(feature.GetActualPath())
               #BEGIN COORD
               Begin = Axisname.BeginCoordinate
               BeginList.append(Begin)
               BeginStr = str(BeginList[i])
               BeginStr2 = BeginStr.split(',')
               x = BeginStr2[0]
               BeginX.append(x)
               y = BeginStr2[1]
               BeginY.append(y)
               z = BeginStr2[2]
               BeginZ.append(z)
               #END COORD
               End = Axisname.EndCoordinate
               EndList.append(End)
               EndStr = str(EndList[i])
               EndStr2 = EndStr.split(' ')
               x = EndStr2[0]
               EndX.append(x)
               y = EndStr2[1]
               EndY.append(y)
               z = EndStr2[2]
               EndZ.append(z)
               #INC i
               i+=1
    #X CHANGE
    i=0
    changexr = []
    for coord in BeginX:
        BX = BeginX[i]
        BXClean = float(BX[0:12])
        EX = EndX[i]
        EXClean = float(EX[0:12])
        CHANGEX = EXClean - BXClean
        changexr.append(CHANGEX)
        i+=1
    #Y CHANGE
    i=0
    changeyr = []
    for coord in BeginY:
        BY = BeginY[i]
        BYClean = float(BY[0:12])
        EY = EndY[i]
        EYClean = float(EY[0:12])
        CHANGEY = EYClean - BYClean
        changeyr.append(CHANGEY)
        i+=1
    #Z CHANGE
    i=0
    changezr = []
    for coord in BeginZ:
        BZ = BeginZ[i]
        BZClean = float(BZ[0:12])
        EZ = EndZ[i]
        EZClean = float(EZ[0:12])
        CHANGEZ = EZClean - BZClean
        changezr.append(CHANGEZ)
        i+=1
    #FIRST ROLLER NEED ADJUSTMENTS TO BE SQUARE TO BASE LINE??????
    global FlagxRef
    global FlagyRef
    global FlagzRef
    FlagxRef = 0
    FlagyRef = 0
    FlagzRef = 0
    for entry in changexr:
        if float(entry) > HightolPar or float(entry) < LowtolPar:
            FlagxRef +=1
    for entry in changezr:
        if float(entry) > HightolPar or float(entry) < LowtolPar:
            FlagzRef +=1

    
    #*************************************************#
    #ARE ALL OTHER ROLLERS PARALLEL TO FIRST?
    #CREATE A FRAME WITH Z LEVEL AND -Y POINTED ALONG CYLINDER AXIS INSTEAD OF +X ALONG BASE LINE, AND ORIGIN ON REF CYLINDER CARDINAL POINT STILL
    #CREATE FRAME PLACEHOLDER CALLED FIRST ROLLER REF
    cmd0 = IN_AddCoordinateFrame(None,None,"FirstRollerRefFrame",False,False,None,None,None)
    cmd0.Run()
    cmd1 = IN_Copy(List[str](["Level Frame"]),"FirstRollerRefFrame/Input/Secondary Axis",False,-1)
    cmd1.Run()  
    cmd2 = IN_Copy(List[str]([str(Axisname)]),"FirstRollerRefFrame/Input/Primary Axis",False,-1)
    cmd2.Run()
    cmd3 = IN_Copy(List[str]([str(RefCardName)]),"FirstRollerRefFrame/Input/Origin",False,-1)
    cmd3.Run()
    cmd4 = IN_SetWorkingFrame("FirstRollerRefFrame/FirstRollerRefFrame Actual")
    cmd4.Run()

#REST OF ROLLERS CALCS 

#CHECK ALL ROLLERS FOR SQUARNESS TO FIRST ROLLER
    counter = 2
    axiscounter = 1
    #CONSTRUCT AXIS LINE OBJECTS IN TREE FOR EACH ROLLER
    for feature in objectlist:
        if "Cylinder" in feature.GetActualPath() and not "Points" in feature.GetActualPath() and not "Ref" in feature.GetActualPath():
            #CONSTRUCT A CYLINDER SCRIPT OBJECT TO USE
            path = feature.GetActualPath()
            cylindername = IN_Cylinder(feature.GetActualPath())
            #CREATE ALL CYLINDER AXIS' 
            linename = "CylinderAxis_" + str(axiscounter)
            axiscounter +=1 
            #ADD AXISLINE ELEMENT
            cmd6 = IN_AddLineFeature(None,None,linename,True,True)
            cmd6.Run()
            holder = linename + "/Input"
            #ADD CYLINDER AS INPUT TO AXIS LINE
            cmd7 = IN_Copy(List[str]([str(cylindername)]),holder,False,-1)
            cmd7.Run()

    #GET BEGIN AND END OF EACH AXIS AND FIND DIFFERENCE FOR END POINT TO MOVE
    #GET RX AND RZ FROM EACH CYLINDER MEASURED
    namelist =[]
    BeginList=[]
    EndList=[]
    BeginX =[]
    BeginY=[]
    BeginZ=[]
    EndX=[]
    EndY=[]
    EndZ=[]
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    i = int(0)
    counter = int(2)
    for feature in objectlist:
            if "CylinderAxis" in feature.GetActualPath():
               namelist.append(feature.GetActualPath())
               #CONSTRUCT A Line SCRIPT OBJECT TO USE
               Axisname = IN_Line(feature.GetActualPath())
               #BEGIN COORD
               Begin = Axisname.BeginCoordinate
               BeginList.append(Begin)
               BeginStr = str(BeginList[i])
               BeginStr2 = BeginStr.split(',')
               x = BeginStr2[0]
               BeginX.append(x)
               y = BeginStr2[1]
               BeginY.append(y)
               z = BeginStr2[2]
               BeginZ.append(z)
               #END COORD
               End = Axisname.EndCoordinate
               EndList.append(End)
               EndStr = str(EndList[i])
               EndStr2 = EndStr.split(' ')
               x = EndStr2[0]
               EndX.append(x)
               y = EndStr2[1]
               EndY.append(y)
               z = EndStr2[2]
               EndZ.append(z)
               #INC i
               i+=1
    
    #X CHANGE
    i=0
    changex = []
    for coord in BeginX:
        BX = BeginX[i]
        BXClean = float(BX[0:12])
        EX = EndX[i]
        EXClean = float(EX[0:12])
        CHANGEX = EXClean - BXClean
        changex.append(CHANGEX)
        i+=1

    #Y CHANGE
    i=0
    changey = []
    for coord in BeginY:
        BY = BeginY[i]
        BYClean = float(BY[0:12])
        EY = EndY[i]
        EYClean = float(EY[0:12])
        CHANGEY = EYClean - BYClean
        changey.append(CHANGEY)
        i+=1

    #Z CHANGE
    i=0
    changez = []
    for coord in BeginZ:
        BZ = BeginZ[i]
        BZClean = float(BZ[0:12])
        EZ = EndZ[i]
        EZClean = float(EZ[0:12])
        CHANGEZ = EZClean - BZClean
        changez.append(CHANGEZ)
        i+=1

    #NEED ADJUSTMENTS BEFORE FINAL REPORTING??????
    global Flagx
    global Flagy
    global Flagz
    Flagx = 0
    Flagy = 0
    Flagz = 0
    global return_dict
    return_dict = {}
    numrolls = len(changex)
    for entry in changey:
        if float(entry) > HightolPar or float(entry) < LowtolPar:
            Flagy +=1
    for entry in changez:
        if float(entry) > HightolPar or float(entry) < LowtolPar:
            Flagz +=1
    #if Flagx> 0 or Flagy>0 or Flagz>0 or FlagxRef>0 or FlagyRef>0 or FlagzRef>0:
    i= 0
    j= 1
    print("im here")
    for entry in changex:
        return_dict[0] = (("Reference Roller"), str(changexr[0]), str(changeyr[0]), str(changezr[0]))
        return_dict[j] = (str(namelist[i]), str(changey[i]), str(changex[i]), str(changez[i]))
        i+=1
        j+=1
        counter+=1
    return(Flagx, Flagy, Flagz, return_dict,numrolls)


#REF Roller Floating and All Other Rollers Parallel To Ref Roller
def AL2GEOM0(HightolPar, LowtolPar):
    HightolPar = float(HightolPar)
    LowtolPar = float(LowtolPar)

    #CONSTRUCT AXIS LINE FOR REF CYLINDER
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    Cardinals = []
    for feature in objectlist:
        if "Ref" in feature.GetActualPath() and "Cylinder" in feature.GetActualPath() and "Points" in feature.GetActualPath():
            CardinalPointName = IN_Point(feature.GetActualPath())
            Cardinals.append(CardinalPointName)   
        if "Cylinder" in feature.GetActualPath() and "Ref" in feature.GetActualPath() and not "Points" in feature.GetActualPath():
            #CONSTRUCT A CYLINDER SCRIPT OBJECT TO USE
            path = feature.GetActualPath()
            cylindername = IN_Cylinder(feature.GetActualPath())
            #CREATE ALL CYLINDER AXIS' 
            linename = "Ref Axis" 
            #ADD AXISLINE ELEMENT
            cmd6 = IN_AddLineFeature(None,None,linename,True,True)
            cmd6.Run()
            holder = linename + "/Input"
            cmd7 = IN_Copy(List[str]([str(cylindername)]),holder,False,-1)
            cmd7.Run()           

    RefCardName = Cardinals[0]
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    i = int(0)
    counter = int(2)
    for feature in objectlist:
            if "Ref Axis" in feature.GetActualPath():
               global Axisname
               #CONSTRUCT A Line SCRIPT OBJECT TO USE
               Axisname = IN_Line(feature.GetActualPath())
    #*************************************************#
    #ARE ALL OTHER ROLLERS PARALLEL TO FIRST?
    #CREATE A FRAME WITH Z LEVEL AND , X ALONG FIRST ROLLER, AND ORIGIN ON REF CYLINDER CARDINAL POINT STILL
    #CREATE FRAME PLACEHOLDER CALLED FIRST ROLLER REF
    cmd0 = IN_AddCoordinateFrame(None,None,"FirstRollerRefFrame",False,False,None,None,None)
    cmd0.Run()
    cmd1 = IN_Copy(List[str](["Level Frame"]),"FirstRollerRefFrame/Input/Secondary Axis",False,-1)
    cmd1.Run()  
    cmd2 = IN_Copy(List[str]([str(Axisname)]),"FirstRollerRefFrame/Input/Primary Axis",False,-1)
    cmd2.Run()
    cmd3 = IN_Copy(List[str]([str(RefCardName)]),"FirstRollerRefFrame/Input/Origin",False,-1)
    cmd3.Run()
    cmd4 = IN_SetWorkingFrame("FirstRollerRefFrame/FirstRollerRefFrame Actual")
    cmd4.Run()

#REST OF ROLLERS CALCS 

#CHECK ALL ROLLERS FOR SQUARNESS TO FIRST ROLLER
    counter = 2
    axiscounter = 1
    #CONSTRUCT AXIS LINE OBJECTS IN TREE FOR EACH ROLLER
    for feature in objectlist:
        if "Cylinder" in feature.GetActualPath() and not "Points" in feature.GetActualPath() and not "Ref" in feature.GetActualPath():
            #CONSTRUCT A CYLINDER SCRIPT OBJECT TO USE
            path = feature.GetActualPath()
            cylindername = IN_Cylinder(feature.GetActualPath())
            #CREATE ALL CYLINDER AXIS' 
            linename = "CylinderAxis_" + str(axiscounter)
            axiscounter +=1 
            #ADD AXISLINE ELEMENT
            cmd6 = IN_AddLineFeature(None,None,linename,True,True)
            cmd6.Run()
            holder = linename + "/Input"
            #ADD CYLINDER AS INPUT TO AXIS LINE
            cmd7 = IN_Copy(List[str]([str(cylindername)]),holder,False,-1)
            cmd7.Run()
    #GET BEGIN AND END OF EACH AXIS AND FIND DIFFERENCE FOR END POINT TO MOVE
    #GET RX AND RZ FROM EACH CYLINDER MEASURED
    namelist =[]
    BeginList=[]
    EndList=[]
    BeginX =[]
    BeginY=[]
    BeginZ=[]
    EndX=[]
    EndY=[]
    EndZ=[]
    objects = IN_GetTypedObjects("Features")
    objects.Run()
    objectlist = []
    for i in objects.Items:
        if type(i) == IN_Feature:
            objectlist.append(i)
    i = int(0)
    counter = int(2)
    for feature in objectlist:
            if "CylinderAxis" in feature.GetActualPath():
               namelist.append(feature.GetActualPath())
               #CONSTRUCT A Line SCRIPT OBJECT TO USE
               Axisname = IN_Line(feature.GetActualPath())
               #BEGIN COORD
               Begin = Axisname.BeginCoordinate
               BeginList.append(Begin)
               BeginStr = str(BeginList[i])
               BeginStr2 = BeginStr.split(',')
               x = BeginStr2[0]
               BeginX.append(x)
               y = BeginStr2[1]
               BeginY.append(y)
               z = BeginStr2[2]
               BeginZ.append(z)
               #END COORD
               End = Axisname.EndCoordinate
               EndList.append(End)
               EndStr = str(EndList[i])
               EndStr2 = EndStr.split(' ')
               x = EndStr2[0]
               EndX.append(x)
               y = EndStr2[1]
               EndY.append(y)
               z = EndStr2[2]
               EndZ.append(z)
               #INC i
               i+=1
    #X CHANGE
    i=0
    changex = []
    for coord in BeginX:
        BX = BeginX[i]
        BXClean = float(BX[0:12])
        EX = EndX[i]
        EXClean = float(EX[0:12])
        CHANGEX = EXClean - BXClean
        changex.append(CHANGEX)
        i+=1

    #Y CHANGE
    i=0
    changey = []
    for coord in BeginY:
        BY = BeginY[i]
        BYClean = float(BY[0:12])
        EY = EndY[i]
        EYClean = float(EY[0:12])
        CHANGEY = EYClean - BYClean
        changey.append(CHANGEY)
        i+=1

    #Z CHANGE
    i=0
    changez = []
    for coord in BeginZ:
        BZ = BeginZ[i]
        BZClean = float(BZ[0:12])
        EZ = EndZ[i]
        EZClean = float(EZ[0:12])
        CHANGEZ = EZClean - BZClean
        changez.append(CHANGEZ)
        i+=1
    #NEED ADJUSTMENTS BEFORE FINAL REPORTING??????
    global Flagx
    global Flagy
    global Flagz
    Flagx = 0
    Flagy = 0
    Flagz = 0
    for entry in changey:
        if float(entry) > HightolPar or float(entry) < LowtolPar:
            Flagy +=1
    for entry in changez:
        if float(entry) > HightolPar or float(entry) < LowtolPar:
            Flagz +=1
    #if Flagx> 0 or Flagy>0 or Flagz>0 or FlagxRef>0 or FlagyRef>0 or FlagzRef>0:
    global return_dict
    return_dict = {}
    i= 0
    for entry in changex:
        return_dict[i] = (str(namelist[i]), str(changey[i]), str(changez[i]), str(changex[i]))
        i+=1
    numRolls = len(BeginZ)
    return(Flagx, Flagy, Flagz, return_dict,numRolls)

def AL0GEOM1(): 
    #All Rollers Square to Base Line INPUT GEOMETRY IS ALL CIRCLES
    print("AL0GEOM1")