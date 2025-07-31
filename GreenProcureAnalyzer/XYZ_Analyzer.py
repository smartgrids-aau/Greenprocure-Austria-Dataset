
from matplotlib import pyplot as plt
from pandas import DataFrame
import pandas as pd
from tableConfig import TableRunConfig
import seaborn as sns

def Analyze(runConfig: TableRunConfig):
    prodStr = runConfig.jsonData['columns']['Products']
    if not runConfig.df_abc_fuels.empty:
        runConfig.df_xyz_fuels = __analyze(runConfig, "Treibstoffe", runConfig.df_split_fuels, runConfig.df_abc_fuels)
        #runConfig.df_abc_fuels = runConfig.df_abc_fuels.merge(runConfig.df_xyz_fuels, how="right", on=prodStr)        
        runConfig.df_xyz_co2_fuels = __analyze_CO2(runConfig, "Treibstoffe", runConfig.df_split_fuels, runConfig.df_abc_fuels)
        #runConfig.df_abc_fuels = runConfig.df_abc_fuels.merge(runConfig.df_xyz_co2_fuels, how="right", on=prodStr)
        #runConfig.df_abc_fuels.columns = runConfig.df_abc_fuels.iloc[0]
    
    if not runConfig.df_abc_consumables.empty:
        runConfig.df_xyz_consumables = __analyze(runConfig, "Verbrauchsgüter", runConfig.df_split_consumables, runConfig.df_abc_consumables)
        #runConfig.df_abc_consumables = runConfig.df_abc_consumables.merge(runConfig.df_xyz_consumables,how="right",on=prodStr)
        runConfig.df_xyz_co2_consumables = __analyze_CO2(runConfig, "Verbrauchsgüter", runConfig.df_split_consumables, runConfig.df_abc_consumables)
        #runConfig.df_abc_consumables = runConfig.df_abc_consumables.merge(runConfig.df_xyz_co2_consumables, how="right", on=prodStr)
        #runConfig.df_abc_consumables.columns = runConfig.df_abc_consumables.iloc[0]
    
    if not runConfig.df_abc_usables.empty:    
        runConfig.df_xyz_reusables = __analyze(runConfig, "Gebrauchsgüter", runConfig.df_split_resuables, runConfig.df_abc_usables)
        #runConfig.df_abc_usables = runConfig.df_abc_usables.merge(runConfig.df_xyz_reusables, how="right", on=prodStr)
        runConfig.df_xyz_co2_reusables = __analyze_CO2(runConfig, "Gebrauchsgüter", runConfig.df_split_resuables, runConfig.df_abc_usables)
        #runConfig.df_abc_usables = runConfig.df_abc_usables.merge(runConfig.df_xyz_co2_reusables, how="right", on=prodStr)
        #runConfig.df_abc_usables.columns = runConfig.df_abc_usables.iloc[0]
    
    
