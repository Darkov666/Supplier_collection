/*
    function addPersonField() {
        const additionalPeopleDiv = document.getElementById('additional-people');
        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'additional_people';
        input.placeholder = 'Nombre de Persona Adicional';
        input.classList.add('input', 'input-bordered', 'w-full', 'my-2');
        additionalPeopleDiv.appendChild(input);
    }

    // Para el autocompletado de lugares
    const placesAutocomplete = places({
        appId: 'YOUR_PLACES_APP_ID',
        apiKey: 'YOUR_PLACES_API_KEY',
        container: document.querySelector('#id_pickup_start')
    });

    placesAutocomplete.on('change', function resultSelected(e) {
        document.querySelector('#id_pickup_start').value = e.suggestion.value;
    });
*/