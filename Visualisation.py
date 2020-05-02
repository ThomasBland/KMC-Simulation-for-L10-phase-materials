from vpython import *
import numpy as np
from PIL import ImageGrab
import random
import time

NoXUCs = 5
NoYUCs = 5
NoZUCs = 5
FeFraction = 0.5
LatticeConstant = int(5)
Temperature = 973

def SaveSystem(AtomCoords, AtomTypes, NearestNeighbourDictionary):
    AtomCoordsSaveFile = open("AtomCoords.txt", "w")
    AtomTypesSaveFile = open("AtomTypes.txt", "w")
    NeighbourDictionarySF = open("NeighbourDictionary.txt", "w")
    
    for i in range(0,len(AtomCoords)):
        AtomCoordsSaveFile.write(str(AtomCoords[i]) + "\n")
        AtomTypesSaveFile.write(str(AtomTypes[i]) + "\n")
        NeighbourDictionarySF.write(str(NearestNeighbourDictionary[str(AtomCoords[i])]) + "\n")
                
    AtomCoordsSaveFile.close()
    AtomTypesSaveFile.close()
    NeighbourDictionarySF.close()

def LoadSystem():
    AtomCoordsSaveFile = open("AtomCoords.txt", "r")
    AtomTypesSaveFile = open("AtomTypes.txt", "r")
    NeighbourDictionarySF = open("NeighbourDictionary.txt", "r")

    AtomCoords = list()
    AtomTypes = list()
    LatticeDict = {}
    NearestNeighbourDictionary = {}

    AtomCoordsFileContents = AtomCoordsSaveFile.readlines()
    AtomTypesFileContents = AtomTypesSaveFile.readlines()
    NeighbourDictionaryFC = NeighbourDictionarySF.readlines()

    for i in range(0,len(AtomCoordsFileContents)):
        AtomCoord = AtomCoordsFileContents[i].replace("<", "")
        AtomCoord = AtomCoord.replace(">", "")
        AtomCoord = AtomCoord.replace("\n", "")
        AtomCoord = AtomCoord.split(",")
        AtomCoord = vector(float(AtomCoord[0]), float(AtomCoord[1]), float(AtomCoord[2]))
        AtomCoords.append(AtomCoord)
        
        AtomTypes.append(int(AtomTypesFileContents[i]))

        #Nearest neighbour dictionary
        NeighbourDict = NeighbourDictionaryFC[i].replace("\n", "")
        NeighbourDict = NeighbourDict.replace(">", "")
        NeighbourDict = NeighbourDict.replace("[", "")
        NeighbourDict = NeighbourDict.replace("]", "")
        NeighbourDict = NeighbourDict.split("<")

        ListToAppendToNND = list()
        
        for j in range(1,13): #Note this is because the first thing in the list is just a ''
            OneParticularVector = NeighbourDict[j].split(", ")
            ListToAppendToNND.append(vector(float(OneParticularVector[0]), float(OneParticularVector[1]), float(OneParticularVector[2])))

        NearestNeighbourDictionary[str(AtomCoord)] = ListToAppendToNND

        # Lattice dict
        LatticeDict[str(AtomCoord)] = int(AtomTypes[i])

    return AtomCoords, AtomTypes, NearestNeighbourDictionary, LatticeDict
    
    
def DrawStructure(AtomCoords, AtomTypes):
    for i in range(0,len(AtomCoords)):
        ball = sphere() # Create a sphere
        if AtomTypes[i] == 0:
            ball.color = color.blue
        elif AtomTypes[i] == 2:
            ball.color = color.red
        else:
            ball.color = color.white
        ball.pos = AtomCoords[i]
    
