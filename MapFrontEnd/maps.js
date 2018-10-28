        var map;
        var directionsService;
        var polylines = [];
        var shadows = [];
        var data = [];
        var infowindow;
        function initMap() {
            map = new google.maps.Map(document.getElementById('map'), {
                center: {lat:40.109631,lng:-88.227170},
                zoom: 13,
            });


            infoWindow = new google.maps.InfoWindow;

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

            // get current location
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


            google.maps.event.addDomListener(document.getElementById('form'), 'submit', function(e) {
                calcRoute(
                    document.getElementById('to').value
                );

                // prevent the form from really submitting
                e.preventDefault();
                return false;
            });

            directionsService = new google.maps.DirectionsService();


            // get the bounds of the polyline
            // http://stackoverflow.com/questions/3284808/getting-the-bounds-of-a-polyine-in-google-maps-api-v3
            google.maps.Polyline.prototype.getBounds = function(startBounds) {
                if(startBounds) {
                    var bounds = startBounds;
                }
                else {
                    var bounds = new google.maps.LatLngBounds();
                }
                this.getPath().forEach(function(item, index) {
                    bounds.extend(new google.maps.LatLng(item.lat(), item.lng()));
                });
                return bounds;
            };
        }


        // this function calculates multiple suggested routes.
        // We will draw 3 (broad stroke) suggested routs in grey.  These are broad to click on them easier.
        // We duplicate these routes with a thin, colored line; only route 0 is shown.
        function calcRoute(end) {
            var request = {
                origin: currentLocation,
                destination: end,
                provideRouteAlternatives: true,
                travelMode: google.maps.TravelMode['WALKING']
            };
            directionsService.route(request, function(response, status) {
                // clear former polylines
                for(var j in  polylines ) {
                    polylines[j].setMap(null);
                    shadows[j].setMap(null);
                }
                polylines = [];
                shadows = [];
                data = [];
                if (status == google.maps.DirectionsStatus.OK) {
                    var bounds = new google.maps.LatLngBounds();
                    for(var i in response.routes) {
                        // let's make the first suggestion highlighted;
                        var hide = (i==0 ? false : true);
                        var shadow = drawPolylineShadow(response.routes[i].overview_path, '#666666');
                        var line = drawPolyline(response.routes[i].overview_path, '#0000ff', hide);
                        polylines.push(line);
                        shadows.push(shadow);
                        // let's add some data for the infoWindow
                        data.push({
                            distance: response.routes[i].legs[0].distance,
                            duration: response.routes[i].legs[0].duration,
                            end_address: response.routes[i].legs[0].end_address,
                            start_address: response.routes[i].legs[0].start_address,
                            end_location: response.routes[i].legs[0].end_location,
                            start_location: response.routes[i].legs[0].start_location
                        });
                        bounds = line.getBounds(bounds);
                        google.maps.event.addListener(shadow, 'click', function(e) {
                            // detect which route was clicked on
                            var index = shadows.indexOf(this);
                            highlightRoute(index, e);
                        });

                    }
                    map.fitBounds(bounds);
                }
            });
        }
        // this makes one of the colored routes visible.
        function highlightRoute(index, e) {
            for(var j in  polylines ) {
                if(j==index) {
                    //var color = '#0000ff';
                    polylines[j].setMap(map);
                    // feel free to customise this string
                    var contentString =
                        '<span>'+ data[j].distance.text +'</span><br/>'+
                        '<span>'+ data[j].duration.text +'</span><br/>'+
                        '<span>route: '+ j +'</span><br/>'+
                        //'From: <span>'+ data[j].start_address +'</span><br/>'+
                        //'To: <span>'+ data[j].end_address +'</span><br/>'+
                        '';
                    if(e) {
                       var position = new google.maps.LatLng(e.latLng.lat(), e.latLng.lng());
                        // it may be needed to close the previous infoWindow
                        if(infowindow) {
                            infowindow.close();
                            infowindow = null;
                        }
                        infowindow = new google.maps.InfoWindow({
                            content: contentString,
                            position: position,
                            map: map
                        });
                        //infowindow.open(map, polylines[j]);
                    }
                }
                else {
                    polylines[j].setMap(null);
                }
            }
        }
        // returns a polyline.
        // if hide is set to true, the line is not put on the map
        function drawPolyline(path, color, hide) {
            var line = new google.maps.Polyline({
                path: path,
                strokeColor: color,
                strokeOpacity: 0.9,
                strokeWeight: 3
            });
            if(! hide) {
                line.setMap(map);
            }
            return line;
        }
        function drawPolylineShadow(path, color, hide) {
            var line = new google.maps.Polyline({
                path: path,
                strokeColor: color,
                strokeOpacity: 0.4,
                strokeWeight: 7
            });
            if(! hide) {
                line.setMap(map);
            }
            return line;
        }
        google.maps.event.addDomListener(window, 'load', initMap);