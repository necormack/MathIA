from pysgf import SGF
# Parses SGF files into readable strings
def getfilenames(FileName):
    with open(FileName) as file:
        lines = [line.rstrip() for line in file]
    return lines

def getValueFromRoot(root, property):
    # 
    val = root.get_list_property(property)
    if val != None:
        val = val[0]
    return val

def compareRank(BR, WR):
    # Isolates variables from spaces and commas
    BR = (BR.split(" "))[0]
    WR = (WR.split(" "))[0]
    BR = (BR.split(","))[0]
    WR = (WR.split(","))[0]

    try:
    # Separates BR/WR number and letter
        BlackN = float(BR[0:-1])
        BlackL = BR[-1]
        WhiteN = float(WR[0:-1])
        WhiteL = WR[-1]
    except:
        return False, False, True, BR, WR

    tmpDict = {'p', 'd', 'k'}

    if BlackL not in tmpDict or WhiteL not in tmpDict:
        return False, False, True, BR, WR

    # Assigns p (ping) and d (don) as the same value
    if BlackL == "p":
        BlackL = "d"
    if WhiteL == "p":
        WhiteL = "d"
    BR = str(int(BlackN)) + BlackL
    WR = str(int(WhiteN)) + WhiteL
    BGW = False
    EqualRank = False
    # If the ranks are the same, set equal rank to true
    if BR == WR:
        EqualRank = True
    elif BlackL != WhiteL:
        if BlackL == "d":
            # If Black Letter is d, and different from white, Black is greater rank
            BGW = True
        else:
            BGW = False
    elif BlackL == "d":
        # compare by number if letter the same
        BGW = BlackN > WhiteN
    else:
        BGW = BlackN < WhiteN
    return BGW, EqualRank, False, BR, WR

def printInfoToTerminal(info):
    keyOrder =['9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', '1d', '1k', '2k', '3k', '4k', '5k', '6k', '7k', '8k', '9k', '10k', '11k', '12k', '13k', '14k', '15k', '16k', '17k', '18k', '19k', '20k', '21k', '22k', '23k', '24k', '25k', '26k', '27k', '28k', '29k', '30k']
    
    cntr = 0
    for i in range(len(keyOrder)):
        higherRank = keyOrder[i]
        if higherRank not in info:
            continue
        print("HIGHER RANK          :", higherRank)
        for j in range(i, len(keyOrder)):
            lowerRank = keyOrder[j]
            if lowerRank not in info[higherRank]:
                continue
            cntr += info[higherRank][lowerRank][0]
            print("Lower Rank ", lowerRank + ":", info[higherRank][lowerRank][0], info[higherRank][lowerRank][1])
    print(cntr)

def main():
    # Gets the list of all filenames in the database
    FileNames = getfilenames("jgdb/train.txt")
    print("JGDB DB:", len(FileNames))

    info = {}
    cntr= 0
    errCntr = 0
    # iterating through each file
    for filename in FileNames:
        cntr += 1
        if cntr%1000==0:
            print(cntr)

        if cntr > 100000:
            break
        
        # create path to file
        fullPath = "jgdb" + filename[1:len(filename)]

        # try to parse
        try:
            root = SGF.parse_file(fullPath)
        except:
            errCntr += 1
            continue

        # get required values from game files
        BR = getValueFromRoot(root, "BR")
        WR = getValueFromRoot(root, "WR")
        re = getValueFromRoot(root, "RE")

        # if values don't exist in file, ignore
        if BR == None or WR == None or re == None:
            errCntr += 1
            continue

        # call CompareRank to know which rank is greater, if they are equal, or if the rank is malformed. 
        BGW, equalRank, error, BR, WR = compareRank(BR, WR)
        
        if error:
            errCntr += 1
            continue

        # in case of equal rank, 'higher rank' will be black. Equal rank is sub-dictionary.
        higherRank = WR
        lowerRank = BR
        higherIsWhite = True
        if BGW:
            # we know here that equalRank == False
            higherIsWhite = False
            higherRank = BR
            lowerRank = WR

        # add entry to dictionary for higher rank
        if higherRank not in info:
            info[higherRank] = {}
        
        # add entry to dictionary of higher rank for lower rank
        if lowerRank not in info[higherRank]:
            # list is [totalgames, gamesWonByHigher]
            info[higherRank][lowerRank] = [0, 0]

        # Increment total games of this setup
        info[higherRank][lowerRank][0] = info[higherRank][lowerRank][0] + 1

        WhiteWon = re[0] == "W"

        # Tallies total number of equal rank games
        if equalRank:
            # 'higherRank' is White
            if WhiteWon:
                # tally games won by higher
                info[higherRank][lowerRank][1] = info[higherRank][lowerRank][1] + 1
            continue

        # if the player who won is the same as the 'higherRank' player
        if WhiteWon == higherIsWhite:
            info[higherRank][lowerRank][1] = info[higherRank][lowerRank][1] + 1

    printInfoToTerminal(info)
    print(errCntr)
    print(cntr)

    return

if __name__ == "__main__":
    main()