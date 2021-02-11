let tagsFullList = [];
let tagsSelectedList = [];
const tagSelectInput = document.getElementById("tag-select")
const tagButton = document.getElementById("create-tag-button")
const hiddenTagInput = document.getElementById("tags")

tagSetUp();


/* Function initializes the list of existing tags (async operation), the hidden tag DOM field, adds the 
event listener on any existing tags to remove the tag and on the input field
for whenever the user types, and appends to the DOM any existing tags. 
    Called above automatically on load.*/
async function tagSetUp() {
    tagsFullList = await Tag.getTagFullList();
    tagSelectInput.addEventListener("keyup", checkTag)
    document.getElementById("selected-tags").addEventListener("click", tagRemove)
    
    const exising_tags = tagSelectInput.dataset.existing;
    if (exising_tags != "None") {
        hiddenTagInput.value = exising_tags;
        tagsSelectedList = exising_tags.split("|");
        for (each of tagsSelectedList) {
            document.getElementById("selected-tags").innerHTML +=
            `<li class="tag-tile" 
                data-name="${each}">${each}   <button><i class="fas fa-trash-alt text-danger"></i></button>
            </li>`;
}}};


/* Function will execute if event target is the delete button. It will 
remove that tag from the frontend array, the hidden input field, and 
then delete the DOM element.
    Called in tagSetUp() function as the event listener callback function
    on the "selected-tags" list.  */
function tagRemove(event){
    event.preventDefault(); 
    let itemElement;
    if (event.target.tagName == "BUTTON") {
        itemElement = event.target.parentElement;
    } else if (event.target.tagName == "I") {
        itemElement = event.target.parentElement.parentElement;
    } else {
        return;
    }
    const itemName = itemElement.dataset.name;
        tagsSelectedList = tagsSelectedList.filter(each => each != itemName)
        hiddenTagInput.value = tagsSelectedList.join("|");
        itemElement.remove();
}


/* Function hides the Add button when the project tag input field is empty
and renders it depending on the results of its comparison, whether the 
input matches any existing tags, or requires a new tag to be created. When
Add button is rendered, an event listener to add the tag is attached.
    Called in tagSetUp() function as the event listener callback function
    on the tagSelectInput (project tag input field). */
function checkTag(event) {
    event.preventDefault();

    if (tagSelectInput.value == ""){
        tagButton.style.display = "none";
        return
    }
    tagButton.style.display = "inline";
    tagButton.addEventListener("click", addTag)

    if (tagsFullList.includes(tagSelectInput.value)){
        tagButton.innerText = "Add Existing Tag";
    } else {
        tagButton.innerText = "Add New Tag"
    }
}


/* Function extracts the project tag input field value, and adds
the value to the frontend arrays, the DOM list and the hidden
input field for the form submit, then resets the tag input field.
    Called in checkTag() function as the event listener callback
    function on the tagButton (Add button for tags). */
function addTag(event){
    event.preventDefault();
    let tag_name = tagSelectInput.value;
    if (tagsSelectedList.includes(tag_name)){
        tagSelectInput.value = "";
        return;
    }
    if (tagButton.innerText == "Add New Tag"){
        tagsFullList.push(tag_name);
        document.getElementById("tags-all").innerHTML += `<option value="${tag_name}" />`;
    };
    document.getElementById("selected-tags").innerHTML +=
    `<li class="tag-tile" 
        data-name="${tag_name}">${tag_name}   <button><i class="fas fa-trash-alt text-danger"></i></button>
    </li>`;
    tagsSelectedList.push(tag_name);
    hiddenTagInput.value = tagsSelectedList.join("|");
    tagSelectInput.value = "";
}


/* Function containing all the functionalities for the Google Maps
JavaScript API on the page.
    Called in the API script tag in the template page head section. */
function initMap() {
    let myLatlong, markerCurrentLocation;
    retrieveUserCoords();
    
    const map = new google.maps.Map(document.getElementById("map"), {
        center: myLatlong,
        zoom: 11,
        gestureHandling: "greedy"
    });
    positionCurrentMarker(myLatlong);

    map.addListener("click", updateCurrentMarker);

    generateAutoComplete();
    document.getElementById("map-search-button").addEventListener("click", mapSearch)


    /* Function will pull dataset information from the DOM to use 
    as default starting coordinates to initialize the map object.
        Called above automatically upon load. */
    function retrieveUserCoords(){
        const mapContainer = document.getElementById("map-container");
        const lat = Number(mapContainer.dataset.lat);
        const lng = Number(mapContainer.dataset.long);
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