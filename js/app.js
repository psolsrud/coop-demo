var selection;
var selectedLayer;

L.mapbox.accessToken = 'pk.eyJ1Ijoid3RnZW9ncmFwaGVyIiwiYSI6ImNpdGFicWJqYjAwdzUydHM2M2g0MmhsYXAifQ.oO-MYNUC2tVeXa1xYbCIyw';
var map = L.mapbox.map('map');
//set initial view
map.setView([45.74172, -95.943603], 8);

L.control.layers({
    'Mapbox Streets': L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11').addTo(map),
    'Mapbox Light':  L.mapbox.styleLayer('mapbox://styles/mapbox/satellite-streets-v9')
}).addTo(map);

// Set style function that sets fill color property
// define the styles for the my layer (unselected and selected)
function myStyle(feature) {
    return {
        fillColor: "#FF00FF",
        fillOpacity: 1,
        color: '#B04173',
    };
}

function mySelectedStyle(feature) {
    return {
        fillColor: "#00FFFB",
        color: '#0000FF',
        fillOpacity: 1
    };
}

// handle clicks on the map that didn't hit a feature
map.addEventListener('click', function (e) {
    if (selection) {
        resetStyles();
        selection = null;
    }
});

// function to set the old selected feature back to its original symbol. Used when the map or a feature is clicked.
function resetStyles() {
    selectedLayer.resetStyle(selection);
}

// handle click events on my features
function forEachFeature(feature, layer) {
    layer.on({
        click: function (e) {
            if (selection) {
                resetStyles();
            }

            e.target.setStyle(mySelectedStyle());
            selection = e.target;
            selectedLayer = myLayer;

            map.fitBounds(e.target.getBounds());

            L.DomEvent.stopPropagation(e); // stop click event from being propagated further
        }
    });
}

function polygonClick(e) {

    $('#my-modal').modal({
        show: 'true'
    });

    var feature = e.layer.feature;

    // reset classes
    $(".title").empty();
    $(".speed").empty();
    $(".digital_tv").empty();
    $(".phone").empty();
    $(".home_automation").empty();

    $(".title").prepend('Available Services');
    $(".speed").prepend('<div class="product-content"><img src="https://static.wixstatic.com/media/aee650_f58d71badf48432bbd277b61d9314ba2~mv2.png/v1/fill/w_188,h_188,al_c/aee650_f58d71badf48432bbd277b61d9314ba2~mv2.png" style="vertical-align: middle;width:60px;height:60px;">' + '&nbsp;&nbsp;' + feature.properties.speed + ' Mb</div>');
    $(".digital_tv").prepend('<div class="product-content"><img src="https://static.wixstatic.com/media/aee650_20ebd546c5524639a900e589108450e5~mv2.png/v1/fill/w_188,h_188,al_c/aee650_20ebd546c5524639a900e589108450e5~mv2.png" style="vertical-align: middle;width:60px;height:60px;">' + '&nbsp;&nbsp;' + feature.properties.digital_tv + '</div>');
    $(".phone").prepend('<div class="product-content"><img src="https://static.wixstatic.com/media/aee650_0d4fdf26e061469dba4e8f2a83d81147~mv2.png/v1/fill/w_188,h_188,al_c/aee650_0d4fdf26e061469dba4e8f2a83d81147~mv2.png" style="vertical-align: middle;width:60px;height:60px;">' + '&nbsp;&nbsp;' + feature.properties.phone + '</div>');
    $(".home_automation").prepend('<div class="product-content"><img src="https://static.wixstatic.com/media/aee650_7d28d8b31fb849b1aaf528ca5296ea06~mv2.png/v1/fill/w_188,h_188,al_c/aee650_7d28d8b31fb849b1aaf528ca5296ea06~mv2.png" style="vertical-align: middle;width:60px;height:60px;">' + '&nbsp;&nbsp;' + feature.properties.home_autom + '</div>');
}

// Null variable that will hold layer
var myLayer = L.geoJson(null, { onEachFeature: forEachFeature, style: myStyle }).addTo(map);

var polygons = L.featureGroup().on('click', polygonClick).addTo(map);

var territories = "data/map.geojson";

$.getJSON(territories, function (data) {
    L.geoJson(data, {
        onEachFeature: forEachFeature,
        style: myStyle
    }).addTo(polygons);
});

// Fit all markers after 1/2 second.
//    used to counter async loading
setTimeout(function () {
    map.fitBounds(polygons.getBounds());
}, 500);
