table_list = ['immigration', 'city_demographics', 'airport_codes', 'country_codes', 'port_of_entry', 'mode_of_trans', 'address', 'visa']

drop_table_template = "DROP TABLE IF EXISTS {}"

create_immigration = """
CREATE TABLE IF NOT EXISTS immigration (
    cicid FLOAT PRIMARY KEY,
    i94yr FLOAT SORTKEY,
    i94mon FLOAT DISTKEY,
    i94cit FLOAT REFERENCES country_codes(code),
    i94res FLOAT REFERENCES country_codes(code),
    i94port VARCHAR REFERENCES port_of_entry(code),
    arrdate FLOAT,
    i94mode FLOAT REFERENCES mode_of_trans(code),
    i94addr VARCHAR REFERENCES address(code),
    depdate FLOAT,
    i94bir FLOAT,
    i94visa FLOAT REFERENCES visa(code),
    count FLOAT,
    dtadfile VARCHAR,
    visapost VARCHAR,
    occup VARCHAR,
    entdepa VARCHAR,
    entdepd VARCHAR,
    entdepu VARCHAR,
    matflag VARCHAR,
    biryear FLOAT,
    dtaddto VARCHAR,
    gender VARCHAR,
    insnum VARCHAR,
    airline VARCHAR,
    admnum FLOAT,
    fltno VARCHAR,
    visatype VARCHAR
);
"""

create_city_demographics = """
CREATE TABLE IF NOT EXISTS city_demographics (
    city VARCHAR,
    state VARCHAR,
    median_age FLOAT,
    male_population INT,
    female_population INT,
    total_population INT,
    number_of_veterans INT,
    foreign_born INT,
    average_household_size FLOAT,
    state_code VARCHAR REFERENCES address(code),
    race VARCHAR,
    count INT
)
DISTSTYLE ALL
"""

create_airport_codes = """
CREATE TABLE IF NOT EXISTS airport_codes (
    ident VARCHAR,
    type VARCHAR,
    name VARCHAR,
    elevation_ft FLOAT,
    continent VARCHAR,
    iso_country VARCHAR,
    iso_region VARCHAR,
    municipality VARCHAR,
    gps_code VARCHAR,
    iata_code VARCHAR,
    local_code VARCHAR,
    coordinates VARCHAR
);
"""

create_country_codes = """
CREATE TABLE IF NOT EXISTS country_codes (
    code FLOAT PRIMARY KEY,
    country VARCHAR
)
DISTSTYLE ALL
"""

create_port_of_entry = """
CREATE TABLE IF NOT EXISTS port_of_entry (
    code VARCHAR PRIMARY KEY,
    port VARCHAR
)
DISTSTYLE ALL
"""

create_mode_of_trans = """
CREATE TABLE IF NOT EXISTS mode_of_trans (
    code FLOAT PRIMARY KEY,
    mode VARCHAR
)
DISTSTYLE ALL
"""

create_address = """
CREATE TABLE IF NOT EXISTS address (
    code VARCHAR PRIMARY KEY,
    addr VARCHAR
)
DISTSTYLE ALL
"""

create_visa = """
CREATE TABLE IF NOT EXISTS visa (
    code FLOAT PRIMARY KEY,
    type VARCHAR
)
DISTSTYLE ALL
"""

drop_table_queries = [drop_table_template.format(table) for table in table_list]
create_table_queries = [create_immigration, create_city_demographics, create_airport_codes, create_country_codes, create_port_of_entry, create_mode_of_trans, create_address, create_visa]