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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(itineraryData),
        });
        const newItinerary = await response.json();
        if (response.ok) {
            displayItineraries([newItinerary], true); 
        } else {
            throw new Error('Failed to create itinerary');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function updateItinerary(id, updatedData) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData),
        });
        if (!response.ok) {
            throw new Error('Failed to update itinerary');
        }
        await fetchItineraries(); 
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
        await fetchItineraries(); 
    } catch (error) {
        console.error('Error:', error);
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