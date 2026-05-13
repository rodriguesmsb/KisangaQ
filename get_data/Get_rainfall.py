#%%
# import libraries
import ee
import geemap
import pandas as pd
from datetime import date



# %%
# Authenticate and initialize the Earth Engine API
ee.Authenticate(force=True)
ee.Initialize()

# %%
# Load asset with Brazilian municipalities
mun_fc = ee.FeatureCollection("projects/ee-rodriguesmsb/assets/ibge_municipios")

# Keep only the ID field and force it to be a string
mun_fc = mun_fc.map(lambda f: f.set("CD_MUN", ee.String(f.get("CD_MUN"))))

#%%
# CHIRPS daily rainfall dataset
# precipitation is in mm/day
chirps_daily = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")

# Rainy day threshold in mm/day
RAIN_THRESHOLD_MM = 1.0

#%%
# Define a function to calculate monthly rainfall statistics for a given year and month
def monthly_rain_stats_image(y, m, rain_threshold_mm=1.0):
    start = ee.Date.fromYMD(y, m, 1)
    end = start.advance(1, "month")

    monthly = (
        chirps_daily
        .filterDate(start, end)
        .select("precipitation")
    )

    # Per-pixel monthly summaries from daily rainfall
    mean_img = monthly.mean().rename("rain_mean_mm")

    # Monthly accumulated rainfall
    total_img = monthly.sum().rename("rain_total_mm")

    # Minimum rainfall considering only rainy days (> threshold)
    monthly_rainy_only = monthly.map(
        lambda img: img.updateMask(img.gt(rain_threshold_mm))
    )
    min_img = monthly_rainy_only.min().rename("rain_min_mm")

    # Maximum rainfall across all days in the month
    max_img = monthly.max().rename("rain_max_mm")

    # Number of rainy days in the month per pixel
    rainy_days_img = (
        monthly
        .map(lambda img: img.gt(rain_threshold_mm).rename("rainy_day"))
        .sum()
        .rename("rainy_days")
    )

    return (
        mean_img
        .addBands(total_img)
        .addBands(min_img)
        .addBands(max_img)
        .addBands(rainy_days_img)
        .set({
            "year": y,
            "month": m,
            "system:time_start": start.millis(),
            "rain_threshold_mm": rain_threshold_mm
        })
    )


# %%
# Define a function to reduce all rainfall statistics to municipality level
def reduce_to_municipalities(img):
    y = ee.Number(img.get("year"))
    m = ee.Number(img.get("month"))
    d = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")
    rain_threshold_mm = ee.Number(img.get("rain_threshold_mm"))

    reducer = (
        ee.Reducer.mean()
        .combine(ee.Reducer.percentile([2.5, 97.5]), sharedInputs=True)
    )

    fc = img.reduceRegions(
        collection=mun_fc,
        reducer=reducer,
        scale=5566,
        tileScale=16
    )

    fc = fc.map(lambda f: ee.Feature(
        None,
        {
            "CD_MUN": ee.String(f.get("CD_MUN")),
            "year": y,
            "month": m,
            "date": d,
            "rain_threshold_mm": rain_threshold_mm,

            "mean_rain_mm": f.get("rain_mean_mm_mean"),
            "total_rain_mm": f.get("rain_total_mm_mean"),
            "min_rain_mm":  f.get("rain_min_mm_mean"),
            "max_rain_mm":  f.get("rain_max_mm_mean"),
            "rainy_days_mean": f.get("rainy_days_mean")
        }
    ))

    return fc


# %%
def export_month(y, m, folder="chirps_rain_monthly", rain_threshold_mm=1.0):
    img = monthly_rain_stats_image(y, m, rain_threshold_mm=rain_threshold_mm)
    fc = reduce_to_municipalities(img)

    desc = f"RAIN_STATS_CHIRPS_{y}_{m:02d}"

    task = ee.batch.Export.table.toDrive(
        collection=fc,
        description=desc,
        folder=folder,
        fileNamePrefix=desc,
        fileFormat="CSV",
        selectors=[
            "CD_MUN", "year", "month", "date", "rain_threshold_mm",
            "mean_rain_mm", "total_rain_mm", "min_rain_mm", "max_rain_mm",
            "rainy_days_mean"
        ]
    )
    task.start()
    print("Started:", desc)


#%%
#Run exports for 1981-01 through 2025-12
for y in range(1981, 2026):
    for m in range(1, 13):
        export_month(y, m, rain_threshold_mm=1.0)

# %%
# Cancel all running or pending tasks (if needed)
def cancel_all_tasks():
    tasks = ee.data.listOperations()

    for task in tasks:
        task_id = task['name']
        state = task['metadata']['state']

        if state in ['RUNNING', 'PENDING']:
            print(f"Cancelling task: {task_id}")
            ee.data.cancelOperation(task_id)

#%%
cancel_all_tasks()
# %%
