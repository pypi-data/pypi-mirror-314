import argparse
import json
import os
from datetime import datetime
import pandas as pd
from itertools import chain
from DSSATTools import (
    Crop, SoilProfile, Weather, Management, DSSAT, TabularSubsection,
)
import dssatsim.utils as ut
from dssatsim.explain_dssat_outputs import explain_summary_out
from dssatsim.envs import (
    DB_VARS, MINIMUM_REQUIRED_FARMER_INPUTS,
    OUTDIR, INSTI_CODE, SUMMARY_OUT_AS_JSON_NAN,
)
pd.options.mode.chained_assignment = None

# Constants
db_params = {
    'dbname': DB_VARS['DB_NAME'],
    'user': DB_VARS['DB_USER'],
    'password': DB_VARS['DB_PASSWORD'],
    'host': DB_VARS['DB_HOST'],
    'port': DB_VARS['DB_PORT']
}


def is_simulation_possible(input_data):
    for min_input in MINIMUM_REQUIRED_FARMER_INPUTS:
        got = input_data.get(min_input, None)

        if got is None:
            return False
        
        if isinstance(got, str) and got == "-99":
            return False

        if isinstance(got, int) and got == -99:
            return False
        
        if isinstance(got, list) :
            is_irrigation_applied = input_data.get("is_irrigation_applied", None)
            if is_irrigation_applied.lower() == "yes" and -99 in list(chain.from_iterable(got)):
                return False
    return True


def setup_irrigation_table(irr_apps_list):
    schedule = pd.DataFrame(irr_apps_list, columns=["IDATE", "IRVAL"]) # IRVAL is in mm
    schedule["IDATE"] = pd.to_datetime(schedule["IDATE"])
    schedule['IDATE'] = schedule.IDATE.dt.strftime('%y%j')
    schedule['IROP'] = 'IR001'  # TO-DO: check if this must be changed also
    schedule = schedule[['IDATE', 'IROP', 'IRVAL']]
    return TabularSubsection(schedule)


def exec(input_file, output_file=None, remove_temp_files=True):

    # check if input is dictionary or json file. if it is dictionary, you don't need to open the file
    if isinstance(input_file, dict):
        input_data = input_file
    else:
        # Load input JSON file
        input_file = os.path.abspath(input_file)
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

    # Check if simulation is possible
    if not is_simulation_possible(input_data):
        return None, SUMMARY_OUT_AS_JSON_NAN

    # Prep Weather
    planting_date = input_data["planting_date"]
    year = int(planting_date.split("-")[0])

    extracted_wth_res = ut.location_to_WTH_file(
        db_params, 
        target_lat=input_data["latitude"], 
        target_lon=input_data["longitude"], 
        year=year, 
        outdir=OUTDIR, 
        institution_code=INSTI_CODE
    )

    weather_dates = pd.date_range(f"{year}-01-01", f"{year}-12-30")
    weather_df = extracted_wth_res['wth_table_df']
    weather_df = weather_df[['TMIN', 'TMAX', 'RAIN', 'SRAD']]
    weather_df["DATES"] = weather_dates
    weather_df = weather_df.set_index("DATES")

    dssat_weather_module = Weather(
        df=weather_df,
        pars={'TMIN': 'TMIN', 'TMAX': 'TMAX', 'RAIN': 'RAIN', 'SRAD': 'SRAD',},
        lat=input_data["latitude"],
        lon=input_data["longitude"],
        elev=input_data["elevation"],
    )

    # Prep Soil
    extracted_sol_res = ut.location_to_SOL_file(
        db_params=db_params, 
        target_lat=input_data["latitude"], 
        target_lon=input_data["longitude"], 
        outdir=OUTDIR, 
    )

    sol_fpath = extracted_sol_res['sol_fpath']
    soil_profile_name = extracted_sol_res['soil_profile_name']

    dssat_soil_module = SoilProfile(file=sol_fpath, profile=soil_profile_name)

    # Prep Crop module
    dssat_crop_module = Crop(
        crop_name=input_data["crop_name"].lower(),
    )

    # Prepare the management
    dssat_management_module = Management(
        planting_date=datetime.strptime(planting_date, "%Y-%m-%d"),
        sim_start=None, # assumption - will be calculated as previous day to the planting date
        emergence_date=None, # assumption - will be calculated as 5 days after planting
        initial_swc=1, # assumption - Fraction of the total available water set to 100%
        harvest="M", # assumption - harvest to Maturity
        fertilization='N', # assumption - Not fertilized
        organic_matter='G', # assumption - Ceres (Godiwn)
    )

    if input_data["is_irrigation_applied"].lower() == "no":
        dssat_management_module.simulation_controls['IRRIG'] = "N"
    else:
        dssat_management_module.simulation_controls['IRRIG'] = "R"
        dssat_management_module.irrigation['table'] = setup_irrigation_table(input_data["irrigation_application"])
        print(dssat_management_module.irrigation['table'])

    # Run DSSAT experiment
    dssat = DSSAT()
    dssat.setup()
    dssat.run(
        soil=dssat_soil_module, 
        weather=dssat_weather_module, 
        crop=dssat_crop_module, 
        management=dssat_management_module,
    )

    # Finalize
    if dssat.output is None:
        print(f"Simulation `{input_data['experiment_name']}` did not run successfully")
    else:
        summary_out_fpath = ut.retrieve_fout_path(code="Summary")
        if not os.path.exists(summary_out_fpath):
            print(f"Summary file not found at {summary_out_fpath}")
            explanations = SUMMARY_OUT_AS_JSON_NAN
        else:
            explanations, _ = explain_summary_out(summary_out_fpath, output_file)


    dssat.close()
    
    if remove_temp_files: ut.clean_up_folder(OUTDIR)

    return output_file, explanations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a DSSAT simulation based on input JSON file.")
    parser.add_argument('input_file', type=str, help="Path to the input JSON file.")

    args = parser.parse_args()
    exec(args.input_file)
