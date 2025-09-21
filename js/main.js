
// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api/plant';

// File Upload Handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const previewImage = document.getElementById('previewImage');

    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
        dropZone.addEventListener('dragover', handleDragOver);
        dropZone.addEventListener('drop', handleDrop);
    }
});

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displayPreviewAndUpload(file);
    }
}

function handleDragOver(event) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}

function handleDrop(event) {
    event.stopPropagation();
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
        displayPreviewAndUpload(file);
    }
}

function displayPreviewAndUpload(file) {

    const previewImage = document.getElementById('previewImage');
    const reader = new FileReader();

    console.log('Previewing file:', file.name);

    reader.onload = function(e) {
        previewImage.src = e.target.result;
        previewImage.classList.remove('hidden');
        uploadImage(file);
    };

    reader.readAsDataURL(file);
}

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    console.log('Uploading image:', file);
    const spinner = document.getElementById('spinner');
    spinner.classList.remove('hidden');
    try {
       // const response = await fetch(`${API_BASE_URL}/verify`, {
         //   method: 'POST',
           // body: formData
       // });
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'POST',
            body: formData
        });
        

        if (!response.ok) throw new Error('Network response was not ok');

        console.log('Image uploaded successfully!');
        const result = await response.json();
        displayPlantResult(result);
        spinner.classList.add('hidden');
    } catch (error) {
        console.error('Error:', error);
        spinner.classList.add('hidden');
        alert('Error uploading image. Please try again.');
    }
}

function displayPlantResult(plant) {
    console.log('Plant detected: ' + plant);
    const resultSection = document.getElementById('resultSection');
    const plantResult = document.getElementById('plantResult');
    
    resultSection.classList.remove('hidden');

    marked.marked(plant);

    // Convert Markdown to HTML
    let plantHTML = marked.marked(plant);
    if (typeof marked.marked === 'function') {
        plantHTML = marked.marked(plant);
    } else {
        console.warn('Marked.js is not available. Displaying raw Markdown.');
        plantHTML = plant;
    }

    plantResult.innerHTML = ``;
    plantResult.innerHTML = `
        <div class="plant-info p-4">
            <p class="text-gray-600"><strong>Scientific Name:</strong> ${plantHTML}</p>
        </div>
    `;
}

// Plant Search Functionality
async function searchPlants() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const noResults = document.getElementById('noResults');
    
    const query = searchInput.value.trim();
    if (!query) return;

    try {
        const response = await fetch(`${API_BASE_URL}/search?name=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // First check the response content type
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new TypeError('Response was not JSON');
        }

        // Get the raw text first for debugging
        const rawText = await response.text();
        console.log('Raw response:', rawText);

        // Try parsing the text into JSON
        let results;
        try {
            results = JSON.parse(rawText);
        } catch (parseError) {
            console.error('JSON Parse Error:', parseError);
            throw new Error('Invalid JSON response from server');
        }

        console.log('Parsed results:', results);
        
        if (!Array.isArray(results) || results.length === 0) {
            searchResults.innerHTML = '';
            noResults.classList.remove('hidden');
            return;
        }

        noResults.classList.add('hidden');
        displaySearchResults(results);
    } catch (error) {
        console.error('Error:', error);
        searchResults.innerHTML = '';
        noResults.innerHTML = 'An error occurred while searching. Please try again.';
        noResults.classList.remove('hidden');
    }
}

function displaySearchResults(plants) {
    const searchResults = document.getElementById('searchResults');
    
    searchResults.innerHTML = plants.map(plant => `
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
            <img src="${plant['Image URL']}" 
                 alt="${plant['Common Name']}" 
                 class="w-full h-48 object-cover"
                 onerror="this.src='img/calathea-ornata.png'">
            <div class="p-6">
                <h3 class="text-xl font-bold text-green-700 mb-2">${plant['Common Name']}</h3>
                <p class="text-gray-600 mb-2"><em>${plant['Scientific Name']}</em></p>
                <div class="space-y-2">
                    <p class="text-gray-600"><strong>Family:</strong> ${plant['Family']}</p>
                    <p class="text-gray-600"><strong>Native Region:</strong> ${plant['Native Region']}</p>
                    <p class="text-gray-600"><strong>Air Purification:</strong> ${plant['Air Pollutants Removed']}</p>
                    <p class="text-gray-600"><strong>Care Level:</strong> ${plant['Growth Rate'] === 'Fast' ? 'Easy' : plant['Growth Rate'] === 'Moderate' ? 'Medium' : 'Advanced'}</p>
                </div>
            </div>
        </div>
    `).join('');
}