def __analyze(runConfig: TableRunConfig, prefixStr : str, df_original : DataFrame, df_abc : DataFrame):
    print("running Cost XYZ on ", prefixStr)
    costStr = runConfig.jsonData['columns']['Cost']
    prodStr = runConfig.jsonData['columns']['Products']
    dateStr = runConfig.jsonData['columns']['Date']
    dateFormat = runConfig.jsonData['dateformat']
    
    #Cost development
    As = df_abc.nlargest(500, costStr)
    df_orig_filtered = df_original[df_original[prodStr].isin(As[prodStr])].copy()
    #(df_orig_filtered.head())
    
    df_orig_filtered[dateStr] = pd.to_datetime(df_orig_filtered[dateStr], format=dateFormat).dt.date
    
    df_12m = df_orig_filtered.assign(cost_date = pd.to_datetime(df_orig_filtered[dateStr]).dt.strftime("%Y-%m"))

    #pivot table along months
    df_12m_units = df_12m.groupby([prodStr,'cost_date'])[costStr].sum().to_frame().reset_index()
    #print(df_12m_units.head())
    
    #Since our above data is in long format, rather than wide format, we need to reshape the data using Pandas. 
    # We can do this using the pivot() function. We’ll put each SKU on its own line and store the quantity of 
    # units sold in each month in its own column.
    df_12m_units = df_12m_units.pivot(index=prodStr, columns='cost_date', values=costStr)\
                           .reset_index().fillna(0)
    #print(df_12m_units.head())

    #calculate standard deviation
    #"""Next we need to calculate the standard deviation in the monthly demand for each SKU. 
    # We can do this by creating a subset of the month columns and appending .std(axis=1) 
    # in order to calculate the standard deviation in the values within each row. 
    # We’ll assign that value back to the dataframe in a new column.
    df_12m_units['std_cost'] = df_12m_units[df_12m_units.columns.difference([prodStr, 'cost_date'])].std(axis=1)

    #Calculate total demand
    #Since we also need to know the annual demand, we next need to calculate the sum() of all of the monthly data, 
    # which we can do simply by adding the columns together and then assigning them to a new field using the assign() function.
    df_12_units_months = df_12m_units.columns.difference([prodStr, 'cost_date', 'std_cost'])
    df_12m_units['total_cost'] = df_12m_units[df_12_units_months].sum(numeric_only=True, axis=1)

    #Calculate average monthly demand
    #To calculate the average demand for each SKU across the year we can divide the total_demand column value 
    # by the number of months in the dataset - 12 - to obtain the mean for the period.
    df_12m_units = df_12m_units.assign(avg_monthly_cost = df_12m_units['total_cost'] / len(df_12_units_months) )
    #print(df_12m_units.head())

    #Calculate Coefficient of Variation in demand
    #Finally, we can calculate the amount of variation seen in demand for each SKU across the year. 
    # To measure the variation, and therefore the forecastability, we can use a calculation called the Coefficient of Variation or CV. 
    # This is the mean demand over the standard deviation in demand. A value closer to zero implies that there’s minimal variation and
    # higher predictability, while high values imply the opposite.
    df_12m_units['cov_cost'] = df_12m_units['std_cost'] / df_12m_units['avg_monthly_cost']
    
    #df_12m_units['XYZ_Cost'] = df_12m_units['cov_cost'].apply(XYZ_Assignment)
    df_12m_units['XYZ_Cost'] = "Z"
    df_12m_units.loc[df_12m_units['cov_cost'] <= df_12m_units['cov_cost'].max() / 100 * 80, 'XYZ_Cost'] = "Y"
    df_12m_units.loc[df_12m_units['cov_cost'] <= df_12m_units['cov_cost'].max() / 100 * 50, 'XYZ_Cost'] = "X"
    
    #df_12m_units['XYZ_Cost'][df_12m_units['cov_cost'] <= df_12m_units['cov_cost'].max() / 100 * 50] = 
    #df_12m_units['XYZ_Cost'][df_12m_units['cov_cost'] <= df_12m_units['cov_cost'].max() / 100 * 25] = "X"
    
   # print(df_12m_units.sort_values(by='cov_cost', ascending=False).head(5))
    #print("min : ", df_12m_units['cov_cost'].min(),", mean : ", df_12m_units['cov_cost'].mean(),", max : ",df_12m_units['cov_cost'].max() )

    #f, ax = plt.subplots(figsize=(15, 6))
    #ax = sns.distplot(df_12m_units['cov_cost']).set_title("Coefficient of Variation",fontsize=15)
    #plt.clf()
    #df_12m_units['XYZ_Cost'] = df_12m_units['cov_cost'].apply(XYZ_Assignment)
    #print(df_12m_units.XYZ_Cost.value_counts())
    df_12m_units.to_excel(runConfig.output + prefixStr + "XYZ_Cost_Timeline.xlsx")
    #df_12m_units.to_excel('../Output/xyz_' + prefixStr +  runConfig.tableFileName)
    
    ###df_abc.sort_values(prodStr, inplace=True, ascending=False)
    df_12m_units.sort_values(prodStr, inplace=True, ascending=False)
    df_abc["XYZ_Cost"] = df_12m_units['XYZ_Cost']
    
    #df_abc["XYZ_Cost_Class"] = df_12m_units[df_12m_units[prodStr] == df_abc[prodStr]]["XYZ_Cost"]
    
    return df_12m_units

