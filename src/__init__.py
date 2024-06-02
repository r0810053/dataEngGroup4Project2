from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)

from . import import_data

all_assets = load_assets_from_modules([import_data])

import_assest = load_assets_from_modules([import_data], group_name="import_data")

assest_download_job = define_asset_job(
    "download_data_job",
    selection=AssetSelection("import_data"),
)

download_schedule = ScheduleDefinition(
    name="download_data_schedule",
    cron_schedule="0 0 * * *",
    job=assest_download_job,
)

defs = Definitions(
    assets=all_assets,
    schedules=[download_schedule],
)