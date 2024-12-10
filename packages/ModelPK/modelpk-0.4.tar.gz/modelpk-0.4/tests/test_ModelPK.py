import unittest
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from ModelPK.extractPKparam import LoadData
from ModelPK.extractPKparam import PrepData
from ModelPK.extractPKparam import findCmax
from ModelPK.extractPKparam import findCo
from ModelPK.extractPKparam import findT_half
from ModelPK.extractPKparam import findPK
from simulatePK import findSubtherapeuticTime

testdf=LoadData("src/Test_PK.xlsx")
testdf2=PrepData(testdf,"IV Concentration","LnConc")
testresult=findPK(testdf2,"Time","IV Concentration","LnConc",10)

class TestModelPK(unittest.TestCase):
    def test_LoadData(self):
        result=LoadData('src/Test_PK.xlsx')
        self.assertIsInstance(result,pd.DataFrame)
    def test_badLoadData(self):
        result=LoadData("Functional Specification.docx")
        with self.assertRaises(Exception):
            self.assertIsInstance(result,pd.DataFrame)
    
    def test_PrepData(self):
        result=PrepData(testdf,"IV Concentration","LnConc")
        self.assertNotIn(np.nan,result)
        self.assertGreater(result.size,testdf.size)
        self.assertIsInstance(result,pd.DataFrame)
    def test_badPrepData(self):
        with self.assertRaises(Exception):
            PrepData(testdf,"Not Real Column Name","LnConc")

    def test_findT_half(self):
        result=findT_half(testdf2,"Time","IV Concentration",10)
        print(result)
        for i in testdf2.index:
            for j in testdf2.index:
                if j>i and testdf2["Time"][j]-testdf2["Time"][i]==result:
                    self.assertAlmostEquals(testdf2["IV Concentration"][j]/testdf2["IV Concentration"][i],0.5,delta=0.05)
                    break

    def test_findCmax(self):
        result=findCmax(testdf2,"Time","IV Concentration")
        self.assertEqual(result[0],np.nanmax(testdf2["IV Concentration"]))
        self.assertEqual(len(result),2)

    def test_findCo(self):
        result=findCo(testdf2,"Time","LnConc")
        with self.assertRaises(Exception):
            findCo(testdf2,"Time","LnConc","not an established model")
        self.assertEqual(len(result),2)

    def test_findPK(self):
        result=findPK(testdf2,"Time","IV Concentration","LnConc",10)
        self.assertIsInstance(result,tuple)
        self.assertEqual(len(result),5)

    def test_findSubtherapeuticTime(self):
        result=findSubtherapeuticTime(testresult,10,3,simendtime=75)
        result2=findSubtherapeuticTime(testresult,10,3,setCo=1000)
        self.assertEqual(result,121.5)
        self.assertGreater(result2,result)

if __name__ == '__main__':
    unittest.main()