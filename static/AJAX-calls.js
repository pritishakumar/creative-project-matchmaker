const GEOCODE_BASE_URL = `http://127.0.0.1:5000/api/geocode`;
const NEIGHBORHOOD_BASE_URL = `http://127.0.0.1:5000/api/neighborhood`;
const TAG_LIST_BASE_URL = `http://127.0.0.1:5000/api/tags`

class Geocode {
    constructor(coordinates){
        this.lat = coordinates.lat;
        this.lng = coordinates.lng;
    }
     
    static async getCoordFromAddress(address){
        const urlSafeAddress = address.replace(/\s/g, "%20");
        const url = `${GEOCODE_BASE_URL}?address=${urlSafeAddress}`
        const response = await axios.get(url)
        
        return new Geocode(response.data.results[0].geometry.location);
    }
}

class Project {
    constructor(projectObj){
        this.id = projectObj.id;
        this.name = projectObj.name;
        this.display_name = projectObj.display_name;
        this.lat = projectObj.lat;
        this.long = projectObj.long;
        this.tags = projectObj.tags;
    }

    /* Creates Project instances from a database query for projects
    within the given map viewport boundaries
        Input Parameter: object with keys called north (high lat range), 
        south (low lat range), east (high long range) and west (low 
        long range).
        Returns: an array of Project instances */
    static async searchForNearbyMarkers({ north, south, east, west }){
        const projects = [];
        const response = await axios.get(NEIGHBORHOOD_BASE_URL,
            { params: { north, south, east, west } });
        
        for (let each of response.data.projects){
            projects.push(new Project(each));
        }
        return projects
    }
}

// A class for retrieving a full listing of Tag instances as an array
class Tag {
    static async getTagFullList() {
        const response = await axios.get(TAG_LIST_BASE_URL);
        return response.data;
    }
}