def PullNearestNeighbours(AIQ, LatticeDict, LatticeConstant, AtomCoords, AtomTypes):
    #AIQ = Atom in question
    XExtreme = AtomCoords[-1].x
    YExtreme = AtomCoords[-2].y
    ZExtreme = AtomCoords[-1].z
    
    #Nearest Neighbour 1 AIQ + (-1/2,0,+1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)
    if AIQTU.x == 0:
        AIQTU.x = XExtreme + LatticeConstant*1/2
            
    if AIQTU.z == ZExtreme:
        AIQTU.z = -LatticeConstant*1/2

    NN1 = AIQTU + LatticeConstant*vector(-1/2,0,+1/2)
    
    #NN2 AIQ + (0,+1/2,+1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.z == ZExtreme:
        AIQTU.z = -LatticeConstant*1/2
            
    if AIQTU.y == YExtreme:
        AIQTU.y = -LatticeConstant*1/2
        
    NN2 = AIQTU + LatticeConstant*vector(0,+1/2,+1/2)
    
    #NN3 AIQ + (+1/2,0,+1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.z == ZExtreme:
        AIQTU.z = -LatticeConstant*1/2
            
    if AIQTU.x == XExtreme:
        AIQTU.x = -LatticeConstant*1/2
        
    NN3 = AIQTU + LatticeConstant*vector(+1/2,0,+1/2)
    
    #NN4 AIQ + (0,-1/2,+1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.z == ZExtreme:
        AIQTU.z = -LatticeConstant*1/2
            
    if AIQTU.y == 0:
        AIQTU.y = YExtreme + LatticeConstant*1/2            
    
    NN4 = AIQTU + LatticeConstant*vector(0,-1/2,+1/2)
    
    #NN5 AIQ + (-1/2,+1/2,0)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.x == 0:
        AIQTU.x = XExtreme + LatticeConstant*1/2
            
    if AIQTU.y == YExtreme:
        AIQTU.y = -LatticeConstant*1/2
        
    NN5 = AIQTU + LatticeConstant*vector(-1/2,+1/2,0)
    
    #NN6 AIQ + (+1/2,+1/2,0)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.y == YExtreme:
        AIQTU.y = -LatticeConstant*1/2
            
    if AIQTU.x == XExtreme:
        AIQTU.x = -LatticeConstant*1/2
        
    NN6 = AIQTU + LatticeConstant*vector(+1/2,+1/2,0)
    
    #NN7 AIQ + (+1/2,-1/2,0)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.x == XExtreme:
        AIQTU.x = -LatticeConstant*1/2
            
    if AIQTU.y == 0:
        AIQTU.y = YExtreme + LatticeConstant*1/2
        
    NN7 = AIQTU + LatticeConstant*vector(+1/2,-1/2,0)
    
    #NN8 AIQ + (-1/2,-1/2,0)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.x == 0:
        AIQTU.x = XExtreme + LatticeConstant*1/2
            
    if AIQTU.y == 0:
        AIQTU.y = YExtreme + LatticeConstant*1/2
        
    NN8 = AIQTU + LatticeConstant*vector(-1/2,-1/2,0)
    
    #NN9 AIQ + (-1/2,0,-1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.x == 0:
        AIQTU.x = XExtreme + LatticeConstant*1/2
            
    if AIQTU.z == 0:
        AIQTU.z = ZExtreme + LatticeConstant*1/2
        
    NN9 = AIQTU + LatticeConstant*vector(-1/2,0,-1/2)
    
    #NN10 AIQ + (0,+1/2,-1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.y == YExtreme:
        AIQTU.y = -LatticeConstant*1/2
            
    if AIQTU.z == 0:
        AIQTU.z = ZExtreme + LatticeConstant*1/2
        
    NN10 = AIQTU + LatticeConstant*vector(0,+1/2,-1/2)
    
    #NN11 AIQ + (+1/2,0,-1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.x == XExtreme:
        AIQTU.x = -LatticeConstant*1/2
            
    if AIQTU.z == 0:
        AIQTU.z = ZExtreme + LatticeConstant*1/2
        
    NN11 = AIQTU + LatticeConstant*vector(+1/2,0,-1/2)
    
    #NN12 AIQ + (0,-1/2,-1/2)
    AIQTU = vector(AIQ.x,AIQ.y,AIQ.z)

    if AIQTU.y == 0:
        AIQTU.y = YExtreme + LatticeConstant*1/2
            
    if AIQTU.z == 0:
        AIQTU.z = ZExtreme + LatticeConstant*1/2
        
    NN12 = AIQTU + LatticeConstant*vector(0,-1/2,-1/2)

    NearestNeighbourVectors = [NN1,NN2,NN3,NN4,NN5,NN6,NN7,NN8,NN9,NN10,NN11,NN12]
    NearestNeighbourTypes = list()
    for i in range(0,12):
        VectorAsString = str(NearestNeighbourVectors[i])
        NearestNeighbourTypes.append(LatticeDict[VectorAsString])

    return NearestNeighbourVectors, NearestNeighbourTypes

