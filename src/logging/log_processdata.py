"""Log process data example.

This module demonstrates use of the StatLogger class to log process data into a log file
in jsonl format as specified in:
https://github.com/statisticsnorway/arkitektur-informasjonsmodeller/tree/main/process-data

The defined json-schema is converted to a Pydantic model for data validation.
"""

import json
from datetime import datetime

from process_data import ProcessData
from pydantic import ValidationError
from statlogger import LoggerType
from statlogger import StatLogger


loggers = [LoggerType.JSONL_EXTRA_ONLY, LoggerType.CONSOLE]
logger = StatLogger(log_file="process.log", loggers=loggers).getLogger()


def validate_jsonl_process_data(file_path: str) -> None:
    """Reads a JSONL file and validates each line against the ProcessData model."""
    with open(file_path, encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # Parse the JSON from the current line
                data = json.loads(line)

                # Validate the JSON data against the ProcessData model
                process_data = ProcessData(**data)

                # If valid, print or process the data
                logger.info(f"Line {line_number}: Valid - {process_data}")
            except json.JSONDecodeError as e:
                logger.info(f"Line {line_number}: Invalid JSON - {e}")
            except ValidationError as e:
                logger.info(f"Line {line_number}: Validation error - {e}")


def main() -> None:
    current_datetime = datetime.now().astimezone()
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
    logger.info("Log processdata without extra")

    # Read back the logged process data and checks that it validates
    # according to the schema
    validate_jsonl_process_data("process.jsonl")


if __name__ == "__main__":
    main()
