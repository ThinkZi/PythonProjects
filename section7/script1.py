""" A script to generate random names with user controling the use of vowels and consonants"""
import string
import random

NumberofNames = 10
#Determin the number of letters in the name
NumberofLetters = 0
if NumberofLetters <1:
    NumberOfLetters = int(input("Enter the number of letters in the name: "))

#Determine if each letter is a vowel, consonant or any letter
Vowels="aeiouy"

#Generating consonant by removing the vowels from lowercase letters
Consonants=string.ascii_lowercase
for letter in Vowels:
    Consonants.replace(letter,"")

def GetValidLetterType():
    LetterType="00"
    #repeat asking for valid entry as long as the inputs are not correct
    while(not(LetterType in string.ascii_letters or LetterType in ["1","2","3"]) or len(LetterType)!=1):
        LetterType=input("Enter the letter you want or 1 for vowel, 2 for consonant, 3 for any letter: ")
    return LetterType

def DefineNameLetter(LetterType):
    if LetterType=='1':
        return random.choice(Vowels)
    elif LetterType=='2':
        return random.choice(Consonants)
    elif LetterType=='3':
        return random.choice(string.ascii_letters)
    else:
        return LetterType
#Returns a list which contains the string indexes of the name e.g. ["1","a","3"] for a three letter name
def ConstructNamekey():
    Namekey=list()
    for i in range(NumberOfLetters):
        print("Letter #", i+1, ":")
        Namekey.append(GetValidLetterType())
    return Namekey

def ConstructName(Namekey):
    Name=""
    for i in range(len(Namekey)):
        Name=Name+DefineNameLetter(Namekey[i])
    return Name

Namekey=ConstructNamekey()

print(Namekey)
for i in range(NumberofNames):
    print(ConstructName(Namekey))
