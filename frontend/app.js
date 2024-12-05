const API_URL = process.env.YOUR_API_URL || 'http://localhost:3000/api/itineraries';

async function fetchItineraries() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('Failed to fetch itineraries');
        }
        const itineraries = await response.json();
        displayItineraries(itineraries);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function addItinerary(itineraryData) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(itineraryData),
        });
        if (!response.ok) {
            throw new Error('Failed to create itinerary');
        }
        const newItinerary = await response.json();
        displayItineraries([newItinerary], true);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function updateItinerary(id, updatedData) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData),
        });
        if (!response.ok) {
            throw new Error('Failed to update itinerary');
        }
        await fetchItineraries(); // Refresh list after update
    } catch (error) {
        console.error('Error:', error);
    }
}

async function deleteItinerary(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete itinerary');
        }
        await fetchItineraries(); // Refresh list after deletion
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchItineraries(); // Initially fetch all itineraries

    document.getElementById('itineraryForm').addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the form from submitting in the traditional manner
        const formData = new FormData(event.target);
        const itineraryData = {}; 
        formData.forEach((value, key) => {
            itineraryData[key] = value; // Convert form data into an object
        });
        addItinerary(itineraryData); // Add the new itinerary
    });
    
    document.getElementById('itinerariesContainer').addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-button')) { 
            const id = event.target.dataset.id; // Get the data-id attribute
            deleteItinerary(id);
        } else if (event.target.classList.contains('update-button')) { 
            const id = event.target.dataset.id;
            const updatedData = {}; // Placeholder for real update data
            updateItinerary(id, updatedData);
        }
    });
});

function displayItineraries(itineraries, append = false) {
    const container = document.getElementById('itinerariesList'); 
    if (!append) { // Clear the container if not appending
        container.innerHTML = ''; 
    }
    itineraries.forEach((itinerary) => {
        const itineraryElement = document.createElement('div');
        itineraryElement.textContent = itinerary.name; // Set itinerary name as text content
        container.appendChild(itineraryElement); // Add to the container
    });
}