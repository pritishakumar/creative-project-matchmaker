/* Function containing all the functionalities for the Google Maps
JavaScript API on the page.
    Called in the API script tag in the template page head section. */
function initMap() {
	let myLatlong;
	let zoomLevel = 11;
	retrieveDefaultCoords();

	const map = new google.maps.Map(document.getElementById("map"), {
		center: myLatlong,
		zoom: zoomLevel,
		gestureHandling: "greedy"
	});
	positionCurrentMarker(myLatlong);
	map.addListener("click", updateCurrentMarker);
	
	document.getElementById("map-search-button").addEventListener("click", mapSearch)
	generateAutoComplete();


	/* Function will pull dataset information from the DOM to use 
    as default starting coordinates to initialize the map object.
        Called above automatically upon load. */
	function retrieveDefaultCoords(){
		let lat, lng;
			const mapContainer = document.getElementById("map-container");
			lat = Number(mapContainer.dataset.lat);
			lng = Number(mapContainer.dataset.long);
		myLatlong = { lat, lng };
	};


	/* Function will retrieve the coordinate information from the mouse
    event, update the input coordinate field values in the DOM and 
    move the currentMarker on the map to that position.
        Called as event listener callback function on the map object 
        itself. */
	function updateCurrentMarker(mapsMouseEvent) {               
		const lat = mapsMouseEvent.latLng.lat();
        const lng = mapsMouseEvent.latLng.lng();
        document.getElementById("lat").value = lat;
        document.getElementById("long").value = lng;
        myLatlong = { lat, lng };
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
		} catch(err) {}
		
		markerCurrentLocation = new google.maps.Marker({
			position: latlng,
			label: "*",
			map
		});
	}


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