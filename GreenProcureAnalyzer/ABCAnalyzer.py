from pandas import DataFrame
from CO2_Assigner import CO2_Assignment
from co2data import CO2Values
from tableConfig import TableRunConfig


def Analyze(runConfig : TableRunConfig):
    print("ABC analysis on", runConfig.outFileNameWithoutExtension)
    print(runConfig.df_split_fuels.head())
    print(runConfig.df_split_consumables.head())
    print(runConfig.df_split_resuables.head())
    runConfig.df_abc_fuels = __analyze(runConfig, runConfig.df_split_fuels)
    runConfig.df_abc_consumables = __analyze(runConfig, runConfig.df_split_consumables)
    runConfig.df_abc_usables = __analyze(runConfig, runConfig.df_split_resuables)
    
    co2Data : CO2Values = CO2Values(productColumnName=runConfig.jsonData['columns']['Products'])
    runConfig.df_abc_fuels = co2Data.ProcessValues(runConfig.df_abc_fuels, runConfig.outFileNameWithoutExtension)
    runConfig.df_abc_consumables = co2Data.ProcessValues(runConfig.df_abc_consumables, runConfig.outFileNameWithoutExtension)
    runConfig.df_abc_usables = co2Data.ProcessValues(runConfig.df_abc_usables, runConfig.outFileNameWithoutExtension)

def __analyze(runConfig : TableRunConfig, df : DataFrame):
    print("ABC analysis on", runConfig.outFileNameWithoutExtension )
    print(df.head())
    costStr = runConfig.jsonData['columns']['Cost']
    prodStr = runConfig.jsonData['columns']['Products']
    outputColumns = set(runConfig.jsonData['outputcolumns'])
    outputColumns.add(costStr)
    outputColumns.add(prodStr)
    df_sub = df.copy()
    
    df_sub = df_sub[df_sub[costStr] >= 0]

    df_sub = df_sub.groupby([prodStr]).sum(numeric_only=True)
    
    print(df_sub.head())
    
    df_sub = df_sub.sort_values(by=[costStr], ascending=False)    
    
    df_sub['CostCumSum'] = round(df_sub[costStr].cumsum(),2)
    df_sub["TotalCost"] = round(df_sub[costStr].sum(), 2)
    df_sub['Cost%'] = round(df_sub[costStr] / df_sub["TotalCost"], 2)
    df_sub['CostCum%'] = round(df_sub['CostCumSum'] / df_sub["TotalCost"], 2)
    df_sub['ABC_Cost_Rank'] = df_sub[costStr].rank().astype(int)
    df_sub['ABC_Cost'] = df_sub['ABC_Cost_Rank'].apply(ABC_segmentation_Ranked, maxRank = df_sub["ABC_Cost_Rank"].max())
    df_sub.reset_index(inplace=True)
    
    print("CO2 value ABC...")
    print(df_sub.head())
        
    co2valStr = "kgCO2Equivalent"
    df_sub = df_sub.sort_values(by=[co2valStr], ascending=False)
    df_sub['RunningCO2Cumulative'] = round(df_sub[co2valStr].cumsum(), 2)
    df_sub["totalCO2"] = round(df_sub[co2valStr].sum(),2)
    df_sub['CO2%'] = round(df_sub[co2valStr] / df_sub["totalCO2"], 2)
    df_sub['CO2Cumulative%'] = round(df_sub['RunningCO2Cumulative'] / df_sub["totalCO2"], 2)
    df_sub['ABC_CO2_Rank'] = df_sub['kgCO2Equivalent'].rank().astype(int)
    df_sub['ABC_CO2'] = df_sub['ABC_CO2_Rank'].apply(ABC_segmentation_Ranked, maxRank = df_sub["ABC_CO2_Rank"].max())
    df_sub.reset_index(inplace=True)

    print(df_sub.head())
    
    return df_sub

def ABC_segmentation(RunPerc):
    if RunPerc > 0 and RunPerc < 0.2:
        return 'A'
    elif RunPerc >= 0.2 and RunPerc < 0.50:
        return 'B'
    elif RunPerc >=0.50:
        return 'C'
    else:
        return 'Q'
    
def ABC_segmentation_Ranked(rank, maxRank : float):
    ratio : float = rank / maxRank
    if ratio > 0.8 :
        return 'A'
    elif ratio <= 0.8 and ratio > 0.50:
        return 'B'
    elif ratio <=0.50:
        return 'C'
    else:
        return 'Q'
