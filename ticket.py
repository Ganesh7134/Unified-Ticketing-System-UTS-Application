# Import necessary libraries
import streamlit as st  # Streamlit for building the web app
import requests  # Requests for making HTTP requests
import time  # Time-related functions
import pandas as pd  # Pandas for data manipulation and analysis
import re  # Regular expressions
from streamlit_option_menu import option_menu  # Streamlit option menu for creating menus
from geopy.geocoders import Nominatim  # Geopy for geocoding (converting addresses into geographic coordinates)
from geopy.distance import geodesic  # Geopy for calculating distances between points
import folium  # Folium for creating interactive maps
from streamlit_folium import folium_static  # Streamlit-Folium for embedding Folium maps in Streamlit
from selenium import webdriver  # Selenium for web browser automation
from selenium.webdriver.common.by import By  # Selenium module for locating elements on a webpage
import time  # Time-related functions (imported again, but not necessary)
from selenium.webdriver.chrome.options import Options  # Selenium options for Chrome browser configuration
from folium.features import CustomIcon  # Folium for adding custom icons on the map
# import ast  # Abstract Syntax Trees, used here for converting strings to Python objects
from PIL import Image # python Image library to deal with images
import re # regular expressions
from datetime import datetime,timedelta
import random
import qrcode
from io import BytesIO
import mysql.connector
from mysql.connector import Error
import json
from streamlit_lottie import st_lottie

# Set the title of the Streamlit app
st.title("Hybrid UTS Ticketing for Easy Travel")

# Load the data from a CSV file into a DataFrame using Pandas
df = pd.read_csv("Chennai_project_data.csv")


# Establish the database connection
host = "localhost"
port = 3306
user = "root"
password = "root143@"

# Create a connection object
connection = mysql.connector.connect(host=host, port=port, user=user, password=password,database="UTS_Ticket_info",auth_plugin="mysql_native_password")

def normal_ticket_booking(T_type,v_type,origin, destination, price):
# Slider to select the number of tickets
    Num = st.slider("Select number of tickets: ", min_value=1, max_value=20)

    # Subheader for payment options section
    st.subheader("Payment Options")
    
    # List of available payment options
    payment_options = ["Credit Card", "Debit Card", "PayPal", "UPI", "Other"]
    
    # Radio button to select a payment option from the list
    payment_option = st.radio("Select Payment Option", payment_options)

    # Conditional input fields based on selected payment option
    if payment_option in ["Credit Card", "Debit Card"]:
        # Text input for card number
        card_number = st.text_input("Enter Card Number", "")
        
        # Validate card number format
        # This regex checks if the input is exactly 16 digits.
        if not re.match(r'^[0-9]{16}$', card_number):
            st.warning("Please enter a valid 16-digit card number.")
        
        # Text input for expiry date
        expiry_date = st.text_input("Enter Expiry Date (MM/YY)", "")
        
        # Validate expiry date format
        # This regex checks if the input is in the MM/YY format where MM is between 01 and 12.
        if not re.match(r'^(0[1-9]|1[0-2])\/[0-9]{2}$', expiry_date):
            st.warning("Please enter expiry date in the format MM/YY.")
        
        # Text input for CVV
        cvv = st.text_input("Enter CVV", "")
        
        # Validate CVV format
        # This regex checks if the input is either 3 or 4 digits.
        if not re.match(r'^[0-9]{3,4}$', cvv):
            st.warning("Please enter a valid CVV.")
    elif payment_option == "PayPal":
        # Text input for PayPal email
        paypal_email = st.text_input("Enter PayPal Email", "")
        
        # Validate PayPal email format
        # This regex checks if the input is a valid email format.
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', paypal_email):
            st.warning("Please enter a valid PayPal email.")
        
        # Password input for PayPal password
        password = st.text_input("Enter Password", "", type="password")
        
        # Validate password length
        # This regex checks if the input is at least 8 characters long.
        if not re.match(r'^.{8,}$', password):
            st.warning("Password must be at least 8 characters long.")
    elif payment_option == "UPI":
        # Text input for UPI ID
        upi_id = st.text_input("Enter UPI ID", "")
        
        # Validate UPI ID format
        # This regex checks if the input is a valid UPI ID format.
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', upi_id):
            st.warning("Please enter a valid UPI ID.")
    elif payment_option == "Other":
        # Text input for other payment options (e.g., cash)
        other_option = st.text_input("Enter Other Payment Option", "cash")

    price = int(price.replace('₹', '')) * Num
    st.info(f"Total ticket amount: {price}")
    
    # Input field for entering the payment amount
    payment = st.text_input("Enter amount to pay for ticket: ", "")

    # Button to proceed with the payment
    if st.button("Proceed to Payment", key=1, use_container_width=True):
        # Verify the payment amount matches the ticket price multiplied by the number of tickets
        if str(price) == payment:
            # Display success message
            st.success("**Thank you for booking your tickets! Your order has been processed successfully.**")
            
            # Display balloons animation
            st.balloons()

            # Get the current time
            current_time = datetime.now()
            
            # Add 24 hours to the current time to get the ticket validity
            ticket_validity = current_time + timedelta(hours=24)

            # Generate a random ticket ID (6 digits)
            ticket_id = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))

            # Mark the payment status as paid
            payment_status = "paid"

            # Inform the user about their UTS ticket
            st.markdown("Here is your UTS ticket ")

            # Create the QR code data
            qr_data = f"TicketID: {ticket_id}\nTicket_type: {T_type}\nFrom Station: {origin}\nTo Station: {destination}\nVehicle_type: {v_type}\nPrice: {price}\nTicket Validity: {ticket_validity}"

            # Create a QR code instance with specified parameters
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_data)

            # Generate the QR code pattern
            qr.make(fit=True)

            # Create an image from the QR code pattern
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert the image to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")

            # Display the image of the QR code in Streamlit
            st.image(img_bytes, caption=f"TicketID: {ticket_id}")

            st.info("**Note**: Valid only for selected station and transport. Not valid for UTS.")

