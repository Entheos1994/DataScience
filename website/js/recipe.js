// Agency Theme JavaScript

var geocoder;
var map;
var placesService;
var infoWindow;

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
    })


    
})(jQuery); // End of use strict


function initMap() {

    /* Map Setup */
    var latlng = new google.maps.LatLng(53.181957, -3.876466);
    var mapOptions = {
        zoom: 6,
        center: latlng
    }

    /* Initialize Google Services */
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    geocoder = new google.maps.Geocoder();
    placesService = new google.maps.places.PlacesService(map);
    infoWindow = new google.maps.InfoWindow();
}


function findRestaurants() {

    /* Get information user entered */
    var location = document.getElementById("location-entry").value;
    var recipe = document.getElementById("recipe-entry").value;

    /* Convert location into coordinates and retrieve restaurants */
    geocoder.geocode( {'address': location}, function(results, status) {
        if (status == 'OK') {
            console.log(results);
            placesService.nearbySearch({
                location: results[0].geometry.location,
                radius: 2000,
                type: ['restaurant']
            }, callback);
    
            map.setCenter(results[0].geometry.location);
            map.setZoom(14);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}


function callback(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
        }
    }
}

/* Place a marker on the map with restaurant name */
function createMarker(place) {

    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(place.name);
        infoWindow.open(map,this);
    });
}


