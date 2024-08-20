# libraries
library(RSQLite)
library(DBI)

# connect to the database
connection <- dbConnect(
  drv = SQLite(),
  dbname = "data/unis.sqlite"
)

# fetch results
tbl(connection, "stops") %>%
  collect() -> data

# disconnect
dbDisconnect(connection)

# preview
data