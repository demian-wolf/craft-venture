let map;
let marker;

async function initMap() {
    // The location of Uluru
    const position = { lat: -25.344, lng: 131.031 };

    // Request needed libraries.
    //@ts-ignore
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
        zoom: 4,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    // The marker, positioned at Uluru
    // const marker = new AdvancedMarkerElement({
    //     map: map,
    //     position: position,
    //     title: "Uluru",
    // });



    google.maps.event.addListener(map, "click", (event) => {
        placeMarker(event.latLng);
    });

    console.log('Map initialized successfully.');
    return 'Initialization complete'; // Optional: return a value if needed
}

async function placeMarker(location) {
    if (marker != null) {
        marker.map = null
    }
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    marker = new AdvancedMarkerElement({
        map: map,
        position: location,
        title: "Uluru",
    });
}

// This function can be called when the DOM content is loaded
function loadMap() {
    initMap().then((text) => {
        console.log(text); // Logs "Initialization complete"
    }).catch((error) => {
        console.error('Error initializing map:', error);
    });
}

// Use DOMContentLoaded to ensure the map initializes after the HTML has loaded
document.addEventListener('DOMContentLoaded', loadMap);