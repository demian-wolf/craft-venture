let map;
let marker;

async function initMap() {
    const position = { lat: -25.344, lng: 131.031 };

    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("map"), {
        zoom: 4,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    google.maps.event.addListener(map, "click", (event) => {  
        let pos = event.latLng.toJSON();
        
        lngElement = document.getElementsByName("lng")[0];
        lngElement.value = pos.lng;

        latElement = document.getElementsByName("lat")[0];
        latElement.value = pos.lat;

        submitButton = document.getElementById("submitButton");
        submitButton.disabled = false;

        placeMarker(event.latLng);
    });
}

async function placeMarker(location) {    
    if (marker != null) {
        marker.map = null
    }
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    marker = new AdvancedMarkerElement({
        map: map,
        position: location,
        title: "",
    });
}

function loadMap() {
    initMap().then((text) => {
        console.log(text);
    }).catch((error) => {
        console.error('Error initializing map:', error);
    });
}

document.addEventListener('DOMContentLoaded', loadMap);
