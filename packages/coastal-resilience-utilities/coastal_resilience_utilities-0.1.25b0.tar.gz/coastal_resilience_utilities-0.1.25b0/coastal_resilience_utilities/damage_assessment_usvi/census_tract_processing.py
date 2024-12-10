import pandas as pd
import geopandas as gpd
import numpy as np
import re
import logging
import re

logging.basicConfig()
logging.root.setLevel(logging.INFO)


def convert_to_percentage(df, columns):
    """
    Convert specified columns of a dataframe to percentages of the sum across a row.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    columns (list): The list of columns to be converted.

    Returns:
    pd.DataFrame: A new dataframe with specified columns converted to percentages.
    """
    df_copy = df.copy()
    row_sums = df_copy[columns].sum(axis=1)
    for column in columns:
        df_copy[column] = df_copy[column] / row_sums
    return df_copy


def generate_weighted_vulnerability_curve(df1, df2, id_column, column_mapping_to_nsi, column_to_match, column_identifier_regex):
    """
    Get a weighted mean of rows in df2, using weights from the columns of df1

    Parameters:
    df1 Dataframe of weights
    df2 Dataframe to get weighted mean from
    id_column Column to group by
    column_mapping Mapping of columns to vulnerability curve
    column_to_match Column to match on in df2
    column_identifier_regex Regex to identify columns to match on in df2

    Returns:
    list of str: List of strings with trailing letters removed.
    """
    import pandas as pd
    
    def process_row(row, id_column):
        results = []
        for key, value in column_mapping_to_nsi.items():
            perc = row[key]
            matching_rows = df2[df2[column_to_match] == value]
            if (matching_rows.shape[0] == 0):
                raise ValueError
            
            filtered_columns = [col for col in matching_rows.columns if re.search(column_identifier_regex, col)]
            if not filtered_columns:
                raise ValueError
            
            mean_values = matching_rows[filtered_columns].mean(axis=0)
            weighted_mean = mean_values * perc
            results.append(weighted_mean.rename(key))
        
        if results:
            combined_df = pd.concat(results, axis=1).sum(axis=1)
            combined_df[id_column] = row[id_column]
            return combined_df
        else:
            raise ValueError
        
    results = df1.apply(lambda row: process_row(row, id_column), axis=1)
    return results


def main():
    vuln_curves = pd.read_csv('damage_assessment/supporting_data/damage_curves_and_values/nsi_median_vulnerability_curves.csv')

    StateAbbr = "VI"
    structure_types = ("RES", "COM", "IND", "AGR", "REL", "GOV", "EDU")

    # Open dependencies
    occupancy_path = f'damage_assessment_usvi/USVI_data/BuildingCountByOccupancyCensusBlock_{StateAbbr}.csv'
    total_values_path = f'damage_assessment_usvi/USVI_data/BuildingContentFullReplacementValueByOccupancyCensusBlockLevel_{StateAbbr}.csv'
    occupancies = pd.read_csv(occupancy_path)
    values = pd.read_csv(total_values_path)

    # Clean up the occupancies counts
    occupancies = occupancies.rename(columns={col: col.split(" - ")[0] for col in occupancies.columns})
    building_columns = [c for c in occupancies.columns if np.any([c.startswith(t) for t in structure_types])]

    # Get frequencies
    frequencies = convert_to_percentage(occupancies, building_columns)
    column_mapping_to_nsi = {
        c: re.sub(r'[a-zA-Z]+$', '', c)
        for c in building_columns
    }

    # Rename columns to match NSI
    frequencies = frequencies[
        [c for c in frequencies.columns if np.any([c.startswith(t) for t in structure_types])]
        + 
        ["CensusBlock",]
    ]

    # Generate weighted vulnerability curve
    weighted_vulnerability_curves = generate_weighted_vulnerability_curve(frequencies, vuln_curves, "CensusBlock", column_mapping_to_nsi, "Occupancy", r'^m\d*\.?\d*$')
    logging.info(weighted_vulnerability_curves)

    # Format Values
    values = values.rename(columns={col: col.split(" - ")[0] for col in values.columns})
    values_columns = [c for c in values.columns if np.any([i in c for i in structure_types])]

    # Set the Indexes
    values = values.set_index("CensusBlock")
    values = values.sort_index()
    occupancies = occupancies.set_index("CensusBlock")
    occupancies = occupancies.sort_index()
    frequencies = frequencies.set_index("CensusBlock")
    frequencies = frequencies.sort_index()
    weighted_vulnerability_curves = weighted_vulnerability_curves.set_index("CensusBlock")
    weighted_vulnerability_curves = weighted_vulnerability_curves.sort_index()

    # Adjust values
    values[values_columns] = values[values_columns] * 1000
    for c in values_columns:
        values[c] = values[c] / occupancies[c]

    weighted_values = (frequencies[values_columns] * values[values_columns])
    weighted_values = weighted_values.sum(axis=1).rename("OccupancyWeightedValue")

    # Join and write output
    composite_values = pd.merge(weighted_vulnerability_curves, weighted_values, left_index=True, right_index=True)
    composite_values.to_csv(f"damage_assessment_usvi/vulnerability_curves/{StateAbbr}_Block_weighted_vulnerability_curves_and_values.csv")

    geogs = gpd.read_file("damage_assessment_usvi/USVI_data/CensusBlock_VI.gpkg")
    geogs = geogs[geogs["StateAbbr"] == StateAbbr].set_index("CensusBlock")
    composite_values.index = composite_values.index.astype(int).astype(str)
    geogs = pd.merge(geogs, composite_values, left_index=True, right_index=True)
    geogs.to_file(f"damage_assessment_usvi/vulnerability_curves/{StateAbbr}_Block_weighted_vulnerability_curves_and_values.gpkg")


if __name__ == "__main__":
    main()