def InitialiseSystem(NoXUCs,NoYUCs,NoZUCs, LatticeConstant, FeFraction):
    AtomCoords = list()
    AtomTypes = list()
    LatticeDict = {}
    NearestNeighbourDictionary = {}
    FeCount = 0
    NiCount = 0
    OrderedOrRandom = "Random"

    TotalAtomNumber = 4*NoXUCs*NoYUCs*NoZUCs
    FeAtomNumber = int(FeFraction*TotalAtomNumber)
    VacancyNumber = 1
    NiAtomNumber = TotalAtomNumber - FeAtomNumber - VacancyNumber


    ChanceOfFe = FeAtomNumber/TotalAtomNumber
    ChanceOfNi = NiAtomNumber/TotalAtomNumber
    ChanceOfVacancy = VacancyNumber/TotalAtomNumber

    if OrderedOrRandom == "Random":
        for i in range(0,NoXUCs):
            CurrX = i*LatticeConstant
            for j in range(0,NoYUCs):
                CurrY = j*LatticeConstant
                for k in range(0,NoZUCs):
                    CurrZ = k*LatticeConstant
                    #Creates atom at these coordinates

                    #0,0,0
                    AtomCoords.append(vector(CurrX,CurrY,CurrZ))
                    AtomTypeChosen = np.random.choice([0,1,2],p=[ChanceOfFe,ChanceOfNi,ChanceOfVacancy])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    elif AtomTypeChosen == 2:
                        VacancyNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    ChanceOfFe = FeAtomNumber/TotalAtomNumber
                    ChanceOfNi = NiAtomNumber/TotalAtomNumber
                    ChanceOfVacancy = VacancyNumber/TotalAtomNumber

                    #1/2,1/2,0
                    AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY+LatticeConstant/2,CurrZ))
                    AtomTypeChosen = np.random.choice([0,1,2],p=[ChanceOfFe,ChanceOfNi,ChanceOfVacancy])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    elif AtomTypeChosen == 2:
                        VacancyNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    ChanceOfFe = FeAtomNumber/TotalAtomNumber
                    ChanceOfNi = NiAtomNumber/TotalAtomNumber
                    ChanceOfVacancy = VacancyNumber/TotalAtomNumber

                    #0,1/2,1/2
                    AtomCoords.append(vector(CurrX,CurrY+LatticeConstant/2,CurrZ+LatticeConstant/2))
                    AtomTypeChosen = np.random.choice([0,1,2],p=[ChanceOfFe,ChanceOfNi,ChanceOfVacancy])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    elif AtomTypeChosen == 2:
                        VacancyNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    ChanceOfFe = FeAtomNumber/TotalAtomNumber
                    ChanceOfNi = NiAtomNumber/TotalAtomNumber
                    ChanceOfVacancy = VacancyNumber/TotalAtomNumber

                    #1/2,0,1/2
                    AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY,CurrZ+LatticeConstant/2)) 
                    AtomTypeChosen = np.random.choice([0,1,2],p=[ChanceOfFe,ChanceOfNi,ChanceOfVacancy])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    elif AtomTypeChosen == 2:
                        VacancyNumber -= 1
                    else:
                        NiAtomNumber -= 1                  

                    TotalAtomNumber -= 1
                    if TotalAtomNumber != 0: #After the last atom has been created the TotalAtomNumber goes to zero, if statement avoids the divide by zero error
                        ChanceOfFe = FeAtomNumber/TotalAtomNumber
                        ChanceOfNi = NiAtomNumber/TotalAtomNumber
                        ChanceOfVacancy = VacancyNumber/TotalAtomNumber

    elif OrderedOrRandom == "Ordered":
        for i in range(0,NoXUCs):
            CurrX = i*LatticeConstant
            for j in range(0,NoYUCs):
                CurrY = j*LatticeConstant
                for k in range(0,NoZUCs):
                    CurrZ = k*LatticeConstant
                    #Creates atom at these coordinates
                    
                    AtomCoords.append(vector(CurrX,CurrY,CurrZ)) #0,0,0
                    AtomTypes.append(0) #Creates type of atom
                    AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY+LatticeConstant/2,CurrZ)) #1/2,1/2,0
                    AtomTypes.append(0) #Creates type of atom
                    AtomCoords.append(vector(CurrX,CurrY+LatticeConstant/2,CurrZ+LatticeConstant/2)) #0,1/2,1/2
                    AtomTypes.append(1) #Creates type of atom
                    AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY,CurrZ+LatticeConstant/2)) #1/2,0,1/2
                    AtomTypes.append(1) #Creates type of atom

    elif OrderedOrRandom == "50/50":
        
        NoZUCsDisOrdered = int(NoZUCs/2)

        TotalAtomNumber = TotalAtomNumber/2
        FeAtomNumber = FeAtomNumber/2
        NiAtomNumber = NiAtomNumber/2
        
        for i in range(0,NoXUCs):
            CurrX = i*LatticeConstant
            for j in range(0,NoYUCs):
                CurrY = j*LatticeConstant
                for k in range(0,NoZUCsDisOrdered):
                    CurrZ = k*LatticeConstant
                    #Creates atom at these coordinates

                    #0,0,0
                    AtomCoords.append(vector(CurrX,CurrY,CurrZ)) 
                    AtomTypeChosen = np.random.choice([0,1],p=[ChanceOfFe,ChanceOfNi])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    ChanceOfFe = FeAtomNumber/TotalAtomNumber
                    ChanceOfNi = NiAtomNumber/TotalAtomNumber

                    #1/2,1/2,0
                    AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY+LatticeConstant/2,CurrZ))
                    AtomTypeChosen = np.random.choice([0,1],p=[ChanceOfFe,ChanceOfNi])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    ChanceOfFe = FeAtomNumber/TotalAtomNumber
                    ChanceOfNi = NiAtomNumber/TotalAtomNumber

                    #0,1/2,1/2
                    AtomCoords.append(vector(CurrX,CurrY+LatticeConstant/2,CurrZ+LatticeConstant/2))
                    AtomTypeChosen = np.random.choice([0,1],p=[ChanceOfFe,ChanceOfNi])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    ChanceOfFe = FeAtomNumber/TotalAtomNumber
                    ChanceOfNi = NiAtomNumber/TotalAtomNumber

                    #1/2,0,1/2
                    AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY,CurrZ+LatticeConstant/2)) 
                    AtomTypeChosen = np.random.choice([0,1],p=[ChanceOfFe,ChanceOfNi])
                    AtomTypes.append(AtomTypeChosen) #Creates type of atom

                    if AtomTypeChosen == 0:
                        FeAtomNumber -= 1
                    else:
                        NiAtomNumber -= 1

                    TotalAtomNumber -= 1
                    if TotalAtomNumber != 0: #After the last atom has been created the TotalAtomNumber goes to zero, if statement avoids the divide by zero error
                        ChanceOfFe = FeAtomNumber/TotalAtomNumber
                        ChanceOfNi = NiAtomNumber/TotalAtomNumber

        for i in range(0,NoXUCs):
                CurrX = i*LatticeConstant
                for j in range(0,NoYUCs):
                    CurrY = j*LatticeConstant
                    for k in range(NoZUCsDisOrdered,NoZUCs):
                        CurrZ = k*LatticeConstant
                        #Creates atom at these coordinates
                        
                        AtomCoords.append(vector(CurrX,CurrY,CurrZ)) #0,0,0
                        AtomTypes.append(1) #Creates type of atom
                        AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY+LatticeConstant/2,CurrZ)) #1/2,1/2,0
                        AtomTypes.append(1) #Creates type of atom
                        AtomCoords.append(vector(CurrX,CurrY+LatticeConstant/2,CurrZ+LatticeConstant/2)) #0,1/2,1/2
                        AtomTypes.append(0) #Creates type of atom
                        AtomCoords.append(vector(CurrX+LatticeConstant/2,CurrY,CurrZ+LatticeConstant/2)) #1/2,0,1/2
                        AtomTypes.append(0) #Creates type of atom






                        

    #The following section builds two dictionaries, one with the type of each atom and one with the nearest neighbours of each atom

    for i in range(0,len(AtomCoords)):
        TempVar = str(AtomCoords[i])
        LatticeDict[TempVar] = AtomTypes[i]
        if AtomTypes[i] == 0:
            FeCount += 1
        else:
            NiCount += 1

    for i in range(0,len(AtomCoords)):
        TempVar = str(AtomCoords[i])
        NearestNeighbours, NearestNeighbourTypes = PullNearestNeighbours(AtomCoords[i], LatticeDict, LatticeConstant, AtomCoords, AtomTypes)
        NearestNeighbourDictionary[TempVar] = NearestNeighbours
                
    return AtomCoords, AtomTypes, LatticeDict, NearestNeighbourDictionary, FeCount, NiCount


