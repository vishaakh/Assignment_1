
import streamlit as st
import mysql.connector
import pandas as pd
import config

# Establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

# Streamlit UI
st.set_page_config(page_title="Student Placement Filter", layout="wide")

# Sidebar - Page Selection
page = st.sidebar.radio("Select Page", ["Eligibility Filter", "Placement Insights"])

if page == "Eligibility Filter":
    st.title("📌 Student Placement Eligibility Filter")
    
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
    
    # Dropdown to select a query
    selected_query = st.selectbox("Select an Insight", list(queries.keys()))
    
    # Fetch and display the result for the selected query
    conn = get_db_connection()
    query = queries[selected_query]
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Display the result
    st.subheader(selected_query)
    st.dataframe(df)

    
   
    
   
   
   


    
   


   
       

 
   

        

  
