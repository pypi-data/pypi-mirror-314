import json
import pandas as pd
import numpy as np
import json
import dssatsim.utils as ut
from dssatsim.envs import (
    OUTPUT_CODE_TYPES_FROM_DSSATTOOLS, 
    ALL_DSSAT_CDE_FILES, 
    CDE_SUFIX_SEP, 
    SUMMARY_OUT_CATEGORIES_COLS
)


def get_proper_description(code):
    df_dssat_codes = pd.read_csv(ALL_DSSAT_CDE_FILES)
    res = df_dssat_codes[df_dssat_codes["@CDE"] == code]["DESCRIPTION"]

    if res.size == 1:
        res = res.item()
    elif res.size > 1:
        res = res.to_list()[0]
    else:
        res = code
    return res


def get_dssat_code_characteristic(code, value, dssat_output_category):

    code_no_suffix = code.split(CDE_SUFIX_SEP)[0]
    # base_output = {"code": code, "value": value, "dssat_output_category":dssat_output_category,}
    base_output = {"code": code, "value": value,}
    df_ = pd.read_csv(ALL_DSSAT_CDE_FILES)

    if code_no_suffix not in df_["@CDE"].values:
        return base_output

    df_ = df_[df_["@CDE"]==code_no_suffix]
    df_.replace({np.nan: "None"}, inplace=True)

    base_output.update({
        "label": df_["LABEL"].iloc[0],
        "description": df_["DESCRIPTION"].iloc[0],
        "unit": df_["UNIT"].iloc[0],
    })
    return base_output

def rename_year_doy_das_columns_in_dssat_output(dssat_output_df, suffix):
    dssat_output_df_copy = dssat_output_df.copy()
    dssat_output_df_copy.rename(columns={
        '@YEAR': f'@year{CDE_SUFIX_SEP}{suffix}',
        'DOY': f'DOY{CDE_SUFIX_SEP}{suffix}',
        'DAS': f'DAS{CDE_SUFIX_SEP}{suffix}' 
        }, 
        inplace=True)
    return dssat_output_df_copy

def average_numerical_dssat_output(dssat_output_df):
    return dssat_output_df.select_dtypes(include='number').mean().round(3).to_dict()


def explain_dssatobj_outs(dssat_output_obj, out_fname, save_individual=False):
    explanations = dict()
    for output_code in OUTPUT_CODE_TYPES_FROM_DSSATTOOLS:
        output_df = dssat_output_obj.output[output_code]
        output_df = rename_year_doy_das_columns_in_dssat_output(output_df, output_code)
        averages = average_numerical_dssat_output(output_df)

        for code, value in averages.items():
            new_key_name = f"{output_code}_{code}"
            new_key_name = new_key_name.replace(f"__{output_code}", "")
            explanations[code] = get_dssat_code_characteristic(code, value, output_code)

    with open(out_fname, "w") as f:
        json.dump(explanations, f)

    return explanations


def explain_irrigation_only(dssat_obj, out_fname):

    explanations = dict()
    df_SoilWat = dssat_obj.output['SoilWat']
    df_SoilWat.rename_axis('dates', inplace=True)
    df_SoilWat.reset_index(inplace=True)
    
    cols_oi = ['dates', 'PREC', 'IR#C', 'IRRC', 'ROFD']
    new_cols = ["dates", "Cumulative_Precipitation", "Cumulative_Irrigation_Applications", "Cumulative_Irrigation_Amount", "Cumulative_Surface_Runoff",]
    
    df_irrigation = df_SoilWat[cols_oi].copy()
    df_irrigation.columns = new_cols

    df_irrigation['Daily_Irrigation_Application'] = df_irrigation['Cumulative_Irrigation_Applications'].diff()
    df_irrigation['Daily_Irrigation_Amount'] = df_irrigation['Cumulative_Irrigation_Amount'].diff()
    df_irrigation.fillna({"Daily_Irrigation_Application": 0, "Daily_Irrigation_Amount": 0}, inplace=True)
    df_irrigation['Day_Of_Year'] = df_irrigation['dates'].dt.dayofyear

    qlist, a_list = generate_irrigation_qa_pairs(df_irrigation, nsample=5)

    df_irrigation['dates'] = df_irrigation['dates'].dt.strftime('%Y-%m-%d')

    df_irrigation.set_index('dates', inplace=True)
    date_keyed_dict = df_irrigation.to_dict(orient='index')    
    
    with open(out_fname, "w") as f:
        json.dump(date_keyed_dict, f, indent=4)

    return {"output_file": out_fname, 
            "output_structure": date_keyed_dict,
            "questions": qlist,
            "answers": a_list
            }


