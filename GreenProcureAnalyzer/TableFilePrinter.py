from pandas import DataFrame
from tableConfig import TableRunConfig


def PrintTables(runConfigs : list[TableRunConfig]):
    
    for runConfig in runConfigs:
        runConfig.df_abc_usables.set_index("index", inplace=True)
        runConfig.df_abc_usables.reset_index(drop=True,inplace=True)
        runConfig.df_abc_usables.to_excel(runConfig.output + '_abc_gebrauch.xlsx')
        #runConfig.df_abc_usables.to_excel('../Output/' + runConfig.outFileNameWithoutExtension + '_abc_gebrauch_' + runConfig.outFileExtension)
        runConfig.df_abc_consumables.set_index("index", inplace=True)
        runConfig.df_abc_consumables.reset_index(drop=True,inplace=True)
        runConfig.df_abc_consumables.to_excel(runConfig.output + '_abc_verbrauch.xlsx')
        #runConfig.df_abc_consumables.to_excel('../Output/' + runConfig.outFileNameWithoutExtension + '_abc_verbrauch_' + runConfig.outFileExtension)
        Print_Counts(runConfig)


def Print_Counts(runConfig : TableRunConfig):
    costStr = runConfig.jsonData['columns']['Cost']
    prodStr = runConfig.jsonData['columns']['Products']
    dateStr = runConfig.jsonData['columns']['Date']
    
    def l(runConfig : TableRunConfig, suffix : str, df: DataFrame) :
        df_counts = df.copy()
        df_counts['num'] = 1
        df_counts = df_counts.groupby(prodStr).sum(numeric_only=True)
        df_counts.sort_values(by=['num'], ascending = False, inplace=True )
        df_counts.reset_index(drop=True,inplace=True)
        df_counts.to_excel(runConfig.output + suffix + '_Num.xlsx')
    
    l(runConfig, "Treibstoff", runConfig.df_split_fuels)
    l(runConfig, "Verbrauch", runConfig.df_split_consumables)
    l(runConfig, "Gebrauch", runConfig.df_split_resuables)
