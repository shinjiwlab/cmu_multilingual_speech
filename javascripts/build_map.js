    var map = L.map('map', {
        minZoom: 2,
        maxZoom: 5,
    });

    var cartodbAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>';

    var positron = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', ).addTo(map);


    map.setView([0, 0], 0);
    
// var myLines = [{
//     "type": "Point",
//     "coordinates": [0, 0],
//     "popupContent": "<a href='https://www.google.com'>hello</a>"
// }, {
//     "type": "Point",
//     "coordinates": [30, 30],
//     "popupContent": "world"
// }];

var myStyle = {
    "color": "#ff7800",
    "weight": 5,
    "opacity": 0.65,
    "radius": 500000
};

var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.popupContent) {
        layer.bindPopup(feature.popupContent);
    }
}

L.geoJSON(langs,
        {
    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
    },
    onEachFeature: onEachFeature}

).addTo(map);

    circle.bindPopup("<b>Hello world!</b><br>I am a popup.");
