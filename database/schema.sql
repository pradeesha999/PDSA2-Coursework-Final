CREATE DATABASE IF NOT EXISTS puzzle;
USE puzzle;

-- Players table
CREATE TABLE players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Solutions table
CREATE TABLE solutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    board_state VARCHAR(64) NOT NULL,
    is_found BOOLEAN DEFAULT FALSE,
    found_by INT,
    found_at TIMESTAMP NULL,
    FOREIGN KEY (found_by) REFERENCES players(id)
);

-- Performance metrics
CREATE TABLE performance_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    algorithm_type ENUM('sequential', 'threaded'),
    execution_time DECIMAL(10,4),
    total_solutions INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test solutions table
CREATE TABLE IF NOT EXISTS test_solutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    solution TEXT NOT NULL,
    is_valid BOOLEAN NOT NULL DEFAULT TRUE
);

-- Optional: Insert sample data for testing
INSERT INTO test_solutions (solution, is_valid) VALUES
('Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8', TRUE),
('Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8', FALSE);