def ticket_booking(T_type,v_type,origin, destination, price):

    # Slider to select the number of tickets
    Num = st.slider("Select number of tickets: ", min_value=1, max_value=20)

    # Subheader for payment options section
    st.subheader("Payment Options")
    
    # List of available payment options
    payment_options = ["Credit Card", "Debit Card", "PayPal", "UPI", "Other"]
    
    # Radio button to select a payment option from the list
    payment_option = st.radio("Select Payment Option", payment_options)

    # Conditional input fields based on selected payment option
    if payment_option in ["Credit Card", "Debit Card"]:
        # Text input for card number
        card_number = st.text_input("Enter Card Number", "")
        
        # Validate card number format
        # This regex checks if the input is exactly 16 digits.
        if not re.match(r'^[0-9]{16}$', card_number):
            st.warning("Please enter a valid 16-digit card number.")
        
        # Text input for expiry date
        expiry_date = st.text_input("Enter Expiry Date (MM/YY)", "")
        
        # Validate expiry date format
        # This regex checks if the input is in the MM/YY format where MM is between 01 and 12.
        if not re.match(r'^(0[1-9]|1[0-2])\/[0-9]{2}$', expiry_date):
            st.warning("Please enter expiry date in the format MM/YY.")
        
        # Text input for CVV
        cvv = st.text_input("Enter CVV", "")
        
        # Validate CVV format
        # This regex checks if the input is either 3 or 4 digits.
        if not re.match(r'^[0-9]{3,4}$', cvv):
            st.warning("Please enter a valid CVV.")
    elif payment_option == "PayPal":
        # Text input for PayPal email
        paypal_email = st.text_input("Enter PayPal Email", "")
        
        # Validate PayPal email format
        # This regex checks if the input is a valid email format.
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', paypal_email):
            st.warning("Please enter a valid PayPal email.")
        
        # Password input for PayPal password
        password = st.text_input("Enter Password", "", type="password")
        
        # Validate password length
        # This regex checks if the input is at least 8 characters long.
        if not re.match(r'^.{8,}$', password):
            st.warning("Password must be at least 8 characters long.")
    elif payment_option == "UPI":
        # Text input for UPI ID
        upi_id = st.text_input("Enter UPI ID", "")
        
        # Validate UPI ID format
        # This regex checks if the input is a valid UPI ID format.
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', upi_id):
            st.warning("Please enter a valid UPI ID.")
    elif payment_option == "Other":
        # Text input for other payment options (e.g., cash)
        other_option = st.text_input("Enter Other Payment Option", "cash")

    price = int(price.replace('₹', '')) * Num
    st.info(f"Total ticket amount: {price}")
    
    # Input field for entering the payment amount
    payment = st.text_input("Enter amount to pay for ticket: ", "")

    # Button to proceed with the payment
    if st.button("Proceed to Payment", key=1, use_container_width=True):
        # Verify the payment amount matches the ticket price multiplied by the number of tickets
        if str(price) == payment:
            # Display success message
            st.success("**Thank you for booking your tickets! Your order has been processed successfully.**")
            
            # Display balloons animation
            st.balloons()

            # Get the current time
            current_time = datetime.now()
            
            # Add 24 hours to the current time to get the ticket validity
            ticket_validity = current_time + timedelta(hours=24)

            # Generate a random ticket ID (6 digits)
            ticket_id = ''.join(random.choices('0123456789', k=6))

            # Mark the payment status as paid
            payment_status = "paid"

            # Inform the user about their UTS ticket
            st.markdown("Here is your UTS ticket ")

            # Create the QR code data
            qr_data = f"TicketID: {ticket_id}\nTicket_type: {T_type}\nFrom Station: {origin}\nTo Station: {destination}\nVehicle_type: {v_type}\nPrice: {price}\nTicket Validity: {ticket_validity}"

            # Create a QR code instance with specified parameters
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_data)

            # Generate the QR code pattern
            qr.make(fit=True)

            # Create an image from the QR code pattern
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert the image to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")

            # Display the image of the QR code in Streamlit
            st.image(img_bytes, caption=f"TicketID: {ticket_id}")

            # Define the output file path for saving the QR code image
            output_file_path = f"D:/streamlit/{ticket_id}.png"

            # Save the QR code image as a PNG file
            img.save(output_file_path)

            # Save the QR code image file path
            qr_ticket = output_file_path

            # Display the file path where the QR code image is saved
            st.markdown(f"QR code image saved at: {output_file_path}")
            try:
                if connection.is_connected():
                    cursor = connection.cursor()

                    # SQL query to create the tickets table
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS Hybrid_Ticket_Info (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ticket_id VARCHAR(255) NOT NULL,
                        ticket_type VARCHAR(255) NOT NULL,
                        origin VARCHAR(255) NOT NULL,
                        destination VARCHAR(255) NOT NULL,
                        no_of_tickets INT NOT NULL,
                        price_of_the_ticket INT NOT NULL,
                        vehicle_type VARCHAR(255) NOT NULL,
                        payment_options VARCHAR(255) NOT NULL,
                        payment_status VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        Ticket_validity TIMESTAMP,
                        qr_ticket TEXT
                    );
                    """

                    # Execute the query to create the table
                    cursor.execute(create_table_query)
                    connection.commit()
                    # st.success("Table 'Ticket_info' created successfully.")

            except Error as e:
                st.error("Error while connecting to MySQL",e)

            def insert_ticket(ticket_id, T_type, origin, destination, Num , price ,v_type, payment_option, payment_status, ticket_validity, qr_ticket):
                try:
                    # Establish the database connection
                    host = "localhost"
                    port = 3306
                    user = "root"
                    password = "root143@"
                    database = "UTS_Ticket_info"

                    # Create a connection object
                    connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database, auth_plugin="mysql_native_password")

                    if connection.is_connected():
                        cursor = connection.cursor()

                        # SQL query to insert data into the tickets table
                        insert_query = """
                        INSERT INTO Hybrid_Ticket_Info (ticket_id, ticket_type, origin, destination,no_of_tickets,price_of_the_ticket,vehicle_type,payment_options, payment_status, Ticket_validity, qr_ticket)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s);
                        """

                        # Data to be inserted
                        ticket_data = (ticket_id, T_type, origin, destination, Num , price ,v_type, payment_option, payment_status, ticket_validity, qr_ticket)

                        # Execute the query to insert data
                        cursor.execute(insert_query, ticket_data)
                        connection.commit()
                        # st.success("Ticket data inserted successfully.")

                except Error as e:
                    st.error(f"Error while inserting data into MySQL: {e}")

            insert_ticket(ticket_id, T_type, origin, destination, Num , price ,v_type, payment_option, payment_status, ticket_validity, qr_ticket)

        else:
            st.error("Payment is not matched to the price of the ticket please verify it")


def ticket_verify(ticket_id):
    try:
        if connection.is_connected(): # To delete tickets automatically when it exceeds 24 hours
            cursor = connection.cursor()
            delete_query = "DELETE FROM Hybrid_Ticket_Info WHERE Ticket_validity < NOW();"
            cursor.execute(delete_query)
            connection.commit()
            st.info("Expired tickets deleted successfully.")
    except:
        print("table not yet create")

    try:
        if connection.is_connected():
            cursor = connection.cursor()
            select_query = "SELECT Ticket_validity FROM Hybrid_Ticket_Info WHERE ticket_id = %s;"
            cursor.execute(select_query, (ticket_id,))
            result = cursor.fetchone()

            if result:
                validity = result[0]
                current_time = datetime.now()
                if validity > current_time:
                    success_message = f"""
                        <div style="color: green; font-size: 24px;">
                            <b>🎉 Ticket ID</b>: <span style="color: blue; font-weight: bold;">{ticket_id}</span><br>
                            <b>🕒 Valid until</b>: <span style="color: red; font-weight: bold;">{validity}</span><br>
                            <b>🚀 Enjoy your journey and have a fantastic day!</b> 🤗
                        </div>
                    """

                    # Display the success message using Streamlit's markdown
                    st.markdown(success_message, unsafe_allow_html=True)
                else:
                    st.warning(f"Ticket ID {ticket_id} has expired.")
            else:
                st.error(f"Ticket ID {ticket_id} not found because its Normal Ticket ")
    except Error as e:
        st.error(f"Error while checking ticket validity: {e}")

    
# Define a function to handle travel information display
def travel_info():

    @st.cache_data(ttl=60 * 60)
    def load_lottie_file(filepath : str):
        with open(filepath, "r") as f:
            gif = json.load(f)
        return gif

    gif = load_lottie_file("travel.json")
    st_lottie(gif, speed=1, width=650, height=450)
    # Create two columns in the Streamlit app layout
    col1, col2 = st.columns(2)

    # In the first column, create a dropdown (select box) for selecting the origin station
    # Populated with unique values from the 'Origin_station' column of the DataFrame
    with col1:
        Origin = st.selectbox("select origin: ", df["Origin_station"].to_list())

    # Filter the DataFrame to get the destinations corresponding to the selected origin station
    des = df[df["Origin_station"] == Origin]["Destination"]

    # In the second column, create a dropdown for selecting the destination station
    # Populated with unique values from the filtered 'Destination' column
    with col2:
        destination = st.selectbox("select destination : ", des.to_list())

    # Filter the DataFrame to get the row corresponding to the selected origin and destination
    res = df[(df["Origin_station"] == Origin) & (df["Destination"] == destination)]

    # Create a button that, when clicked, will fetch and display the details
    but = st.button("click here to fetch the details", use_container_width=True)
    if but:
        # Adding custom CSS styles using HTML within Markdown
        st.markdown(
            """
            <style>
                .grid-container {
                    display: grid; /* Setting display property to grid for grid layout */
                    grid-template-columns: repeat(3, 1fr); /* Setting grid to have 3 columns */
                    grid-gap: 20px; /* Adding gap between grid items */
                }
                .grid-item {
                    background-color: #f9f9f9; /* Setting background color for grid items */
                    padding: 20px; /* Adding padding around grid items */
                    border-radius: 5px; /* Adding border radius to grid items */
                    margin-bottom: 20px; /* Adding margin to create space between rows */
                }
                .grid-item h2 {
                    color: #333333; /* Setting color for h2 headings */
                    margin-bottom: 10px; /* Adding margin below h2 headings */
                }
                .grid-item h3 {
                    color: #666666; /* Setting color for h3 headings */
                    margin-bottom: 5px; /* Adding margin below h3 headings */
                }
                .grid-item p {
                    color: black; /* Setting color for paragraph text */
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Opening the grid container div
        st.markdown("<div class='grid-container'>", unsafe_allow_html=True)

        # Extracting data from the filtered DataFrame 'res' and assigning to variables
        bus_route_id = res["Bus Route ID"].values[0]
        intermediate_stations = res["Intermediate_stations"].values[0]
        bus_timings = res["Bus Timings"].values[0]
        bus_price = res["Bus Price"].values[0]
        nearest_metro_stations = res["Nearest Metro Stations"].values[0]
        metro_ticket_price = res["Metro Ticket Price"].values[0]
        metro_timings = res["Metro Timings"].values[0]
        nearest_cab_booking_places = res["Nearest Cab Booking Places"].values[0]
        cab_booking_price = res["Cab Booking Price"].values[0]
        nearest_local_trains = res["Nearest Local Trains"].values[0]
        train_ticket_price = res["Train Ticket Price"].values[0]
        train_timings = res["Train Timings"].values[0]

        # Creating HTML elements with extracted data and adding them to the columns list
        columns = [
            f"<div class='grid-item'><h2 style='color: #FF5733;'>🚍 Bus Route ID:</h2><h3>{bus_route_id}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #C70039;'>🚩 Intermediate Stations:</h2><h3>{intermediate_stations}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #900C3F;'>🕗 Bus Timings:</h2><h3>{bus_timings}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #581845;'>💰 Bus Price:</h2><h3>{bus_price}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #FF5733;'>🚝 Nearest Metro Stations:</h2><h3>{nearest_metro_stations}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #C70039;'>🎟️ Metro Ticket Price:</h2><h3>{metro_ticket_price}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #900C3F;'>🕙 Metro Timings:</h3><h3>{metro_timings}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #581845;'>🚖 Nearest Cab Booking Places:</h2><h3>{nearest_cab_booking_places}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #FF5733;'>📠 Cab Booking Price:</h2><h3>{cab_booking_price}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #C70039;'>🚉 Nearest Local Trains:</h2><h3>{nearest_local_trains}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #900C3F;'>🎫 Train Ticket Price:</h2><h3>{train_ticket_price}</h3></div>",
            f"<div class='grid-item'><h2 style='color: #581845;'>🕧 Train Timings:</h2><h3>{train_timings}</h3></div>"
        ]

        # Displaying elements in three columns
        for i in range(0, len(columns), 4):
            st.markdown("<div style='display: flex;'>", unsafe_allow_html=True) # Opening flex container
            for j in range(i, min(i + 4, len(columns))): # Iterating over items in the current row
                st.markdown(columns[j], unsafe_allow_html=True) # Adding each item to the row
            st.markdown("</div>", unsafe_allow_html=True) # Closing flex container

        # Closing the grid container div
        st.markdown("</div>", unsafe_allow_html=True)


# Caching the data to improve performance
@st.cache_data(ttl=(60*60))
def get_coordinates(location, website_url):
    # Start a Selenium WebDriver session with Chrome options
    options = Options()
    options.add_argument("--headless")  # Run the browser in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        # Open the specified website
        driver.get(website_url)

        # Find the search input field by ID
        search_box = driver.find_element(By.ID, "searchboxinput")

        # Enter the location in the search box
        search_box.send_keys(location)
        
        # Wait for the map to load
        time.sleep(5)  # Adjust the wait time as needed

        # Get the current URL (it might change after the map loads)
        updated_url = driver.current_url
        
        # Extract the latitude and longitude from the updated URL
        lat_long_str = updated_url.split("@")[1].split(",")[0:2]
        latitude = lat_long_str[0]
        longitude = lat_long_str[1]

        return (latitude, longitude)

    finally:
        # Close the WebDriver session
        driver.quit()

@st.cache_data(ttl=(60*60))
def locations(location):
    # Build the URL for the Google Maps search
    website_url = f"https://www.google.com/maps/search/{location}/@13.0847497,80.2692163,16z/data=!3m1!4b1?entry=ttu"
    latitude, longitude = get_coordinates(location, website_url)
    return latitude, longitude

def map_view():
    # Create two columns in the Streamlit app layout
    col1, col2 = st.columns(2)

    # In the first column, create a dropdown (select box) for selecting the origin station
    with col1:
        Origin = st.selectbox("select origin: ", df["Origin_station"].to_list())

    # Filter the DataFrame to get the destinations corresponding to the selected origin station
    des = df[df["Origin_station"] == Origin]["Destination"]

    # In the second column, create a dropdown for selecting the destination station
    with col2:
        destination = st.selectbox("select destination : ", des.to_list())

    # Filter the DataFrame to get the row corresponding to the selected origin and destination
    res = df[(df["Origin_station"] == Origin) & (df["Destination"] == destination)]

    # Extracting data from the DataFrame 'res' and assigning to variables

    intermediate_stations = res["Intermediate_stations"].values[0]
   
    nearest_metro_stations = res["Nearest Metro Stations"].values[0]
    
    nearest_cab_booking_places = res["Nearest Cab Booking Places"].values[0]
   
    nearest_local_trains = res["Nearest Local Trains"].values[0]
   

    # Fetch coordinates for the origin and destination locations
    lat1, lon1 = locations(Origin)
    lat2, lon2 = locations(destination)

    st.info(f"First station - Latitude: {lat1}, Longitude: {lon1}")
    st.info(f"Second station - Latitude: {lat2}, Longitude: {lon2}")

    # Calculate the distance between the two coordinates
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    distance = geodesic(coord1, coord2).kilometers
    st.info(f"Distance between {Origin} and {destination}: {distance:.2f} km")

    # Check if coordinates are found for both origin and destination
    if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
        try:
            # Convert coordinates to floats
            lat1 = float(lat1)
            lon1 = float(lon1)
            lat2 = float(lat2)
            lon2 = float(lon2)
            
            # Calculate the midpoint
            midpoint = [(lat1 + lat2) / 2, (lon1 + lon2) / 2]

            # Create a Folium map centered around the midpoint
            folium_map = folium.Map(location=midpoint, zoom_start=10)

            # Add markers for the origin and destination
            folium.Marker(location=[lat1, lon1], popup=Origin, tooltip=Origin).add_to(folium_map)
            folium.Marker(location=[lat2, lon2], popup=destination, tooltip=destination).add_to(folium_map)

            # Add a line between the origin and destination
            folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color='blue').add_to(folium_map)
            
            # Create a dropdown for selecting the type of route
            sel = st.selectbox("select routes: ", ["Bus routes", "Metro route", "cab route", "local trains"])

            if sel == "Bus routes":
                # Split the string by commas and strip whitespace from each station name
                intermediate_stations_list = [station.strip("[]").strip() for station in intermediate_stations.split(',')]

                # Add markers for the first 3 intermediate stations
                for station in intermediate_stations_list[:3]:
                    lat, lon = locations(station)
                    if lat is not None and lon is not None:
                        # Use a custom PNG icon for the bus
                        icon = folium.CustomIcon(r'D:\streamlit\Bus.png', icon_size=(30, 30))
                        folium.Marker(
                            location=[lat, lon],
                            popup=station,
                            tooltip=station,
                            icon=icon
                        ).add_to(folium_map)

                # Display the updated map
                folium_static(folium_map, width=700, height=500)
            
            if sel == "Metro route":
                # Split the string by commas and strip whitespace from each station name
                nearest_metro_stations_list = [station.strip("[]").strip() for station in nearest_metro_stations.split(',')]

                for metro in nearest_metro_stations_list[:3]:
                    # Fetch coordinates for the intermediate station
                    lat, lon = locations(metro)
                    if lat is not None and lon is not None:
                        icon = folium.CustomIcon(r'D:\streamlit\Train.png', icon_size=(30, 30))
                        folium.Marker(
                            location=[lat, lon],
                            popup=metro,
                            tooltip=metro,
                            icon=icon
                        ).add_to(folium_map)
            
            if sel == "cab route":
                # Split the string by commas and strip whitespace from each station name
                nearest_cab_booking_places_list = [station.strip("[]").strip() for station in nearest_cab_booking_places.split(',')]

                for cab in nearest_cab_booking_places_list[:3]:
                    # Fetch coordinates for the intermediate station
                    lat, lon = locations(cab)
                    if lat is not None and lon is not None:
                        icon = folium.CustomIcon(r'D:\streamlit\cab.png', icon_size=(30, 30))
                        folium.Marker(
                            location=[lat, lon],
                            popup=cab,
                            tooltip=cab,
                            icon=icon
                        ).add_to(folium_map)
            
            if sel == "local trains":
                # Split the string by commas and strip whitespace from each station name
                nearest_local_trains_list = [station.strip("[]").strip() for station in nearest_local_trains.split(',')]

                for train in nearest_local_trains_list[:3]:
                    # Fetch coordinates for the intermediate station
                    lat, lon = locations(train)
                    if lat is not None and lon is not None:
                        icon = folium.CustomIcon(r'D:\streamlit\engine.webp', icon_size=(30, 30))
                        folium.Marker(
                            location=[lat, lon],
                            popup=train,
                            tooltip=train,
                            icon=icon
                        ).add_to(folium_map)
                        
        except ValueError:
            st.error("Invalid latitude or longitude values")
        else:
            # Display the Folium map
            st.subheader("Map View of Locations and Route")
            folium_static(folium_map, width=700, height=500)
    else:
        st.warning("Coordinates not found for one or both of the towns. Please enter valid town names.")

       
