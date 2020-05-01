### Business Case
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. 

### Objectives
- Model data with PostgreSQL
- Build the ETL pipelines with Python
- Build schemas using star schema with fact and dimension tables
- Implement full CRUD functionality

### Schema Design
#### Fact Table
I created the fact table song plays 

#### Dimension tables
**users**: user data of the Sparkify users
**songs**: songs, titles, year, duration, and id's
**artists**: name and location
**time**: timestamp broken down in various time units

### Database and Pipeline Design
The schema design following the star schema is very well suited for the data necessary for this project.
The number of tables is fairly limited and this makes for easy querying and occasional joins of denormalized tables.
The joins are never very complicated and therefore performant.

The pipeline design is pretty straight forward as song and log JSON data is read into Pandas, transformed where necessary and stored in PostgreSQL.

