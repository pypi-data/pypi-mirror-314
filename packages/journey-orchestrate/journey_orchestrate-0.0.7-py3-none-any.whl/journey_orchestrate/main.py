import pandas as pd
import dask.dataframe as dd
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def  customer_journey_orchestrate(df,key,timestamp_column, touch , join_str, n_partition): 
    if  n_partition == '' or n_partition <=0 :
        n_partition = 1
    if join_str == "":
        join_str = '>'
    flg = input_check(df,key, timestamp_column, touch)
    if flg == False :
        print( """Please check the input to the function . Either or all are missing: 
                1.  Either the key column name is missing/incorrect 
                2.  The data in the timestamp column does not adhere to the timestamp format 
                3.  Timestamp column not found in the dataframe.
                4.  Supplied input is not a pandas dataframe

                
                Please input a dataframe with ID column on which you would like to group the journey,
                Timestamp column on which you would like to order
                the journey and the join string for the journey orchestration. Default join string if not supplied is  > """)
    else:
        df[timestamp_column] = pd.to_datetime(df[timestamp_column])
        ddf = dd.from_pandas(df, npartitions=n_partition)  # You can adjust npartitions based on the dataset size
        ddf_sorted = ddf.sort_values(by=[key, timestamp_column])
        df_sorted = ddf_sorted.compute()
        df_orchestration = df_sorted.groupby(key)[touch].agg(join_str.join).reset_index()
        df_orchestration.rename(columns={touch: 'journey_orchestration'}, inplace=True)
        print(df_orchestration)
    return df_orchestration
    
def input_check(df, column_name, ts_col, touch):
    if column_name in df.columns and touch in df.columns  and ts_col in df.columns and pd.api.types.is_datetime64_any_dtype(df[ts_col]):
        return True
    else:
        return False



def generate_random_cust_journey_data(n,n_ids,start_date, end_date,channel_list,random_seed):
    # Random seed for reproducibility
    random.seed(random_seed)
    
    # Define the range for the ID column
    ids = np.random.randint(0, n_ids, size=n)  # Random IDs between 1 and 20
    
    # Define the channels from which to sample
    channels = channel_list
    
 
    
    timestamps = generate_random_timestamps(start_date, end_date, n)
    
    # Generate random channel data
    channel_data = [random.choice(channels) for _ in range(n)]
    
    # Create the DataFrame
    df = pd.DataFrame({
        'ID': ids,
        'time': timestamps,
        'channel': channel_data
    })
    
    # Display the first few rows of the DataFrame
    return df

# Function to generate random timestamps
def generate_random_timestamps(start_date, end_date, num_samples):
    # Ensure start_date and end_date are datetime objects
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Calculate the total time difference between start and end date
    time_diff = end_date - start_date

    # Generate random timestamps within the time difference
    timestamps = [
        start_date + timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))
        for _ in range(num_samples)
    ]
    return timestamps

 