def bus_travel():
    with st.sidebar.container():
        image = Image.open(r"D:\streamlit\Bus.png")
        st.image(image,use_column_width=True)
    with st.sidebar:
        select = st.selectbox("**select mode of ticket** :",["Normal-Ticket","UTS-Ticket"])
        # Create two columns in the Streamlit app layout
        col1, col2 = st.columns(2)

        # In the first column, create a dropdown (select box) for selecting the origin station
        # Populated with unique values from the 'Origin_station' column of the DataFrame
        with col1:
            Origin = st.selectbox("select origin: ", df["Origin_station"].to_list())

        # Filter the DataFrame to get the destinations corresponding to the selected origin station
        des = df[df["Origin_station"] == Origin]["Destination"]

        # In the second column, create a dropdown for selecting the destination station
        # Populated with unique values from the filtered 'Destination' column
        with col2:
            destination = st.selectbox("select destination : ", des.to_list())

        # Filter the DataFrame to get the row corresponding to the selected origin and destination
        res = df[(df["Origin_station"] == Origin) & (df["Destination"] == destination)]

        bus_route_id = res["Bus Route ID"].values[0]
        intermediate_stations = res["Intermediate_stations"].values[0]
        bus_timings = res["Bus Timings"].values[0]
        bus_ticket_price = res["Bus Price"].values[0]
        
        
        # Split the string by commas and strip whitespace from each station name
        intermediate_stations_list = [station.strip("[]").strip() for station in intermediate_stations.split(',')]
        st.markdown("<h3 style='color:Green;font-size:24px'><strong>select nearest bus stations</strong></h3>",unsafe_allow_html=True)
        if select:
            sel = st.selectbox("",intermediate_stations_list)


        but = st.button("click here to check",use_container_width=True)

        if but:
            # Adding custom CSS styles using HTML within Markdown
            st.markdown(
                """
                <style>
                    .grid-container {
                        display: grid; /* Setting display property to grid for grid layout */
                        grid-template-columns: repeat(3, 1fr); /* Setting grid to have 3 columns */
                        grid-gap: 20px; /* Adding gap between grid items */
                    }
                    .grid-item {
                        background-color: #f9f9f9; /* Setting background color for grid items */
                        padding: 20px; /* Adding padding around grid items */
                        border-radius: 5px; /* Adding border radius to grid items */
                        margin-bottom: 20px; /* Adding margin to create space between rows */
                    }
                    .grid-item h2 {
                        color: #333333; /* Setting color for h2 headings */
                        margin-bottom: 10px; /* Adding margin below h2 headings */
                    }
                    .grid-item h3 {
                        color: #666666; /* Setting color for h3 headings */
                        margin-bottom: 5px; /* Adding margin below h3 headings */
                    }
                    .grid-item p {
                        color: black; /* Setting color for paragraph text */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Opening the grid container div
            st.markdown("<div class='grid-container'>", unsafe_allow_html=True)

            # Extracting data from the filtered DataFrame 'res' and assigning to variables
            bus_route_id = res["Bus Route ID"].values[0]
            intermediate_stations = res["Intermediate_stations"].values[0]
            bus_timings = res["Bus Timings"].values[0]
            bus_ticket_price = res["Bus Price"].values[0]
            

            # Creating HTML elements with extracted data and adding them to the columns list
            columns = [
                f"<div class='grid-item'><h2 style='color: #FF5733;'>🚍 Bus Route ID:</h2><h3>{bus_route_id}</h3></div>",
                f"<div class='grid-item'><h2 style='color: #C70039;'>🚩 Intermediate Stations:</h2><h3>{intermediate_stations}</h3></div>",
                f"<div class='grid-item'><h2 style='color: #900C3F;'>🕗 Bus Timings:</h2><h3>{bus_timings}</h3></div>",
                f"<div class='grid-item'><h2 style='color: #581845;'>💰 Bus Price:</h2><h3>{bus_ticket_price}</h3></div>",
            ]

            # Joining all elements into a single string
            all_columns = "".join(columns)

            # Displaying all elements within a single <div> tag
            st.markdown(f"<div class='display:flex'>{all_columns}</div>", unsafe_allow_html=True)

        

        

    if select == "Normal-Ticket":
        st.title("Normal ticket booking site")
        st.warning("**Note**: This ticket is valid for **one transportation vehicle**")
        normal_ticket_booking("Hybrid - UTS","Bus - " + sel ,Origin,destination,bus_ticket_price)
        
            
    
    if select == "UTS-Ticket":
        st.title("UTS - Hybrid ticket booking site")
        st.warning("**Note**: This ticket is valid for all transportation vehicles for 24 hours.")
        try:
            menu = {
                "🗳️ UTS_Ticket_booking": "ticket_booking",
                "🔐 Ticket_verify": "ticket_verify",
            }

            selected = option_menu("", list(menu.keys()), orientation="horizontal",key=12)


            page_funct = {
                "ticket_booking": "1",
                "ticket_verify": "2",
            }
            if page_funct[menu[selected]] == "1":
                ticket_booking("Hybrid - UTS","Bus - " + sel ,Origin,destination,bus_ticket_price)
            else:
                st.subheader("Check the Ticket validity:")
                # Check ticket validity
                ticket_id_input = st.text_input("Enter Ticket ID to check UTS ticket validity:")
                if st.button("Check Ticket Validity",use_container_width=True):
                    ticket_verify(ticket_id_input)

        except:
            print("do not raise error")
    
            

def metro_travel():
    with st.sidebar.container():
        image = Image.open(r"D:\streamlit\metro.png")
        st.image(image,use_column_width=True)
    with st.sidebar:
        select = st.selectbox("**select mode of ticket** :",["Normal-Ticket","UTS-Ticket"])

        # Create two columns in the Streamlit app layout
        col1, col2 = st.columns(2)

        # In the first column, create a dropdown (select box) for selecting the origin station
        # Populated with unique values from the 'Origin_station' column of the DataFrame
        with col1:
            Origin = st.selectbox("select origin: ", df["Origin_station"].to_list())

        # Filter the DataFrame to get the destinations corresponding to the selected origin station
        des = df[df["Origin_station"] == Origin]["Destination"]

        # In the second column, create a dropdown for selecting the destination station
        # Populated with unique values from the filtered 'Destination' column
        with col2:
            destination = st.selectbox("select destination : ", des.to_list())

        # Filter the DataFrame to get the row corresponding to the selected origin and destination
        res = df[(df["Origin_station"] == Origin) & (df["Destination"] == destination)]

    
        nearest_metro_stations = res["Nearest Metro Stations"].values[0]
        metro_ticket_price = res["Metro Ticket Price"].values[0]
        metro_timings = res["Metro Timings"].values[0]
        
        
        # Split the string by commas and strip whitespace from each station name
        nearest_metro_stations_list = [station.strip("[]").strip() for station in nearest_metro_stations.split(',')]
        st.markdown("<h3 style='color:Green;font-size:24px'><strong>select nearest metro tations</strong></h3>",unsafe_allow_html=True)
        if select:
            sel = st.selectbox("",nearest_metro_stations_list)
        

        but = st.button("click here to check",use_container_width=True)

        if but:
            # Adding custom CSS styles using HTML within Markdown
                st.markdown(
                    """
                    <style>
                        .grid-container {
                            display: grid; /* Setting display property to grid for grid layout */
                            grid-template-columns: repeat(3, 1fr); /* Setting grid to have 3 columns */
                            grid-gap: 20px; /* Adding gap between grid items */
                        }
                        .grid-item {
                            background-color: #f9f9f9; /* Setting background color for grid items */
                            padding: 20px; /* Adding padding around grid items */
                            border-radius: 5px; /* Adding border radius to grid items */
                            margin-bottom: 20px; /* Adding margin to create space between rows */
                        }
                        .grid-item h2 {
                            color: #333333; /* Setting color for h2 headings */
                            margin-bottom: 10px; /* Adding margin below h2 headings */
                        }
                        .grid-item h3 {
                            color: #666666; /* Setting color for h3 headings */
                            margin-bottom: 5px; /* Adding margin below h3 headings */
                        }
                        .grid-item p {
                            color: black; /* Setting color for paragraph text */
                        }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Opening the grid container div
                st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
            
                # Creating HTML elements with extracted data and adding them to the columns list
                columns = [
                    f"<div class='grid-item'><h2 style='color: #FF5733;'>🚝 Nearest Metro Stations:</h2><h3>{nearest_metro_stations}</h3></div>",
                    f"<div class='grid-item'><h2 style='color: #C70039;'>🎟️ Metro Ticket Price:</h2><h3>{metro_ticket_price}</h3></div>",
                    f"<div class='grid-item'><h2 style='color: #900C3F;'>🕙 Metro Timings:</h3><h3>{metro_timings}</h3></div>"
                ]

                # Joining all elements into a single string
                all_columns = "".join(columns)

                # Displaying all elements within a single <div> tag
                st.markdown(f"<div class='display:flex'>{all_columns}</div>", unsafe_allow_html=True)

    if select == "Normal-Ticket":
        st.title("Normal ticket booking site")
        st.warning("**Note**: This ticket is valid for **one transportation vehicle**")
        normal_ticket_booking("Hybrid - UTS","Metro - " + sel,Origin,destination,metro_ticket_price)

    if select == "UTS-Ticket":
            st.title("UTS - Hybrid ticket booking site")
            st.warning("**Note**: This ticket is valid for all transportation vehicles for 24 hours.")
            try:
                menu = {
                    "🗳️ UTS_Ticket_booking": "ticket_booking",
                    "🔐 Ticket_verify": "ticket_verify",
                }

                selected = option_menu("", list(menu.keys()), orientation="horizontal",key=12)


                page_funct = {
                    "ticket_booking": "1",
                    "ticket_verify": "2",
                }
                if page_funct[menu[selected]] == "1":
                    ticket_booking("Hybrid - UTS","Metro - " + sel,Origin,destination,metro_ticket_price)
                else:
                    st.subheader("Check the Ticket validity:")
                    # Check ticket validity
                    ticket_id_input = st.text_input("Enter Ticket ID to check validity:")
                    if st.button("Check Ticket Validity",use_container_width=True):
                        ticket_verify(ticket_id_input)

            except:
                print("do not raise error")

def cab_travel():
    with st.sidebar.container():
        image = Image.open(r"D:\streamlit\cab.png")
        st.image(image,use_column_width=True)
    with st.sidebar:
        select = st.selectbox("**select mode of ticket** :",["Normal-Ticket","UTS-Ticket"])
        # Create two columns in the Streamlit app layout
        col1, col2 = st.columns(2)

        # In the first column, create a dropdown (select box) for selecting the origin station
        # Populated with unique values from the 'Origin_station' column of the DataFrame
        with col1:
            Origin = st.selectbox("select origin: ", df["Origin_station"].to_list())

        # Filter the DataFrame to get the destinations corresponding to the selected origin station
        des = df[df["Origin_station"] == Origin]["Destination"]

        # In the second column, create a dropdown for selecting the destination station
        # Populated with unique values from the filtered 'Destination' column
        with col2:
            destination = st.selectbox("select destination : ", des.to_list())

        # Filter the DataFrame to get the row corresponding to the selected origin and destination
        res = df[(df["Origin_station"] == Origin) & (df["Destination"] == destination)]

    
        nearest_cab_booking_places = res["Nearest Cab Booking Places"].values[0]
        cab_booking_price = res["Cab Booking Price"].values[0]
        
        
        # Split the string by commas and strip whitespace from each station name
        nearest_cab_booking_places_list = [station.strip("[]").strip() for station in nearest_cab_booking_places.split(',')]
        st.markdown("<h3 style='color:Green;font-size:24px'><strong>select nearest cab bookings</strong></h3>",unsafe_allow_html=True)
        if select:
            sel = st.selectbox("",nearest_cab_booking_places_list)
        
        
        but = st.button("click here to check",use_container_width=True)
        if but:
            # Adding custom CSS styles using HTML within Markdown
                st.markdown(
                    """
                    <style>
                        .grid-container {
                            display: grid; /* Setting display property to grid for grid layout */
                            grid-template-columns: repeat(3, 1fr); /* Setting grid to have 3 columns */
                            grid-gap: 20px; /* Adding gap between grid items */
                        }
                        .grid-item {
                            background-color: #f9f9f9; /* Setting background color for grid items */
                            padding: 20px; /* Adding padding around grid items */
                            border-radius: 5px; /* Adding border radius to grid items */
                            margin-bottom: 20px; /* Adding margin to create space between rows */
                        }
                        .grid-item h2 {
                            color: #333333; /* Setting color for h2 headings */
                            margin-bottom: 10px; /* Adding margin below h2 headings */
                        }
                        .grid-item h3 {
                            color: #666666; /* Setting color for h3 headings */
                            margin-bottom: 5px; /* Adding margin below h3 headings */
                        }
                        .grid-item p {
                            color: black; /* Setting color for paragraph text */
                        }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Opening the grid container div
                st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
                

                # Creating HTML elements with extracted data and adding them to the columns list
                columns = [
                    f"<div class='grid-item'><h2 style='color: #581845;'>🚖 Nearest Cab Booking Places:</h2><h3>{nearest_cab_booking_places}</h3></div>",
                    f"<div class='grid-item'><h2 style='color: #FF5733;'>📠 Cab Booking Price:</h2><h3>{cab_booking_price}</h3></div>"
                ]

                # Joining all elements into a single string
                all_columns = "".join(columns)

                # Displaying all elements within a single <div> tag
                st.markdown(f"<div class='display:flex'>{all_columns}</div>", unsafe_allow_html=True)

    if select == "Normal-Ticket":
        st.title("Normal ticket booking site")
        st.warning("**Note**: This ticket is valid for **one transportation vehicle**")
        normal_ticket_booking("Hybrid - UTS","Cab - " + sel,Origin,destination,cab_booking_price)
    
    if select == "UTS-Ticket":
            st.title("UTS - Hybrid ticket booking site")
            st.warning("**Note**: This ticket is valid for all transportation vehicles for 24 hours.")
            try:
                menu = {
                    "🗳️ UTS_Ticket_booking": "ticket_booking",
                    "🔐 Ticket_verify": "ticket_verify",
                }

                selected = option_menu("", list(menu.keys()), orientation="horizontal",key=12)


                page_funct = {
                    "ticket_booking": "1",
                    "ticket_verify": "2",
                }
                if page_funct[menu[selected]] == "1":
                    ticket_booking("Hybrid - UTS","Cab - " + sel,Origin,destination,cab_booking_price)
                else:
                    st.subheader("Check the Ticket validity:")
                    # Check ticket validity
                    ticket_id_input = st.text_input("Enter Ticket ID to check validity:")
                    if st.button("Check Ticket Validity",use_container_width=True):
                        ticket_verify(ticket_id_input)

            except:
                print("do not raise error")
            
def train_travel():
    with st.sidebar.container():
        image = Image.open(r"D:\streamlit\engine.webp")
        st.image(image,use_column_width=True)
    with st.sidebar:
        select = st.selectbox(":green[**select mode of ticket** :",["Normal-Ticket","UTS-Ticket"])
        # Create two columns in the Streamlit app layout
        col1, col2 = st.columns(2)

        # In the first column, create a dropdown (select box) for selecting the origin station
        # Populated with unique values from the 'Origin_station' column of the DataFrame
        with col1:
            Origin = st.selectbox("select origin: ", df["Origin_station"].to_list())

        # Filter the DataFrame to get the destinations corresponding to the selected origin station
        des = df[df["Origin_station"] == Origin]["Destination"]

        # In the second column, create a dropdown for selecting the destination station
        # Populated with unique values from the filtered 'Destination' column
        with col2:
            destination = st.selectbox("select destination : ", des.to_list())

        # Filter the DataFrame to get the row corresponding to the selected origin and destination
        res = df[(df["Origin_station"] == Origin) & (df["Destination"] == destination)]

    
        nearest_local_trains = res["Nearest Local Trains"].values[0]
        train_ticket_price = res["Train Ticket Price"].values[0]
        train_timings = res["Train Timings"].values[0]
        
        
        # Split the string by commas and strip whitespace from each station name
        nearest_local_trains_list = [station.strip("[]").strip() for station in nearest_local_trains.split(',')]
        st.markdown("<h3 style='color:Green;font-size:24px'><strong>select nearest local trains</strong></h3>",unsafe_allow_html=True)
        if select:
            sel = st.selectbox("",nearest_local_trains_list)
        
        

        but = st.button("click here to check",use_container_width=True)
        
        if but:
            # Adding custom CSS styles using HTML within Markdown
                st.markdown(
                    """
                    <style>
                        .grid-container {
                            display: grid; /* Setting display property to grid for grid layout */
                            grid-template-columns: repeat(3, 1fr); /* Setting grid to have 3 columns */
                            grid-gap: 20px; /* Adding gap between grid items */
                        }
                        .grid-item {
                            background-color: #f9f9f9; /* Setting background color for grid items */
                            padding: 20px; /* Adding padding around grid items */
                            border-radius: 5px; /* Adding border radius to grid items */
                            margin-bottom: 20px; /* Adding margin to create space between rows */
                        }
                        .grid-item h2 {
                            color: #333333; /* Setting color for h2 headings */
                            margin-bottom: 10px; /* Adding margin below h2 headings */
                        }
                        .grid-item h3 {
                            color: #666666; /* Setting color for h3 headings */
                            margin-bottom: 5px; /* Adding margin below h3 headings */
                        }
                        .grid-item p {
                            color: black; /* Setting color for paragraph text */
                        }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Opening the grid container div
                st.markdown("<div class='grid-container'>", unsafe_allow_html=True)

            
                

                # Creating HTML elements with extracted data and adding them to the columns list
                columns = [
                    f"<div class='grid-item'><h2 style='color: #C70039;'>🚉 Nearest Local Trains:</h2><h3>{nearest_local_trains}</h3></div>",
                    f"<div class='grid-item'><h2 style='color: #900C3F;'>🎫 Train Ticket Price:</h2><h3>{train_ticket_price}</h3></div>",
                    f"<div class='grid-item'><h2 style='color: #581845;'>🕧 Train Timings:</h2><h3>{train_timings}</h3></div>"
                ]

                # Joining all elements into a single string
                all_columns = "".join(columns)

                # Displaying all elements within a single <div> tag
                st.markdown(f"<div class='display:flex'>{all_columns}</div>", unsafe_allow_html=True)

    if select == "Normal-Ticket":
        st.title("Normal ticket booking site")
        st.warning("**Note**: This ticket is valid for **one transportation vehicle**")
        normal_ticket_booking("Hybrid - UTS","Train - " + sel,Origin,destination,train_ticket_price)
            
        
    if select == "UTS-Ticket":
            st.title("UTS - Hybrid ticket booking site")
            st.warning("**Note**: This ticket is valid for all transportation vehicles for 24 hours.")
            try:
                menu = {
                    "🗳️ UTS_Ticket_booking": "ticket_booking",
                    "🔐 Ticket_verify": "ticket_verify",
                }

                selected = option_menu("", list(menu.keys()), orientation="horizontal",key=12)


                page_funct = {
                    "ticket_booking": "1",
                    "ticket_verify": "2",
                }
                if page_funct[menu[selected]] == "1":
                    ticket_booking("Hybrid - UTS","Train - " + sel,Origin,destination,train_ticket_price)
                else:
                    st.subheader("Check the Ticket validity:")
                    # Check ticket validity
                    ticket_id_input = st.text_input("Enter Ticket ID to check validity:")
                    if st.button("Check Ticket Validity",use_container_width=True):
                        ticket_verify(ticket_id_input)

            except:
                print("do not raise error")

menu_options = {
    "✈️ Travel_info": "travel_info",
    "🗺️ Map_view": "map_view",
    "🚌 Bus_trip": "bus_travel",
    "🚝 Metro_trip": "metro_trip",
    "🚕 Cab_trip": "cab_trip",
    "🚂 Train_trip": "train_trip"
}

try:
    selected = option_menu("", list(menu_options.keys()), orientation="horizontal")

    page_functions = {
        "travel_info": travel_info,
        "map_view": map_view,
        "bus_travel": bus_travel,
        "metro_trip": metro_travel,
        "cab_trip": cab_travel,
        "train_trip": train_travel
    }
    page_functions[menu_options[selected]]()

except:
    print("Dont raise error...")