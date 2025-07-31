from pandas import DataFrame
from tableConfig import TableRunConfig
from datetime import datetime, timedelta
import pandas as pd
from config import Config

def FilterTime(runConfig: TableRunConfig, df : DataFrame):
    print("Filtering time for", runConfig.outFileNameWithoutExtension)
    yearColumn = runConfig.jsonData["columns"]["Year"]
    if(not yearColumn):
        print("no year column, skipping filtering dates")
        return df
    minYearInt : int = Config.get("MinYear", 2000)
    maxYearInt : int = Config.get("MaxYear", 3000)
    
    df = df[df[yearColumn] >= minYearInt]
    df = df[df[yearColumn] <= maxYearInt]
    
    df.to_excel(runConfig.output + "Timefiltered.xlsx")
    
    #outputName = '../Output/' + runConfig.outFileNameWithoutExtension + "_Time_" + str(minYearInt) + "_" + str(maxYearInt) + runConfig.outFileExtension
    #df.to_excel(outputName)
    return df
