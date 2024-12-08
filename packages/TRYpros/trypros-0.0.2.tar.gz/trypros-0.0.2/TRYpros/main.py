import copy
import numpy as np
import pandas as pd
import global_land_mask
import datetime
from pyproj import Transformer
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# PRIVATE GLOBAL VARIABLES

# List of month full names.
__months_full = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

# List of month short names.
__months_short = [ 
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

# Mapping of month short names to month numbers.
__month_nums = { 
    "jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, 
    "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12
}

# List of season names.
__seasons = ["summer", "autumn", "winter", "spring"]

# PRIVATE FUNCTIONS

def __replace_month(date_str, is_form):
    '''
    Replaces the month in the given string.
    @parameter date_str: The string containing the month.
    @parameter is_form: Whether the replacement is being made in
                        a value_form. Else, this means the replacement
                        is beign made in a value. So, if false, this function
                        will replace with month full names with 
                        month short names. If true, month names (full/short)
                        are replaced by "m".
    @return: String with the month replaced with "m" / month short name.
    '''
    if date_str == date_str and type(date_str) == str:
        date_str = str.lower(date_str)
        for m in __months_full:
            replace_with = "m" if is_form else m[:3]
            date_str = date_str.replace(m, replace_with)
        if is_form:
            for m in __months_short: 
                date_str = date_str.replace(m, "m")
    return date_str

def __replace_season(date_str):
    '''
    Replaces the month in the given string.
    @parameter date_str: The string containing the month.
    @return: String with the season name replaced by "s".
    '''
    date_str = str.lower(date_str)
    for s in __seasons:  date_str = date_str.replace(s, "s")
    return date_str

def __trait_value_agg(group):
    '''
    Aggregates trait values such that the "StdValue" with 
    greatest "priority" is selected if there is more than 
    one "StdValue" associated with each group. Also, if there is 
    more than one "StdValue" with the same "priority", mean shall
    be computed as long as all strings in the "StdValue" column 
    are all numeric or mode shall be computed instead, 
    if they are not numeric (cannot be converted to a float value).
    @parameter group: The group with possibly multiple StdValue values.
    @return: A single StdValue.
    '''
    # Get the rows with the greatest "priority".
    max_priority = group["priority"].max()
    max_priority_rows = group[group["priority"] == max_priority]
    try: # mean if numeric, and
        return max_priority_rows["StdValue"].astype(float).mean()
    except: # mode otherwise.
        return max_priority_rows["StdValue"].mode().iloc[0]

# PUBLIC FUNCTIONS

def load_trait_table(path):
    '''
    Loads the trait table downloaded from TRY 
    and saved as a TSV file.
    @parameter path: Path to the trait table .tsv file.
    '''
    return pd.read_csv(path, sep="\t").drop(['Unnamed: 5'], axis=1)

def search_trait_table(trait_table_df, search_str_list, print_matches=True):
    ''' 
    Returns rows of the trait table containing
    the given search string. The search has following
    characteristics.
    - AND search w.r.t words in each search string.
    - OR search w.r.t search strings.
    @parameter trait_table_df: Trait table as pandas dataframe.
    @parameter search_str_list: List of search strings.
    @parameter print_matches: Whether or not matches should be
                              printed.
    @return: Subsection of DF that matches search.
    '''
    trait_desc_list = [
        str.lower(trait) 
        for trait in trait_table_df.Trait
    ]
    trait_idx_list = set([])
    for i in range(len(trait_desc_list)):
        for search_str in search_str_list:
            all_words_present = True
            for word in search_str.split():
                all_words_present &= word in trait_desc_list[i]
            if all_words_present: trait_idx_list.add(i)
    trait_idx_list = list(trait_idx_list)
    trait_table_df_subset = trait_table_df.iloc[trait_idx_list, 0:2]
    if print_matches:
        for trait_id, trait_name in trait_table_df_subset.values:
            print(f"({trait_id}) - {trait_name}")
    return trait_table_df_subset

def is_float(s):
    '''
    Returns if this string is that of a float or not.
    @parameter s: String value.
    @return: Whether this is a float string.
    '''
    try: float(s)
    except: return False
    return True

def is_lat_lon_valid_terrestrial(lat, lon, antarctica_valid=False):
    '''
    Returns true if the given latitude and longitude
    values are both not NaN, are valid floating point
    numbers on land.
    @parameter lat: Latitude in decimal degrees.
    @parameter lon: Longitude in decimal degrees.
    @parameter antarctica_valid: Whether or not to consider 
                                 points in antacrtica valid.
    @return: True if all aforementioned conditions are met.
             False otherwise.
    '''
    # Invalid if NaN.
    if lat != lat or lon != lon: return False
    
    # Invalid if not a valid floating point number.
    if not (is_float(lat) and is_float(lon)): return False
    
    # Latitude must be in the range of -90 to 90 decimal degrees.
    # Longitude must be in the range of -180 to 180 decimal degrees.
    if lat < -90 or lat > 90 or lon < -180 or lon > 180: return False

    # Locations in Antarctica are invalid. 
    # There are no plants on Antarctica.
    # Antarctica is typically defined as the region south of 60°S latitude,
    # so any latitude less than -60 is considered Antarctic.
    if not antarctica_valid:
        if lat < -60: return False

    # Only other locations on land are considered valid.
    return global_land_mask.is_land(lat = lat, lon = lon)
     
def search_covariates(df, search_str_list, print_matches=True):
    ''' 
    Returns DataIDs of co-variates whose names are matched
    with the given search string. The search has the following
    characteristics.
    - AND search w.r.t words in each search string.
    - OR search w.r.t search strings.
    @parameter df: Pandas data frame with data from TRY containing 
                   columns "DataID" and "DataName".
    @parameter search_str_list: List of search strings.
    @parameter print_matches: Whether or not matches are to be 
                              printed out (default = False).
    @return: List of DataIDs.
    '''
    df_subset = df[["DataID", "DataName"]].dropna().drop_duplicates()
    ids = set([])
    for data_id, data_name in df_subset.values:
        name = str.lower(data_name)
        for search_str in search_str_list:
            all_words_present = True
            for word in search_str.split():
                all_words_present &= word in name
            if all_words_present: ids.add(data_id)
    if print_matches:
        for data_id, data_name in df_subset[df_subset.DataID.isin(ids)].values:
            print(f"({data_id}) {data_name}")
    return list(ids)

def load_big_data(path, drop_cols=[], clean=True, verbose=True):
    '''
    Loads a large data file. This function sees to it that NaN
    values in the StdValue column are filled with values from the
    StdValueStr column so that all standardized values, if available,
    may be found in a single column "StdValue" instead of sometimes
    being present under column "StdValueStr" instead of "StdValue".
    @parameter path: Path to the large datafile.
    @parameter drop_cols: Columns to drop. Important columns for 
                          data exploration ["TraitID", "DataID", 
                          "DatasetID", "ObsDataID", "ObservationID", 
                          "AccSpeciesID", "StdValue", "StdValueStr", 
                          "UnitName", "OrigValueStr", "OrigUnitStr",
                          "OriglName", "Comment"] will not be dropped
                          on request.
    @parameter rename: If true (default), renames columns to 
                       more comprehensive and intuitive names.
    @parameter clean: If true (default), performs the following 
                      two cleaning steps.
                      1. Drop duplicates.
                      2. Remove high risk error values. 
    @parameter verbose: Whether or not to print status comments.
    @return data: Data in given file as a pandas data frame.
    @return trait_id_list: List of all trait ids found in the 
                           loaded data set.
    '''
    # Load downloaded data from TRY.
    chunk_list = []
    for chunk in pd.read_csv(
        path, delimiter="\t", 
        encoding="ISO-8859-1", chunksize=10000
    ): chunk_list.append(chunk)
    data = pd.concat(chunk_list, axis=0)

    # Optionally clean dataset.
    if clean:
        # Drop duplicates.
        # The TRY 6.0 data release notes states that if a row contains 
        # an integer for the OrigObsDataID column, then this integer 
        # refers to the original obs_id of the observation that this
        # row is a duplicate of. Such duplicate records exist because
        # multiple studies can upload same data. Thus, keeping only those
        # records for which obs_id_of_original is NaN is equivalent to
        # dropping all duplicate observations in the dataset.
        data = data[data.OrigObsDataID.isna()]
        data.drop(["OrigObsDataID"], axis=1, inplace=True)

        # Risk minimization.
        # Also in TRY 6.0 data release notes, it is suggested that 
        # all records with Error Risk > 4 be dropped. 
        # Thus, this is done here as well.
        data.drop(data[data.ErrorRisk > 4].index, inplace=True)
        data.drop(["ErrorRisk"], axis=1, inplace=True)

    # Drop less useful columns.
    drop_cols += [col for col in drop_cols if not col in 
        [ # Ensure key columns are still retained.
            "TraitID", "DataID", "DatasetID", "ObsDataID",
            "ObservationID", "AccSpeciesID",
            "StdValue", "StdValueStr", "UnitName",
            "OrigValueStr", "OrigUnitStr",
            "OriglName", "Comment"
        ]
    ] + ["Unnamed: 28"]
    data.drop(drop_cols, axis=1, inplace=True)

    # Fillna in StdValue column with value in StdValueStr column.
    data = data.assign(StdValue = data.StdValue.fillna(
        data.StdValueStr
    ))

    # Extract all unique trait ids in the the dataset.
    trait_id_list = data.TraitID.dropna().unique().astype(int).tolist()

    # Optionally print information about loaded data.
    if verbose:
        print(f"Loaded {len(data)} data points from '{path}'.")
        print("\nTraits Found:")
        for trait_id, trait_name in data[
            ["TraitID", "TraitName"]
        ].drop_duplicates().dropna().values:
            print(f"({int(trait_id)}) {trait_name}")

    return data, trait_id_list

def get_form(val, num_placeholder="@", rep_month=True, rep_season=True):
    '''
    Replaces all number quantities in a mixed string 
    with a symbol while retaining non-numeric parts so 
    that the general form of the alphanumeric string is returned.
    @parameter val: Value, the form of which, is to be returned.
    @parameter num_placeholder: The symbol that will replace 
                                numbers (default = @).
    @parameter rep_month: Whether or not to replace month names.
    @parameter rep_season: Whether or not to replace season names.
    @return: General form of the given value.
    '''
    if val != val: return val # If value is NaN, return NaN.
    val_str = str(val) if type(val) != str else val
    val_form = ""
    is_num = False
    num_points = 0
    for i in range(len(val_str)):
        c = val_str[i]
        if c.isnumeric(): # character is a number
            if not is_num: # previous character was not a number
                is_num = True
                val_form += num_placeholder
        else: # character is not a number
            if (c == "."): # character is a point
                num_points += 1
            if not(
                c == 1 and # this is the first point encountered
                is_num and # since the previous character was a number
                i + 1 < len(val_str) and # there is a next character
                val_str[i+1].isnumeric() # such that is is also a number
            ):  # the above is not the case
                is_num = False
                num_points = 0
                val_form += c
    if rep_month: val_form = __replace_month(val_form, is_form=True)
    if rep_season: val_form = __replace_season(val_form)
    return val_form.strip()
    
def standardize_data(
        data, preprocessing_steps, 
        unit_std, value_form_std, value_trans
    ):
    '''
    Standardizes data column values in the given pandas dataframe.
    @parameter data: Data dictionary containing one or more
                     pandas dataframes in the format as output by
                     functions like "get_data_trait(...)", 
                     "get_data_latlon(...)", or "get_data_year(...)".
    @parameter preprocessing_steps: List of functions to apply to the
                                    data to preprocess it before applying
                                    other functions. All these functions should
                                    receive input and produce output in the same 
                                    format as parameter "data" here. If no
                                    preprocessing is to be performed, this
                                    parameter may be set to [].
    @parameter unit_std: Function that performs unit form standardization.
                         The aim of unit standardization is to replace
                         invalid and ambiguous unit values with more 
                         appropriate values. This function should have the 
                         following format.
                            def unit_std (data):
                                """ 
                                Standardizes units in data and returns 
                                the dataset with standardized units.
                                @parameter data: Dictionary containing one or more
                                                 Dataframes with non-standardized
                                                 unit forms.
                                @parameter: Dictionary containing Dataframes 
                                            with standardized unit forms only.
                                """
                                ...
                         Set this value to None if unit form standardization
                         is not to be performed.
    @parameter value_form_std: Function that performs value form standardization.
                               The aim of value standardization is to replace 
                               values associated with invalid or ambiguous 
                               value forms, with better alternatives.
                               This function should have the following format.
                                    def value_form_std (data):
                                        """ 
                                        Standardizes values in data and returns 
                                        the dataset with all values written in the
                                        same notation.
                                        @parameter data: Dictionary containing one 
                                                         or more Dataframes with 
                                                         values in non-standardized
                                                         forms.
                                        @parameter: Dictionary containing one 
                                                    or more Dataframes with values
                                                    in standardized forms only.
                                        """
                                        ...
                               Set this value to None if value form standardization
                               is not to be performed.
    @parameter value_trans: Function that performs value conversion and 
                            transforms the trait value expressed in the 
                            original unit, into its equivalent value in a
                            standard unit.
                            The aim of this function is to ensure that all 
                            values are expressd in the same unit.
                            This function should have the following format.
                                def val_trans (data):
                                    """ 
                                    Converts given value from its old given unit
                                    to the standard unit.
                                    @parameter data: Dictionary containing one 
                                                     or more Dataframes with 
                                                     values in multiple units.
                                    @parameter: Dictionary containing one 
                                                or more Dataframes with values
                                                expressed in a single unit.
                                    """
                                    match unit:
                                        case "unit1": return transform(value)
                                        case "unit2": ...
                                    ...
                            Set this value to None if value conversion is not
                            to be performed.
    @return: Data dicitonary in the same format as recieved but with 
             StdValue and possibly UnitName columns in contained
             Data Frames populated with new standardized values
             to replaced previously non-standardized or erroneous values. 
    '''
    # Preprocess data frame.
    for prep_fun in preprocessing_steps:
        # Deep copying to prevent 
        # overwriting original data frame.
        data_copy = copy.deepcopy(data) 
        data = prep_fun(data_copy)

    # Unit form standardization.
    if type(unit_std) != type(None):
        data_copy = copy.deepcopy(data)
        data = unit_std(data_copy)

    # Value form standardization.
    if type(value_form_std) != type(None):
        data_copy = copy.deepcopy(data)
        data = value_form_std(data_copy)

    # Value conversion.
    if type(value_trans) != type(None):
        data_copy = copy.deepcopy(data)
        data = value_trans(data_copy)

    return data

def get_data_trait(data_raw, priority, verbose=True):
    '''
    This function extracts rows associated with prioritised
    TraitIDs from the given data frame containing raw data
    from TRY. Extracted data is separated based on whether 
    the data corresponds to pre-standardized values in TRY 
    or not. This function also adds a new column to corresponding
    data frames called "value_form" containing strings representing
    the general forms of values.
    @parameter data_raw: Pandas dataframe with raw data from try.
    @parameter priority: List of priorities associated with each Trait ID.
                         with 1 = highest priority and higher numbers 
                         representing progressively lower priorities.
                         This value will be added to the table as a new
                         column called "priority". This value is so that it
                         may be used to settle conflicts when there is more 
                         than one StdValue associated with each ObservationID.
                         The value associated with highest TraitID priority 
                         can be picked such that if there is more than one value
                         with the same priority, then the mean or mode depending
                         on whether the feature is numeric or categorical, 
                         may be computed.
                         NOTE: Only those records corresponding to data ids 
                               for which priorites are defined, will be present 
                               in the final dataset.
    @parameter verbose: Whether or not to print possibly helpful
                        information about processed data.
    @return data_trait: A dictionary with trait information
                        in the following form wherein all rows 
                        with no information, are excluded.
                        {
                            "std": A pandas dataframe containing 
                                pre-standardized trait values.,
                            "non_std": A pandas dataframe containing 
                                    non-standardized trait values.
                        }
    @return data_covariate: A dictionary with covariate information
                            in the following form wherein all rows 
                            with no information, are excluded.
                            {
                                "std": A pandas dataframe containing 
                                       pre-standardized covariate values,
                                "non_std": A pandas dataframe containing 
                                           non-standardized covariate values.
                            }
    '''
    # No information => StdValueStr == NaN AND
    #                   StdValue == NaN AND
    #                   OrigValueStr == NaN.
    num_no_info = len(data_raw[np.logical_and(
        data_raw.StdValue.isna(), # Includes StdValueStr.isna() since NaN filled.
        data_raw.OrigValueStr.isna()
    )])

    # Separate trait data from covariate data.
    data_trait = data_raw[data_raw.TraitID.notna()] # Have TraitIDs and DataIDs.
    data_covariate = data_raw[data_raw.TraitID.isna()] # Have only DataIDs.

    # Only keep those traits that have a priority attached to it
    # and add a priority column.
    data_trait = data_trait[
        data_trait.TraitID.isin(priority.keys())
    ].merge(pd.DataFrame(
        priority.items(), columns=["TraitID", "priority"]
    ), on="TraitID", how="left")
    num_data_trait = len(data_trait)
    loaded_trait_ids = data_trait.TraitID.dropna().unique().tolist()
    
    # Only keep those covariate data rows
    # that are associated with selected 
    # trait related observations.
    data_covariate = data_covariate[
        data_covariate.ObservationID.isin(
            data_trait.ObservationID.dropna().unique().tolist()
        )
    ]
    num_data_covariate = len(data_covariate)

    # Separate trait and covarite data into standardized
    # and non-standardized data.
    # Standardized data => StdValue != NaN OR StdValueStr != NaN.
    # Non standardized data => StdValue == StdValueStr == NaN
    #                          AND OrigValueStr != NaN.
    data_trait = {
        "std": data_trait[data_trait.StdValue.notna()], 
        "non_std": data_trait[np.logical_and(
            data_trait.OrigValueStr.notna(),
            data_trait.StdValue.isna()
        )]
    }
    data_covariate = { 
        "std": data_covariate[data_covariate.StdValue.notna()],
        "non_std": data_covariate[np.logical_and(
            data_covariate.OrigValueStr.notna(),
            data_covariate.StdValue.isna()
        )]
    }
    
    # Add a value form column.
    data_trait["std"] = data_trait["std"].assign(
        value_form = data_trait["std"].StdValue.apply(get_form)
    )
    data_covariate["std"] = data_covariate["std"].assign(
        value_form = data_covariate["std"].StdValue.apply(get_form)
    )
    data_trait["non_std"] = data_trait["non_std"].assign(
        value_form = data_trait[
            "non_std"
        ].OrigValueStr.apply(get_form, rep_month=True)
    )
    data_covariate["non_std"] = data_covariate["non_std"].assign(
        value_form = data_covariate[
            "non_std"
        ].OrigValueStr.apply(get_form, rep_month=True)
    )

    # Optionally print separated data details.
    if verbose:
        num_total = len(data_raw)
        print(
            f"\nTotal no. of raw data points = ",
            f"{num_total} \n",
            f"\nNo. of trait data points = ",
            f"{num_data_trait}\n",
            f"No. of standardized trait data points = ",
            f"{len(data_trait["std"])}\n",
            f"No. of non standardized trait data points = ",
            f"{len(data_trait["non_std"])}\n",
            f"\nNo. of covariate data points = ",
            f"{num_data_covariate}\n",
            f"No. of standardized covariate data points = ",
            f"{len(data_covariate["std"])}\n",
            f"No. of non standardized covariate data points = ",
            f"{len(data_covariate["non_std"])}\n",
            f"\nNo. of data points with no information = {num_no_info}\n",
            f"\nLoaded TraitIDs: {loaded_trait_ids}", 
            sep=""
        )

    return data_trait, data_covariate

def display_units_forms(data, data_type="trait"):
    '''
    Displays some key information about pre-standardized
    and non-standardized values like their units and value format.
    This function is expected to be useful during manual
    data investigation.
    @parameter data: Data dictionary as in the format returned by
                     the get_data_trait(...), get_data_latlon(...),
                     or get_data_years(...) function.
    @parameter data_type: The type of data from which units and
                          forms are to be extracted. This may be 
                          "trait" for data in the format as returned 
                          by the get_data_trait(...) function. It may also be
                          "latlon" for data in the format as returned
                          by the get_data_latlon(...) function or "date" 
                          for data in the format as retuned by the 
                          get_data_years(...) function.
    '''
    if data_type == "trait":
        # View units.
        trait_std_units = data[
            "std"
        ].UnitName.dropna().drop_duplicates().values
        trait_non_std_units = data[
            "non_std"
        ].OrigUnitStr.dropna().drop_duplicates().tolist()
        print("Trait Standardised Units:", trait_std_units)
        print("Trait Non-Standardised Units:", trait_non_std_units)
        
        # View value forms.
        print(
            "Trait Standardised Value Forms:", 
            data["std"].value_form.unique().tolist()
        )
        print(
            "Trait Non-Standardised Value Forms:", 
            data["non_std"].value_form.unique().tolist()
        )

    if data_type == "date":
        # View units.
        print("Date Units:", data["data"].UnitName.unique().tolist())
        print( # View value forms.
            "Date Value Forms:", 
            data["data"].value_form.unique().tolist()
        )

    if data_type == "latlon":
        for l in ["latitude", "longitude"]:
            # View units.
            print(
                f"{'L'+l[1:]} Standardised Units:", 
                data[l]["data"]["std"].UnitName.unique().tolist()
            )
            print(
                f"{'L'+l[1:]} Non-Standardised Value Forms:", 
                data[l]["data"]["non_std"].OrigUnitStr.unique().tolist()
            )
            print(
                f"{'L'+l[1:]} Standardised Value Forms:", 
                data[l]["data"]["std"].value_form.unique().tolist()
            )
            print(
                f"{'L'+l[1:]} Non-Standardised Value Forms:", 
                data[l]["data"]["non_std"].value_form.unique().tolist()
            )

def get_vals_with_form(
    data, match_forms,
    keep_cols=[],
    value_form_col="value_form"
):
    '''
    Given a data frame with value form information, and 
    a list of value forms to search for, this function returns
    a subset of that dataframe with just the rows associated with
    value forms in the given match list.
    @parameter data: Data frame with value form information.
    @parameter value_form_col: Name of the column with value
                               form information 
                               (default = "value_form").
    @parameter keep_cols: List of columns to return. If all 
                          columns are to be returned, simply
                          set this to [] or do not set a value
                          for this parameter.
    @parameter match_forms: A list of value forms to match.
    @return: Data frame subset containing rows with 
             matching value forms.
    '''
    if len(keep_cols) > 0:
        return data[
            data[value_form_col].isin(match_forms)
        ][keep_cols].drop_duplicates()
    else:
        return data[
            data[value_form_col].isin(match_forms)
        ].drop_duplicates()

def get_data_latlon_ids(data_covariate):
    '''
    Prints standardized and non-standardized
    ids associated with latitude and longitude data.
    These IDs are also returned.
    @parameter data_covariate: Pre-standardized and non-standarized
                               covariate data as a dictionary in the
                               form {"std": ..., "non_std": ...}.
    @return data_latlon: Dictionary of the following form.
                         data_latlon = {
                            "latitude": {
                                "data_ids": {
                                    "std": [...], 
                                    "non_std": [...]
                                },
                                "data": None
                            },
                            "longitude": {
                                "data_ids": {
                                    "std": [...], 
                                    "non_std": [...]
                                },
                                "data": None
                            }
                         }
    '''
    data_latlon = {
        "latitude": {
            "data_ids": {"std": [], "non_std": []},
            "data": {"std": None, "non_std": None}
        }, 
        "longitude": {
            "data_ids": {"std": [], "non_std": []},
            "data": {"std": None, "non_std": None}
        },
    }

    print("\nAll Available Data: Standardized Lat Lon")
    data_latlon["latitude"]["data_ids"]["std"] = search_covariates(
        df = data_covariate["std"], 
        search_str_list = ["latitude"]
    )
    data_latlon["longitude"]["data_ids"]["std"] = search_covariates(
        df = data_covariate["std"], 
        search_str_list = ["longitude"]
    )

    print("\nAll Available Data: Non Standardized Lat Lon")
    data_latlon["latitude"]["data_ids"]["non_std"] = search_covariates(
        df = data_covariate["non_std"], 
        search_str_list = ["latitude"]
    )
    data_latlon["longitude"]["data_ids"]["non_std"] = search_covariates(
        df = data_covariate["non_std"], 
        search_str_list = ["longitude"]
    )

    return data_latlon

def get_data_latlon(data_latlon, data_covariate, verbose=True):
    '''
    Extracts pre-standardized and non-standardized latitude and
    longitude data from covariate data and returns this.
    @parameter data_latlon: Output of the function 
                            get_data_ids_latlon(...)
                            containing DataIDs corresponding to 
                            pre-standardized and standardized
                            latitude and longitude data, and space
                            for latitude and longitude related 
                            data frames respectively.
    @parameter data_covariate: A dictionary with both 
                               pre-standardized and standardized
                               covariate data of the form
                               {"std": ..., "non_std": ...}.
    @parameter verbose: Whether or not to print status details.
    @return: data_latlon with added latitude and longitude
             related data frames.
    '''
    # Load separated data.
    data_latlon["latitude"]["data"]["std"] = data_covariate["std"][
        data_covariate["std"].DataID.isin(
            data_latlon["latitude"]["data_ids"]["std"]
        )
    ]
    data_latlon["longitude"]["data"]["std"] = data_covariate["std"][
        data_covariate["std"].DataID.isin(
            data_latlon["longitude"]["data_ids"]["std"]
        )
    ]
    data_latlon["latitude"]["data"]["non_std"] = data_covariate["non_std"][
        data_covariate["non_std"].DataID.isin(
            data_latlon["latitude"]["data_ids"]["non_std"]
        )
    ]
    data_latlon["longitude"]["data"]["non_std"] = data_covariate["non_std"][
        data_covariate["non_std"].DataID.isin(
            data_latlon["longitude"]["data_ids"]["non_std"]
        )
    ]

    if verbose:
        loaded_data_ids = []
        for l in ["latitude", "longitude"]:
            for s in ["std", "non_std"]:
                loaded_data_ids += data_latlon[l][
                    "data"
                ][s].DataID.dropna().unique().tolist()
        loaded_data_ids = list(set(loaded_data_ids))
        print("\nDataIDs Loaded =", loaded_data_ids)

    return data_latlon

def get_data_year_ids(data_covariate):
    '''
    Prints standardized and non-standardized
    ids associated with date-time data.
    These IDs are also returned.
    @parameter data_covariate: Pre-standardized and non-standarized
                               covariate data as a dictionary in the
                               form {"std": ..., "non_std": ...}.
    @return data_year: Dictionary of the following form.
                       data_year = {
                            "data_ids": {
                                "std": [...], 
                                "non_std": [...]
                            },
                            "data": DataFrame
                       }
    '''
    data_year = {
        "data_ids": {"std": [], "non_std": []},
        "data": {"std": None, "non_std": None}
    }

    print("\nAll Available Data: Standardized Dates")
    data_year["data_ids"]["std"] = search_covariates(
        df = data_covariate["std"], 
        search_str_list = ["date"]
    )
    print("\nAll Available Data: Non-Standardized Dates")
    data_year["data_ids"]["non_std"] = search_covariates(
        df = data_covariate["non_std"], 
        search_str_list = ["date"]
    )

    return data_year

def get_data_year(data_year, data_covariate, verbose=True):
    """
    Extracts date related data amidst pre-standardized
    and standardized date related covariate data and 
    returns it, combined in one data frame because in
    TRY, date values are not explicitly standardized to 
    one common format.
    @parameter data_year: Dictionary output by the 
                          get_data_ids_year(...) function
                          of the following form.
                          data_year = {
                            "data_ids": {
                                "std": [...], 
                                "non_std": [...]
                            }, "data": {
                                "std": DataFrame,
                                "non_std": DataFrame
                            }
                          }
    @parameter data_covariate: Dictionary containing pre-standardized
                               and standardized covariate data.
    @parameter verbose: Whether or not to print status details.
    @return: Date-time related covariate data.
    """    
    data_year = copy.deepcopy(data_year)

    # Load separated data.
    data_year["data"]["std"] = data_covariate["std"][
        data_covariate["std"].DataID.isin(
            data_year["data_ids"]["std"]
        )
    ]
    data_year["data"]["non_std"] = data_covariate["non_std"][
        data_covariate["non_std"].DataID.isin(
            data_year["data_ids"]["non_std"]
        )
    ]

    # Merge std and non_std data.
    data_year["data"] = pd.concat([
        data_year["data"]["std"],
        data_year["data"]["non_std"]
    ])

    # Handle StdValue column
    std_value = data_year["data"].StdValue.fillna(
        data_year["data"].OrigValueStr
    )
    std_value = std_value.apply(
        lambda v: v if not isinstance(v, str) else v.lower()
    )

    # Handle UnitName column
    unit_name = data_year["data"].UnitName.astype(str)
    unit_name = unit_name.fillna(
        data_year["data"].OrigUnitStr.astype(str)
    )

    # Reassign columns explicitly
    data_year["data"] = data_year["data"].assign(
        StdValue = std_value,
        UnitName = unit_name
    )

    # Drop redundant columns.
    data_year["data"].drop([
        "OrigValueStr", "OrigUnitStr", "StdValueStr"
    ], axis=1, inplace=True)

    # Print data ids present.
    if verbose:
        print(
            "\nDataIDs Loaded =", 
            data_year["data"].DataID.drop_duplicates().tolist()
        )

    return data_year

def combine_date(
    data_trait, data_latlon, data_year, 
    feature_name, feature_std_unit
):
    '''
    Given processed trait, geo-location, and year data,
    this function combined them into one dataframe.
    Following are the keys that the data dictionaries
    are expected to have. All data frames should have
    the standardized value in the StdValue column.

    NOTE: It is expected that data_trait, data_latlon, and
          data_year data frames contain the following columns.
          * data_trait: [
                "StdValue", "ObservationID", 
                "AccSpeciesID", "priority"
            ]
          * data_latlon: [
                "StdValue", "ObservationID"
          ]
          * data_year: [
                "StdValue", "ObservationID"
          ]

    @parameter data_trait: {"std": Dataframe, "non_std": Dataframe}
    @parameter data_latlon: {
        "latitide": {"data": {"std": Dataframe, "non_std": Dataframe}}, 
        "longitude": {"data": {"std": Dataframe, "non_std": Dataframe}} 
    }
    @parameter data_year: {"data": {"std": Dataframe, "non_std": Dataframe}}
    @parameter feature_name: Name of the feature of interest.
    @parameter feature_std_unit: The standardized unit of the
                                 feature in standard notation.
    @return: Single data frame with all standardized values.
    '''
    # Combine standardized and non standardized trait data.
    data = pd.concat([
        data_trait["std"],
        data_trait["non_std"]
    ])

    # Add location data.
    data_lat = pd.concat([
        data_latlon["latitude"]["data"]["std"],
        data_latlon["latitude"]["data"]["non_std"]
    ]).rename(columns={
        "StdValue": "latitude" 
    })[["ObservationID", "latitude"]]
    data_lon = pd.concat([
        data_latlon["longitude"]["data"]["std"],
        data_latlon["longitude"]["data"]["non_std"]
    ]).rename(columns={
        "StdValue": "longitude"
    })[["ObservationID", "longitude"]]
    data = data.merge(data_lat, on="ObservationID", how="left")
    data = data.merge(data_lon, on="ObservationID", how="left")

    # Add date information.
    data = data.merge(
        data_year["data"][[
            "ObservationID", "StdValue"
        ]].rename(columns = {
            "StdValue": "year"
        }), 
        on = "ObservationID", how = "left"
    )[[
        "year", "latitude", "longitude", 
        "AccSpeciesID", "StdValue", "priority"
    ]].drop_duplicates()

    # Reduce data so that there is one unique
    # feature value for every unique combination
    # of year + latitude + longitude + species.
    data = data.groupby([
        "year", "latitude", "longitude", "AccSpeciesID"
    ]).apply(lambda group: pd.Series({
        "StdValue": __trait_value_agg(group)
    }), include_groups=False).reset_index()
    
    # Rename column to be feature name.
    data = data.rename(columns = {
        "AccSpeciesID": "species_id",
        "StdValue": f"{feature_name}{
            '_'+feature_std_unit if feature_std_unit != "" else ""
        }"
    })
    
    return data

