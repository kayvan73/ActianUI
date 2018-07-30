//var dataURL = 'http://127.0.0.1:5000/api/imgBytes'
//var dataURL = 'http://127.0.0.1:5000/api/targetImages'
var dataURL = 'http://127.0.0.1:5000/api/targetVideo'
//var testString = 'helo';
//console.log(typeof(testString));
//var encoded = btoa(testString);
//console.log(encoded);
var img2 = document.createElement('img');
img2.src = 'foo2.jpg';
document.body.appendChild(img2);


var add_psqlMarkers = function(data) {
    console.log('recieved json data; beginning marker insertion');
    //console.log(data[1]);
    //console.log(data[0]);
    //console.log('Incoming image base64 string is: ' + typeof(data[1]));
    console.log(data.length);
    for (j=0; j<data.length; j++) {
        var decoded = atob(data[j]);  //encoded_bytes=>string
        //var decoded = btoa(data[1]);  //string=>encode_byte

        // ============================
        // this implementation below works
        var byteNumbers = new Array(decoded.length);
        for (var i = 0; i < decoded.length; i++) {
             byteNumbers[i] = decoded.charCodeAt(i);
        }
        var byteArray = new Uint8Array(byteNumbers);
        // ===== uncomment the line below if dealing with images =======
        //var blob = new Blob([byteArray], {type: 'image/jpg'});
        // ================================

        // ===== use line below if dealing with video =====
        var blob = new Blob([byteArray], {type: 'video/webm'});


        var blobUrl = URL.createObjectURL(blob);
        var video = document.createElement('video');
	video.width='320';
	video.height='240';
	//video.src='myMovie2.mkv';
	video.src = blobUrl;
	video.controls = true;
        document.body.appendChild(video);


        // ============ lines below for images ===========
        //var blobUrl = URL.createObjectURL(blob);
        //console.log(imgName);
        //var img = document.createElement('img');
        //img.src = blobUrl;
        //document.body.appendChild(img);
    
    //for (i=0; i<data.length; i++) {
		//console.log(data[i][2]);
        // (title, location, time, status, img
        //var time = String(data[i][11]) + ':' + String(data[i][10]) + ':' + String(data[i][9]) 
        //figure out a way to just grab the name of jpg file w/o the .jpg
        //one way i can accomplish this is by saving the title in the db w/o the .jpg
        //var psqlMarker = new NewMarker(data[i][2], {lat: data[i][4], lng: data[i][6]}, time, 'regular', data[i][2]);
	//}
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

get_table()

