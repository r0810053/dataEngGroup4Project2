from dagster import AssetSelection, DefaultScheduleStatus, Definitions, ScheduleDefinition, define_asset_job, load_assets_from_modules

from . import assets
from . import cleaning
from . import statistics

all_assets = load_assets_from_modules([assets, cleaning, statistics])

import_assets = load_assets_from_modules([assets], group_name="data_import")
cleaning_assets = load_assets_from_modules([cleaning], group_name="data_cleaning")
dashboard_assets = load_assets_from_modules([statistics], group_name="dashboard")

asset_download_job = define_asset_job(
    "download_data_job",
    selection=AssetSelection.groups("data_import"),
)

cleaning_job = define_asset_job(
    "cleaning_job",
    selection=AssetSelection.groups("cleaning"),
)

dashboard_job = define_asset_job(
    "dashboard_job",
    selection=AssetSelection.groups("dashboard"),
)

import_schedule = ScheduleDefinition(
    name="download_hackernews_data",
    cron_schedule="0 0 * * *",
    job=asset_download_job,
    default_status=DefaultScheduleStatus.RUNNING,
)

cleaning_schedule = ScheduleDefinition(
    name="clean_data",
    cron_schedule="0 3 * * *",
    job=cleaning_job,
    default_status=DefaultScheduleStatus.RUNNING
)

dashboard_schedule = ScheduleDefinition(
    name="dashboard",
    cron_schedule="0 6 * * *",
    job=dashboard_job,
    default_status=DefaultScheduleStatus.RUNNING
)

defs = Definitions(
    assets=all_assets,  # type: ignore
    schedules=[import_schedule, cleaning_schedule, dashboard_schedule],
)