-- analysis_base: one row per arrival with weather and calendar, built IN SQL.
-- Runs on SQLite and PostgreSQL (CREATE TABLE AS, JOIN, CASE are standard SQL).
--
-- Joins:
--   arrivals --(bpuic)--> stop_station: which stations belong to the stop
--   --(precip_station, weather_hour_utc)--> weather_hourly AS wp: precipitation
--   --(temp_station,   weather_hour_utc)--> weather_hourly AS wt: temperature
--   --(local_date)--> calendar_days: holidays, winter, month
-- weather_hour_utc = scheduled arrival in UTC floored to the hour; MeteoSwiss
-- hourly values carry the END of their interval, so this is the last full hour
-- before the scheduled arrival (decided by ER on 2026-11-03).
-- LEFT JOINs: an arrival without a weather value stays in the table (precip_cat NULL)
-- and is counted in the integration log instead of silently disappearing.

CREATE TABLE analysis_base AS
SELECT
    a.service_date, a.trip_id, a.line, a.category, a.traffic_type, a.extra_trip,
    a.bpuic, s.stop_name,
    a.sched_arr_utc, a.arr_delay_min, a.delayed,
    a.prev_dep_delay_min, a.entry_delay_min, a.delay_gain_min,
    a.weather_hour_utc, a.local_date, a.hour, a.weekday, a.rush_hour,
    ss.precip_station, ss.precip_distance_km, ss.temp_station, ss.temp_distance_km,
    wp.precip_mm,
    wt.temp_c,
    CASE
        WHEN wp.precip_mm IS NULL THEN NULL
        WHEN wp.precip_mm = 0 THEN 'dry'
        WHEN wt.temp_c IS NULL THEN NULL          -- wet, but rain or snow unknown
        WHEN wt.temp_c > 0 THEN 'rain'
        ELSE 'snow'                               -- >= 0.1 mm and <= 0 degC
    END AS precip_cat,
    CASE
        WHEN wp.precip_mm IS NULL THEN NULL
        WHEN wp.precip_mm = 0 THEN 0
        ELSE 1
    END AS precip_any,                            -- main comparison: precipitation vs. dry
    c.public_holiday, c.school_holiday, c.holiday, c.winter, c.month
FROM arrivals AS a
JOIN stops AS s ON s.bpuic = a.bpuic
JOIN stop_station AS ss ON ss.bpuic = a.bpuic
LEFT JOIN weather_hourly AS wp
       ON wp.station_abbr = ss.precip_station AND wp.time_utc = a.weather_hour_utc
LEFT JOIN weather_hourly AS wt
       ON wt.station_abbr = ss.temp_station AND wt.time_utc = a.weather_hour_utc
LEFT JOIN calendar_days AS c ON c.local_date = a.local_date;
