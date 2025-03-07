import mysql.connector
import config  # Import database credentials from config.py

# Connect to MySQL
connection = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
cursor = connection.cursor()

# Creating tables
table_queries = {
    "Students": """
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            gender ENUM('Male', 'Female', 'Other'),
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(10) UNIQUE,
            enrollment_year INT,
            course_batch VARCHAR(20),
            city VARCHAR(100),
             graduation_year INT
        )
    """,
    
    "Programming": """
        CREATE TABLE IF NOT EXISTS Programming (
            programming_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            language VARCHAR(50),
            problems_solved INT,
            assessments_completed INT,
            mini_projects INT,
            certifications_earned INT,
            latest_project_score INT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
        )
    """,
    
    "SoftSkills": """
        CREATE TABLE IF NOT EXISTS SoftSkills (
            soft_skill_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            communication INT CHECK(communication BETWEEN 0 AND 100),
            teamwork INT CHECK(teamwork BETWEEN 0 AND 100),
            presentation INT CHECK(presentation BETWEEN 0 AND 100),
            leadership INT CHECK(leadership BETWEEN 0 AND 100),
             critical_thinking INT CHECK(critical_thinking BETWEEN 0 AND 100),
            interpersonal_skills INT CHECK(interpersonal_skills BETWEEN 0 AND 100),
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
        )
    """,
    
    "Placements": """
        CREATE TABLE IF NOT EXISTS Placements (
            placement_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            mock_interview_score INT CHECK(mock_interview_score BETWEEN 0 AND 100),
            internships_completed INT,
            placement_status ENUM('Ready', 'Not Ready', 'Placed'),
            company_name VARCHAR(255),
            placement_package DECIMAL(10,2),
            interview_rounds_cleared INT,
            placement_date DATE,
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
        )
    """
}

# Execute queries
for table_name, query in table_queries.items():
    cursor.execute(query)
    # Commit and close
connection.commit()
cursor.close()
connection.close()

print("Tables created successfully!")
    
