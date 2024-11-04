import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from collections import Counter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
#credentials = ServiceAccountCredentials.from_json_keyfile_name("/workspaces/thanks/thanks-vote-440718-8020ffdbe27a.json", scope)
credentials_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
client = gspread.authorize(credentials)

# Open the Google Sheet (replace with your own Google Sheet ID)
sheet = client.open_by_key("1_0Xil-STpEyo5MdYz7Lz4g1Qyay51y-neSDvpZBgOgY").sheet1

# List of dinner packages and their details
dinner_packages = [
    "Traditional Turkey Dinner",
    "Traditional Turkey Breast Dinner",
    "Orange Glazed Spiral Cut Ham Dinner",
    "Boneless Ribeye Roast Dinner",
    "Braised Brisket Dinner",
    "Beef Wellington Dinner"
]

# Dictionary of dinner package details, including sides, pie options, and image URLs
dinner_info = {
    "Traditional Turkey Dinner": {
        "Potatoes": "Mashed",
        "Green Beans Almondine": "✓",
        "Dinner Rolls": "✓",
        "Herb Stuffing": "✓",
        "Candied Yams": "✓",
        "Roasted Root Vegetables": "",
        "Cranberry Relish": "✓",
        "Turkey Gravy": "✓",
        "Brisket Sauce": "",
        "Creamed Horseradish": "",
        "Pie": "Pumpkin or Apple",
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/7419baea05bf4b85adc4354a85aef957_540w.jpg"
    },
    "Traditional Turkey Breast Dinner": {
        "Potatoes": "Mashed",
        "Green Beans Almondine": "✓",
        "Dinner Rolls": "✓",
        "Herb Stuffing": "✓",
        "Candied Yams": "✓",
        "Roasted Root Vegetables": "",
        "Cranberry Relish": "✓",
        "Turkey Gravy": "✓",
        "Brisket Sauce": "",
        "Creamed Horseradish": "",
        "Pie": "Pumpkin or Apple",
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/f3a68ba6ec4343988983f697da3aa2a8_540w.jpg"
    },
    "Orange Glazed Spiral Cut Ham Dinner": {
        "Potatoes": "Scalloped",
        "Green Beans Almondine": "✓",
        "Dinner Rolls": "✓",
        "Herb Stuffing": "",
        "Candied Yams": "✓",
        "Roasted Root Vegetables": "",
        "Cranberry Relish": "✓",
        "Turkey Gravy": "",
        "Brisket Sauce": "",
        "Creamed Horseradish": "",
        "Pie": "Pumpkin or Apple",
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/077cf99592614a4f9cf18c5a38202896_540w.jpg"
    },
    "Boneless Ribeye Roast Dinner": {
        "Potatoes": "Scalloped",
        "Green Beans Almondine": "✓",
        "Dinner Rolls": "✓",
        "Herb Stuffing": "",
        "Candied Yams": "",
        "Roasted Root Vegetables": "",
        "Cranberry Relish": "",
        "Turkey Gravy": "",
        "Brisket Sauce": "",
        "Creamed Horseradish": "✓",
        "Pie": "Apple",
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/7315c3ac09694746ab1ac1f485784a35_540w.jpg"
    },
    "Braised Brisket Dinner": {
        "Potatoes": "Latkes",
        "Green Beans Almondine": "✓",
        "Dinner Rolls": "✓",
        "Herb Stuffing": "",
        "Candied Yams": "",
        "Roasted Root Vegetables": "✓",
        "Cranberry Relish": "",
        "Turkey Gravy": "",
        "Brisket Sauce": "✓",
        "Creamed Horseradish": "",
        "Pie": "Caramel Apple",
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/b815f8ce6c474441ada34503f63fd3f6_540w.jpg"
    },
    "Beef Wellington Dinner": {
        "Potatoes": "Scalloped",
        "Green Beans Almondine": "✓",
        "Dinner Rolls": "✓",
        "Herb Stuffing": "",
        "Candied Yams": "",
        "Roasted Root Vegetables": "",
        "Cranberry Relish": "",
        "Turkey Gravy": "",
        "Brisket Sauce": "",
        "Creamed Horseradish": "",
        "Pie": "Apple",
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/9d03a461727e4fa6a21858b15873fcea_540w.jpg"
    }
}

