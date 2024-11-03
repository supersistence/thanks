import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

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

# Display the table with sides and images
st.title("Holiday Dinner Package Comparison")
st.write("Compare dinner packages by sides and see an image of each option.")
st.dataframe(dinner_df.drop(columns=["Image URL"]))  # Display the data without image URLs

# Display images and titles in two columns
st.header("Dinner Packages with Images")
cols = st.columns(2)  # Create two columns

for idx, (dinner, details) in enumerate(dinner_info.items()):
    with cols[idx % 2]:  # Alternate columns
        st.subheader(dinner)
        st.image(details["Image URL"], caption=dinner, width=150)  # Set image width to 150 pixels

# Voting section
st.header("Rank Your Top Three Choices")
if "has_voted" not in st.session_state:
    st.session_state.has_voted = False
if "votes" not in st.session_state:
    st.session_state.votes = []

if not st.session_state.has_voted:
    choices = st.multiselect("Select your top three dinner packages in order of preference:", dinner_packages, [])

    if len(choices) == 3:
        if st.button("Submit Vote"):
            st.session_state.votes.append(choices)
            st.session_state.has_voted = True
            st.success("Your vote has been submitted!")
    elif len(choices) > 3:
        st.warning("Please select exactly three options.")
else:
    st.info("You have already voted. Thank you for participating!")

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