def __analyze_CO2(runConfig: TableRunConfig, prefixStr : str, df_original : DataFrame, df_abc : DataFrame):
    print("running CO2 XYZ on ", prefixStr)
    costStr = "kgCO2Equivalent"
    prodStr = runConfig.jsonData['columns']['Products']
    dateStr = runConfig.jsonData['columns']['Date']
    dateFormat = runConfig.jsonData['dateformat']
    
    #Cost development
    As = df_abc.nlargest(500, costStr)
    df_orig_filtered = df_original[df_original[prodStr].isin(As[prodStr])].copy()
    #print(df_orig_filtered.head())
    
    df_orig_filtered[dateStr] = pd.to_datetime(df_orig_filtered[dateStr], format=dateFormat).dt.date
    
    df_12m = df_orig_filtered.assign(date = pd.to_datetime(df_orig_filtered[dateStr]).dt.strftime("%Y-%m"))

    #pivot table along months
    df_12m_units = df_12m.groupby([prodStr,'date'])[costStr].sum().to_frame().reset_index()
    #print(df_12m_units.head())
    
    #Since our above data is in long format, rather than wide format, we need to reshape the data using Pandas. 
    # We can do this using the pivot() function. We’ll put each SKU on its own line and store the quantity of 
    # units sold in each month in its own column.
    df_12m_units = df_12m_units.pivot(index=prodStr, columns='date', values=costStr)\
                           .reset_index().fillna(0)
    #print(df_12m_units.head())

    #calculate standard deviation
    #"""Next we need to calculate the standard deviation in the monthly demand for each SKU. 
    # We can do this by creating a subset of the month columns and appending .std(axis=1) 
    # in order to calculate the standard deviation in the values within each row. 
    # We’ll assign that value back to the dataframe in a new column.
    df_12m_units['std_co2'] = df_12m_units[df_12m_units.columns.difference([prodStr, 'date'])].std(axis=1)

    #Calculate total demand
    #Since we also need to know the annual demand, we next need to calculate the sum() of all of the monthly data, 
    # which we can do simply by adding the columns together and then assigning them to a new field using the assign() function.
    df_12_units_months = df_12m_units.columns.difference([prodStr, 'date', 'std_co2'])
    df_12m_units['total_co2'] = df_12m_units[df_12_units_months].sum(numeric_only=True, axis=1)

    #Calculate average monthly demand
    #To calculate the average demand for each SKU across the year we can divide the total_demand column value 
    # by the number of months in the dataset - 12 - to obtain the mean for the period.
    df_12m_units = df_12m_units.assign(avg_monthly_co2 = df_12m_units['total_co2'] / len(df_12_units_months) )
    #print(df_12m_units.head())

    #Calculate Coefficient of Variation in demand
    #Finally, we can calculate the amount of variation seen in demand for each SKU across the year. 
    # To measure the variation, and therefore the forecastability, we can use a calculation called the Coefficient of Variation or CV. 
    # This is the mean demand over the standard deviation in demand. A value closer to zero implies that there’s minimal variation and
    # higher predictability, while high values imply the opposite.
    df_12m_units['cov_co2'] = df_12m_units['std_co2'] / df_12m_units['avg_monthly_co2']
    
    #df_12m_units['XYZ_Cost'] = df_12m_units['cov_cost'].apply(XYZ_Assignment)
    df_12m_units['XYZ_CO2'] = "Z"
    df_12m_units.loc[df_12m_units['cov_co2'] <= df_12m_units['cov_co2'].max() / 100 * 80, 'XYZ_CO2'] = "Y"
    df_12m_units.loc[df_12m_units['cov_co2'] <= df_12m_units['cov_co2'].max() / 100 * 50, 'XYZ_CO2'] = "X"
    

    #fac = (df_12m_units['cov_co2'].max() / df_12m_units['cov_co2'].min())**(1/3)
    # df_12m_units['cov_co2'].min()*fac = X
    # df_12m_units['cov_co2'].min()*(fac^2) = Z

    #df_12m_units['XYZ_Cost'][df_12m_units['cov_cost'] <= df_12m_units['cov_cost'].max() / 100 * 50] = 
    #df_12m_units['XYZ_Cost'][df_12m_units['cov_cost'] <= df_12m_units['cov_cost'].max() / 100 * 25] = "X"
    
   # print(df_12m_units.sort_values(by='cov_cost', ascending=False).head(5))
    #print("min : ", df_12m_units['cov_cost'].min(),", mean : ", df_12m_units['cov_cost'].mean(),", max : ",df_12m_units['cov_cost'].max() )

    #f, ax = plt.subplots(figsize=(15, 6))
    #ax = sns.distplot(df_12m_units['cov_cost']).set_title("Coefficient of Variation",fontsize=15)
    #plt.clf()
    #df_12m_units['XYZ_Cost'] = df_12m_units['cov_cost'].apply(XYZ_Assignment)
    #print(df_12m_units.XYZ_Cost.value_counts())
    df_12m_units.to_excel(runConfig.output + prefixStr + "XYZ_CO2_Timeline.xlsx")
    #df_12m_units.to_excel('../Output/xyz_co2_' + prefixStr +  runConfig.tableFileName)
    
    ###df_abc.sort_values(prodStr, inplace=True, ascending=False)
    df_12m_units.sort_values(prodStr, inplace=True, ascending=False)
    df_12m_units.set_index("Text")
    #print(df_12m_units.head())
    df_abc["XYZ_CO2"] = df_12m_units['XYZ_CO2']
    
    #df_abc["XYZ_Cost_Class"] = df_12m_units[df_12m_units[prodStr] == df_abc[prodStr]]["XYZ_Cost"]
    
    return df_12m_units

def XYZ_Assignment(cov):
    """Apply an XYZ classification to each product based on 
    its coefficient of variation in order quantity.

    :param cov: Coefficient of variation in order quantity for SKU
    :return: XYZ inventory classification class
    """

    if cov <= 0.5:
        return 'X'
    elif cov > 0.5 and cov <= 1.0:
        return 'Y'
    else:
        return 'Z'
