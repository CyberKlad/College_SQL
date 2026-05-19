#MySQL query that lists the sID, name, and GPA of every student with a GPA > 3.6
#listed in alphabetical order by name
SELECT sId, sName, GPA
FROM Student
WHERE GPA > 3.6
ORDER BY sName 

#MySQL query that lists the name and majors of every student applying to a major related to biology.
SELECT sId, major
FROM Apply
WHERE major LIKE '%bio%'

#SQL code to increase the enrollment of all colleges except WSU by 1000.
UPDATE College
SET enrollment = enrollment + 1000 
WHERE cName != 'WSU'

#SQL code to create the table
#CollegeStats (cName: VARCHAR(20), appCount: int, minGPA: dec(3,2), maxGPA: dec(3,2)).
#and all columns will not be NULL
CREATE TABLE CollegeStats(
	cName VARCHAR(20) NOT NULL,
	appCount int NOT NULL,
	minGPA dec(3,2) NOT NULL,
	maxGPA dec(3,2) NOT NULL,
	primary key (cName)
);

#SQL code to insert the cNames of the colleges from the College table into CollegeStat along with the appCount,
#minGPA and maxGPA.
INSERT INTO CollegeStats (cName, appCount, minGPA, maxGPA) 
VALUES (
	'Cornell',
	(SELECT COUNT(cName) FROM Apply WHERE cName = 'Cornell'),
	(SELECT MIN(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'Cornell'),
	(SELECT MAX(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'Cornell')
)

INSERT INTO CollegeStats (cName, appCount, minGPA, maxGPA) 
VALUES (
	'MIT',
	(SELECT COUNT(cName) FROM Apply WHERE cName = 'MIT'),
	(SELECT MIN(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'MIT'),
	(SELECT MAX(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'MIT')
)

INSERT INTO CollegeStats (cName, appCount, minGPA, maxGPA) 
VALUES (
	'WSU',
	(SELECT COUNT(cName) FROM Apply WHERE cName = 'WSU'),
	(SELECT MIN(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'WSU'),
	(SELECT MAX(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'WSU')
)

INSERT INTO CollegeStats (cName, appCount, minGPA, maxGPA) 
VALUES (
	'U of O',
	(SELECT COUNT(cName) FROM Apply WHERE cName = 'U of O'),
	(SELECT MIN(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'U of O'),
	(SELECT MAX(Student.GPA) FROM Student JOIN Apply WHERE Apply.cName = 'U of O')
)
