-- setup
.headers on
.mode csv


-- statewide line chart stops by race by year
.output viz/statewide_race_by_year.csv
select year, driver_race, count(*) 
from stops 
group by year, driver_race 
order by year, driver_race;

-- chicago line chart stops by race by year
select year, driver_race, count(*) 
from stops 
where AgencyName = 'CHICAGO POLICE' 
group by year, driver_race 
order by year, driver_race;


-- cpd beat map 2022
.output viz/cpd_beat_stop_counts_2022.csv
select substr('000' || BeatLocationOfStop,-4,4) dist_beat, count(*) 
from stops 
where AgencyName = 'CHICAGO POLICE' 
and year = 2022 
group by dist_beat;

-- cpd district map 2016-2022
.output viz/cpd_beat_stop_counts_2022.csv
select substr(BeatLocationOfStop,-4,4) dist_beat, count(*) 
from stops 
where AgencyName = 'CHICAGO POLICE' 
and year > 2016
group by dist_beat;

-- outcomes by race

