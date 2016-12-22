// Google Maps Variables
var geocoder;
var map;
var placesService;
var infoWindow;

// Array to keep track of map markers
var markersArray = [];

// four square api variables
var fourSquareKey = 'LECWBWPT1G4HKYS2UMOIG0TVROVLEODL2AIYH1SYK4ZOZSCM';
var fourSquareId = 'GEYHVEZTATSETIP3J4ZDFIHTQWIPPKLPRV0VQUF1P23L1JJ2';
var fourSquareRestaurant = '4d4b7105d754a06374d81259';

(function($) {
    "use strict"; // Start of use strict

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function(){ 
            $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    });

    $('.list-group-item').hover();
    
})(jQuery); // End of use strict

/**
 * Initialize google map variables
 */
function initMap() {

    /* Map Setup - Initial map is the UK */
    var latlng = new google.maps.LatLng(53.181957, -3.876466);
    var mapOptions = {
        zoom: 6,
        center: latlng
    };

    /* Initialize Google Services */
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    geocoder = new google.maps.Geocoder();
    placesService = new google.maps.places.PlacesService(map);
    infoWindow = new google.maps.InfoWindow();
}


/**
 * Convert the location the user entered into coordinates to search restaurants using Google Places.
 */
function findLocation() {

    /* Get information user entered */
    var location = document.getElementById("location-entry").value;
    var recipe = document.getElementById("recipe-entry").value;

    var ll = null;

    /* Convert location into coordinates and retrieve restaurants */
    geocoder.geocode( {'address': location}, function(results, status) {
        if (status == 'OK') {
            console.log(results);
            console.log(results[0].geometry.location.lat());

            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            ll = latitude.toFixed(2)+ ',' + longitude.toFixed(2);
            console.log(ll);

        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });

    /* Rest request to get restaurant information based on user's query */
    $.ajax({
        type:'get',
        url: 'https://api.foursquare.com/v2/venues/search',
        data: {client_id: fourSquareKey, client_secret: fourSquareId, ll: '50.91,-1.40',
            query: recipe, v:'20161130', categoryId: fourSquareRestaurant, intent: 'browse',
            radius: 5000},
        success: function(data) {

            /* Clear the previous markers */
            clearMarkers();

            /* Place markers on the map */
            var venues = data.response.venues;
            for(var i = 0; i < venues.length; i++) {
                console.log(venues[i]);
                createMarker(venues[i]);
            }

            /* Set the map boundaries */
            var bounds = new google.maps.LatLngBounds();
            for (i = 0; i < markersArray.length; i++) {
                bounds.extend(markersArray[i].getPosition());
            }
            map.fitBounds(bounds);
            map.setCenter(bounds.getCenter());
        },
        error: function (xhr) {
            console.log(xhr.status + ": " + xhr.responseText);
        }

    });
}

/**
 * Place a marker on the map with restaurant name
 * @param place Place object from Google Places
 */
function createMarker(place) {

    /* Create the marker */
    var latlng = {lat: place.location.lat, lng: place.location.lng};
    var marker = new google.maps.Marker({
        map: map,
        position: latlng
    });

    var venueId = place.id;
    $.ajax({
        type:'get',
        url: 'https://api.foursquare.com/v2/venues/' + venueId + '/photos',
        data: {client_id: fourSquareKey, client_secret: fourSquareId, v:'20161130'},
        success: function(data) {

            if(data.response.photos.count > 0)
                console.log(data);
        },
        error: function (xhr) {
            console.log(xhr.status + ": " + xhr.responseText);
        }

    });

    // Set the default red Icon
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');

    // Push marker to array
    markersArray.push(marker);

    /* Marker listener */
    marker.addListener('click', function() {
        infoWindow.setContent(place.name);
        infoWindow.open(map,marker);
    });

    /* Add restaurant information to list beside map */
    addToList(place, marker);
}


/**
 * Add restaurant information to list beside the map
 * @param place Restaurant object
 * @param marker Google Maps Marker
 */
function addToList(place, marker) {

    $('.list-group').append('<div><a class="list-group-item list-group-item-action" id="' + place.id + '"><h6>' + place.name + '</h6></a></div>');
    $('#' + place.id).hover(function() {
        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
    }, function() {
        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png')
    });
}

/**
 * Remove all markers from the map and clear the list of restaurants
 */
function clearMarkers() {

    // Remove markers from the map
    for(var i = 0; i < markersArray.length; i++) {
        markersArray[i].setMap(null);
    }

    // Reset the markers array
    markersArray.length = 0;

    // Reset the restaurant list
    $('.list-group').html('');
}

