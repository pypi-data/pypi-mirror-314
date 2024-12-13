# pbip_extractor
`pbip_extractor` is a Python package designed to extract metadata and information from Power BI reports (pbip files). It helps in analyzing and understanding the components of Power BI reports, giving insights into which columns and measures are used in the report and where/how.

## Installation

Install the package using pip:

```bash
pip install pbip_extractor
```

## Usage

Import the package in your Python script or notebook:

```python
from pbip_extractor import PBIPExtractor
```

### Extracting from a Report with a Data Model

For reports containing an embedded data model:

```python
# initialize the extractor
pbip_path = "path/to/datamodel_dir/"
pbip_filename = "datamodel"
pbip = PbipExtractor(pbip_path=pbip_path, 
                    pbip_filename=pbip_filename, 
                    verbose=False,
                    )
# run the analysis
pbip.run()
# inspect the output
pbip.report_df.head()
pbip.column_in_report_df.head()
```

### Extracting from a Report with a Live Connection

For reports using live connections to external data sources:

```python
# report with the datamodel
# initialize the extractor
pbip_path_datamodel = "path/to/datamodel_dir/"
pbip_filename_datamodel = "datamodel"
datamodel_pbip = PbipExtractor(pbip_path=pbip_path, 
                               pbip_filename=pbip_filename, 
                               verbose=False,
                               )
# run the analysis
datamodel_pbip.run()
# extract the output needed as input in the next step
df_datamodel_overview = datamodel_pbip.report_df[['table', 'column']]

# report with live connection
# initialize the extractor
pbip_path_liveconn = "path/to/report_dir/"
pbip_filename_liveconn = "live connection report"
pbip_liveconn = PbipExtractor(pbip_path=pbip_path_liveconn, 
                              pbip_filename=pbip_filename_liveconn, 
                              df_source=df_datamodel_overview, 
                              verbose=True,
                              )
# run the analysis
pbip_liveconn.run()
# inspect the output
pbip_liveconn.report_df.head()
pbip_liveconn.column_in_report_df.head()
```

## Repository

The source code is available on [GitLab](https://gitlab.com/jeaninejuliette/pbip_extractor).

## Contributing

Contributions are welcome. Please fork the repository and submit merge requests on GitLab. For major changes, open an issue to discuss proposed modifications.

## License

This project is licensed under the [MIT License](LICENSE).