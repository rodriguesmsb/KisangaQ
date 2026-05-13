#%%
#import libraries
import ee
import geemap
import pandas as pd
from datetime import date

# %%
# Authenticate and initialize the Earth Engine API
ee.Authenticate()
ee.Initialize()

# %%
# Load asset with Brazilian municipalities
mun_fc = ee.FeatureCollection("projects/ee-rodriguesmsb/assets/ibge_municipios")


# %%
# Keep only the ID field and force it to be a string
mun_fc = mun_fc.map(lambda f: f.set("CD_MUN", ee.String(f.get("CD_MUN"))))

#%%
# ERA5-Land hourly dataset 
era5_land_hourly = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")

#%%
#define a function to calculate monthly temperature statistics for a given year and month
def monthly_temp_stats_image(y, m):
    start = ee.Date.fromYMD(y, m, 1)
    end = start.advance(1, "month")

    monthly = (
        era5_land_hourly
        .filterDate(start, end)
        .select("temperature_2m")
    )

    # Per-pixel monthly summaries
    mean_img = monthly.mean().subtract(273.15).rename("temp_mean_c")
    min_img  = monthly.min().subtract(273.15).rename("temp_min_c")
    max_img  = monthly.max().subtract(273.15).rename("temp_max_c")

    return (
        mean_img
        .addBands(min_img)
        .addBands(max_img)
        .set({
            "year": y,
            "month": m,
            "system:time_start": start.millis()
        })
    )
# %%
#define a function to get all the temperature statistics for a given year and month, reduced to the municipality level
def reduce_to_municipalities(img):
    y = ee.Number(img.get("year"))
    m = ee.Number(img.get("month"))
    d = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")

    # Mean and percentiles over each municipality
    reducer = (
        ee.Reducer.mean()
        .combine(ee.Reducer.percentile([5, 95]), sharedInputs=True)
    )

    fc = img.reduceRegions(
        collection=mun_fc,
        reducer=reducer,
        scale=11132,
        tileScale=16
    )

    fc = fc.map(lambda f: ee.Feature(
        None,
        {
            "CD_MUN": ee.String(f.get("CD_MUN")),
            "year": y,
            "month": m,
            "date": d,

            # Municipality-average summaries
            "mean_temp_c": f.get("temp_mean_c_mean"),
            "min_temp_c":  f.get("temp_min_c_mean"),
            "max_temp_c":  f.get("temp_max_c_mean"),

            # Robust municipal extremes
            "p05_min_temp_c": f.get("temp_min_c_p5"),
            "p95_max_temp_c": f.get("temp_max_c_p95")
        }
    ))

    return fc

# %%
def export_month(y, m, folder="era5_land_temp_monthly"):
    img = monthly_temp_stats_image(y, m)
    fc = reduce_to_municipalities(img)

    desc = f"TEMP_STATS_PCTL_ERA5LAND_{y}_{m:02d}"

    task = ee.batch.Export.table.toDrive(
        collection=fc,
        description=desc,
        folder=folder,
        fileNamePrefix=desc,
        fileFormat="CSV",
        selectors=[
            "CD_MUN", "year", "month", "date",
            "mean_temp_c", "min_temp_c", "max_temp_c",
            "p05_min_temp_c", "p95_max_temp_c"
        ]
    )
    task.start()
    print("Started:", desc)

#%%
# Run exports for 1980-01 through 2025-12
for y in range(1980, 2026):
    for m in range(1, 13):
        export_month(y, m)

# %%
#cancel all running or pending tasks (if needed)
# Retrieve all tasks
def cancel_all_tasks():
    tasks = ee.data.listOperations()
    # Iterate and cancel each task
    for task in tasks:
        task_id = task['name']
        state = task['metadata']['state']
    
        # Check if the task is still running or pending
        if state in ['RUNNING', 'PENDING']:
            print(f"Cancelling task: {task_id}")
            ee.data.cancelOperation(task_id)
# %%
cancel_all_tasks()