import streamlit as st
import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        st.write(e)
    return conn

# Function to insert a new team member into the database
def add_team_member(conn, team_member):
    sql = ''' INSERT INTO team_members(name, project_management, public_speaking, ppt_story_dev, database_management, coding, deployment, passion, delivery_accountability)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, team_member)
    conn.commit()
    return cur.lastrowid

# Function to fetch all team members from the database
def get_all_team_members(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM team_members")
    rows = cur.fetchall()
    return rows

# Function to create table if it doesn't exist
def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS team_members
                 (id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  project_management TEXT,
                  public_speaking TEXT,
                  ppt_story_dev TEXT,
                  database_management TEXT,
                  coding TEXT,
                  deployment TEXT,
                  passion TEXT,
                  delivery_accountability TEXT)''')
    conn.commit()

# Streamlit UI
st.title("Team Selection App")

# Create a database connection
conn = create_connection("team_selector.db")
create_table(conn)

# Input form for team member details
with st.form("team_member_form"):
    name = st.text_input("Name")
    project_management = st.selectbox("Project Management", ["Novice", "Competent", "Proficient", "Expert"])
    public_speaking = st.selectbox("Public Speaking", ["Novice", "Competent", "Proficient", "Expert"])
    ppt_story_dev = st.selectbox("PPT/Story Development", ["Novice", "Competent", "Proficient", "Expert"])
    database_management = st.selectbox("Database Management", ["Novice", "Competent", "Proficient", "Expert"])
    coding = st.selectbox("Coding", ["Novice", "Competent", "Proficient", "Expert"])
    deployment = st.selectbox("Deployment", ["Novice", "Competent", "Proficient", "Expert"])
    passion = st.selectbox("Passion", ["Coding", "Documentation & Research", "Presentation", "Communication"])
    delivery_accountability = st.selectbox("Delivery Accountability", ["Coding", "Documentation & Research", "Presentation", "Communication"])

    submitted = st.form_submit_button("Add Team Member")

# Handle form submission
if submitted:
    with conn:
        team_member = (name, project_management, public_speaking, ppt_story_dev, database_management, coding, deployment, passion, delivery_accountability)
        team_member_id = add_team_member(conn, team_member)
        st.success(f"Team member {name} added successfully!")

# Display all team members
with conn:
    st.write("All Team Members")
    team_members = get_all_team_members(conn)
    for member in team_members:
        st.write(member)
