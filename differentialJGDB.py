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
        return False, False, True, 0

    # Assigns p (ping) and d (don) as the same value
    if BlackL == "p":
        BlackL = "d"
    if WhiteL == "p":
        WhiteL = "d"
    
    keyOrder =['9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', '1d', '1k', '2k', '3k', '4k', '5k', '6k', '7k', '8k', '9k', '10k', '11k', '12k', '13k', '14k', '15k', '16k', '17k', '18k', '19k', '20k', '21k', '22k', '23k', '24k', '25k', '26k', '27k', '28k', '29k', '30k']

    BR = str(int(BlackN)) + BlackL
    WR = str(int(WhiteN)) + WhiteL

    if BR not in keyOrder or WR not in keyOrder:
        return False, False, True, 0

    BGW = False
    EqualRank = False
    # If the ranks are the same, set equal rank to true
    if BR == WR:
        EqualRank = True
    elif BlackL != WhiteL:
        if BlackL == "d":
            # If Black Letter is p, and different from white, Black is greater rank
            BGW = True
        else:
            BGW = False
    elif BlackL == "d":
        # compare by number if letter the same
        BGW = BlackN > WhiteN
    else:
        BGW = BlackN < WhiteN
    
    blackInd = keyOrder.index(BR)
    whiteInd = keyOrder.index(WR)

    return BGW, EqualRank, False, abs(blackInd - whiteInd)

def printInfoToTerminal(info):
    cntr = 0
    keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    for i in range(len(keys)):
        differential = keys[i]
        if differential not in info:
            continue
        cntr += info[differential][0]
        print("DIFFERENTIAL:", differential, "TOTAL GAMES:", info[differential][0], "WON BY HIGHER:", info[differential][1])
    print(cntr)

def main():
    # Gets the list of all filenames in the database
    FileNames = getfilenames("jgdb/train.txt")

    # stores a map of point differential to pairs, of games played, and games won by higher
    # key = diff, value = [total, wonByHigher]
    diffMap = {}
    errcntr = 0
    cntr = 0
    print("JGDB TRAIN DIFFERENTIAL\n\n")
    # iterating through each file
    for filename in FileNames:
        cntr += 1
        if cntr % 1000 == 0:
            print(cntr)
        if cntr > 100000:
            break
        # create path to file
        fullPath = "jgdb" + filename[1:len(filename)]

        # try to parse
        try:
            root = SGF.parse_file(fullPath)
        except:
            errcntr += 1
            continue

        # get required values from game files
        BR = getValueFromRoot(root, "BR")
        WR = getValueFromRoot(root, "WR")
        re = getValueFromRoot(root, "RE")

        # if values don't exist in file, ignore
        if BR == None or WR == None or re == None:
            errcntr += 1
            continue

        # call CompareRank to know which rank is greater, if they are equal, or if the rank is malformed. 
        BGW, equalRank, error, differential = compareRank(BR, WR)
        
        if error:
            errcntr += 1
            continue

        #Tallies total number of equal rank games
        if equalRank:
            errcntr += 1
            continue

        #
        BlackWon = re[0] == "B"

        #Tallies games won by higher rank and games won by lower rank
        if (BlackWon == BGW):
            if differential not in diffMap:
                diffMap[differential] = [0, 0]
            #increment total games
            diffMap[differential][0] += 1

            #increment games won by higher
            diffMap[differential][1] += 1
        else:
            if differential not in diffMap:
                diffMap[differential] = [0, 0]
            #increment total games
            diffMap[differential][0] += 1
    printInfoToTerminal(diffMap)
    print(errcntr)
    print(cntr)
    return

if __name__ == "__main__":
    main()