def SwapAtoms(LatticeDict, LatticeConstant, AtomCoords, AtomTypes, AIQPos, SwapPartPos):
    AIQ = AtomCoords[AIQPos]
    SwapPartner = AtomCoords[SwapPartPos]

    
    AIQType = LatticeDict[str(AIQ)]
    SwapPartnerType = LatticeDict[str(SwapPartner)]

    AtomTypes[AIQPos] =  SwapPartnerType #Makes atom in question type equal type of the swap partner
    AtomTypes[SwapPartPos] = AIQType #Makes swap partner type equal AIQ type
    LatticeDict[str(AIQ)] = SwapPartnerType #Same for the dictionary now
    LatticeDict[str(SwapPartner)] = AIQType #Same for the dictionary now

    return AtomTypes, LatticeDict
    
def EnergyOfSystem(AIQNeighbourTypes, AIQType):
    J1 = 0.774*10**-20
    SystemEnergy = 0

    #Fe is 0, Ni is 1
    
    for i in range(0, 12):
        if AIQNeighbourTypes[i] == 0 and AIQType == 0: #FeFe
            SystemEnergy += J1
        elif AIQNeighbourTypes[i] == 1 and AIQType == 1: #PtPt
            SystemEnergy += J1
        elif AIQNeighbourTypes[i] == 2 or AIQType == 2:
            SystemEnergy += 0 #4.304*10**-20
        else:
            SystemEnergy -= J1

    return SystemEnergy

