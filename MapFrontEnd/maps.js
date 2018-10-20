// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
var currentLocation = {lat:40.109631,lng:-88.227170};

function initMap() {

    /*
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
        lat
        });
    }*/

    var map = new google.maps.Map(document.getElementById('map'), {
        mapTypeControl: false,
        //center: {lat:40.109631,lng:-88.227170},
        center: currentLocation,
        //center: {latitude, longitude},
        zoom: 13
    });

    infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        currentLocation = pos;

        var marker = new google.maps.Marker({
            position:pos,
            map:map,
            icon: 'http://www.robotwoods.com/dev/misc/bluecircle.png'
            //icon: src = 'current.png'
        });
        //infoWindow.setPosition(pos);
        //infoWindow.setContent('Current location.');
        //infoWindow.open(map);
        map.setCenter(pos);
        map.setZoom(16);
        }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    // array of markers
    var markers = [
        {
        coords:{lat:40.108241,lng:-88.223865},
        //iconImage: src = 'robbery.png',
        iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
        content: '<h1>Robbery</h1>'
        },

        {
        coords:{lat:40.110342,lng: -88.228865},
        //iconImage: src = 'assault.png',
        iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
        content: '<h1>Assault</h1>'
        },
        {
        coords:{lat:40.107938,lng: -88.229562},
        //iconImage: src = 'assault.png',
        iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
        content: '<h1>Assault</h1>'
        }
    ];

    // loop through markers
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

    new AutocompleteDirectionsHandler(map);


}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}


/**
* @constructor
*/
function AutocompleteDirectionsHandler(map) {
    this.map = map;
    this.originPlaceId = null;
    this.destinationPlaceId = null;
    this.travelMode = 'WALKING';
    //var originInput = document.getElementById('origin-input');
    var destinationInput = document.getElementById('destination-input');
    var modeSelector = document.getElementById('mode-selector');
    this.directionsService = new google.maps.DirectionsService;
    //this.directionsDisplay = new google.maps.DirectionsRenderer;
    //this.directionsDisplay.setMap(map);

    // added draggable marker option to the renderer and right panel
    this.directionsDisplay = new google.maps.DirectionsRenderer({
        draggable: true,
        map: map,
        panel: document.getElementById('right-panel')
    }); 
    //var originAutocomplete = new google.maps.places.Autocomplete(
    //    originInput, {placeIdOnly: true});
    var destinationAutocomplete = new google.maps.places.Autocomplete(
        destinationInput, {placeIdOnly: true});

    this.directionsDisplay.addListener('directions_changed', function() {
        computeTotalDistance(directionsDisplay.getDirections());
    });

    this.setupClickListener('changemode-walking', 'WALKING');
    this.setupClickListener('changemode-transit', 'TRANSIT');
    this.setupClickListener('changemode-driving', 'DRIVING');

    //this.setupPlaceChangedListener(originAutocomplete, 'ORIG');
    this.setupPlaceChangedListener(destinationAutocomplete, 'DEST');

    //this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(destinationInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
}

// Sets a listener on a radio button to change the filter type on Places
// Autocomplete.
AutocompleteDirectionsHandler.prototype.setupClickListener = function(id, mode) {
    var radioButton = document.getElementById(id);
    var me = this;
    radioButton.addEventListener('click', function() {
        me.travelMode = mode;
        me.route();
    });
;

AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function(autocomplete, mode) {
    var me = this;
    autocomplete.bindTo('bounds', this.map);
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.place_id) {
            window.alert("Please select an option from the dropdown list.");
            return;
        }
        //if (mode === 'ORIG') {
        //  me.originPlaceId = place.place_id;
        //} else {
        me.destinationPlaceId = place.place_id;
        //}
        me.route();
    });

};
  
AutocompleteDirectionsHandler.prototype.route = function() {
    if (!this.destinationPlaceId) {
        return;
    }
    var me = this;

    this.directionsService.route({
        //origin: {'placeId': this.originPlaceId},
        origin: currentLocation,
        destination: {'placeId': this.destinationPlaceId},
        travelMode: this.travelMode,
        //provideRouteAlternatives: true
    }, function(response, status) {
        if (status === 'OK') {
            me.directionsDisplay.setDirections(response);
        } else {
        window.alert('Directions request failed due to ' + status);
        }
    });
}}   
