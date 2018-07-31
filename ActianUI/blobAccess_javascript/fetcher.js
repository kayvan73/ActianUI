//var dataURL = 'http://127.0.0.1:5000/api/imgBytes'
//var dataURL = 'http://127.0.0.1:5000/api/targetImages'
//var dataURL = 'http://127.0.0.1:5000/api/targetVideo'
var dataURL = 'http://127.0.0.1:5000/api/Matches'

//var testString = 'helo';
//console.log(typeof(testString));
//var encoded = btoa(testString);
//console.log(encoded);

// ====== uncomment below lines if you get unkown bugs =====
//var img2 = document.createElement('img');
//img2.src = 'foo2.jpg';
//document.body.appendChild(img2);


var add_psqlMarkers = function(data) {
    console.log('recieved json data; beginning marker insertion');
    //console.log(data[1]);
    //console.log(data[0]);
    //console.log('Incoming image base64 string is: ' + typeof(data[1]));
    console.log(data['fixedRecords'].length);
    console.log(data['encodedImages'].length);

    for (j=0; j<data['fixedRecords'].length; j++) {
        console.log('the current image is: ' + String(j));
        console.log('the size should be: ' + String(data['fixedRecords'][j][5]));
        //console.log('the size actually is: ' + String(data['encodedImages'][j].length));
        var decoded = atob(data['encodedImages'][j]);  //encoded_bytes=>string
        //NOTE that i am iternating through the 'encodedImges' section of the dictionary
        var byteNumbers = new Array(decoded.length);
        for (var i = 0; i < decoded.length; i++) {
             byteNumbers[i] = decoded.charCodeAt(i);
        }
        var byteArray = new Uint8Array(byteNumbers);
        // ===== uncomment the line below if dealing with images =======
        var blob = new Blob([byteArray], {type: 'image/jpg'});
        // ================================
        // ============ lines below for images ===========
        var blobUrl = URL.createObjectURL(blob);
        var img = document.createElement('img');
        img.src = blobUrl;
        img.id = 'img' + String(j);
        document.body.appendChild(img);
    }


    // =============== uncomment the block when encoded video is being sent over http api ==========
    for (j=0; j<data['fixedRecords'].length; j++) {
        for (k=0; k<2; k++) {
            var decoded = atob(data['encodedVideo'][j][k]);  //encoded_bytes=>string
            //NOTE that i am iternating through the 'encodedImges' section of the dictionary
            var byteNumbers = new Array(decoded.length);
            for (var i = 0; i < decoded.length; i++) {
                 byteNumbers[i] = decoded.charCodeAt(i);
            }
            var byteArray = new Uint8Array(byteNumbers);
            // ===== use line below if dealing with video =====
            var blob = new Blob([byteArray], {type: 'video/webm'});
            // ================================

            var blobUrl = URL.createObjectURL(blob);
            var video = document.createElement('video');
            video.width='320';
            video.height='240';
            video.src = blobUrl;
            video.controls = true;
            document.body.appendChild(video);
        }
    }
    // =====================================================================

    
    //for (i=0; i<data.length; i++) {
		//console.log(data[i][2]);
        // (title, location, time, status, img
        //var time = String(data[i][11]) + ':' + String(data[i][10]) + ':' + String(data[i][9]) 
        //figure out a way to just grab the name of jpg file w/o the .jpg
        //one way i can accomplish this is by saving the title in the db w/o the .jpg
        //var psqlMarker = new NewMarker(data[i][2], {lat: data[i][4], lng: data[i][6]}, time, 'regular', data[i][2]);
	//}
}


var get_table = function() {
   var parentPromise = fetch(dataURL)     //get the HTTP promise
   var parentPromise_json = parentPromise.then(function(response) {  //use .then() to access parent promise
	return(response.json())        //get the json attribute of the parent promise
   })
   parentPromise_json.then(function(data) {
	   console.log(data)
       //add_psqlMarkers(data['results'])  //simplifying the output of the function to make processing easier
       add_psqlMarkers(data)
   })
}

get_table()

