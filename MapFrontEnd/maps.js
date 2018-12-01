var currentLocation = {lat:40.109631,lng:-88.227170};
var map;
var directionsService;
var crimeData = []; 
var coordinates = [];
var markers = [];

function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        center: currentLocation,
        zoom: 13
    });

    plotCrimes();


    // get current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        currentLocation = pos;

        var currentLocationMarker = new google.maps.Marker({
            position:pos,
            map:map,
            icon: 'http://www.robotwoods.com/dev/misc/bluecircle.png'
        });
        map.setCenter(pos);
        map.setZoom(16);
        }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // if browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }


    new AutocompleteDirectionsHandler(map);
}



function plotCrimes() {

    // get csv file
    $(document).ready(function() {
        $.ajax({
           type: "GET",
           url: "test.csv",
           dataType: "text",
           success: function(test) {processData(test);}
         });
     });


    // process crime data from csv, add markers to map
    function processData(allText) {
        var allTextLines = allText.split(/\r\n|\n/);
        var headers = allTextLines[0].split(',');

        // parse csv text into a 2d array
        for (var i=1; i<allTextLines.length; i++) {
            var data = allTextLines[i].split(',');
            if (data.length == headers.length) {

                var tarr = [];
                for (var j=0; j<headers.length; j++) {
                        tarr.push(data[j]);
                }
                crimeData.push(tarr);
            }
        }


        // pick out latitude and longitude data from all the data, store that in crimes array
        for (var i = 0; i < crimeData.length; i++) {
            var row = [];
            for (var j = 1; j <= 2; j++) {
                row.push(crimeData[i][j]);
            }
            coordinates.push(row);
        }


        // loop through crimes and create markers for each
        for (var i = 0; i < coordinates.length; i++) {
            markers.push(
                {
                    coords:{lat: Number(coordinates[i][0]),lng: Number(coordinates[i][1])},
                    iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
                    content: '<h1>Sample Data</h1>'
                }
            );
        }


        // add each crime marker to the map
        for(var i = 0; i < markers.length; i++){
            // add marker
            addMarker(markers[i]);
        }


        // add marker function
        function addMarker(props){
            var marker = new google.maps.Marker({
            position:props.coords,
            map:map,
            });

            // check for custom icon
            if(props.iconImage){
                // set icon image
                marker.setIcon(props.iconImage);
            }

            // check content
            if(props.content){
                var infoWindow = new google.maps.InfoWindow({
                    content:props.content
                });

                marker.addListener('click', function(){
                    infoWindow.open(map, marker);
                });
            }
        }
    }
}



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}


// set up autocomplete directions functionality
function AutocompleteDirectionsHandler(map) {
    this.map = map;
    this.originPlaceId = null;
    this.destinationPlaceId = null;
    this.travelMode = 'WALKING';

    var destinationInput = document.getElementById('destination-input');
    var modeSelector = document.getElementById('mode-selector');
    this.directionsService = new google.maps.DirectionsService;


    // added draggable marker option to the renderer and right panel
    this.directionsDisplay = new google.maps.DirectionsRenderer({
        draggable: true,
        map: map,
        panel: document.getElementById('right-panel')
    }); 


    var destinationAutocomplete = new google.maps.places.Autocomplete(
        destinationInput, {placeIdOnly: true});

    this.directionsDisplay.addListener('directions_changed', function() {
        computeTotalDistance(directionsDisplay.getDirections());
    });

    this.setupClickListener('changemode-walking', 'WALKING');
    this.setupClickListener('changemode-transit', 'TRANSIT');
    this.setupClickListener('changemode-driving', 'DRIVING');

    this.setupPlaceChangedListener(destinationAutocomplete, 'DEST');

    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(destinationInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
}


// sets a listener on a radio button to change the filter type on places autocomplete
AutocompleteDirectionsHandler.prototype.setupClickListener = function(id, mode) {
    var radioButton = document.getElementById(id);
    var me = this;
    radioButton.addEventListener('click', function() {
        me.travelMode = mode;
        me.route();
    });
;


// sets up a listener for a new destination
AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function(autocomplete, mode) {
    var me = this;
    autocomplete.bindTo('bounds', this.map);
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.place_id) {
            window.alert("Please select an option from the dropdown list.");
            return;
        }

        me.destinationPlaceId = place.place_id;
        me.route();
    });

};
  
//find route from current location to autocomplete location
AutocompleteDirectionsHandler.prototype.route = function() {
    if (!this.destinationPlaceId) {
        return;
    }
    var me = this;

    this.directionsService.route({
        origin: currentLocation,
        destination: {'placeId': this.destinationPlaceId},
        provideRouteAlternatives: true,
        travelMode: this.travelMode,
    }, function(response, status) {
        if (status === 'OK') {
            var polyline = new google.maps.Polyline({
              path: [],
              strokeColor: '#FF0000',
              strokeWeight: 3
            });
            var bounds = new google.maps.LatLngBounds();


            var legs = response.routes[0].legs;
            for (i=0;i<legs.length;i++) {
              var steps = legs[i].steps;
              for (j=0;j<steps.length;j++) {
                var nextSegment = steps[j].path;
                for (k=0;k<nextSegment.length;k++) {
                  polyline.getPath().push(nextSegment[k]);
                  bounds.extend(nextSegment[k]);
                }
              }
            }

            polyline.setMap(map);
            map.fitBounds(bounds);

            var pos1 = new google.maps.LatLng(40.110413,-88.223920);
            var marker1 = new google.maps.Marker({position: pos1, map: map});

            if (google.maps.geometry.poly.isLocationOnEdge(pos1, polyline, 0.0005)) {
                console.log("POS 1: Relocate!");
            } else {
                console.log("POS 1: No danger");
            }

            var pos2 = new google.maps.LatLng(40.110434,-88.223475);
            var marker2 = new google.maps.Marker({position: pos2, map: map});

            if (google.maps.geometry.poly.isLocationOnEdge(pos2, polyline, 0.0005)) {
                console.log("POS 2: Relocate!");
            } else {
                console.log("POS 2: No danger");
            }

            var pos3 = new google.maps.LatLng(40.110452,-88.222957);
            var marker3 = new google.maps.Marker({position: pos3, map: map});

            if (google.maps.geometry.poly.isLocationOnEdge(pos3, polyline, 0.0005)) {
                console.log("POS 3: Relocate!");
            } else {
                console.log("POS 3: No danger");
            }

            me.directionsDisplay.setDirections(response);

            

        } else {
        window.alert('Directions request failed due to ' + status);
        }
    });
}}

