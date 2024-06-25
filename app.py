import streamlit as st
import json
import random
from datetime import datetime

# Function to load restaurants from JSON file
def load_restaurants():
    try:
        with open('restaurants.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save restaurants to JSON file
def save_restaurants(restaurants):
    with open('restaurants.json', 'w') as f:
        json.dump(restaurants, f)

# Function to load events from JSON file
def load_events():
    try:
        with open('events.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save events to JSON file
def save_events(events):
    with open('events.json', 'w') as f:
        json.dump(events, f)

# Function to add an event
def add_event(event_type, restaurant):
    events = load_events()
    event = {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "type": event_type,
        "restaurant": restaurant
    }
    events.append(event)
    save_events(events)
    
#  function to delete a restaurant
def delete_restaurant(restaurant):
    restaurants = load_restaurants()
    restaurants.remove(restaurant)
    save_restaurants(restaurants)
    add_event("deletion", restaurant)

# Streamlit app
def main():
    st.title("Restaurant Roulette")

    # Load restaurants and events
    restaurants = load_restaurants()
    events = load_events()

    # Sidebar for restaurant list and adding new restaurants
    with st.sidebar:
        st.header("Restaurants disponibles")
        
        # Display the list of restaurants
        if restaurants:
            for restaurant in restaurants:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(restaurant)
                with col2:
                    if st.button("❌", key=f"delete_{restaurant}"):
                        delete_restaurant(restaurant)
                        st.rerun()
        else:
            st.write("No restaurants in the database.")
        
        # Add Restaurant button
        if st.button("Propose un nouveau restaurant !"):
            st.session_state.show_input = True
        
        # Show input box when Add Restaurant is clicked
        if 'show_input' in st.session_state and st.session_state.show_input:
            new_restaurant = st.text_input("Enter a new restaurant name")
            if st.button("Submit"):
                if new_restaurant and new_restaurant not in restaurants:
                    restaurants.append(new_restaurant)
                    save_restaurants(restaurants)
                    add_event("addition", new_restaurant)
                    st.success(f"Added {new_restaurant} to the database!")
                    st.session_state.show_input = False  # Hide the input box
                    st.rerun()  # Rerun the app to update the sidebar
                elif new_restaurant in restaurants:
                    st.warning("This restaurant is already in the database.")
                else:
                    st.warning("Please enter a restaurant name.")

    # Main area
    # Get Random Restaurant button
    if st.button("Choisir un Restaurant"):
        if restaurants:
            selected = random.choice(restaurants)
            add_event("selection", selected)
            st.session_state.last_selected = selected  # Store the selected restaurant
            st.rerun()  # Force a rerun to update the events
        else:
            st.warning("No restaurants in the database. Please add some!")

    # Display the last selected restaurant
    if 'last_selected' in st.session_state:
        st.success(f"🎉 Restaurant du jour : **{st.session_state.last_selected}**")

    # View Events
    st.subheader("Events")
    events = load_events()  # Reload events before displaying
    if events:
        for event in sorted(events, key=lambda x: datetime.strptime(x['date'], "%d/%m/%Y %H:%M:%S"), reverse=True):
            if event['type'] == 'selection':
                st.write(f"🍕 {event['date']}: The restaurant **{event['restaurant']}** has been picked")
            elif event['type'] == 'addition':
                st.write(f"🍔 {event['date']}: Nouveau restaurant ajouté à la liste : **{event['restaurant']}**")
            elif event['type'] == 'deletion':
                st.write(f"🗑️ {event['date']}: Restaurant supprimé de la liste : **{event['restaurant']}**")
    else:
        st.write("Pas encore d'évènements")

if __name__ == "__main__":
    main()