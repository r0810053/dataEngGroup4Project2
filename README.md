# Data Engineering Project

Task for the course Data Engineering to scrape data from hackernews and set up a data lake pipeline. Everything runs in docker containers. I am using Dagster to orchestrate the pipeline, running on port 3000. On port 8501 i run an simple streamlit dashboard. The database used is MongoDB

V1.0

- Basic version based on Dagster tutorial setup

V1.1

- Removed mongoDB login credentials from pythong script
- Fixed bug where layer and database name were switched
- Updated sheduling and fixed bug in dagster schedules
- Updated project name from tutorial to dataEngineering
- Made fix for when you start and rss feed is empty ( in weekends )
- cleaned up code and added documentation
