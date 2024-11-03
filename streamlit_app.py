import streamlit as st
from collections import Counter
import pandas as pd

# List of dinner packages
dinner_packages = [
    "Traditional Turkey Dinner",
    "Traditional Turkey Breast Dinner",
    "Orange Glazed Spiral Cut Ham Dinner",
    "Boneless Ribeye Roast Dinner",
    "Braised Brisket Dinner",
    "Beef Wellington Dinner"
]

# Information about each dinner package
dinner_info = {
    "Traditional Turkey Dinner": {
        "description": "Mashed potatoes, herb stuffing, candied yams, green beans almondine, turkey gravy, cranberry relish, choice of pie.",
        "image_url": "https://catering.ajsfinefoods.com/images/Traditional_Turkey_Dinner.jpg"
    },
    "Traditional Turkey Breast Dinner": {
        "description": "Mashed potatoes, herb stuffing, candied yams, green beans almondine, turkey gravy, cranberry relish, choice of pie.",
        "image_url": "https://catering.ajsfinefoods.com/images/Traditional_Turkey_Breast_Dinner.jpg"
    },
    "Orange Glazed Spiral Cut Ham Dinner": {
        "description": "Scalloped potatoes, candied yams, green beans almondine, cranberry relish, choice of pie.",
        "image_url": "https://catering.ajsfinefoods.com/images/Orange_Glazed_Spiral_Cut_Ham_Dinner.jpg"
    },
    "Boneless Ribeye Roast Dinner": {
        "description": "Scalloped potatoes, green beans almondine, creamed horseradish, apple pie.",
        "image_url": "https://catering.ajsfinefoods.com/images/Boneless_Ribeye_Roast_Dinner.jpg"
    },
    "Braised Brisket Dinner": {
        "description": "Potato latkes, roasted root vegetables, green beans almondine, brisket sauce, caramel apple pie.",
        "image_url": "https://catering.ajsfinefoods.com/images/Braised_Brisket_Dinner.jpg"
    },
    "Beef Wellington Dinner": {
        "description": "Scalloped potatoes, green beans almondine, apple pie.",
        "image_url": "https://catering.ajsfinefoods.com/images/Beef_Wellington_Dinner.jpg"
    }
}

# Display dinner options
st.title("Holiday Dinner Package Selection")
st.write("Learn about each dinner package and rank your top three choices!")

for dinner, details in dinner_info.items():
    st.subheader(dinner)
    st.write(details["description"])
    st.image(details["image_url"], use_column_width=True)

# Check if the user has already voted
if "has_voted" not in st.session_state:
    st.session_state.has_voted = False
if "votes" not in st.session_state:
    st.session_state.votes = []

# Ballot section
st.header("Rank Your Top Three Choices")
if not st.session_state.has_voted:
    choices = st.multiselect("Select your top three dinner packages in order of preference:", dinner_packages, [])

    # Ensure exactly three choices
    if len(choices) == 3:
        if st.button("Submit Vote"):
            st.session_state.votes.append(choices)
            st.session_state.has_voted = True
            st.success("Your vote has been submitted!")
    elif len(choices) > 3:
        st.warning("Please select exactly three options.")
else:
    st.info("You have already voted. Thank you for participating!")

# Show current votes (for debugging or viewing purposes)
if st.checkbox("Show all votes"):
    st.write(st.session_state.votes)

# Single Transferable Voting (STV) calculation
def stv_winner(votes, dinner_packages):
    counts = Counter()
    active_candidates = set(dinner_packages)
    
    # First preferences count
    for vote in votes:
        counts[vote[0]] += 1
    
    while True:
        # Check if any candidate has more than half of the votes
        for candidate, count in counts.items():
            if count > len(votes) / 2:
                return candidate
        
        # Find the candidate with the fewest votes
        min_candidate = min(counts, key=counts.get)
        active_candidates.remove(min_candidate)
        
        # Redistribute votes from the eliminated candidate
        new_counts = Counter()
        for vote in votes:
            for candidate in vote:
                if candidate in active_candidates:
                    new_counts[candidate] += 1
                    break
        counts = new_counts

if st.button("Calculate Winner"):
    if st.session_state.votes:
        winner = stv_winner(st.session_state.votes, dinner_packages)
        st.success(f"The winning dinner package is: {winner}")
        
        # Count total first-choice votes for each dinner package
        total_votes = Counter([vote[0] for vote in st.session_state.votes])
        
        # Prepare data for bar chart
        results_df = pd.DataFrame.from_dict(total_votes, orient='index', columns=["Votes"])
        results_df = results_df.reindex(dinner_packages).fillna(0)  # Ensure all packages are included
        
        # Display bar chart of votes
        st.bar_chart(results_df)
        
        # Display total votes cast
        st.write(f"Total Votes Cast: {len(st.session_state.votes)}")
    else:
        st.warning("No votes have been cast yet.")
