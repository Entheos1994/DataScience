// Google Maps Variables
var geocoder;
var map;
var placesService;
var infoWindow;

// Arrays to keep track of map markers and place ids
var markersArray = [];
var placeIds = [];

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

    /* Convert location into coordinates and retrieve restaurants */
    geocoder.geocode( {'address': location}, function(results, status) {
        if (status == 'OK') {
            console.log(results);
            placesService.radarSearch({
                location: results[0].geometry.location,
                radius: 5000,
                type: ['restaurant']
            }, radarCallback);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });



}

function radarCallback(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {


        // Clear the previous search
        clearMarkers();

        for(var i = 0; i < results.length; i++) {
            placeIds.push(results[i].place_id);

            geocoder.geocode({'placeId': results[i].place_id}, function(results, status) {
                console.log(results);
            });
            createMarker(results[i]);
        }

        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < markersArray.length; i++) {
            bounds.extend(markersArray[i].getPosition());
        }

        map.fitBounds(bounds);
        map.setCenter(bounds.getCenter());

        console.log(placeIds.length);
    }
}

/**
 * Place a marker on the map with restaurant name
 * @param place Place object from Google Places
 */
function createMarker(place) {

    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    // Set the default red Icon
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');

    // Push marker to array
    markersArray.push(marker);

    google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(place.id);
        infoWindow.open(map,this);
    });

    addToList(place, marker);
}

function addToList(place, marker) {

    $('.list-group').append('<a href="#" class="list-group-item list-group-item-action" id="' + place.id + '">' + place.id + '</a>');
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

