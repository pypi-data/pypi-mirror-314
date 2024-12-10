# TogglReports

![Latest Release](https://img.shields.io/github/v/release/ro-56/togglReports)
[![Python package](https://github.com/ro-56/togglReports/actions/workflows/test.yml/badge.svg)](https://github.com/ro-56/togglReports/actions/workflows/test.yml)
![License, MIT](https://img.shields.io/badge/license-MIT-green)
![Python, 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)

---

TogglReports is a Python library for creating time entry reports from Toggl's detailed report data.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TogglReports.

```bash
pip install togglreports
```

## Usage
TogglReports comes by default with only one type of report (sgu). To create a sgu report, run the following script:

```bash
togglReports build sgu
```

The first time you run the script, you will be prompted to configure your installation. Follow each step to configure the core application and each report type installed.

To reset and redo the configuration script, run the script:

```bash
togglReports config
```

### Arguments
You can specify the start and end times used for a report with the tags `-p` (`-period`), `-s` (`--start`), and `-e` (`--end`).

The `--period` tag can be used to build reports with common start and end times. Possible values are: 
 - `today`: entries for today
 - `thisweek`: entries from the last sunday to the next saturday
 - `lastweek`: entries from past week, from sunday to saturday
 - `thismonth`: entries from the first day to the last day of this month

The `--start` and `--end` tags can be used to define a specific time frame. Expects `YYYY-MM-DD` format, e.g. 2023-10-30. 

The generated report will contain entries from the specified `--start` date, to the specified `--end` date.


The `--end` tag is optional. If not specified, today's date will be used.

**Default:** If no argument is specified, the report will contain only this week's time entries (Same behaviour as using `-p thisweek`).

## Report: SGU - Expected Toggl Data Structure

- **Time entry:** The name and duration of the sgu task;
- **Project:** The sgu project;
- **Tag:** The sgu category (if multiple, only one is used);

While configuring the report, you can define a specific tag to indicate that a time entry should be ignored while creating a report. 

## FAQ

### 1. How to locate the Toggl API Token?

Your personal Toggl api token can be found following [these instructions](https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located).

### 2. How to create other report types?

Included in this repository is an example report type containing the basic files structure and required configuration for a report type.

The `src\togglreports\plugins\example.py` file is where the report is built: where the data is manipulated from the information extracted from the Toggl API and where the output file is created.

The `data\reports_example.json` file is where you define the report required configuration parameters. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
