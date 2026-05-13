#%%
import ee
import geemap
import pandas as pd
from datetime import date



# %%
#authenticate and initialize the Earth Engine API
ee.Authenticate()

#%%
ee.Initialize()

#%%
#load asset with Brazilian municipalities
mun_fc = ee.FeatureCollection("projects/ee-rodriguesmsb/assets/ibge_municipios")


#%%
# Keep only the ID field and force it to be a string
mun_fc = mun_fc.map(lambda f: f.set("CD_MUN", ee.String(f.get("CD_MUN"))))



# %%
modis = ee.ImageCollection("MODIS/061/MOD13Q1")  # NDVI 16-day 250m
NDVI_SCALE = 0.0001  # MOD13Q1 NDVI scale factor

#%%
def monthly_ndvi_image(y, m):
    start = ee.Date.fromYMD(y, m, 1)
    end = start.advance(1, "month")

    return (modis
            .filterDate(start, end)
            .select("NDVI")
            .mean()
            .multiply(NDVI_SCALE)
            .rename("ndvi")
            .set({"year": y, "month": m, "system:time_start": start.millis()}))

#%%
def reduce_to_municipalities(img):
    y = ee.Number(img.get("year"))
    m = ee.Number(img.get("month"))
    d = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")

    fc = img.reduceRegions(
        collection=mun_fc,
        reducer=ee.Reducer.mean(),
        scale=250,
        tileScale=16
    )

    # Rename "mean" column and remove geometry
    fc = fc.map(lambda f: (
        ee.Feature(
            None,
            {
                "CD_MUN": ee.String(f.get("CD_MUN")),
                "year": y,
                "month": m,
                "date": d,
                "mean_ndvi": f.get("mean")
            }
        )
    ))

    return fc

# %%
def export_month(y, m, folder="ndvi_modis_monthly"):
    img = monthly_ndvi_image(y, m)
    fc = reduce_to_municipalities(img)

    desc = f"NDVI_MOD13Q1_{y}_{m:02d}"

    task = ee.batch.Export.table.toDrive(
        collection=fc,
        description=desc,
        folder=folder,
        fileNamePrefix=desc,
        fileFormat="CSV",
        selectors=["CD_MUN", "year", "month", "date", "mean_ndvi"]
    )
    task.start()
    print("Started:", desc)
    
# %%
# Run exports for 2010-01 through 2023-12
for y in range(2010, 2024):
    for m in range(1, 13):
        export_month(y, m)
# %%
