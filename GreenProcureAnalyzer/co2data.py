from pandas import DataFrame
import pandas as pd

from tableConfig import TableRunConfig

class CO2Values:
    co2df : DataFrame
    prodStr : str
    co2ValuesColName : str = "gCO2Kg"
    def __init__(self, productColumnName : str) -> None:
        self.prodStr = productColumnName
        self.co2df : DataFrame = pd.read_excel("./CO2Data.xlsx")
        #self.co2df[self.co2ValuesColName].fillna(-1,inplace=True)
    
    def Valid(self) -> bool:
        return self.prodStr != None and not self.co2df.empty
    
    def GetValueFor(self, product : str) -> float:
        #print("Getting CO2 value for", product)
        co2df = self.co2df
        df_l = co2df.loc[co2df["Material"] == product, self.co2ValuesColName]
        if not df_l.empty :
            return df_l.item()        
        return None
    
    def ProcessValues(self, df : DataFrame, tblName : str):#
        print("Assigning CO2 values for table ", tblName)
        #df = runConfig.df_replaced.copy()
        print(df.head())
        print(len(df))
        #add in zero values for missing weight 
        
        df = df[df["Menge (in Gramm)"].notna()]
        #df = df[df["Menge (in Gramm)"] == -1]
        df["Menge (in kg)"] = df["Menge (in Gramm)"] / 1000
        print(df.head())
        print(len(df))
        df["gCO2PerKGWare"] = df[self.prodStr].apply(self.GetValueFor)
        #throw out all rows we don't have CO2 values for
        

        df = df[df["gCO2PerKGWare"].notna()]
        df["kgCO2PerKGWare"] = df["gCO2PerKGWare"] / 1000
        print(df.head())
        df["kgCO2Equivalent"] = df["kgCO2PerKGWare"] * df["Menge (in kg)"]
        print(len(df))
        print(df.head())
        return df
        #exit()


co2Values = {
    "Kopierpapier" : 0.75,
    "Toilettenpapier" : 0.4,
    "Müllsäcke" : 0.5376,
    "Blumen" : 0.1,
    "Splitt" : 0.0851, #Menge geschätzt
    "Flockungsmittel" : 0.47,
    "Diesel" : 16.81,
    "Treibstoff" : 16.81
}