def extract_year(data_year_row, handle_special_cases=None):
    ''' 
    Given a date, returns the year from it in standard format.
    @parameter data_year_row: A row from the data_year dataframe
                              containing date related information.
                              This data frame is expected to have
                              columns [StdValue, value_form].
    @parameter handle_special_cases: Optional function that accepts 
                                     date_str, date_split, years, and 
                                     the dataframe row as inputs and 
                                     handles special cases
                                     to return a single year value alongwith
                                     a boolean value that indicates whether
                                     or not the special condition was met.
                                     Thus, this function should look as follows.
                                     def handle_special_cases(
                                        data_year_row, data_split, years, 
                                     ): 
                                        is_special_condition_met = ...
                                        to_return = ...
                                        return is_special_condition_met, to_return
    @return: Year if the date form is a single date or 
             mean year if it is a date range date range.
    '''
    current_year = datetime.date.today().year

    date_str = data_year_row.StdValue
    if date_str == date_str: # No NaN.
        if type(date_str) != str: # Make string, if not already so.
            date_str = str(date_str)

        date_str = date_str.replace("(", "")
        date_str = date_str.replace(")", "")
        date_str = date_str.replace(",", "-")
        date_str = date_str.replace("/", "-")
        date_str = date_str.replace("&", "-")
        date_str = date_str.replace(".", "-")
        date_str = date_str.replace("t", "-")
        date_str = date_str.replace("?", "")
        date_str = date_str.replace(" ", "-")

        date_split = date_str.split("-")

        years = np.sort([
            y.strip() for y in date_split 
            if y.strip().isnumeric() and len(y.strip()) == 4
        ]).tolist()

        # Special cases.
        if type(handle_special_cases) != type(None) :
            is_special_condition_met, to_return = handle_special_cases(
                data_year_row, date_split, years
            )
            if is_special_condition_met: return to_return
        
        # General case.
        if len(years) > 0:
            # For all other valid cases,
            # a year_start and year_end
            # can be obtained.
            year_start = int(years[0])
            year_end = int(years[-1])
            if (year_start <= current_year and year_end <= current_year):
                year_final = str(int(np.ceil((year_start+year_end)/2)))
                return year_final
            
    # Any other situation is invalid. 
    return np.nan 