def SwapRateReturner(AIQ, SwapPartner, LatticeDict, NearestNeighbourDictionary, Temperature):
    #define my constants
    BarrierEnergy = 1.6*10**-19
    BoltzConst = 1.38*10**-23
    AttemptFrequency = 4*10**13 #One used in KMC paper for FePt
    KbT = Temperature*BoltzConst

    #Find my atoms
    AIQNeighbourVectors = NearestNeighbourDictionary[str(AIQ)] #Assembles list of neigbours for atom in question
    SwapPartNeighVec = NearestNeighbourDictionary[str(SwapPartner)] #Assembles list of neighbours for atom you're swapping with
        
    AIQNeighbourTypes = list()
    SwapPartNeighTypes = list()
    
    for i in range(0,12):
        AIQNeighbourTypes.append(LatticeDict[str(AIQNeighbourVectors[i])]) #Assembles list of types for neighbours of atom in question
        SwapPartNeighTypes.append(LatticeDict[str(SwapPartNeighVec[i])]) #Assembles list of types for neighbours of atom you're swapping with

    AIQType = LatticeDict[str(AIQ)]
    SwapPartnerType = LatticeDict[str(SwapPartner)]

    ### Finding delta E
    if AIQType == SwapPartnerType:
        DeltaE = BarrierEnergy

    else:
        #System energy of initial state:

        InitialStateEnergy = EnergyOfSystem(AIQNeighbourTypes, AIQType) + EnergyOfSystem(SwapPartNeighTypes, SwapPartnerType) #Energy of initial state

        #System energy if the two atoms were to swap:

        IndexInQuestion = AIQNeighbourVectors.index(SwapPartner) #Find the position of swappartner in AIQNeighbourVectors
        AIQNeighbourTypes[IndexInQuestion] = AIQType #Swap the type in AIQNeighbourTypes at the same index as above

        IndexInQuestion = SwapPartNeighVec.index(AIQ) #Find the position of AIQ in SwapPartNeighVec
        SwapPartNeighTypes[IndexInQuestion] = SwapPartnerType #Swap the type in SwapPartNeighTypes at the same index as above

        TempVar = AIQType
        AIQType = SwapPartnerType #Flip AIQType
        SwapPartnerType = TempVar #Flip SwapPartnerType

        FinalStateEnergy = EnergyOfSystem(AIQNeighbourTypes, AIQType) + EnergyOfSystem(SwapPartNeighTypes, SwapPartnerType) #Energy of final state plus the barrier against a swap
        
        if (FinalStateEnergy - InitialStateEnergy) <= 0: # The following is as per the KMC paper
            DeltaE = BarrierEnergy
            if AIQType == 2 or SwapPartnerType == 2: #Vacancy condition
                DeltaE = 0
        else:
            DeltaE = FinalStateEnergy - InitialStateEnergy + BarrierEnergy
            if AIQType == 2 or SwapPartnerType == 2: #Vacancy condition
                DeltaE = FinalStateEnergy - InitialStateEnergy
    ### Now to find the transition rate

    TransitionRate = AttemptFrequency*2.718281828**(-DeltaE/KbT) # vj = v0*exp(dE/kT) as in example paper

    return TransitionRate

