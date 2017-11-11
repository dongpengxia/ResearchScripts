# -*- coding: utf-8 -*-

"""
This program processes a text file created by ReportToJudgeFile.py and extracts the judge names. Unnecessary content
such as "and also of", "having deliberated", "and", "judges", and other words or phrases are removed.

IMPORTANT: The program has code like phrase = phrase.strip(" ").strip(" ").strip(" ") which may appear to be repetitive
and unnecessary. There are different space characters across different court reports, even though all the space characters
appear the same. Thus the character in double quotes in the first strip() is different from the character in double quotes
in the second strip().

IMPORTANT: JudgeList and registrarList undergo similar processing, but are separate to help with diagnostics in checking
the code. Overall, normal judges are in judgeList while most ad hoc judges and registrars are located in registrarList.
"""

#Location of File Created by ReportToJudgeFile.py
#File has one line for each court report.
#Example of a line: 001-100036	Josep Casadevall, President,Elisabet Fura,Corneliu Bîrsan,Alvina Gyulumyan,Egbert Myjer,Ineta Ziemele, appointed to sit in respect of Lithuania,Ann Power, judges,and Santiago Quesada, Section Registrar,
JUDGES_FILE = '' #Fill in (text file)

#Location of Output File
OUTPUT_FILE = '' #Fill in with location of output text file

#Read all the lines from JUDGES_FILE, one line for each court case
n = open(JUDGES_FILE,'r')
judgelines = n.readlines()
n.close()

o = open(OUTPUT_FILE, 'w')
o.write("URL" + '\t' + "itemid (filename)" + '\t' + "Name" + '\t' + "President" + '\t' + "Ad Hoc Judge" + '\t' + "Substitute Judge" + '\t' + "Jurisconsult" + '\t' + "Registrar" + '\n')

numlines = 0

#counts
numPresident = 0
numAdHoc = 0
numSubstitute = 0
numJurisconsult = 0
numRegistrar = 0
numPeople = 0

#class Judge will be used to represent a single judge from a single court case
class Judge(object):
    def __init__(self,itemid,name):
        self.itemid = itemid #itemid of court case
        self.name = name #name of judge
        self.president = False #whether or not the judge is a court president
        self.adhoc = False
        self.substitute = False
        self.jurisconsult = False
        self.registrar = False
    def display_judge(self):
        result = self.itemid + '\t' + self.name + '\t'
        if(self.president):
            result = result + "1"
        else:
            result = result + "0"
        result = result + '\t'
        if(self.adhoc):
            result = result + "1"
        else:
            result = result + "0"
        result = result + '\t'
        if(self.substitute):
            result = result + "1"
        else:
            result = result + "0"
        result = result + '\t'
        if(self.jurisconsult):
            result = result + "1"
        else:
            result = result + "0"
        result = result + '\t'
        if(self.registrar):
            result = result + "1"
        else:
            result = result + "0"
        return result



