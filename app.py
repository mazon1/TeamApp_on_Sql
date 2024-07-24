import streamlit as st
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('team_members.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS team_members
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, project_management TEXT, public_speaking TEXT, ppt_development TEXT, database_management TEXT, coding TEXT, deployment TEXT, passion TEXT, recommended_role TEXT)''')
conn.commit()

def save_to_db(data):
    with conn:
        c.execute('''INSERT INTO team_members (name, project_management, public_speaking, ppt_development, database_management, coding, deployment, passion, recommended_role)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                     (data['name'], data['project_management'], data['public_speaking'], data['ppt_development'], data['database_management'], data['coding'], data['deployment'], data['passion'], data['recommended_role']))

st.title("Team Selection App")

# Load and display the logo
st.image("teamselectorapp.jpg", width=100)

# Input fields
name = st.text_input("Name")
project_management = st.selectbox("Project Management", ["Novice", "Competent", "Proficient", "Expert"])
public_speaking = st.selectbox("Public Speaking", ["Novice", "Competent", "Proficient", "Expert"])
ppt_development = st.selectbox("PPT/Story Development", ["Novice", "Competent", "Proficient", "Expert"])
database_management = st.selectbox("Database Management", ["Novice", "Competent", "Proficient", "Expert"])
coding = st.selectbox("Coding", ["Novice", "Competent", "Proficient", "Expert"])
deployment = st.selectbox("Deployment", ["Novice", "Competent", "Proficient", "Expert"])
passion = st.selectbox("Passion", ["Coding", "Documentation & Research", "Presentation & Communication"])

# Function to recommend role based on inputs
def recommend_role(data):
    if data["coding"] == "Expert":
        return "Lead Developer"
    elif data["project_management"] == "Expert":
        return "Lead Project Manager"
    elif data["ppt_development"] == "Expert":
        return "Lead Presenter"
    elif data["public_speaking"] == "Expert":
        return "Lead Speaker"
    elif data["database_management"] == "Expert":
        return "Lead Database Manager"
    elif data["deployment"] == "Expert":
        return "Lead Deployment Specialist"
    else:
        return data["passion"]

# Button to save input and recommend role
if st.button("Submit"):
    data = {
        "name": name,
        "project_management": project_management,
        "public_speaking": public_speaking,
        "ppt_development": ppt_development,
        "database_management": database_management,
        "coding": coding,
        "deployment": deployment,
        "passion": passion,
    }
    recommended_role = recommend_role(data)
    data["recommended_role"] = recommended_role
    save_to_db(data)
    st.success(f"Data saved! Recommended Role: {recommended_role}")

# Button to recommend lead role
if st.button("Recommend Lead Role"):
    data = {
        "project_management": project_management,
        "public_speaking": public_speaking,
        "ppt_development": ppt_development,
        "database_management": database_management,
        "coding": coding,
        "deployment": deployment,
        "passion": passion,
    }
    recommended_role = recommend_role(data)
    st.write(f"Recommended Lead Role: {recommended_role}")

# Display all team members
st.subheader("All Team Members")
with conn:
    c.execute("SELECT * FROM team_members")
    rows = c.fetchall()
    for row in rows:
        st.write(row)
