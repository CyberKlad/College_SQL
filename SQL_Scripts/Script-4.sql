SELECT AVG(budget)
FROM movies;

SELECT title, GROUP_CONCAT(name SEPARATOR ', ')
FROM
(
	(
	SELECT movies.id, movies.title
	FROM movies JOIN pcountry_movie_relation
	ON movies.id=pcountry_movie_relation.m_id
	WHERE pcountry_movie_relation.pcountry_iso='US'
	) AS table1
	JOIN
	(
	SELECT pcompany_movie_relation.m_id, production_companies.name
	FROM pcompany_movie_relation JOIN production_companies
	ON pcompany_movie_relation.pcompany_id=production_companies.id
	) AS table2
	ON table1.id=table2.m_id
)
GROUP BY title;

SELECT title, revenue
FROM

SELECT title, revenue
FROM movies
ORDER BY revenue DESC
LIMIT 5;

SELECT title, GROUP_CONCAT(name SEPARATOR ', ')
FROM (genres
JOIN
(SELECT title, g_id
FROM movies
JOIN
(SELECT table2.m_id, g_id
FROM g_movie_relation
JOIN
((SELECT m_id
FROM g_movie_relation
JOIN
(SELECT id
FROM genres
WHERE genres.name='Science Fiction') AS table0
ON g_movie_relation.g_id=table0.id)
INTERSECT
(SELECT m_id
FROM g_movie_relation
JOIN
(SELECT id
FROM genres
WHERE genres.name='Mystery') AS table1
ON g_movie_relation.g_id=table1.id)) AS table2
ON table2.m_id=g_movie_relation.m_id) AS table3
ON table3.m_id=movies.id) AS table4
ON table4.g_id=genres.id)
GROUP BY title;



((SELECT m_id
FROM g_movie_relation
JOIN
(SELECT id
FROM genres
WHERE genres.name='Science Fiction') AS table0
ON g_movie_relation.g_id=table0.id)
INTERSECT
(SELECT m_id
FROM g_movie_relation
JOIN
(SELECT id
FROM genres
WHERE genres.name='Mystery') AS table1
ON g_movie_relation.g_id=table1.id))


SELECT title, popularity
FROM movies
WHERE movies.popularity>(
SELECT AVG(popularity)
FROM movies
)