for line in judgelines:

    #remove newline character
    line = line.strip('\n')
    #itemid is the report number
    itemid = line.split('\t')[0].strip(' ')
    #judgeSentence is the sentence containing all the judge names
    judgeSentence = line.split('\t')[1]

    #Modify specific lines to fit in with sentence formatting for judge name processing
    #The subsequent code was produced through trial-and-error. Not all the reports listed judge names in the same format.
    if itemid in ['001-58742', '001-59352']:
        judgeSentence = judgeSentence.split(":")[1] #remove introduction info before colon
    elif itemid in ['001-100555','001-78918','001-89113']:
        judgeSentence = judgeSentence[:judgeSentence.index(' Deputy Section Registrar')] + ',' + judgeSentence[judgeSentence.index(' Deputy Section Registrar'):]
    elif itemid in ['001-148654','001-160613','001-58339']:
        judgeSentence = judgeSentence[:judgeSentence.index(' Section Registrar')] + ',' + judgeSentence[judgeSentence.index(' Section Registrar'):]
    elif itemid in ['001-159057','001-159059','001-159774','001-161811']:
        judgeSentence = judgeSentence[:judgeSentence.index(' Acting Deputy Section Registrar')] + ',' + judgeSentence[judgeSentence.index(' Acting Deputy Section Registrar'):]
    elif itemid in ['001-57435','001-57496']:
        judgeSentence = judgeSentence[::-1].replace("and"[::-1],","[::-1],1)[::-1]
    elif itemid in ['001-58277']:
        judgeSentence = judgeSentence[::-1].replace("and"[::-1],","[::-1],1).replace("and"[::-1],",Deputy Registrar,"[::-1],1)[::-1]
    elif itemid in ['001-58298','001-58270','001-58271','001-58272','001-58273','001-58274','001-58275','001-58276','001-58278','001-58279','001-58280','001-58281','001-58372','001-58906','001-58251']:
        judgeSentence = judgeSentence[::-1].replace("and"[::-1],",Deputy Registrar,"[::-1],1)[::-1]
    elif itemid in ['001-58069']:
        judgeSentence = judgeSentence.replace("Deputy","Deputy Registrar",1)
    elif itemid in ['001-60396']:
        judgeSentence = judgeSentence[:judgeSentence.index(' ad hoc judge')] + ',' + judgeSentence[judgeSentence.index(' ad hoc judge'):]
    elif itemid in ['001-60397','001-60621','001-67427','001-91360','001-57544']:
        judgeSentence = judgeSentence.replace('and',',',1)
    elif itemid in ['001-60419']:
        judgeSentence = judgeSentence.replace('1',"",1)
    elif itemid in ['001-59590','001-59591']:
        judgeSentence = judgeSentence.replace(" for the Registrar,","")
    elif itemid in ['001-76721']:
        judgeSentence = judgeSentence.replace(", judges","",1).replace("and","judges,",1)
    elif itemid in ['001-89307','001-93314']:
        judgeSentence = judgeSentence.replace(", judges","",1).replace(" appointed to sit in respect of Lithuania,","judges",1)
    elif itemid in ['001-77995']:
        judgeSentence = judgeSentence.split('Having')[0]
    elif itemid in ['001-57433']:
        judgeSentence = 'R. Cassin, President,A. Verdross,G. Maridakis,A. Ross,T. Wold,K. F. Arik,Baron L. Fredericq, ad hoc judge, Judges,P. Modinos, Registrar'
    elif itemid in ['001-57516','001-57518']:
        judgeSentence = 'R. Cassin, President,G. Maridakis,E. Rodenbourg,R. McGonigal,G. Balladore Pallieri,E. Arnalds,K.F. Arik, Judges,P. Modinos, Registrar'
    elif itemid in ['001-57467']:
        judgeSentence = 'Sir Humphrey Waldock, President,H. Rolin,T. Wold,M. Zekia,A. Favre,J. Cremona,G. Wiarda, Mr. M.-A. Eissen, Registrar and Mr. J.F. Smyth, Deputy Registrar,'
    elif itemid in ['001-144139','001-85152']:
        judgeSentence = judgeSentence.replace(" judges,","",1)
    elif itemid in ['001-112993']:
        judgeSentence = "Françoise Tulkens, President,Dragoljub Popović,Isabelle Berro-Lefèvre,András Sajó,Guido Raimondi,Paulo Pinto de Albuquerque,Helen Keller, judges,Danutė Jočienė, substitute judge,Işıl Karakaş, substitute judge,and Françoise Elens-Passos, Deputy Section Registrar,"
    elif itemid in ['001-61822']:
        judgeSentence = "SirNicolas Bratza, President,MrsV. Strážnická,MrJ. Casadevall,MrR. Maruste,MrL. Garlicki,MrsE. Fura-Sandström,MsL. Mijović, judges,MrM. Pellonpää,substitute judge,MrS. Pavlovschi,substitute judge,MrJ. Borrego Borrego, substitute judge,and Mr M. O’Boyle, Section Registrar,"
    elif itemid in ['001-79419']:
        judgeSentence = "MrP. Lorenzen, President,MrK. Jungwiert,MrV. Butkevych,MrsM. Tsatsa-Nikolovska,MrJ. Borrego Borrego,MrsR. Jaeger,MrM. Villiger, judges,MrsS. Botoucharova, substitute judge,MrR. Maruste, substitute judge,and Mrs C. Westerdiek, Section Registrar,"
    elif itemid in ['001-88836']:
        judgeSentence = "Françoise Tulkens, President,Antonella Mularoni,Ireneu Cabral Barreto,Danutė Jočienė,Dragoljub Popović,Nona Tsotsoria,Işıl Karakaş, judges,Vladimiro Zagrebelsky,substitute judge,András Sajó, substitute judge,and Sally Dollé, Section Registrar,"
    elif itemid in ['001-88904']:
        judgeSentence = "Françoise Tulkens, President,Ireneu Cabral Barreto,Vladimiro Zagrebelsky,Danutė Jočienė,András Sajó,Nona Tsotsoria,Işıl Karakaş, judges,Antonella Mularoni,substitute judge,Dragoljub Popović, substitute judge,and Sally Dollé, Section Registrar,"
    elif itemid in ['001-58031']:
        judgeSentence = judgeSentence[::-1].replace(",and "[::-1],","[::-1],1)[::-1]
    elif itemid in ['001-57529']:
        judgeSentence = judgeSentence.replace("replacing the late Mrs. H. PEDERSEN,","",1)
    elif itemid in ['001-59454']:
        judgeSentence = judgeSentence.replace(" in respect of Turkey","",1).replace(" in respect of Cyprus","",1)
    elif itemid in ['001-57605']:
        judgeSentence = judgeSentence.replace("(Rules 21, paragraph 7, and 48, paragraph 3)","",1)
    elif itemid in ['001-57420','001-57467','001-57479','001-57543','001-57565','001-57596','001-57997','001-57553','001-57569','001-57970','001-57978','001-57985','001-58004','001-58042','001-58043','001-58060','001-58062','001-58066','001-58076','001-58269']:
        judgeSentence = judgeSentence.replace("and also ",",",1)
    elif itemid in ['001-57427','001-57539','001-57625','001-57628','001-57669','001-57704','001-57718','001-57776','001-57777','001-57792','001-57793']:
        judgeSentence = judgeSentence + "Deputy Registrar"
    elif itemid in ['001-57524']:
        judgeSentence = judgeSentence + "judges "
    elif itemid in ['001-58806','001-59077']:
        judgeSentence = judgeSentence.replace("President",",President",1)
    elif itemid in ['001-58744','001-98493']:
        judgeSentence = judgeSentence.replace(",",",President,",1)
    elif itemid in ['001-75888']:
        judgeSentence = "J.-P. Costa, president," + judgeSentence
    elif itemid in ['001-154007']:
        judgeSentence = "Dean Spielmann, President,Josep Casadevall,Mark Villiger,Isabelle Berro,Işıl Karakaş,Ineta Ziemele,Luis López Guerra,Mirjana Lazarova Trajkovska,Nona Tsotsoria,Zdravka Kalaydjieva,Vincent A. De Gaetano,Angelika Nußberger,Paul Lemmens,Helena Jäderblom,Krzysztof Wojtyczek,Faris Vehabović,Robert Spano, judges,and Johan Callewaert, Deputy Grand Chamber Registrar,"
    elif itemid in ['001-57537']:
        judgeSentence = "H. Rolin, President,A. HOLMBÄCK,A. Verdross,G. Balladore Pallieri,M. Zekia,J. Cremona,S. Bilge,judges, Mr. M.-A. Eissen, Registrar, Mr. J.F. Smyth, Deputy Registrar,"
    elif itemid in ['001-71615']:
        judgeSentence = judgeSentence + "S. Dollé, Registrar"
    elif itemid in ['001-102766']:
        judgeSentence = "Nina Vajić, President,Khanlar Hajiyev,Dean Spielmann, judges,André Wampach,Deputy Registrar"
    elif itemid in ['001-163114']:
        judgeSentence = 'András Sajó, President,Işıl Karakaş,Josep Casadevall,Elisabeth Steiner,Ján Šikuta,Nona Tsotsoria,Ganna Yudkivska,André Potocki,Paul Lemmens,Aleš Pejchal,Faris Vehabović,Ksenija Turković,Egidijus Kūris,Robert Spano,Iulia Antoanella Motoc,Jon Fridrik Kjølbro, judges,Jautrīte  Briede, ad hoc judge,Johan Callewaert, Deputy Grand Chamber Registrar'


    #Make "judges" a separator for the first part which gives judge names and the second part which gives registrar names.
    #Keep in mind this separation of judge names and registrar names is not absolute. Sometimes judge names will show
    #up in the half containing registrar names.
    if "Judges" in judgeSentence and len(judgeSentence.split("Judges")) == 2:
        judgeSentence = judgeSentence.replace("Judges","judges",1)
    if "juges" in judgeSentence and len(judgeSentence.split("juges")) == 2:
        judgeSentence = judgeSentence.replace('juges','judges',1)
    if not "judges" in judgeSentence and ",and " in judgeSentence:
        judgeSentence = judgeSentence.replace(",and ","judges",1)
    if not "judges" in judgeSentence and " and " in judgeSentence:
        judgeSentence = judgeSentence.replace(" and ","judges",1)
        if "Deputy" in judgeSentence and not "Deputy Registrar" in judgeSentence:
            judgeSentence = judgeSentence.replace("Deputy","Deputy Registrar",1)
    if not "judges" in judgeSentence and " and " in judgeSentence:
        judgeSentence = judgeSentence.replace(" and ","judges",1)
    if not "judges" in judgeSentence and "and" in judgeSentence:
        judgeSentence = judgeSentence.replace("and","judges",1)


    #This is where we begin filtering only the judge names.
    if "judges" in judgeSentence and len(judgeSentence.split("judges")) == 2:
        #phraseList is a list of names and the word "president", with other phrases such as "appointed for Finland" mixed in
        phraseList = judgeSentence.split("judges")[0].split(',')
        #judgeList is a list of judge names and words like "president" or "ad hoc judge" to give greater specificity
        judgeList = []
        for phrase in phraseList:
            phrase = phrase.strip(" ").strip(" ").strip(" ")
            if phrase.strip(' ') != "":
                if phrase[:3] == "and":
                    phrase = phrase.replace("and","",1)
                phrase = phrase.strip(' ').strip(' ').strip(' ')
                if phrase[:3] == "and":
                    phrase = phrase.replace("and","",1)
                if phrase[:4] == "also":
                    phrase = phrase.replace("also","",1)
                phrase = phrase.strip(' ')
                if phrase[:2] == "of":
                    phrase = phrase.replace("of","",1)
                phrase = phrase.strip(' ').strip(' ')
                if not "appoint" in phrase and phrase.strip(' ') != "" and phrase.strip(' ') != "":
                    phrase = phrase.strip(' ').strip(' ').strip(' ').strip(' ')
                    judgeList.append(phrase)

        #secondPhraseList is a list mainly composed of registrar names and ad hoc judges, along with some extraneous info
        secondPhraseList = judgeSentence.split("judges")[1].split(',')
        #registrarList is a list of registrar names and ad hoc judge names, plus words like "deputy registrar" or "ad hoc judge"
        #Every registrarList should have an even number of items (each name should be followed by a title like "ad hoc judge" or "Deputy Section Registrar")
        registrarList = []
        for phrase in secondPhraseList:
            if not "appoint" in phrase and phrase.strip(' ') != "":
                phrase = phrase.strip('\n')
                if phrase[:3] == "and":
                    phrase = phrase.replace("and","",1)
                phrase = phrase.strip(' ').strip(' ').strip(' ')
                if phrase[:4] == "[a1]":
                    phrase = phrase.replace("[a1]","",1)
                elif phrase[:4] == "[a2]":
                    phrase = phrase.replace("[a2]","",1)
                elif phrase[:4] == "[a3]":
                    phrase = phrase.replace("[a3]","",1)
                elif "[Note1]" in phrase:
                    phrase = phrase.replace("[Note1]","",1)
                elif "[1]" in phrase:
                    phrase = phrase.replace("[1]","",1)
                if phrase[:3] == "and":
                    phrase = phrase.replace("and","",1)
                if phrase[:4] == "also":
                    phrase = phrase.replace("also","",1)
                phrase = phrase.strip(' ')
                if phrase[:2] == "of":
                    phrase = phrase.replace("of","",1)
                phrase = phrase.strip(' ').strip(' ')
                if phrase[:5] == 'AndMr':
                    phrase = phrase.replace("And","",1)
                if "deliberate" in phrase and "." in phrase:
                    phrase = phrase.split('.')[0]
                elif "deliberate" in phrase and "having" in phrase:
                    phrase = phrase.split("having")[0].strip(' ')
                elif "Having" in phrase:
                    phrase = phrase.split("Having")[0].strip(' ')
                if phrase.strip(' ') != "":
                    registrarList.append(phrase)

        #write information to output file
        #Each line = itemid of court report + tab space + judgename1 + tab + "president" (if judgename1 is a president) + tab + judgename2 + ... + judgenameN + tab + "ad hoc judge" (if judgenameN is an ad hoc) + tab + registrarname + tab + "Section Registrar"
        """
        o.write(itemid)
        o.write('\t')
        for name in judgeList:
            o.write(name)
            o.write('\t')
        for name in registrarList:
            o.write(name)
            o.write('\t')
        o.write('\n')
        """

        #concatenate the two lists
        totalList = judgeList + registrarList


        for i in range(0,len(totalList)):
            if not "president" in totalList[i].lower() and not "président" in totalList[i].lower() and not "hoc" in totalList[i] and not "substitute judge" in totalList[i] and not "jurisconsult" in totalList[i].lower() and not "registrar" in totalList[i].lower() and not "registar" in totalList[i].lower() and not "regisrar" in totalList[i].lower() and not "regitrar" in totalList[i].lower() and not "regstrar" in totalList[i].lower():
                #94392 people in total
                numPeople += 1
                current_judge = Judge(itemid, totalList[i])
                #if i+1 is a valid index (if there is a next item in totalList after totalList[i])
                if (i+1) < len(totalList):
                    #Fun Fact: Every first judge name in each line is a president
                    #11377 presidents
                    if "president" in totalList[i+1].lower() or "président" in totalList[i+1].lower():
                        current_judge.president = True
                        numPresident += 1
                    #775 ad hoc judges
                    if "hoc" in totalList[i+1]:
                        current_judge.adhoc = True
                        numAdHoc += 1
                    #18 substitute judges
                    if "substitute judge" in totalList[i+1]:
                        current_judge.substitute = True
                        numSubstitute += 1
                    #50 jurisconsults
                    if "jurisconsult" in totalList[i+1].lower():
                        current_judge.jurisconsult = True
                        numJurisconsult += 1
                    #12066 registrars
                    if "registrar" in totalList[i+1].lower() or "registar" in totalList[i+1].lower() or "regisrar" in totalList[i+1].lower() or "regitrar" in totalList[i+1].lower() or "regstrar" in totalList[i+1].lower():
                        current_judge.registrar = True
                        numRegistrar += 1
                o.write('http://hudoc.echr.coe.int/eng?i=' + current_judge.itemid + '\t')
                o.write(current_judge.display_judge())
                o.write('\n')


    #count number of lines in source file (number of court cases)
    numlines += 1


o.close()

print "There are", numlines, "lines in the source file."
print numPresident,"Presidents"
print numAdHoc,"Ad Hoc Judges"
print numSubstitute,"Substitute Judges"
print numJurisconsult,"Jurisconsults"
print numRegistrar,"Registrars"
print numPeople,"People In Total"