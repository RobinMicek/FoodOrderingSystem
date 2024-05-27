/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


--
-- EVENTS
--

--
-- TODAY
--
-- Run stats_insertDailyStatsOverall on a schedule
CREATE EVENT event_insertDailyStatsOverall_today
ON SCHEDULE EVERY 30 MINUTE
STARTS DATE(CURRENT_TIMESTAMP)
ON COMPLETION PRESERVE
DO CALL stats_insertDailyStatsOverall(CURDATE());


-- Run stats_insertDailyStatsEstablishments on a schedule
CREATE EVENT event_insertDailyStatsEstablishments_today
ON SCHEDULE EVERY 30 MINUTE
STARTS DATE(CURRENT_TIMESTAMP)
ON COMPLETION PRESERVE
DO CALL stats_insertDailyStatsEstablishments(CURDATE());


--
-- PREVIOUS DAY - Once a day update stats for previous day 
--
-- Run stats_insertDailyStatsOverall on a schedule
CREATE EVENT event_insertDailyStatsOverall_previousDay
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY
ON COMPLETION PRESERVE
DO CALL stats_insertDailyStatsOverall((CURRENT_DATE - INTERVAL 1 DAY));


-- Run stats_insertDailyStatsEstablishments on a schedule
CREATE EVENT event_insertDailyStatsEstablishments_previousDay
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY
ON COMPLETION PRESERVE
DO CALL stats_insertDailyStatsEstablishments((CURRENT_DATE - INTERVAL 1 DAY));