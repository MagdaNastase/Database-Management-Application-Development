CREATE DATABASE bazadedate;
USE bazadedate;


CREATE TABLE Sculptures (
    SculptureID INT AUTO_INCREMENT PRIMARY KEY,
    Titlu VARCHAR(150) NOT NULL,
    Material VARCHAR(100),
    Inaltime DECIMAL(5,2), 
    Greutate DECIMAL(6,2),
    AnCreatie INT,
    LocatieMuzeu VARCHAR(100) 
);


CREATE TABLE Sculptors (
    SculptorID INT AUTO_INCREMENT PRIMARY KEY,
    Nume VARCHAR(100) NOT NULL, 
    Prenume VARCHAR(100) NOT NULL, 
    AnNastere INT,
    AnDeces INT, -- Dacă sculptorul este decedat, altfel NULL
    Nationalitate VARCHAR(50),
    StilArtistic VARCHAR(100) 
);

CREATE TABLE Sculpture_Sculptor (
    SculptureID INT,
    SculptorID INT,
    PRIMARY KEY (SculptureID, SculptorID),
    FOREIGN KEY (SculptureID) REFERENCES Sculptures(SculptureID) ON DELETE CASCADE,
    FOREIGN KEY (SculptorID) REFERENCES Sculptors(SculptorID) ON DELETE CASCADE
);



INSERT INTO Sculptures (Titlu, Material, Inaltime, Greutate, AnCreatie, LocatieMuzeu)
VALUES
('David', 'Marmură', 5.17, 6000.00, 1504, 'Galleria dell\'Accademia, Florența'),
('Gânditorul', 'Bronz', 1.89, 700.50, 1904, 'Musée Rodin, Paris'),
('Pietà', 'Marmură', 1.74, 2500.00, 1499, 'Bazilica Sfântul Petru, Vatican'),
('Coloana Infinitului', 'Oțel', 29.33, 9000.00, 1938, 'Târgu Jiu, România');


INSERT INTO Sculptors (Nume, Prenume, AnNastere, AnDeces, Nationalitate, StilArtistic)
VALUES
('Michelangelo', 'Buonarroti', 1475, 1564, 'Italian', 'Renaștere'),
('Auguste', 'Rodin', 1840, 1917, 'Francez', 'Modern'),
('Constantin', 'Brâncuși', 1876, 1957, 'Român', 'Avangardist'),
('Antonio', 'Canova', 1757, 1822, 'Italian', 'Neoclasic');

INSERT INTO Sculpture_Sculptor (SculptureID, SculptorID)
VALUES
(1, 1), -- Michelangelo - David
(2, 2), -- Rodin - Gânditorul
(3, 1), -- Michelangelo - Pietà
(4, 3); -- Brâncuși - Coloana Infinitului


SHOW TABLES;
SELECT * FROM Sculptures;
SELECT * FROM Sculptors;
SELECT * FROM Sculpture_Sculptor;
DESCRIBE Sculptors;
DESCRIBE Sculptures;
DESCRIBE Sculpture_Sculptor;




DROP TABLE IF EXISTS Sculpture_Sculptor;
DROP TABLE IF EXISTS Sculptures;
DROP TABLE IF EXISTS Sculptors;


