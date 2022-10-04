import re
# import math

stage_name = "Smolness"  # change this to the text file of the stage you want mirrored (minus the .txt)

file_read = open(stage_name + ".txt", "r")
file_write = open(stage_name + "_M.txt", "w")

set_road = ""
suffix = ""

for line in file_read:
    print(line, end='')
    line = line.replace("\n", "")

    if len(line) == 0:  # check suffix (p, s, r, pt, pr, ph)
        continue
    elif line[-1] != ")":
        if line[-1] == "t":
            suffix = ")pt"
        elif line[-2:] == "pr":
            suffix = ")pr"
        elif line[-1] == "h":
            suffix = ")ph"
        elif line[-1] == "l":
            suffix = ")pl"
        elif line[-1] == "s":
            suffix = ")s"
        elif line[-1] == "r":
            suffix = ")r"
        else:
            suffix = ")p"
    else:
        suffix = ")"

    if line[:3] == "set" or line[:3] == "chk" or line[:3] == "fix":
        if line[-1] == ")":
            set_road = re.split(',', line[4:len(line) - 1])
        elif line[-1] == "p" or line[-1] == "s" or (line[-1] == "r" and line[-2:] != "pr"):
            set_road = re.split(',', line[4:len(line) - 2])
        else:
            set_road = re.split(',', line[4:len(line) - 3])

        set_road[1] = int(set_road[1])
        set_road[3] = int(set_road[3])
        set_road[1] *= -1

        # TODO implement curved road and check
        #if (set_road[0] == '10' or set_road[0] == '11' or set_road[0] == '15' or set_road[0] == '18' or set_road[0] == '43') and (set_road[3] != 0 or set_road[3] != 90 or set_road[3] != -90 or set_road[3] != 180):  # curved roads
            #set_road[3] = abs(set_road[3]) - 90

        print(set_road)

        if line[:3] == "set":  # roads/stage pieces
            if set_road[0] != '10' or set_road[0] != '11' or set_road[0] != '15' or set_road[0] != '18' or set_road[0] != '43':  # if not a road
                if set_road[0] == '14' or set_road[0] == '17' or set_road[0] == '19':  # turns
                    if set_road[3] == -90:
                        set_road[3] = 0
                    elif set_road[3] == 0:
                        set_road[3] = -90
                    elif set_road[3] == 90:
                        set_road[3] = 180
                    else:
                        set_road[3] = 90
                elif set_road[0] == '12':  # twisted right becomes left
                    set_road[0] = '13'
                    if set_road[3] == -30 or set_road[3] == 150:
                        set_road[3] = 30
                    elif set_road[3] == -60:
                        set_road = 60
                    elif set_road[3] == -120:
                        set_road[3] = 120
                    elif set_road[3] == 60:
                        set_road[3] = -60
                elif set_road[0] == '13':  # twisted left becomes right
                    set_road[0] = '12'
                    if set_road[3] == 30:
                        set_road[3] = -30
                    elif set_road[3] == 60:
                        set_road = -60
                    elif set_road[3] == 120:
                        set_road[3] = -120
                    elif set_road[3] == -60:
                        set_road[3] = 60
                elif set_road[0] == '29':  # two way high low ramp (asymmetrical parts)
                    if set_road[3] == 0:
                        set_road[3] = 180
                    elif set_road[3] == 90:
                        set_road[3] = -90
                    elif set_road[3] == 180:
                        set_road[3] = 0
                    else:
                        set_road[3] = 90
                elif set_road[0] == '36':  # halfpipe
                    if set_road[3] == 90:
                        set_road[3] = -90
                    elif set_road[3] == -90:
                        set_road[3] = 90
                elif set_road[0] == '49':  # tunnel side ramp
                    if set_road[3] == 0:
                        set_road[3] = 180
                    elif set_road[3] == 180:
                        set_road[3] = 0
                elif set_road[0] == '16' or set_road[0] == '20' or set_road[0] == '21' or set_road[0] == '22' or set_road[0] == '23' or set_road[0] == '24' or set_road[0] == '44' or set_road[0] == '45' or set_road[0] == '56' or set_road[0] == '57' or set_road[0] == '58' or set_road[0] == '59' or set_road[0] == '60' or set_road[0] == '61' or set_road[0] == '26' or set_road[0] == '28' or set_road[0] == '32' or set_road[0] == '27' or set_road[0] == '31' or set_road[0] == '30' or set_road[0] == '52' or set_road[0] == '50' or set_road[0] == '53' or set_road[0] == '55':  # "one-way" parts
                    if set_road[3] == -90:
                        set_road[3] = 90
                    elif set_road[3] == 90:
                        set_road[3] = -90

            file_write.write(
                "set(" + set_road[0] + "," + str(set_road[1]) + "," + set_road[2] + "," + str(set_road[
                                                                                                  3]) + suffix + "\n")
        elif line[:3] == "chk":  # checkpoints
            if len(set_road) == 4:  # ground check
                file_write.write(
                    "chk(" + set_road[0] + "," + str(set_road[1]) + "," + set_road[2] + "," + str(
                        set_road[3]) + suffix + "\n")
            elif len(set_road) == 5:  # air check
                # TODO fix air checks
                file_write.write(
                    "fix(" + set_road[0] + "," + str(set_road[1]) + "," + set_road[2] + "," + str(set_road[3]) + "," +
                    set_road[
                        4] + suffix + "\n")
        elif line[:3] == "fix":  # fix hoops
            file_write.write(
                "fix(" + set_road[0] + "," + str(set_road[1]) + "," + set_road[2] + "," + str(set_road[3]) + "," +
                set_road[
                    4] + suffix + "\n")
    elif line[:4] == "pile":  # ignore piles
        continue
    elif line[:3] == "max":  # ignore walls
        continue
    else:
        file_write.write(line + "\n")
