import pandas as pd



def sun():
    df = pd.read_csv('new_data/sun_data.csv')



    # Add a new column "Wind" with a default value (e.g., 0)
    df['technology'] = "SolarPV"
    df['hour'] = df.index
    df = df.rename(columns={'Dauer': 'value'})

    df = df[['technology', 'hour', 'value']]

    print(df)

    output_csv_path = ''

    # Save the DataFrame to a CSV file
    df.to_csv('new_data/sun_data_new.csv', index=False)

def wind():
    input_csv_path = 'new_data/p10y_station_id_282_01.01.2021-31.12.2022.csv'
    output_csv_path = 'new_data/wind.csv'  # Choose a name for the output file

    # Open the input file for reading and the output file for writing
    with open(input_csv_path, 'r') as infile, open(output_csv_path, 'w') as outfile:
        # Iterate through each line in the input file
        for line in infile:
            # Replace commas with periods and write the modified line to the output file
            modified_line = line.replace(',', '.')
            outfile.write(modified_line)

    df = pd.read_csv(output_csv_path)

    mask = df.apply(lambda row: row.astype(str).str.contains('2021').any(), axis=1)

    # Use the mask to drop the rows
    df = df[~mask]

    # Reset the DataFrame index
    df = df.reset_index(drop=True)

    # Split the single column by semicolon and select the part after the first semicolon (index 1)
    df['value'] = df.iloc[:, 0].str.split(';').str[1]
    
    # Add a new column "Wind" with a default value (e.g., 0)
    df['technology'] = "Wind"
    df['hour'] = df.index

    df = df[['technology', 'hour', 'value']]

    print(df)

    output_csv_path = ''

    # Save the DataFrame to a CSV file
    df.to_csv('new_data/wind_data_new.csv', index=False)

def temperature():
    txt_file_path = 'new_data/temp_stunde_20220317_20230917_00282.txt'

    # Read the text file into a DataFrame
    # Use a semicolon as the delimiter and skip rows starting with "#" as comments
    df = pd.read_csv(txt_file_path, delimiter=';', comment='#')

    mask = df.apply(lambda row: row.astype(str).str.contains('202301|202302|202303').any(), axis=1)

    # Create a new DataFrame with the filtered rows
    new_df = df[mask]

    mask = df.apply(lambda row: row.astype(str).str.contains('2023|202203').any(), axis=1)

    # Use the mask to drop the rows
    df = df[~mask]

    df = pd.concat([new_df, df], ignore_index=True)

    df['technology'] = "Temperature"
    df['hour'] = df.index
    df = df.rename(columns={'TT_TU': 'value'})

    df = df[['technology', 'hour', 'value']]

    print(df)

    df.to_csv('new_data/temperature_data_new.csv', index=False)

