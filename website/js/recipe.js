// Agency Theme JavaScript

var geocoder;
var map;

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
}


function findRestaurants() {

    /* Get information user entered */
    var location = document.getElementById("location-entry").value;
    var recipe = document.getElementById("recipe-entry").value;

    /* Convert location into coordinates */
    geocoder.geocode( {'address': location}, function(result, status) {
        if (status == 'OK') {
            map.setCenter(result[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: result[0].geometry.location
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}