def CompleteShellOrNot(AIQNeighbourTypes, AIQType):
#Does it want to order in the z-direction?
    #4,5,6,7 same and 0,1,2,3,8,9,10,11 different

    XComplete = 0
    YComplete = 0
    ZComplete = 0
    
    AtomsOutOfPosZ = int(0)
        
    for i in range(0,4):
        if AIQNeighbourTypes[i] == AIQType:
            AtomsOutOfPosZ += 1
    for i in range(4,8):
        if AIQNeighbourTypes[i] != AIQType:
            AtomsOutOfPosZ += 1
    for i in range(8,12):
        if AIQNeighbourTypes[i] == AIQType:
            AtomsOutOfPosZ += 1

    #Does it want to order in the y-direction?
    #0,2,8,10 same and 1,3,4,5,6,7,9,11 different

    AtomsOutOfPosY = int(0)
    
    if AIQNeighbourTypes[0] != AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[1] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[2] != AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[3] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[4] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[5] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[6] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[7] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[8] != AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[9] == AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[10] != AIQType:
        AtomsOutOfPosY += 1
    if AIQNeighbourTypes[11] == AIQType:
        AtomsOutOfPosY += 1

    #Does it want to order in the x-direction?
    #1,3,9,11 same and 0,2,4,5,6,7,8,10 different

    AtomsOutOfPosX = int(0)
    
    if AIQNeighbourTypes[0] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[1] != AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[2] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[3] != AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[4] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[5] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[6] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[7] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[8] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[9] != AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[10] == AIQType:
        AtomsOutOfPosX += 1
    if AIQNeighbourTypes[11] != AIQType:
        AtomsOutOfPosX += 1

    #Now return the smallest of the three

    if AtomsOutOfPosX == 0:
        XComplete = 1
    elif AtomsOutOfPosY == 0:
        YComplete = 1
    elif AtomsOutOfPosZ == 0:
        ZComplete = 1

    return XComplete, YComplete, ZComplete

