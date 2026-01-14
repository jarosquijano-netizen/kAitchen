// Test the cleaning schedule API response
fetch('http://localhost:7000/api/cleaning/schedule/2026-01-12')
    .then(response => response.json())
    .then(data => {
        console.log('Schedule response:', data);
        console.log('Schedule data type:', typeof data.schedule);
        console.log('Schedule data:', data.schedule);
        
        if (data.schedule) {
            console.log('Schedule keys:', Object.keys(data.schedule));
        }
    })
    .catch(error => console.error('Error:', error));