def generate_irrigation_qa_pairs(df_irrigation, nsample=5):

    # Determine the actual sample size
    actual_sample_size = min(nsample, len(df_irrigation))

    # Perform the sampling
    sampled_df = df_irrigation.sample(n=actual_sample_size, random_state=42)  # random_state for reproducibility

    # Reset the index of the sampled DataFrame
    sampled_df = sampled_df.reset_index(drop=True)  

    questions_list = []
    answers_list = []

    for row_ctr in sampled_df.iterrows():
        row = row_ctr[1]

        questions_list.append(
            f"How many times was irrigation applied on day {row['dates'].date()}?"
        )
        answers_list.append(row['Daily_Irrigation_Application'])

        questions_list.append(
            f"How much irrigation was applied on {row['dates'].date()}?"
        )
        answers_list.append(row['Daily_Irrigation_Amount'])

        questions_list.append(
            f"What was the surface runoff on Day {row['Day_Of_Year']} of the year?"
        )
        answers_list.append(row['Cumulative_Surface_Runoff'])

        questions_list.append(
            f"How much precipitation has been accumulated by day {row['Day_Of_Year']}?"
        )
        answers_list.append(row['Cumulative_Precipitation'])

        questions_list.append(
            f"What was the cumulative irrigation amount on Day {row['Day_Of_Year']}?"
        )
        answers_list.append(row['Cumulative_Irrigation_Amount'])

    return questions_list, answers_list


def summary_out_to_table(out_fpath):
    """
    Reads the Summary.OUT file and returns a pandas DataFrame.
    Args:
        out_fpath (str): The path to the Summary.OUT file.
    Returns:
        pd.DataFrame: A DataFrame containing the contents of the Summary.OUT file.
    """

    def extract_columns_from_header_line(header_line):
        columns = [c.replace(".", "") for c in header_line.strip().split() if c != "@"]
        return columns   

    def convert_dates_columns(row):
        for xdat in SUMMARY_OUT_CATEGORIES_COLS["DATES"]:
            if xdat == "HYEAR":
                row[xdat] = row[xdat]
            else:
                row[xdat] = ut.yrdoy_to_date(row[xdat])
        return row
    
    header_lines = ut.get_header_lines(out_fpath)

    df = pd.read_csv(out_fpath, sep=r"\s+", skiprows=len(header_lines), header=None)

    if len(df[9][0]) == 1:
        # For example, "AG9010", "-" and "IRRIGATED" --> "AG9010 - IRRIGATED"
        df[8] = df[8].astype(str) + " " + df[9].astype(str) + " " + df[10].astype(str)
        df.drop(columns=[9, 10], inplace=True)
    else:
        # For example, "AG9010", "IRRIGATED" --> "AG9010 IRRIGATED"
        df[8] = df[8].astype(str) + " " + df[9].astype(str)
        df.drop(columns=[9], inplace=True)
    
    print(header_lines[-1])
    df.columns = extract_columns_from_header_line(header_lines[-1])

    # convert yrdoy columns to actual dates
    df = df.apply(convert_dates_columns, axis=1)
    
    return df


def explain_xdates(df_summary, columns_oi):
    explanations = dict()
    df_oi_ = df_summary[columns_oi]
    df_oi = df_oi_.copy()

    df_oi["Crop establishment start"] = df_oi["PDAT"]
    df_oi["Crop establishment end"] = df_oi["EDAT"] - pd.Timedelta(days=1)
    df_oi["Crop establishment duration"] = df_oi["Crop establishment end"] - df_oi["Crop establishment start"]

    df_oi["Vegetative growth start"] = df_oi["EDAT"]
    df_oi["Vegetative growth end"] = df_oi["ADAT"] - pd.Timedelta(days=1)
    df_oi["Vegetative growth duration"] = df_oi["Vegetative growth end"] - df_oi["Vegetative growth start"]

    df_oi["Yield formation start"] = df_oi["ADAT"]
    df_oi["Yield formation end"] = df_oi["MDAT"] - pd.Timedelta(days=1)
    df_oi["Yield formation duration"] = df_oi["Yield formation end"] - df_oi["Yield formation start"]

    df_oi["Entire period start"] = df_oi["PDAT"]
    df_oi["Entire period end"] = df_oi["MDAT"]
    df_oi["Entire period duration"] = df_oi["Entire period end"] - df_oi["Entire period start"]

    new_cols = [get_proper_description(c) for c in df_oi.columns]
    df_oi.columns = [c.replace(" (YrDoy)", "").replace(" (YRDOY)", "") for c in new_cols]

    explanations["Dates"] = df_oi.astype(str).to_dict(orient='records')[0]

    return explanations, df_oi


def explain_summary_out(summary_out_fpath, out_fname=None, exclude_columns=None):
    explanations = dict()
    df_summary = summary_out_to_table(summary_out_fpath)

    if exclude_columns is None:
        exclude_columns = []
        
    df_summary = df_summary.drop(columns=exclude_columns)

    for category, columns in SUMMARY_OUT_CATEGORIES_COLS.items():
        if category == "DATES": continue
        df_sub = df_summary[
            [c for c in columns if c in df_summary.columns]
        ]
        df_sub.columns = [get_proper_description(c) for c in df_sub.columns]
        explanations[category.capitalize()] = df_sub.to_dict(orient='records')[0]

    explanations_xdates, df_xdates = explain_xdates(df_summary, columns_oi=SUMMARY_OUT_CATEGORIES_COLS["DATES"])
    explanations_with_updated_dates = {**explanations, **explanations_xdates}

    df_summary_final = pd.concat([df_summary, df_xdates], axis=1)
    
    if out_fname is not None:
        with open(out_fname, "w") as f:
            json.dump(explanations_with_updated_dates, f, indent=4)
        print(f"Summary.OUT was saved as JSON to {out_fname}")

    return explanations_with_updated_dates, df_summary_final

