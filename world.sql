CREATE TABLE cities (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
population INTEGER
);

INSERT INTO cities (name, population) VALUES
('New York', 8000000),
('Los Angeles', 4000000),
('Chicago', 2700000);
	