def MeasureOrder(AtomCoords, AtomTypes, NearestNeighbourDictionary, LatticeDict):
    ###################### LRO METHOD OF MEASURING ORDER
    
    NumberOfAtoms = len(AtomCoords)
    m1 = 0 #Initialises the m variable in all 4 simple cubics
    m2 = 0
    m3 = 0
    m4 = 0
    
    for i in range(0, NumberOfAtoms):
        
        if AtomCoords[i].x == int(AtomCoords[i].x): #Tests if the x coord is integer
            xDirInteger = True
        else:
            xDirInteger = False

        if AtomCoords[i].y == int(AtomCoords[i].y): #Tests if the x coord is integer
            yDirInteger = True
        else:
            yDirInteger = False

        if AtomCoords[i].z == int(AtomCoords[i].z): #Tests if the x coord is integer
            zDirInteger = True
        else:
            zDirInteger = False

        if xDirInteger == True and yDirInteger == True and zDirInteger == True: #Condition for m1
            if AtomTypes[i] == 1: #Add for Fe
                m1 += 1
            else: #Subtract for Ni
                m1 -= 1

        elif xDirInteger == False and yDirInteger == False and zDirInteger == True: #Condition for m2
            if AtomTypes[i] == 1: #Add for Fe
                m2 += 1
            else: #Subtract for Ni
                m2 -= 1

        elif xDirInteger == True and yDirInteger == False and zDirInteger == False: #Condition for m3
            if AtomTypes[i] == 1: #Add for Fe
                m3 += 1
            else: #Subtract for Ni
                m3 -= 1

        else: #Must be m4 then
            if AtomTypes[i] == 1: #Add for Fe
                m4 += 1
            else: #Subtract for Ni
                m4 -= 1

    #Now apply the 1/N condition
    m1 = m1/NumberOfAtoms
    m2 = m2/NumberOfAtoms
    m3 = m3/NumberOfAtoms
    m4 = m4/NumberOfAtoms

    #Now to form the LRO vector
    xOrder = m1-m2+m3-m4
    yOrder = m1-m2-m3+m4
    zOrder = m1+m2-m3-m4
    LRO = vector(xOrder, yOrder, zOrder)

    OrderMagnitude = (xOrder**2 + yOrder**2 + zOrder**2)**0.5


    ################# NO. OF ATOMS WITH COMPLETE NEIGHBOURS METHOD OF MEASURING ORDER

    NoOfAtomsWithCompleteNeighboursX = int(0)
    NoOfAtomsWithCompleteNeighboursY = int(0)
    NoOfAtomsWithCompleteNeighboursZ = int(0)

    for k in range(0, NumberOfAtoms):
        AIQNeighbourVectors = NearestNeighbourDictionary[str(AtomCoords[k])] #Assembles list of neigbours for atom in question

        AIQNeighbourTypes = list()
        
        for j in range(0,12):
            AIQNeighbourTypes.append(LatticeDict[str(AIQNeighbourVectors[j])]) #Assembles list of types for neighbours of atom in question
    
        AIQType = LatticeDict[str(AtomCoords[k])]

        XComplete, YComplete, ZComplete = CompleteShellOrNot(AIQNeighbourTypes, AIQType)
        
        NoOfAtomsWithCompleteNeighboursX += XComplete
        NoOfAtomsWithCompleteNeighboursY += YComplete
        NoOfAtomsWithCompleteNeighboursZ += ZComplete

    xOrder = NoOfAtomsWithCompleteNeighboursX/NumberOfAtoms
    yOrder = NoOfAtomsWithCompleteNeighboursY/NumberOfAtoms
    zOrder = NoOfAtomsWithCompleteNeighboursZ/NumberOfAtoms
    
    AtomsWithCompletedNeighbours = vector(xOrder, yOrder, zOrder)

    return LRO, OrderMagnitude, AtomsWithCompletedNeighbours

def TotalSystemEnergy(AtomCoords, AtomTypes, NearestNeighbourDictionary, LatticeDict):
    TotalEnergy = 0
    for i in range(0, len(AtomCoords)):
        NeighbourTypes = list()
        NearestNeighbourVectors = NearestNeighbourDictionary[str(AtomCoords[i])]
        
        #Pull Types of nearest neighbours
        for j in range(0,12):
            NeighbourTypes.append(LatticeDict[str(NearestNeighbourVectors[j])])
        TotalEnergy += EnergyOfSystem(NeighbourTypes, AtomTypes[i])

    return TotalEnergy
        
