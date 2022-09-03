import numpy as np
from typing import Any, Dict, List
from spellchecker import SpellChecker
import pandas as pd
spell = SpellChecker()


class Atom():
    def __init__(self,experience: float, timezone: str, language1:Any, language2:Any, language3:Any, majors: List[str], exp_weight:float):
        self.experience = experience*exp_weight
        self.timezone = timezone
        self.lang1 = language1
        self.lang2 = language2
        self.lang3 = language3
        self.majors = majors
        self.weight = exp_weight

    def convertTimeZone(self,timezone: str, k:int) -> float:
        # GMT+10.5
        timezoneee = timezone.replace("GMT", "")
        timezonee = float(timezoneee)        
        return (1/(1 + np.exp(-timezonee)))*k

    def normalizeLangs(self)->List[float]:
        p1 = float(list(self.lang1.values())[0])
        p2 = float(list(self.lang2.values())[0])
        p3 = float(list(self.lang3.values())[0])
        sump = p1 + p2 + p3
        return [p1/sump, p2/sump, p3/sump]

    def getlangnames(self)->List[str]:
        n1 = list(self.lang1.keys())[0]
        n2 = list(self.lang2.keys())[0]
        n3 = list(self.lang3.keys())[0]
        return [n1, n2, n3]

    def loadLangs(self,lang1: str, lang2: str, lang3: str):
        normed_langs = self.normalizeLangs()
        langs = self.getlangnames()
        df = pd.read_csv("langs.csv")
        langsArr = np.array([x.lower() for x in df["name"].to_numpy()])
        listLangs = []
        words = [langs[0].lower(), langs[1].lower(), langs[2].lower()]
        for idx,word in enumerate(words):
            wordsList = word.split()
            for i in range(len(wordsList)):
                wordsList[i] = spell.correction(wordsList[i])
            word = " ".join(wordsList)
            listLangs.append((langsArr == word)*normed_langs[idx])
        totalVals = np.zeros(df["name"].size)
        for lang in listLangs:
            totalVals += lang
        return totalVals   , langsArr

    def loadMajors(self,majors: List[str]):
        df = pd.read_csv("majors.csv")
        majors_array = df['Major'].to_numpy()
        listMajors = []
        for major in majors:
            wordsList = major.split()
            for i in range(len(wordsList)):
                wordsList[i] = spell.correction(wordsList[i])
            major = " ".join(wordsList)
            major = major.upper()
            listMajors.append(majors_array == major)
        totalVals = np.zeros(df["Major"].size)
        for major in listMajors:
            totalVals += major
        return (totalVals, majors_array)

    def proccess_for_one(self):
        langnums,langsArr  = self.loadLangs(self.lang1, self.lang2, self.lang3)
        majorsNums, majorArr = self.loadMajors(self.majors)
        years = self.experience
        timezone = self.convertTimeZone(self.timezone, 5)
        bigArr = np.concatenate((langnums, majorsNums, np.array([years, timezone])))
        labelsArr = np.concatenate((langsArr, majorArr, np.array(["experience", "timezone normalized"])))
        return bigArr, labelsArr
    
    def labelsArr(self):
        bigArr, labelsArr = self.proccess_for_one()
        return bigArr

def predict(atom1: Atom, atom2: Atom):
    bigArr1, labelsArr1 = atom1.proccess_for_one()
    bigArr2, labelsArr2 = atom2.proccess_for_one()
    return np.linalg.norm(bigArr1 - bigArr2), 


