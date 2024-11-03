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

# Information about each dinner package with the correct image URLs
dinner_info = {
    "Traditional Turkey Dinner": {
        "description": "Mashed potatoes, herb stuffing, candied yams, green beans almondine, turkey gravy, cranberry relish, choice of pie.",
        "image_url": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/7419baea05bf4b85adc4354a85aef957_540w.jpg"
    },
    "Traditional Turkey Breast Dinner": {
        "description": "Mashed potatoes, herb stuffing, candied yams, green beans almondine, turkey gravy, cranberry relish, choice of pie.",
        "image_url": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/f3a68ba6ec4343988983f697da3aa2a8_540w.jpg"
    },
    "Orange Glazed Spiral Cut Ham Dinner": {
        "description": "Scalloped potatoes, candied yams, green beans almondine, cranberry relish, choice of pie.",
        "image_url": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/077cf99592614a4f9cf18c5a38202896_540w.jpg"
    },
    "Boneless Ribeye Roast Dinner": {
        "description": "Scalloped potatoes, green beans almondine, creamed horseradish, apple pie.",
        "image_url": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/7315c3ac09694746ab1ac1f485784a35_540w.jpg"
    },
    "Braised Brisket Dinner": {
        "description": "Potato latkes, roasted root vegetables, green beans almondine, brisket sauce, caramel apple pie.",
        "image_url": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/b815f8ce6c474441ada34503f63fd3f6_540w.jpg"
    },
    "Beef Wellington Dinner": {
        "description": "Scalloped potatoes, green beans almondine, apple pie.",
        "image_url": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/9d03a461727e4fa6a21858b15873fcea_540w.jpg"
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
