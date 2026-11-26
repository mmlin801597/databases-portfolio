-- Run after setup.sql in a fresh database.
DROP TRIGGER trg_vib_alarm;
CREATE TRIGGER trg_vib_alarm
BEFORE INSERT ON reading
FOR EACH ROW
WHEN NEW.value > 2.0
  AND (SELECT metric FROM sensor WHERE sensor_id = NEW.sensor_id) = 'vib_rms'
BEGIN
    INSERT INTO alarm(sensor_id, ts, value, reason)
    VALUES (NEW.sensor_id, NEW.ts, NEW.value, 'vibration over 2.0 mm/s');
END;

INSERT INTO reading(sensor_id, ts, value, interval_s)
VALUES (2, '2026-05-01 00:00:00', 3.5, 1);
SELECT reading_id, sensor_id, ts, value FROM reading;
SELECT alarm_id, sensor_id, ts, value, reason FROM alarm;