def total():
    df = pd.read_csv('new_data/Realisierter_Stromverbrauch_202201010000_202212312359_Stunde.csv', sep=';')
    df = df[['Datum', 'Anfang', 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen']]
    df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] = df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'].str.replace('.', '').str.replace(',', '.')
    df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] = df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'].astype(float)
    df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] *= 2.362

    # Create a DataFrame with the 'Anfang' column containing hours
    hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    mobility_winter = ['0,3', '0,3', '0,3', '0,3', '0,3', '0,3', '0,1', '0,7', '0,2', '0,2', '0,2', '0,2', '0,2', '0,2', '0,2', '0,2', '0,2', '0,7', '0,1', '0,1', '0,1', '0,1', '0,1', '0,1']
    heat_winter = ['0,2', '0,2', '0,2', '0,2', '0,2', '0,2', '0,5', '0,1', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,1', '0,4', '0,4', '0,3', '0,3', '0,3', '0,3']
    power_winter = ['0,5', '0,5', '0,5', '0,5', '0,5', '0,5', '0,4', '0,2', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,4', '0,2', '0,5', '0,5', '0,6', '0,6', '0,6', '0,6']

    data = {'Anfang': hours, 'Mobility': mobility_winter, 'Heat': heat_winter, 'Power': power_winter}
    winter = pd.DataFrame(data)

    # Create a DataFrame with the 'Anfang' column containing hours
    hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    mobility_summer = ['0,2', '0,2', '0,2', '0,2', '0,2', '0,2', '0,1', '0,65', '0,25', '0,25', '0,25', '0,25', '0,25', '0,25', '0,25', '0,25', '0,25', '0,65', '0,2', '0,2', '0,1', '0,1', '0,1', '0,1']
    heat_summer = ['0,1', '0,1', '0,1', '0,1', '0,1', '0,1', '0,1', '0,15', '0,15', '0,15', '0,15', '0,15', '0,15', '0,15', '0,15', '0,15', '0,15', '0,15', '0,1', '0,1', '0,1', '0,1', '0,1', '0,1']
    power_summer = ['0,7', '0,7', '0,7', '0,7', '0,7', '0,7', '0,8', '0,2', '0,6', '0,6', '0,6', '0,6', '0,6', '0,6', '0,6', '0,6', '0,6', '0,2', '0,7', '0,7', '0,8', '0,8', '0,8', '0,8']

    data = {'Anfang': hours, 'Mobility': mobility_summer, 'Heat': heat_summer, 'Power': power_summer}
    summer = pd.DataFrame(data)

    winter['Mobility'] = winter['Mobility'].str.replace(',', '.').astype(float)
    winter['Heat'] = winter['Heat'].str.replace(',', '.').astype(float)
    winter['Power'] = winter['Power'].str.replace(',', '.').astype(float)

    summer['Mobility'] = summer['Mobility'].str.replace(',', '.').astype(float)
    summer['Heat'] = summer['Heat'].str.replace(',', '.').astype(float)
    summer['Power'] = summer['Power'].str.replace(',', '.').astype(float)

    # Calculate the average for each column
    spring = pd.DataFrame({
        'Anfang': winter['Anfang'],
        'Mobility': (winter['Mobility'] + summer['Mobility']) / 2,
        'Heat': (winter['Heat'] + summer['Heat']) / 2,
        'Power': (winter['Power'] + summer['Power']) / 2
    })

    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')

    # Define the start and end dates for your filter
    start_date = pd.to_datetime('01.01.2022', format='%d.%m.%Y')
    end_date = pd.to_datetime('20.03.2022', format='%d.%m.%Y')

    # Apply the filter
    filtered_winter_1 = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

    # Define the start and end dates for your filter
    start_date = pd.to_datetime('21.03.2022', format='%d.%m.%Y')
    end_date = pd.to_datetime('20.06.2022', format='%d.%m.%Y')

    # Apply the filter
    filtered_spring = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        # Define the start and end dates for your filter
    start_date = pd.to_datetime('21.06.2022', format='%d.%m.%Y')
    end_date = pd.to_datetime('20.09.2022', format='%d.%m.%Y')

    # Apply the filter to keep rows with 'Datum' within the specified date range
    filtered_summer = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

    start_date = pd.to_datetime('21.09.2022', format='%d.%m.%Y')
    end_date = pd.to_datetime('20.12.2022', format='%d.%m.%Y')

    # Apply the filter to keep rows with 'Datum' within the specified date range
    filtered_autumn = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

    start_date = pd.to_datetime('21.12.2022', format='%d.%m.%Y')
    end_date = pd.to_datetime('31.12.2022', format='%d.%m.%Y')

    # Apply the filter to keep rows with 'Datum' within the specified date range
    filtered_winter_2 = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

        # Merge the two DataFrames based on the 'Anfang' column
    merged_df = filtered_winter_1.merge(winter, on='Anfang', how='inner')

    # Create new DataFrames by multiplying the columns
    mobility_total = pd.DataFrame({
        'Mobility': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Mobility']
    })
    heat_total = pd.DataFrame({
        'Heat': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Heat']
    })
    power_total = pd.DataFrame({
        'Power': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Power']
    })

    merged_df = filtered_spring.merge(spring, on='Anfang', how='inner')
    # Create new DataFrames by multiplying the columns
    mobility_temp = pd.DataFrame({'Mobility': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Mobility']})
    heat_temp = pd.DataFrame({'Heat': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Heat']})
    power_temp = pd.DataFrame({'Power': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Power']})
    
    mobility_total = pd.concat([mobility_total, mobility_temp], axis=0, ignore_index=True)
    heat_total = pd.concat([heat_total, heat_temp], axis=0, ignore_index=True)
    power_total = pd.concat([power_total, power_temp], axis=0, ignore_index=True)

    merged_df = filtered_summer.merge(summer, on='Anfang', how='inner')
    # Create new DataFrames by multiplying the columns
    mobility_temp = pd.DataFrame({'Mobility': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Mobility']})
    heat_temp = pd.DataFrame({'Heat': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Heat']})
    power_temp = pd.DataFrame({'Power': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Power']})
    
    mobility_total = pd.concat([mobility_total, mobility_temp], axis=0, ignore_index=True)
    heat_total = pd.concat([heat_total, heat_temp], axis=0, ignore_index=True)
    power_total = pd.concat([power_total, power_temp], axis=0, ignore_index=True)

    merged_df = filtered_autumn.merge(spring, on='Anfang', how='inner')
    # Create new DataFrames by multiplying the columns
    mobility_temp = pd.DataFrame({'Mobility': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Mobility']})
    heat_temp = pd.DataFrame({'Heat': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Heat']})
    power_temp = pd.DataFrame({'Power': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Power']})
    
    mobility_total = pd.concat([mobility_total, mobility_temp], axis=0, ignore_index=True)
    heat_total = pd.concat([heat_total, heat_temp], axis=0, ignore_index=True)
    power_total = pd.concat([power_total, power_temp], axis=0, ignore_index=True)

    merged_df = filtered_winter_2.merge(winter, on='Anfang', how='inner')
    # Create new DataFrames by multiplying the columns
    mobility_temp = pd.DataFrame({'Mobility': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Mobility']})
    heat_temp = pd.DataFrame({'Heat': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Heat']})
    power_temp = pd.DataFrame({'Power': merged_df['Gesamt (Netzlast) [MWh] Berechnete Auflösungen'] * merged_df['Power']})
    
    mobility_total = pd.concat([mobility_total, mobility_temp], axis=0, ignore_index=True)
    heat_total = pd.concat([heat_total, heat_temp], axis=0, ignore_index=True)
    power_total = pd.concat([power_total, power_temp], axis=0, ignore_index=True)

    # Display the new DataFrames
    print("Mobility DataFrame:")
    print(mobility_total)

    print("\nHeat DataFrame:")
    print(heat_total)

    print("\nPower DataFrame:")
    print(power_total)

    new_df_heat = pd.DataFrame({
    "technology": "Heat",  # Set the technology column to a constant value
    "hour": heat_total.index,         # Use the index as the hour column (add 1 to start from 1)
    "value": heat_total["Heat"]           # Use the "Heat" column from your original DataFrame
    })
    new_df_mobility = pd.DataFrame({
    "technology": "Mobility",  # Set the technology column to a constant value
    "hour": mobility_total.index,         # Use the index as the hour column (add 1 to start from 1)
    "value": mobility_total["Mobility"]           # Use the "Heat" column from your original DataFrame
    })
    new_df_power = pd.DataFrame({
    "technology": "Power",  # Set the technology column to a constant value
    "hour": power_total.index,         # Use the index as the hour column (add 1 to start from 1)
    "value": power_total["Power"]           # Use the "Heat" column from your original DataFrame
    })

    # Save the new DataFrame as a CSV file
    new_df_heat.to_csv("new_data/new_heat_data.csv", index=False)
    new_df_mobility.to_csv("new_data/new_mobility_data.csv", index=False)
    new_df_power.to_csv("new_data/new_power_data.csv", index=False)


def demand():
    heat = pd.read_csv("new_data/new_heat_data.csv")
    mobility = pd.read_csv("new_data/new_mobility_data.csv")
    power = pd.read_csv("new_data/new_power_data.csv")

    # Combine the DataFrames
    demand_timeseries = pd.concat([power, mobility, heat], ignore_index=True)

    # Save the combined DataFrame as "capacity_factors.csv"
    demand_timeseries.to_csv("data_use/demand_timeseries_new.csv", index=False)

    print(demand_timeseries)

def capacity():
    wind = pd.read_csv("new_data/wind_data_new.csv")
    sun = pd.read_csv("new_data/sun_data_new.csv")

    # Combine the DataFrames
    capacity_factors = pd.concat([wind, sun], ignore_index=True)

    # Save the combined DataFrame as "capacity_factors.csv"
    capacity_factors.to_csv("data_use/capacity_factors.csv", index=False)

    print(capacity_factors)

capacity()



