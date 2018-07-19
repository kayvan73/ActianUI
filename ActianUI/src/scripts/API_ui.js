console.log('handling dependencies')
//var fetch = require("node-fetch");  --only need this line if NOT running code in browser
var dataURL = 'http://127.0.0.1:5000/api/targetMatches'
//var dataURL = 'http://0.0.0.0:5000/api/allData'
//var imagesURL = 'http://127.0.0.1:5000/api/images'
//var coordinatesURL = 'http://127.0.0.1:5000/api/coordinates'


var CreatePsqlButton = function() {
    var importButton = document.createElement('input');
    importButton.type = 'submit';
    importButton.addEventListener('click', this.get_table);
    importButton.setAttribute('value', 'Access PSQL');
    importButton.style.color = 'blue';
    document.getElementById('divInput').appendChild(importButton);
}


var add_psqlMarkers = function(data) {
    console.log('recieved json data; beginning marker insertion')
	//console.log(data[1])
    for (i=0; i<data.length; i++) {
		//console.log(data[i][2]);
        // (title, location, time, status, img
        var time = String(data[i][11]) + ':' + String(data[i][10]) + ':' + String(data[i][9]) 
        //figure out a way to just grab the name of jpg file w/o the .jpg
        //one way i can accomplish this is by saving the title in the db w/o the .jpg
        var psqlMarker = new NewMarker(data[i][2], {lat: data[i][4], lng: data[i][6]}, time, 'regular', data[i][2]);
	}
}


var get_table = function() {
   var parentPromise = fetch(dataURL)     //get the HTTP promise
   var parentPromise_json = parentPromise.then(function(response) {  //use .then() to access parent promise
	return(response.json())        //get the json attribute of the parent promise
   })
   parentPromise_json.then(function(data) {
	   console.log(data)
       add_psqlMarkers(data['results'])  //simplifying the output of the function to make processing easier
   })
}

console.log('creating import button')
CreatePsqlButton()


//var get_images = function() {
//   fetch(imagesURL)
//      .then(
//   	function(response) {
//   	   if (response.status !== 200) {
//   		console.log('ERROR in accessing site: ' + response.status);
//   	   }
//   	
//   	//console.log(response.json())
//   	response.json()
//   	   .then(
//   	      function(data) {
//   	         //console.log('we in JSON  boys');
//   	         //console.log(data);
//		 return(data)
//   	      }
//   	)}
//      )
//}

//var fetch_json = function(URL) {
//    var parentPromise_json = get_HTTPPromise(URL)   //get the json attribute (also of type prmose)
//    return parentPromise_json.then(function(data) {
//	console.log('we in json')
//	//console.log(data)
//	//console.log(data['result'])
//        return (data)                       //use .then() to access the json promise and get json data
//    })
//}
//get_table(dataURL)


//var get_coords = function() {
//   fetch(coordinatesURL)
//      .then(
//   	function(response) {
//   	   if (response.status !== 200) {
//   		console.log('ERROR in accessing site: ' + response.status);
//   	   }
//   	
//   	//console.log(response.json())
//   	response.json()
//   	   .then(
//   	      function(data) {
//   	         //console.log('we in JSON  boys');
//   	         //console.log(data);
//		 return(data)
//   	      }
//   	)}
//      );
//}

//console.log(imagesURL)
//var images = fetch_json(imagesURL)
//var images = get_HTTPPromise(dataURL)

//console.log(images)           =====> leaving this here since it is a learning expereince
//				=====> when you uncomment that line, the result will be pending, 
//				and that pending will print out before "we in json" since this is
//				an ayncronous process, so the console.log(images) actually occurs before 
//				the other thread finishes execution!
//console.log('successfully grabbed images')
//coords = get_coords()
//console.log('suucessfully grabbed images')
