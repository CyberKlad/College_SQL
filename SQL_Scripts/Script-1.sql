CREATE TABLE College(
	cName VARCHAR(20),
	State CHAR(2),
	enrollment MEDIUMINT(5),
	primary key (cName)
);

CREATE TABLE Student(
	sId SMALLINT(4),
	sName VARCHAR(30),
	GPA FLOAT,
	sizeHS SMALLINT(5),
	primary key (sId)
);

CREATE TABLE Major(
	major VARCHAR(30),
	primary key (major)
);

CREATE TABLE MinimumGPA(
	cName VARCHAR(20),
	major VARCHAR(30),
	minGPA FLOAT,
	primary key (cName),
	foreign key (major) references Major(major),
	foreign key (cName) references College(cName)
);

CREATE TABLE Apply(
	sId SMALLINT(4),
	cName VARCHAR(20),
	major VARCHAR(30),
	decision SET('Y', 'N'),
	foreign key (major) references Major(major),
	foreign key (cName) references MinimumGPA(cName),
	foreign key (sId) references Student(sId)
);


