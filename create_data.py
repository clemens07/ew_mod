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

wind()