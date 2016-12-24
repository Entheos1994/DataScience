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

var restaurantIds = {};
restaurantIds['irish'] = '52e81612bcbc57f1066b7a06';
restaurantIds['mexican'] = '4bf58dd8d48988d1c1941735';
restaurantIds['chinese'] = '4bf58dd8d48988d145941735';
restaurantIds['japanese'] = '4bf58dd8d48988d111941735';
restaurantIds['moroccan'] = '4bf58dd8d48988d1c3941735';
restaurantIds['french'] = '4bf58dd8d48988d10c941735';
restaurantIds['spanish'] = '4bf58dd8d48988d150941735';
restaurantIds['russian'] = '5293a7563cf9994f4e043a44';
restaurantIds['thai'] = '4bf58dd8d48988d149941735';
restaurantIds['southern_us'] = '4bf58dd8d48988d14f941735';
restaurantIds['filipino'] = '4eb1bd1c3b7b55596b4a748f';
restaurantIds['vietnamese'] = '4eb1bd1c3b7b55596b4a748f';
restaurantIds['british'] = '52e81612bcbc57f1066b7a05';
restaurantIds['greek'] = '4bf58dd8d48988d10e941735';
restaurantIds['indian'] = '4bf58dd8d48988d10e941735';
restaurantIds['jamaican'] = '4bf58dd8d48988d144941735';
restaurantIds['brazilian'] = '4bf58dd8d48988d16b941735';
restaurantIds['cajun_creole'] = '4bf58dd8d48988d17a941735';
restaurantIds['korean'] = '4bf58dd8d48988d113941735';
restaurantIds['italian'] = '4bf58dd8d48988d110941735';

var testCuisine = {"irish": 0.0, "mexican": 0.0, "chinese": 50.0, "japanese": 0.0, "moroccan": 0.0, "french": 0.0, "spanish": 0.0, "russian": 0.0, "thai": 0.0, "southern_us": 0.0, "filipino": 0.0, "vietnamese": 0.0, "british": 0.0, "greek": 0.0, "indian": 50.0, "jamaican": 0.0, "brazilian": 0.0, "cajun_creole": 0.0, "korean": 0.0, "italian": 0.0};

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


    $.ajax({
        type:'POST',
        url: '/recipe',
        data: {recipe_name: recipe},
        success: function(data) {

            console.log(data);
       },
        error: function (xhr) {
            console.log(xhr.status + ": " + xhr.responseText);
       }

    });

    var ll = null;

    /* Convert location into coordinates and retrieve restaurants */
    geocoder.geocode( {'address': location}, function(results, status) {
        if (status == 'OK') {
            console.log(results);

            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            var latlng = {lat: latitude, lng: longitude};
            ll = latitude.toFixed(2)+ ',' + longitude.toFixed(2);

            /* Clear the previous markers */
            clearMarkers();

            /* Create the marker */
            var marker = new google.maps.Marker({
                map: map,
                position: latlng
            });

            console.log(marker);

            // Set the default red Icon
            marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');

            // Push marker to array
            markersArray.push(marker);

            console.log(markersArray);

            /* Marker listener */
            marker.addListener('click', function() {
                infoWindow.setContent('You');
                infoWindow.open(map,marker);
            });

            findRestaurants(ll, determineCuisines(testCuisine));

        } else {

            $("#error-title").text("Error");
            $("#error-body").text('Geocode was not successful for the following reason: ' + status);
            $('#modal-error').modal('show')
        }
    });
}

/**
 * Determine which restaurants to search by cuisine
 *
 * @param recipe JSON containing cuisine percentages
 * @returns {string} Restaurant categories from fourspace
 */
function determineCuisines(recipe)
{
    var cuisines = "";

    for (var key in recipe){
        var attrValue = recipe[key];

        if(attrValue >= 0.25)
            cuisines = cuisines + restaurantIds[key] + ",";
    }

    cuisines = cuisines.slice(0, -1);

    return cuisines;
}

function findRestaurants(location, cuisine) {
    /* Rest request to get restaurant information based on user's query */
    $.ajax({
        type:'get',
        url: 'https://api.foursquare.com/v2/venues/search',
        data: {client_id: fourSquareKey, client_secret: fourSquareId, ll: location,
            v:'20161130', categoryId: cuisine, intent: 'browse',
            radius: 5000},
        success: function(data) {



            /* Place markers on the map */
            var venues = data.response.venues;
            for(var i = 0; i < venues.length; i++)
                createMarker(venues[i]);

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
            $("#error-title").text("Error");
            $("#error-body").text('Restaurant search was not successful for the following reason: ' + xhr.status);
            $('#modal-error').modal('show')
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

    /* Restaurant information */
    var name = place.name;
    var id = place.id;
    var phone = place['contact'].formattedPhone;
    var url = String(place.url);
    var formattedAddress = place['location'].formattedAddress;

    /* Don't display information if it doesn't exists */
    if(phone === undefined)
        phone = '';

    /* Remove http:// from url */
    if(url === 'undefined')
        url = '';
    else
        url = url.substring(7);

    /* Create address string */
    var address = "";
    for(var i = 0; i < formattedAddress.length-1; i++)
        address = address + formattedAddress[i] + ", ";

    /* Remove last comma and space from address */
    address = address.substring(0, address.length-2);

    $('.list-group').append('<div><button class="list-group-item list-group-item-action restaurant-list" id="' + id + '"><h4>' + name
        + '</h4><p class="restaurant-info">' + address + '</p><p class="restaurant-info">' + url + '</p><p class="restaurant-info">' + phone + '</p></button></div>');
    $('#' + id).hover(function() {
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

