# Module04 — Task 5: Break Your Own Alarm

## BEFORE INSERT Experiment

I changed the vibration alarm trigger from `AFTER INSERT` to `BEFORE INSERT`.

I inserted a vibration reading with a value of **3.5 mm/s**. The alarm trigger created an alarm successfully.

The main difference is the timing. With `BEFORE INSERT`, the trigger runs before the new reading is completed, while `AFTER INSERT` runs after the reading has been inserted.

For this alarm, `AFTER INSERT` is the better default because the alarm is a consequence of a reading that has already been successfully stored. It also makes the trigger easier to understand: first save the measurement, then create the alarm based on that stored measurement.