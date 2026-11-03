-- Database schema of the project (runs on SQLite and PostgreSQL).
-- Portable SQL only: standard types, no database-specific functions.
-- All times are text 'YYYY-MM-DD HH:MM:SS' in UTC; local dates are 'YYYY-MM-DD'.
-- Executed by src/build_db.py (statements separated by semicolons).

-- Train stops in the study area (canton ZH), from the service point directory
CREATE TABLE IF NOT EXISTS stops (
    bpuic        TEXT PRIMARY KEY,      -- 7-digit stop number = Ist-Daten BPUIC
    stop_name    TEXT,
    canton       TEXT,
    lv95_east    DOUBLE PRECISION,      -- Swiss coordinates (EPSG:2056), metres
    lv95_north   DOUBLE PRECISION,
    height_masl  DOUBLE PRECISION
);

-- Weather stations actually used (SMN and precipitation network)
CREATE TABLE IF NOT EXISTS weather_stations (
    station_abbr   TEXT PRIMARY KEY,    -- e.g. SMA = Zurich / Fluntern
    station_name   TEXT,
    station_canton TEXT,
    height_masl    DOUBLE PRECISION,
    lv95_east      DOUBLE PRECISION,
    lv95_north     DOUBLE PRECISION,
    network        TEXT                 -- 'smn' or 'precip'
);

-- Which station delivers precipitation and temperature for each stop
CREATE TABLE IF NOT EXISTS stop_station (
    bpuic                TEXT PRIMARY KEY REFERENCES stops (bpuic),
    precip_station       TEXT REFERENCES weather_stations (station_abbr),
    precip_distance_km   DOUBLE PRECISION,
    precip_height_diff_m DOUBLE PRECISION,
    temp_station         TEXT REFERENCES weather_stations (station_abbr),
    temp_distance_km     DOUBLE PRECISION,
    temp_height_diff_m   DOUBLE PRECISION
);

-- Hourly weather per station; time_utc = END of the hourly interval (MeteoSwiss)
CREATE TABLE IF NOT EXISTS weather_hourly (
    station_abbr TEXT REFERENCES weather_stations (station_abbr),
    time_utc     TEXT,
    precip_mm    DOUBLE PRECISION,
    temp_c       DOUBLE PRECISION,
    snow_cm      DOUBLE PRECISION,
    PRIMARY KEY (station_abbr, time_utc)
);

-- One row per local date of the study period
CREATE TABLE IF NOT EXISTS calendar_days (
    local_date     TEXT PRIMARY KEY,
    weekday        INTEGER,             -- 0 = Monday
    public_holiday INTEGER,
    school_holiday INTEGER,
    holiday        INTEGER,
    winter         TEXT,                -- e.g. '2025/26'
    month          INTEGER
);

-- One row per train arrival at a study-area stop (after the filters in src/arrivals.py)
CREATE TABLE IF NOT EXISTS arrivals (
    service_date       TEXT,            -- operating day (BETRIEBSTAG)
    trip_id            TEXT,            -- FAHRT_BEZEICHNER
    operator           TEXT,
    line               TEXT,
    category           TEXT,            -- S, IC, IR, RE, EC, ...
    traffic_type       TEXT,            -- 'regional' or 'long_distance'
    extra_trip         INTEGER,
    bpuic              TEXT REFERENCES stops (bpuic),
    sched_arr_utc      TEXT,
    act_arr_utc        TEXT,
    arr_delay_min      DOUBLE PRECISION,
    delayed            INTEGER,         -- target: arrival delay >= 3 min
    prev_dep_delay_min DOUBLE PRECISION, -- known before arrival
    entry_delay_min    DOUBLE PRECISION, -- departure delay at the last stop before the study area
    entry_from_bpuic   TEXT,             -- that stop (outside the study area)
    entry_from_time_utc TEXT,            -- its scheduled departure (always before this arrival)
    delay_gain_min     DOUBLE PRECISION, -- OUTCOME, not a feature
    weather_hour_utc   TEXT,            -- join key to weather_hourly.time_utc
    local_date         TEXT,            -- join key to calendar_days
    hour               INTEGER,
    weekday            INTEGER,
    rush_hour          INTEGER
);
CREATE INDEX IF NOT EXISTS idx_arrivals_date ON arrivals (service_date);
CREATE INDEX IF NOT EXISTS idx_arrivals_stop_hour ON arrivals (bpuic, weather_hour_utc);
