import re
from pandas import DataFrame
from co2data import CO2Values
from config import Config
from tableConfig import TableRunConfig
import TimeFilter
import os
def PreProcess(runConfigs : list[TableRunConfig]):
    print("Preprocessing ...")
    
    #filter out years we are not interested in
    for runConfig in runConfigs:
        print("\nFiltering table", runConfig.outFileNameWithoutExtension, "with", len(runConfig.tableData), "items\n")
        runConfig.tableData = TimeFilter.FilterTime(runConfig, runConfig.tableData)
    """
    for runConfig in runConfigs:
        runConfig.df_split_fuels = ReplaceToCommonTerms(runConfig, runConfig.df_split_fuels)
        runConfig.df_split_consumables = ReplaceToCommonTerms(runConfig, runConfig.df_split_consumables)
        runConfig.df_split_resuables = ReplaceToCommonTerms(runConfig, runConfig.df_split_resuables)
    """     
    #set up split data
    for config in runConfigs:
        print(len(config.tableData))

        config.df_replaced = ReplaceToCommonTerms(config, config.tableData)
        config.df_replaced["Num"] = 1
        
        config.df_replaced.to_excel(runConfig.output + "all_wares_replaced.xlsx")
        #config.df_replaced.to_excel("all_wares_replaced.xlsx")
        
        df_empty = config.df_replaced[config.df_replaced["Menge (in Gramm)"].isna()]
        print(df_empty.head())
        
        df_empty.to_excel(runConfig.output + "unused_wares.xlsx")
        #df_empty.to_excel("unused_wares.xlsx")
        
        #add in CO2 values    
        co2Data : CO2Values = CO2Values(productColumnName=config.jsonData['columns']['Products'])

        if not co2Data.Valid():
            print("CO2Data.xlsx file empty")
            exit()
            
        config.df_replaced = co2Data.ProcessValues(config.df_replaced, config.outFileNameWithoutExtension)
        
        fuelitems : list[str] = config.jsonData["WarenTypen"]["Treibstoffe"]
        consumableItems : list[str] = config.jsonData["WarenTypen"]["Verbrauchsgüter"]
        reusableItems : list[str] = config.jsonData["WarenTypen"]["Gebrauchsgüter"]
        
        #allitems = fuelitems + consumableItems + reusableItems
        #print("Allitems : \n", allitems)        
        prodStr = config.jsonData['columns']['Products']
    
        df_replaced = config.df_replaced
        print("\nSplitting up tables...\n")
        config.df_split_fuels = df_replaced.loc[df_replaced[prodStr].isin(fuelitems)]
        print(len(config.df_split_fuels))
        config.df_split_consumables = df_replaced.loc[df_replaced[prodStr].isin(consumableItems)] 
        print(len(config.df_split_consumables))
        config.df_split_resuables = df_replaced.loc[df_replaced[prodStr].isin(reusableItems)]
        print(len(config.df_split_resuables))
    
        
        #exit()
    
        
        print("\nDone!")

def ReplaceToCommonTerms(runConfig: TableRunConfig, df : DataFrame):
    print("\nReplacing common terms in", runConfig.outFileNameWithoutExtension, "with", len(runConfig.tableData), "items\n")
    data : DataFrame = df.copy()

    """Explanation for the regex:

    ^ is line start
    (space and plus, +) is one or more spaces
    | is or
    $ is line end.

    So it searches for leading (line start and spaces) and trailing (spaces and line end) spaces and replaces them with an empty string.
    """
    data.replace(r"^ +| +$", r"", regex=True, inplace=True)
    #also replace trailing commas
    data.replace(r",$", r"", regex=True, inplace=True)
    
    replacements = runConfig.jsonData["replace"]
    if replacements != None :
        for column in replacements:
            print("Replacing items in column ", column)
            columndata = replacements[column]
            for replacement in columndata:
                print("replacing ", columndata[replacement], " with " , replacement)
                [data.replace(re.compile('.*' + replaced + '.*', re.IGNORECASE), replacement, inplace=True) for replaced in columndata[replacement]]
    print("done")                
    return data
