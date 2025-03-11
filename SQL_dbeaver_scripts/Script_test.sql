-- oppgave 2
--SELECT devices.id, MAX(measurements.ts) AS max_ts, measurements.unit
--FROM devices, measurements
--WHERE category = 'sensor'
--GROUP BY devices.id


-- oppgave 1
SELECT *
FROM rooms r
JOIN devices d ON d.room = r.id
ORDER BY r.id ;


-- oppgave 2
SELECT MAX(measurements.ts) AS max_ts
FROM measurements m
inner JOIN devices d  ON category = sensor
where unit = ''
order by value desc
;


