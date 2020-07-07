#!/bin/bash

export START_DATE=$(date -u +"%m/%d/%Y" -d "${START_DATE_OFFSET_DAYS} day ago")

echo "Computed start date for data fetch as: ${START_DATE}"
echo "(^ in stupid US notation for compatibility)"
envsubst < ../GarminConnectConfigBase.json > GarminConnectConfig.json

echo "Rendered Garmin fetch config:"
cat GarminConnectConfig.json

echo "Downloading and processing Garmin data"
python3 garmin.py --all --download --import
echo "Got Garmin data"
echo "Syncing Garmin data to PostgreSQL"
python3 sync_to_pg.py
echo "Synced Garmin data to PostgreSQL"
