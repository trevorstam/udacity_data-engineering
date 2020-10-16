sas_source_code_tables_data = [
  {'name': 'country_codes',
   'value': 'i94cntyl',
   'columns': ['code', 'country'],
   'qc': [{'check_sql': "SELECT COUNT(*) FROM country_codes WHERE code is null", 'expected_result': 0}]
  },
  {'name': 'port_of_entry',
   'value': 'i94prtl',
   'columns': ['code', 'port_of_entry'],
   'qc': [{'check_sql': "SELECT COUNT(*) FROM port_of_entry WHERE code is null", 'expected_result': 0}]
  },
  {'name': 'mode_of_trans',
   'value': 'i94model',
   'columns': ['code', 'mode_of_transport'],
   'qc': [{'check_sql': "SELECT COUNT(*) FROM mode_of_trans WHERE code is null", 'expected_result': 0}]
  },
  {'name': 'address',
   'value': 'i94addrl',
   'columns': ['code', 'address'],
   'qc': [{'check_sql': "SELECT COUNT(*) FROM address WHERE code is null", 'expected_result': 0}]
  },
  {'name': 'visa',
   'value': 'i94visa',
   'columns': ['code', 'type'],
   'qc': [{'check_sql': "SELECT COUNT(*) FROM visa WHERE code is null", 'expected_result': 0}]
  }
]

copy_s3_keys = [
  {'name': 'immigration',
   'key': 'sas_data',
   'file_format': 'parquet',
   'sep': '',
   'qc': []
  },
  {'name': 'city_demographics',
   'key': 'data/us-cities-demographics.csv',
   'file_format': 'csv',
   'sep': ';',
   'qc': []
  },
  {'name': 'airport_codes',
   'key': 'data/airport-codes_csv.csv',
   'file_format': 'csv',
   'sep': ',',
   'qc': []
  },
]