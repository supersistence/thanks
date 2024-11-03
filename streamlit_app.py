import streamlit as st
from collections import Counter

# Dinner package details
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
        "Image URL": "https://az727718.vo.msecnd.net/cfff44f0457b41e38cf9a0da89949200/images/9d03a461727e4fa6a21858b15873fcea_540w.jpg"
    }
}

# Display table with HTML
st.title("Holiday Dinner Package Comparison")
st.write("Compare dinner packages by sides and view an image of each option.")

# HTML table structure
table_html = """
<table>
    <thead>
        <tr>
            <th>Package</th>
            <th>Image</th>
            <th>Potatoes</th>
            <th>Green Beans Almondine</th>
            <th>Dinner Rolls</th>
            <th>Herb Stuffing</th>
            <th>Candied Yams</th>
            <th>Roasted Root Vegetables</th>
            <th>Cranberry Relish</th>
            <th>Turkey Gravy</th>
            <th>Brisket Sauce</th>
            <th>Creamed Horseradish</th>
        </tr>
    </thead>
    <tbody>
"""

# Populate table rows with data
for name, details in dinner_info.items():
    table_html += f"""
    <tr>
        <td>{name}</td>
        <td><img src="{details['Image URL']}" width="100"/></td>
        <td>{details['Potatoes']}</td>
        <td>{details['Green Beans Almondine']}</td>
        <td>{details['Dinner Rolls']}</td>
        <td>{details['Herb Stuffing']}</td>
        <td>{details['Candied Yams']}</td>
        <td>{details['Roasted Root Vegetables']}</td>
        <td>{details['Cranberry Relish']}</td>
        <td>{details['Turkey Gravy']}</td>
        <td>{details['Brisket Sauce']}</td>
        <td>{details['Creamed Horseradish']}</td>
    </tr>
    """

table_html += "</tbody></table>"

# Display HTML table
st.markdown(table_html, unsafe_allow_html=True)

# Rest of the app (voting section)...
# Note: Voting code is the same as provided in previous examples.