def save_data(data, dest_fold, feature_name, feature_unit):
    '''
    Saves the given data frame at the given path as a 
    csv file.
    @parameter data: Pandas dataframe to save.
    @parameter dest_fold: Destination folder in which to save data.
    @parameter feature_name: Name of the feature that this dataset 
                             records values of, and has a column named
                             after.
    @parameter feature_unit: The standard unit of this feature.
    '''
    filename = feature_name
    if len(feature_unit) > 0: filename += "_" + feature_unit
    data.to_csv(f"{dest_fold}/{filename}.csv", index=False)
    print(f'Saved "{filename}" data at "{dest_fold}/{filename}.csv".')

def wgs84_m_utm_to_decimal_degrees(easting, northing, zone, hemisphere):
    '''
    Converts X and Y values expressed in meters with the 
    coordinate reference system being UTM, which in turn 
    uses WGS84 as reference datum to latitude and longitude values
    expressed in decimal degrees.
    @parameter easting: UTM X (m).
    @parameter northing: UTM Y (m).
    @parameter zone: UTM Zone.
    @parameter hemisphere: Vertical geographic hemisphere (N/S).
    @return: Tuple of (latitude, longitude) in decimal degrees.
    '''
    # Define the UTM CRS based on zone and hemisphere
    utm_crs = f"+proj=utm +zone={zone}" 
    utm_crs += f" +{'north' if hemisphere == 'N' else 'south'}"
    utm_crs += " +datum=WGS84" 
    transformer = Transformer.from_crs( # WGS84 (lat/lon)
        utm_crs, "EPSG:4326", always_xy=True
    )  
    latitude, longitude = transformer.transform(easting, northing)
    return pd.Series([latitude, longitude])