def SaveImage(Name):
    print("Saving image")
    Picture = ImageGrab.grab((300, 100, 500, 325))
    Picture.save(Name + '.jpg')

def RoutesListReturner(LatticeDict, LatticeConstant, AtomCoords, AtomTypes, NearestNeighbourDictionary, Temperature):
    SwapPossibilities = list()
    SwapPosRates = list()
    SwapPossibilitiesSumToDate = 0
    
    for i in range(0, len(AtomCoords)): #For all atoms in sytsem
        #Don't consider the vacancy
        if AtomTypes[i] != 2:

            #Find the nearest neighbours of the atom in question:
            NearestNeighbours = NearestNeighbourDictionary[str(AtomCoords[i])]
            for j in range(0,12): #For all its neighbours
                
                #The ith atom is fine, I can just append i to SwapPossibilities
                #The jth atom on the other hand needs to have its position in AtomCoords found
                for k in range(0, len(AtomCoords)): ##This is going to be hugely inefficient
                    if NearestNeighbours[j] == AtomCoords[k]:
                        jPosInAC = k
                        break #Eliminates needless looping
                        
                SwapPossibilities.append(str(i) + "," + str(jPosInAC))
                
                RateOfThatPos = SwapRateReturner(AtomCoords[i], NearestNeighbours[j], LatticeDict, NearestNeighbourDictionary, Temperature)

                SwapPossibilitiesSumToDate += RateOfThatPos
                
                SwapPosRates.append(SwapPossibilitiesSumToDate)
            
    return SwapPossibilities, SwapPosRates

def OneMonteCarloStep(LatticeDict, LatticeConstant, AtomCoords, AtomTypes, NearestNeighbourDictionary, Temperature, CurrentTime, DoWeNeedARecalc, SwapPossibilities, SwapPosRates):
    
    #Find the possible routes and their rates
    if DoWeNeedARecalc == 1:
        SwapPossibilities, SwapPosRates = RoutesListReturner(LatticeDict, LatticeConstant, AtomCoords, AtomTypes, NearestNeighbourDictionary, Temperature)
        DoWeNeedARecalc = 0
        
    kToT = SwapPosRates[-1]
    
    #Choose random number, r
    r = random.randint(1,10**10)/(10**10) # Should give me r in range 0 to 1
    rkToT = r*kToT
    
    #Find in the list, which one is r*ktot
    for i in range(0, len(SwapPosRates)):
        if SwapPosRates[i] > rkToT:
            AtomsToSwapPositions = SwapPossibilities[i].split(",")

            #Small section that actually means that swapping two identical atoms isn't really done
            if AtomTypes[int(AtomsToSwapPositions[0])] != AtomTypes[int(AtomsToSwapPositions[1])]: #If they're the same type
                AtomTypes, LatticeDict = SwapAtoms(LatticeDict, LatticeConstant, AtomCoords, AtomTypes, int(AtomsToSwapPositions[0]), int(AtomsToSwapPositions[1]))
                DoWeNeedARecalc += 1
            break

    #Now for the timestep
    Timestep = -(np.log(r))/(kToT)

    CurrentTime += Timestep
    
    return LatticeDict, AtomTypes, CurrentTime, DoWeNeedARecalc, SwapPossibilities, SwapPosRates, Timestep

def Excecutable(NoXUCs, NoYUCs, NoZUCs, LatticeConstant, FeFraction, Temperature):
    #Initialise the system
    AtomCoords, AtomTypes, NearestNeighbourDictionary, LatticeDict = LoadSystem()
    #LRO, OrderMagnitude, AtomsWithCompletedNeighbours = MeasureOrder(AtomCoords, AtomTypes, NearestNeighbourDictionary, LatticeDict)
    DrawStructure(AtomCoords, AtomTypes)

    #Initialise relevant variables
    CurrentTime = 0
    MCStepCounter = 0
    DoWeNeedARecalc = 1
    SwapPossibilities = list()
    SwapPosRates = list()
    ZOrderByCompletedNeighbours = 0

Excecutable(NoXUCs, NoYUCs, NoZUCs, LatticeConstant, FeFraction, Temperature)

