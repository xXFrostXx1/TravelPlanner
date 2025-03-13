const API_URL = process.env.YOUR_API_URL || 'http://localhost:3000/api/itineraries';

async function fetchItineraries() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            const message = await response.text() || 'Failed to fetch itineraries';
            throw new Error(message);
        }
        const itineraries = await response.json();
        displayItineraries(itineraries);
    } catch (error) {
        console.error('Error:', error);
        displayError('Failed to load itineraries. Please try again.');
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
            const message = await response.text() || 'Failed to create itinerary';
            throw new Error(message);
        }
        const newItinerary = await response.json();
        displayItineraries([newItinerary], true);
    } catch (error) {
        console.error('Error:', error);
        displayError('An error occurred while adding the itinerary. Please try again.');
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
            const message = await response.text() || 'Failed to update itinerary';
            throw new Error(message);
        }
        await fetchItineraries();
    } catch (error) {
        console.error('Error:', error);
        displayError('Updating the itinerary failed. Please try again.');
    }
}

async function deleteItinerary(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const message = await response.text() || 'Failed to delete itinerary';
            throw new Error(message);
        }
        await fetchItineraries();
    } catch (error) {
        console.error('Error:', error);
        displayError('An error occurred while deleting the itinerary. Please try again.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchItineraries();
    document.getElementById('itineraryForm').addEventListener('submit', (event) => {
        event.preventDefault(); 
        const formData = new FormData(event.target);
        const itineraryData = {}; 
        formData.forEach((value, key) => {
            itineraryData[key] = value; 
        });
        addItinerary(itineraryData); 
    });
    
    document.getElementById('itinerariesContainer').addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-button')) { 
            const id = event.target.dataset.id; 
            deleteItinerary(id);
        } else if (event.target.classList.contains('update-button')) { 
            const id = event.target.dataset.id;
            const updatedData = {}; 
            updateItinerary(id, updatedData);
        }
    });
});

function displayItineraries(itineraries, append = false) {
    const container = document.getElementById('itinerariesList'); 
    if (!append) { 
        container.innerHTML = ''; 
    }
    itineraries.forEach((itinerary) => {
        const itineraryElement = document.createElement('div');
        itineraryElement.textContent = itinerary.name; 
        container.appendChild(itineraryElement); 
    });
}

function displayError(message) {
    const container = document.getElementById('errorContainer'); 
    container.textContent = message; 
    container.style.display = 'block'; 
}