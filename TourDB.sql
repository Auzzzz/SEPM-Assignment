
CREATE TABLE locations (
    LocationID      VARCHAR(8),
    LocationName    VARCHAR(30),
    Duration        DOUBLE(2,2),
    Description     TEXT,
    CONSTRAINT pk_locations PRIMARY KEY (LocationID),
);

CREATE TABLE assisstants (
    AssisstantID    VARCHAR(8),
    FirstName       CHAR(16),
    LastName        CHAR(16),
    CONSTRAINT pk_assisst PRIMARY KEY (AssisstantID),
);

CREATE TABLE tours (
    TourID          VARCHAR(8),
    TourName        VARCHAR(30),
    TourDescrip     TEXT,
    AssisstantID    VARCHAR(8),
    CONSTRAINT pk_tours PRIMARY KEY (TourID),
    CONSTRAINT fk_tours FOREIGN KEY (AssisstantID)
    REFERENCES assisstant (AssisstantID)
);

CREATE TABLE tour_locations (
    LocationID      VARCHAR(8),
    TourID          VARCHAR(8),
    CONSTRAINT pk_tl PRIMARY KEY (LocationID, TourID),
    CONSTRAINT fk_tl1 FOREIGN KEY (LocationID)
    REFERENCES locations (LocationID),
    CONSTRAINT fk_tl2 FOREIGN KEY (TourID)
    REFERENCES tours (TourID)    
);