import streamlit as st
import pandas as pd
from datetime import datetime

# Placeholder data for cricket fields and organizers
fields = ["Ground 1", "Ground 2", "Ground 3", "Ground 4"]
organizers = ["Organizer A", "Organizer B", "Organizer C", "Organizer D"]

# DataFrame to hold tournament bookings
tournaments_df = pd.DataFrame(columns=["Tournament Name", "Organizer", "Field", "Date", "Time", "Teams"])

# Sidebar for navigation
st.sidebar.title("Gully Cricket Board")
menu = st.sidebar.radio("Menu", ["🏠 Home", "📝 Organize Tournament", "📝 Register Team", "📅 View Tournaments"])

# Home Page
if menu == "🏠 Home":
    st.title("Welcome to Gully Cricket Board")
    st.write("""
    Manage and view all cricket tournaments happening every Friday in Kuwait.  
    - **Organizers** can book fields and schedule tournaments.  
    - **Teams** can register for tournaments.  
    - **Viewers** can view upcoming matches in list and calendar formats.  
    """)

# Organize Tournament Page
elif menu == "📝 Organize Tournament":
    st.title("Organize a New Tournament")

    with st.form("tournament_form"):
        tournament_name = st.text_input("Tournament Name")
        organizer_name = st.selectbox("Organizer Name", organizers)
        field = st.selectbox("Select Cricket Ground", fields)
        date = st.date_input("Tournament Date")
        time = st.time_input("Start Time")
        teams = st.text_area("Enter Team Names (comma-separated)")

        submitted = st.form_submit_button("Submit")
        if submitted:
            new_tournament = {
                "Tournament Name": tournament_name,
                "Organizer": organizer_name,
                "Field": field,
                "Date": str(date),
                "Time": str(time),
                "Teams": teams.split(",")
            }
            global tournaments_df
            tournaments_df = tournaments_df.append(new_tournament, ignore_index=True)
            st.success(f"Tournament '{tournament_name}' organized successfully!")

# Register Team Page
elif menu == "📝 Register Team":
    st.title("Register for a Tournament")
    if tournaments_df.empty:
        st.write("No tournaments available for registration.")
    else:
        selected_tournament = st.selectbox("Select a Tournament", tournaments_df["Tournament Name"].unique())
        team_name = st.text_input("Team Name")
        if st.button("Register Team"):
            index = tournaments_df[tournaments_df["Tournament Name"] == selected_tournament].index[0]
            tournaments_df.at[index, "Teams"].append(team_name)
            st.success(f"Team '{team_name}' has been registered for '{selected_tournament}'.")

# View Tournaments Page
elif menu == "📅 View Tournaments":
    st.title("View Tournaments")
    if tournaments_df.empty:
        st.write("No tournaments scheduled.")
    else:
        view_type = st.radio("View Type", ["List View", "Calendar View"])
        if view_type == "List View":
            st.write(tournaments_df)
        else:
            for _, row in tournaments_df.iterrows():
                st.markdown(f"### {row['Tournament Name']}")
                st.write(f"**Organizer:** {row['Organizer']}")
                st.write(f"**Field:** {row['Field']}")
                st.write(f"**Date:** {row['Date']}")
                st.write(f"**Time:** {row['Time']}")
                st.write(f"**Teams Registered:** {', '.join(row['Teams'])}")
                st.markdown("---")
