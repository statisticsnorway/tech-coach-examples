"""Log process data example.

This module demonstrates use of the StatLogger class to log process data into a log file
in jsonl format as specified in:
https://github.com/statisticsnorway/arkitektur-informasjonsmodeller/tree/main/process-data

The defined json-schema is converted to a Pydantic model for data validation.
"""

import json
from datetime import datetime
from zoneinfo import ZoneInfo

from process_data import ProcessData
from statlogger import StatLogger


logger = StatLogger(log_file="process.log", jsonl=True).get_logger()


def main() -> None:
    timezone = ZoneInfo("Europe/Oslo")
    current_datetime = datetime.now(tz=timezone)
    process_data = ProcessData(
        statistics_name="metstat",
        data_target="gs://ssb-tip-tutorials-data-produkt-prod/metstat/inndata/frost/weather_stations_v1.parquet",
        data_period="2025-01-21T08:45:45+0100",
        unit_id="komm_nr",
        change_event="A",
        change_event_reason="OTHER_SOURCE",
        change_datetime=current_datetime,
    )

    process_dict = json.loads(process_data.model_dump_json())
    logger.info("Log processdata", extra={"data": process_dict})


if __name__ == "__main__":
    main()
