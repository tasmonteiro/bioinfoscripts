#!/usr/bin/env python3
import os
import time
import argparse

#========================================#
#       TERMINAL ARGUMENT PARSER         #
#========================================#

parser = argparse.ArgumentParser(description='Dynamic Scrapping Tool (DynaST) is a tool created to download and extract information from the iBeetle (https://ibeetle-base.uni-goettingen.de/) database.')

parser.add_argument('-i', dest="input_path", type=str, help='path in which the data files are located')
parser.add_argument('-o', dest="output_path", type=str, help='path in which the script will save the output file')
parser.add_argument('-n', dest="name",type=str, help='name of the output file')
parser.add_argument('-v', dest="verbose", action='store_true', help='verbose mode')
parser.add_argument('-s', dest="no_download", action='store_true', help='scrapper-only mode')

args = parser.parse_args()

#========================================#
#           EDITABLE VARIABLES           #
#========================================#

if args.output_path == None:
    os.system('mkdir ./ibeetle/')
    outputpath = "./ibeetle/"
else:
    outputpath = args.output_path

if args.name == None:
    outputname = "ibeetle.csv"
else:
    outputname = args.name

if args.input_path == None:
    os.system('mkdir ./ibeetle/data/')
    os.system('mkdir ./ibeetle/data/html')
    inputpath = "./ibeetle/data/"
else:
    inputpath = args.input_path

if args.verbose == False:
    speed = None
else:
    speed = time.sleep(0.05)

htmlpath = inputpath+"html/"

#========================================#
#           TC(ID) LIST CREATOR          #
#========================================#

if os.path.isfile("./ibeetle/ibeetle_tc.txt") == False:
    os.system('wget -q https://ibeetle-base.uni-goettingen.de/downloads/OGS3.gff.gz --no-check-certificate')
    os.system('gzip -d OGS3.gff.gz')
    os.system('grep -o -P "TC[0-9]{6}" OGS3.gff  | uniq > ./ibeetle/ibeetle_tc.txt')
    os.system('rm OGS*')

#removes all new line tags
def parseList(list):
    parsedlist = []
    for i in range(len(list)):
        parsedlist.append(list[i].strip('\n'))
    return parsedlist

def printinfo():
    print("\n" * 50)
    print("INFO\n")
    print("Input dir. path:", inputpath)
    print("Output dir. path:", outputpath)
    print("Output file name:", outputname)
    print("Verbose mode:", args.verbose)
    print("No download (-s):", args.no_download)

#creates a list with all TC IDs, separated by commas
lista = parseList(open("ibeetle/ibeetle_tc.txt").readlines())

if args.no_download == False:
    for i in range(len(lista)):
        if os.path.isfile(htmlpath + lista[i]) == True:
            print(lista[i], "already exists")
            speed
        else:
            printinfo()
            print("\n"+"Downloading HTML files from iBeetle webserver... " + str(i) + "/" + str(len(lista)))
            print("#" * int((i / 100.0) * (8000.0 / len(lista))))
            os.system('wget -q https://ibeetle-base.uni-goettingen.de/details/' + lista[
                i] + ' --no-check-certificate -P ./ibeetle/data/html')
            time.sleep(0.5)

#========================================#
#               HTML SCRAPPER            #
#========================================#

database = []
validDB = []

count = 0

for file in os.listdir(htmlpath):
    filename = file
    file = open(htmlpath+file).readlines()
    include = [[filename],]
    phenotype = []
    flyhomologs = []
    count += 1
    if args.verbose == True:
        printinfo()
        print("\n"+"Getting information from HTML files...",str(
            count) + "/" + str(len(os.listdir(htmlpath))))
        print("#" * int((count / 100.0) * (8000.0/len(os.listdir(htmlpath)))))
    for i in range(len(file)):
        if "includes death" in file[i]:
            if "<br />" in file[i]:
                phenotype.append([file[i].split()[4].capitalize()+file[i].split()[1],file[i].split()[6].split(".")[0]])
                phenotype.append([file[i].split()[4].capitalize() + file[i].split()[14], file[i].split()[19].split(".")[0]])
            else:
                phenotype.append([file[i].split()[4].capitalize()+file[i].split()[1],file[i].split()[6].split(".")[0]])
        elif "flybase.org/" in file[i]:
            flyhomologs.append(file[i].split("/reports/")[1].split(".html")[0])
        else:
            None
    include.append(phenotype)
    include.append(flyhomologs)
    database.append(include)
    speed

#========================================#
#       VALID DATABASE CREATOR           #
#========================================#

count = 0

for entry in database:
    include = []
    count += 1
    if args.verbose == True:
        printinfo()
        print("\n"+"Creating database using HTML information...",str(count)+"/"+str(len(database)))
        print("#" * int((count / 100.0) * (8000.0 / len(database))))
    if (len(entry[1]) > 0) and (len(entry[1]) < 4):
        if ((entry[1][0][1] != "%") and (entry[1][1][1] != "%") and (entry[1][2][1] != "%")) and ((entry[1][0][1] != "-1") and (entry[1][1][1] != "-1") and (entry[1][2][1] != "-1")):
            if len(entry[2]) > 0:
                include.append(entry[0])
                include.append(entry[1])
                include.append(entry[2])
                validDB.append(include)
    speed

#========================================#
#           OUTPUT FILE GENERATOR        #
#========================================#

ibeetleoutput = open(outputpath+outputname,"w+")
ibeetleoutput.write("ID,Pupal11,Larval11,Larval22,Fly Homologs\n")

for entry in validDB:
    flyhomo = '"'
    for i in range(len(entry[2])):
        if i < len(entry[2])-1:
            flyhomo += entry[2][i]+','
        else:
            flyhomo += entry[2][i] + '"'
    ibeetleoutput.write(entry[0][0]+","+entry[1][0][1]+","+entry[1][1][1]+","+entry[1][2][1]+","+flyhomo+"\n")

print("\nDatabase saved as",outputname,"under",outputpath)