# Convert dinner info to a DataFrame for easy display
dinner_df = pd.DataFrame(dinner_info).T

# header image
st.image("/workspaces/thanks/turkey-vote.webp")


# Display the table with sides and images
st.title("Holiday Dinner Package Comparison")
st.write("Compare dinner packages by sides and see an image of each option.")
st.dataframe(dinner_df.drop(columns=["Image URL"]),use_container_width=True)  # Display the data without image URLs

# Display images and titles in two columns
st.header("Dinner Packages with Images")
cols = st.columns(2)  # Create two columns

for idx, (dinner, details) in enumerate(dinner_info.items()):
    with cols[idx % 2]:  # Alternate columns
        st.subheader(dinner)
        st.image(details["Image URL"], caption=dinner, width=150)  # Set image width to 150 pixels


# Function to store votes in Google Sheets
def store_vote(vote):
    sheet.append_row(vote)


# Voting section with improved instructions
st.header("Rank Your Top Three Choices")
st.write("Select exactly three dinner packages in order of preference and submit your vote.")

if "has_voted" not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    choices = st.multiselect("Select your top three dinner packages:", dinner_packages)

    if len(choices) == 3:
        if st.button("Submit Vote"):
            store_vote(choices)  # Store the vote in Google Sheets
            st.session_state.has_voted = True
            st.success("Your vote has been submitted!")
    elif len(choices) > 3:
        st.warning("Please select exactly three options.")
else:
    st.info("You have already voted. Thank you for participating!")
    st.image("/workspaces/thanks/voting wrong.png", caption="We hope your voting experience was satisfactory!")

# Calculate results from Google Sheets data
def calculate_votes():
    votes = sheet.get_all_records()  # Retrieve all votes from the sheet
    ranked_votes = [[vote["First Vote"], vote["Second Vote"], vote["Third Vote"]] for vote in votes]
    return stv_winner(ranked_votes, dinner_packages)

def stv_winner(ranked_votes, candidates):
    active_candidates = set(candidates)
    
    while True:
        counts = Counter(vote[0] for vote in ranked_votes if vote[0] in active_candidates)
        total_votes = sum(counts.values())
        
        for candidate, count in counts.items():
            if count > total_votes / 2:
                return candidate  # Winner found

        min_candidate = min(counts, key=counts.get)
        active_candidates.remove(min_candidate)
        
        new_ranked_votes = []
        for vote in ranked_votes:
            new_vote = [c for c in vote if c in active_candidates]
            if new_vote:
                new_ranked_votes.append(new_vote)
        
        ranked_votes = new_ranked_votes
        
        if len(active_candidates) == 1:
            return list(active_candidates)[0]

if st.button("Calculate Winner"):
    if sheet.row_count > 1:  # Check if any votes have been cast
        winner = calculate_votes()
        st.success(f"The winning dinner package is: {winner}")
        
        # Display first-choice votes for each candidate
        votes = sheet.get_all_records()
        all_votes = [vote["First Vote"] for vote in votes]
        first_choice_counts = Counter(all_votes)
        
        results_df = pd.DataFrame.from_dict(first_choice_counts, orient='index', columns=["Votes"])
        results_df = results_df.reindex(dinner_packages).fillna(0).infer_objects(copy=False)
        
        st.bar_chart(results_df)
        st.write(f"Total Votes Cast: {len(votes)}")
    else:
        st.warning("No votes have been cast yet.")

# STV Explanation Display
st.title("Single Transferable Vote (STV): Dinner Edition")
st.write("Wondering how we pick the winning feast? Here's the STV magic in bite-sized steps:")

st.markdown("""
1. **Count the Faves**: We start with everyone's top pick.
2. **Check for a Winner**: If any dish has over half the votes, congrats—it’s dinner!
3. **Last Place Gets Chopped**: If no one wins, we cut the least popular dish and give those votes to the next favorite.
4. **Repeat as Needed**: Keep chopping until we have a delicious majority!
""")

