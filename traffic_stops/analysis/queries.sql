-- search hit rate by race
select s.driver_race, s.c, h.c, cast(h.c as float)/s.c rate from (select driver_race, count(*) c from stops_stop where search_conducted =1 group by driver_race) s join (select driver_race, count(*) c from stops_stop where search_conducted = 1 and search_hit = 1 group by driver_race) h on s.driver_race = h.driver_race;

-- consent search hit rate by race
select s.driver_race, s.c, h.c, cast(h.c as float)/s.c rate from (select driver_race, count(*) c from stops_stop where consent_search_conducted =1 group by driver_race) s join (select driver_race, count(*) c from stops_stop where consent_search_conducted = 1 and search_hit = 1 group by driver_race) h on s.driver_race = h.driver_race;