def map_plot(data, save_path="", fig_size=(10, 10), title=""):
    '''
    Plots latitude and longitude columns of the given
    pandas dataframe on a map.
    @parameter data: Pandas dataframe containing columns
                     "latitude" and "longitude" with values in
                     decimal degrees.
    @parameter save_path: Saves the generated map to the given
                          location as a png image. By default,
                          the map is not saved as save_path = "".
    @parameter title: Map title.
    @parameter fig_size: Size of the figure.
    ''' 
    # Define figure and axes.
    fig, ax = plt.subplots(
        figsize=fig_size, 
        subplot_kw={'projection': ccrs.Mercator()}
    )

    data.loc[:, "latitude"] = data.latitude.astype(float)
    data.loc[:, "longitude"] = data.longitude.astype(float)

    # Plot the data.
    ax.scatter(
        data['longitude'], 
        data['latitude'], 
        color='green', 
        s=10, 
        transform=ccrs.PlateCarree()
    )

    # Set latitude and longitude range.
    ax.set_extent([
        min(data.longitude) - 5, 
        max(data.longitude) + 5, 
        min(data.latitude) - 5, 
        max(data.latitude) + 5
    ], crs=ccrs.PlateCarree())

    # Add gridlines and features.
    ax.gridlines(draw_labels=True)
    ax.coastlines()

    # Optinally add a title.
    plt.title(title, fontsize=14)

    # Optionally save as png.
    if save_path != "": plt.savefig("static_map.png", dpi=300)
    
    # Display map.
    plt.show()