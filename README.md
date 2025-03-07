# Assignment_1: DS_Placement Eligibility App 
!pip install mysql-connector-python faker pandas streamlit
%%writefile config.py
DB_HOST = "localhost" 
DB_USER = "root"
DB_PASSWORD = "vishaakh@2002"
DB_NAME = "student_placement"
import mysql.connector
import config 

try:
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    if connection.is_connected():
        print("Successfully connected to MySQL database")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
%%writefile create_tables.py
import mysql.connector
import config  # Import database credentials from config.py

connection = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
cursor = connection.cursor()

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
    """}
for table_name, query in table_queries.items():
    cursor.execute(query)
    # Commit and close
connection.commit()
cursor.close()
connection.close()
print("Tables created successfully!")

!python create_tables.py

import mysql.connector
import pandas as pd
import config  # Import database credentials

# Connect to MySQL
connection = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
cursor = connection.cursor()
def fetch_data(query):
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
    return df
print(" First 5 students:")
display(fetch_data("SELECT * FROM Students LIMIT 5"))
print("\n First 5 programming records:")
display(fetch_data("SELECT * FROM Programming LIMIT 5"))
print("\n First 5 soft skills records:")
display(fetch_data("SELECT * FROM SoftSkills LIMIT 5"))
print("\n First 5 placement records:")
display(fetch_data("SELECT * FROM Placements LIMIT 5"))
cursor.close()
connection.close()


%%writefile app.py

import streamlit as st
import mysql.connector
import pandas as pd
import config
def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

st.set_page_config(page_title="Student Placement Filter", layout="wide")

page = st.sidebar.radio("Select Page", ["Eligibility Filter", "Placement Insights"])

if page == "Eligibility Filter":
    st.title("Student Placement Eligibility Filter")
    
    # Input criteria
    min_soft_skills = st.slider("Minimum Soft Skills Score", min_value=50, max_value=100, value=70)
    min_problems_solved = st.slider("Minimum Problems Solved", min_value=10, max_value=200, value=50)
    
    # Fetch eligible students
    query = f"""
    SELECT s.student_id, s.name, s.age, s.course_batch, p.problems_solved, 
           ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6, 2) AS avg_soft_skills,
           CASE WHEN p.problems_solved >= {min_problems_solved} 
                AND ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6, 2) >= {min_soft_skills} 
                THEN 'Eligible' ELSE 'Not Eligible' END AS eligibility_status,
           pl.placement_status
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
    JOIN SoftSkills ss ON s.student_id = ss.student_id
    JOIN Placements pl ON s.student_id = pl.student_id
    """
    
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    
    st.dataframe(df)

elif page == "Placement Insights":
    st.title("📊 Placement Insights")
     queries = {
        "Average Placement Package": "SELECT AVG(placement_package) AS avg_package FROM Placements",
        "Top 5 Students by Mock Interview Score": "SELECT s.name, p.mock_interview_score FROM Students s JOIN Placements p ON s.student_id = p.student_id ORDER BY p.mock_interview_score DESC LIMIT 5",
        "Programming Language Popularity": "SELECT language, COUNT(*) AS student_count FROM Programming GROUP BY language ORDER BY student_count DESC",
        "Soft Skills Performance Distribution": "SELECT AVG(communication) AS avg_comm, AVG(teamwork) AS avg_teamwork, AVG(presentation) AS avg_presentation FROM SoftSkills",
        "Internships vs. Placement": "SELECT internships_completed, COUNT(*) AS student_count FROM Placements GROUP BY internships_completed",
        "Top 5 Students by Problems Solved": "SELECT s.name, p.problems_solved FROM Students s JOIN Programming p ON s.student_id = p.student_id ORDER BY p.problems_solved DESC LIMIT 5",
        "Placement Readiness Ratio": "SELECT placement_status, COUNT(*) AS student_count FROM Placements GROUP BY placement_status",
        "Average Interview Rounds Cleared": "SELECT AVG(interview_rounds_cleared) AS avg_rounds FROM Placements",
        "Most Common Graduation Year Among Students": "SELECT graduation_year, COUNT(*) AS count FROM Students GROUP BY graduation_year ORDER BY count DESC LIMIT 1",
        "Top Companies Hiring": "SELECT company_name, COUNT(*) AS student_count FROM Placements GROUP BY company_name ORDER BY student_count DESC LIMIT 5"
    }
    
    selected_query = st.selectbox("Select an Insight", list(queries.keys()))
    
    conn = get_db_connection()
    query = queries[selected_query]
    df = pd.read_sql(query, conn)
    conn.close()
    
    st.subheader(selected_query)
    st.dataframe(df)

    !streamlit run app.py

