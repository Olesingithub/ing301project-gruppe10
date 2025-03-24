-- oppgave 2
--SELECT devices.id, MAX(measurements.ts) AS max_ts, measurements.unit
--FROM devices, measurements
--WHERE category = 'sensor'
--GROUP BY devices.id


-- oppgave 1
/*SELECT *
FROM rooms r
JOIN devices d ON d.room = r.id
ORDER BY r.id ;*/


/*-- oppgave 2
SELECT MAX(measurements.ts) AS max_ts
FROM measurements m
inner JOIN devices d  ON category = sensor
where unit = ''
order by value desc
;*/


-- oppgave 2
--SELECT devices.id, MAX(measurements.ts) AS max_ts, measurements.unit
--FROM devices, measurements
--WHERE category = 'sensor'
--GROUP BY devices.id


-- oppgave 1
--SELECT * FROM rooms r JOIN devices d ON d.room = r.id ORDER BY r.id ;


-- oppgave 2
/*SELECT MAX(measurements.ts) AS max_ts
FROM measurements m
inner JOIN devices d  ON category = sensor
where unit = ''
order by value desc
;*/


/*SELECT value
FROM measurements m
inner JOIN sensors ON id = sensor 
where  = 'speed'
order by value desc
limit 1;*/

/*SELECT 
d.kind ,
min(m.value), 
max(m.value),
avg(m.value),
count(distinct m.value)
FROM devices d
inner JOIN measurements m ON id = m.device
group by d.room;*/

/*SELECT *,
MAX(m.ts)
FROM devices d, measurements m
where d.id = 'cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5'*/

SELECT *, max(m.ts) FROM devices d, measurements m WHERE d.id = 'cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5' -- motion sensor
--SELECT *, max(m.ts) FROM devices d, measurements m WHERE d.id = 'a2f8690f-2b3a-43cd-90b8-9deea98b42a7' -- no data
--SELECT *, max(m.ts) FROM devices d, measurements m WHERE d.id = '3d87e5c0-8716-4b0b-9c67-087eaaed7b45' -- humidity

--SELECT *
--From measurements m 
--Group by m.device

SELECT *, MAX(m.ts)
FROM devices d, measurements m
WHERE d.id = '3d87e5c0-8716-4b0b-9c67-087eaaed7b45'