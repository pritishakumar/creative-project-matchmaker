/* Function containing all the functionalities for the Google Maps
JavaScript API on the page.
    Called in the API script tag in the template page head section. */
function initMap() {
    let myLatlong, viewport, markersNearby, markerCurrentLocation;
    let neighborhood;
    let zoomLevel = 11;
    retrieveUserCoords();
    
    const map = new google.maps.Map(document.getElementById("map"), {
        center: myLatlong,
        zoom: zoomLevel,
        gestureHandling: "greedy"
    });
    positionCurrentMarker(myLatlong);

    google.maps.event.addListenerOnce(map, 'idle', populate_projects);
    map.addListener("zoom_changed", populate_projects);
    map.addListener("dragend", populate_projects);
    map.addListener("click", updateCurrentMarker);

    generateAutoComplete();
    document.getElementById("map-search-form").addEventListener("submit", mapSearch)


    /* Function will pull dataset information from the DOM to use 
    as default starting coordinates to initialize the map object.
        Called above automatically upon load. */
    function retrieveUserCoords(){
        let lat, lng;
        if (localStorage.getItem("map-zoom") && localStorage.getItem("map-lat")) {
            zoomLevel = JSON.parse(localStorage.getItem("map-zoom"));
            lat = JSON.parse(localStorage.getItem("map-lat"));
            lng = JSON.parse(localStorage.getItem("map-lng"));
        } else {
            const mapContainer = document.getElementById("map-container-large");
            lat = Number(mapContainer.dataset.lat);
            lng = Number(mapContainer.dataset.long);
        }
        myLatlong = { lat, lng };
    };


    /* Function will retrieve the address value in the autocomplete input
    and await the corresponding coordinates, setting that as the new center
    for the map object, and rendering a new marker in the center of the new
    area.
        Called as event listener callback function on the "map-search-button". */
    async function mapSearch(event) {
        event.preventDefault();
        
        const address = document.getElementById("autocomplete-input").value;
        myLatlong = await Geocode.getCoordFromAddress(address);
        map.setCenter(myLatlong)
        positionCurrentMarker(myLatlong)
    }


    /* Function updates the map viewport boundaries and updates the localStorage
    with the most recent map orientation. Then it awaits the nearby projects 
    (neighborhood global variable) within those boundaries. Based on those projects,
    markers are generated and DOM elements are created to show the search results.
        Called as event listener callback function on the on the map upon it's first 
        load, and whenever the map object is dragged or zoomed. */
    async function populate_projects() {
        generateViewportBounds();
        updateLocalStorage();

        neighborhood = await Project.searchForNearbyMarkers(viewport)
        generate_markersNearby(neighborhood);
        generate_projectListing(neighborhood);
    }


    /* Function updates the global variable with the current map object's
    viewport boundary coordinates.
        Called in the populate_projects() function. */
    function generateViewportBounds(){ 
        viewport = map.getBounds().toJSON();
    }


    /* Function extracts the zoom and  coordinate value from the
    map object and stores it in the browser localStorage for the
    next time this page loads.
        Called in the populate_projects() function. */
    function updateLocalStorage(){
        const zoom = map.getZoom();
        const lat = map.getCenter().lat();
        const lng = map.getCenter().lng(); 
        localStorage.setItem("map-zoom", String(zoom));
        localStorage.setItem("map-lat", String(lat));
        localStorage.setItem("map-lng", String(lng));
    }


    /* Function clears the map object of any markersNearby objects,
    and iterates through the array to create a marker for each one.
        Input Parameter: an array of instances with lat & long 
        properties.
        Called in the populate_projects() function. */
    function generate_markersNearby(list){
        try {
            markersNearby.setMap(null);
        } catch (err) {};

        for (let i = 0; i < list.length; i++) {
            markersNearby = new google.maps.Marker({
                position: new google.maps.LatLng(list[i].lat, list[i].long),
                map,
                label: `${i+1}`
            });};
    };


    /* Function selects the DOM element and either appends a message,
    saying no results found, or prints the Project instances.
        Input Parameter: an array of instances with text properties 
        to append to the DOM.
        Called in the populate_projects() function. */
    function generate_projectListing(list) {
        const results = document.getElementById("project-results")
        if (list.length == 0){
            results.innerHTML = "<tr><td>No projects near by..</td></tr>";
        } else {
            results.innerHTML = "";
        }
        
        for (let i = 0; i < list.length; i++) {
            // tagList = String(...neighborhood[i].tags);
            let content = `<tr><td>${i+1}</td>
                    <td>
                        <a class="text-light" 
                            href="/project/${list[i].id}"><b>${list[i].name}</b></a>
                    </td>
                    <td>${list[i].tags.join(", ")}</td>
                    <td>${list[i].display_name}</td>
                    </tr>`
            results.innerHTML += content;
        }
    }


    /* Function will retrieve the coordinate information from the mouse
    event, update the input coordinate field values in the DOM and 
    move the currentMarker on the map to that position.
        Called as event listener callback function on the map object 
        itself. */
    function updateCurrentMarker(mapsMouseEvent) {               
        myLatlong = { lat: mapsMouseEvent.latLng.lat(),
            lng: mapsMouseEvent.latLng.lng()};
        positionCurrentMarker(myLatlong) 
    };


    /* Function when given a set of coordinates, will attempt to 
    clear the map object of any currentMarker, and initialize a 
    new currentMarker in the new position.
        Called automatically upon the page load, in the mapSearch() 
        function, and the updateCurrentMarker() function */
    function positionCurrentMarker(latlng){
        try{
            markerCurrentLocation.setMap(null);
        } catch(err) {};
        
        markerCurrentLocation = new google.maps.Marker({
            position: latlng,
            label: "*",
            map
        });
    }

    
    /* Function will select the DOM input needed for the autocomplete
    input and then attach the Autocomplete object to initialize the
    functionality.
        Called automatically upon the page load. */
    function generateAutoComplete() {
        const input = document.getElementById("autocomplete-input");
        const options = {
            fields: ["address_components", "geometry", "name"],
        };
        const autocomplete = new google.maps.places.Autocomplete(input, options);
    }
}