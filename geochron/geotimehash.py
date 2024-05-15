""" Geotime hash representation"""
import timehash

def hash_tracks_into_timehashdf(track_list: List, timestamps: List, hash_func: Callable):
    """
    Converts a list of tracks into a pandas dataframe using
    a specified hashing function with a timehash of varying resolutions. 
    
    Args:
        track_list: a list of tracks broken down by equal intervals

        timestamps: a list of corresponding timestamps

        hash_func: the hashing function

    Returns:
        A pandas dataframe
    """
    interval_start = track_list[0].start
    row_list = []
    for track,timestamp  in zip(track_list, timestamps):
        hashmap = hash_func(track)
        start_string= interval_start.strftime("%Y-%m-%d %H:%M:%S")
        end_string= timestamp.strftime("%Y-%m-%d %H:%M:%S")
        interval = start_string + ", " + end_string
        new_row = pd.Series(data=hashmap, name=interval)
        row_list.append(new_row)
        interval_start = timestamp

    df = pd.DataFrame(row_list)

    df = df.reset_index(names='interval')

    split_df = df['interval'].str.split(',', expand=True)# pylint: disable=unsubscriptable-object
    df.loc[:, 'start_time'] = split_df[0]
    df.loc[:, 'end_time'] = split_df[1]

    return df