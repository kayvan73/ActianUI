//PURPOSE
//   1) an instance of NewMarker creates a GoogleAPiMarker and adds that marker to an array
//      of googeApiMarkers (NOT an array of NewMarkerObject)
//   2) the marker has a event ahdnler to display its image and coordinates

//NOTES - GoogleMarker
//  1) console.log(pCoords.textContent);  //this is how your print the text node
//  2) I bind the scope of the addListener function, display_markerData, to "this" which makes
//     the display_markerData function have same scope as NewMarker object -> allowing me to
//     access the NewMarker paramters (markerTitle/markerLocation....). If i dont do this, display_markerData
//     will have the scope of GoogleMarker - which is actually ok but i did it anyways.

//**************************************************************
//**************************************************************
//*************************************************************

var NewMarker = function(markerTitle, markerLocation, timeOfPicture, status, markerImage){  //================changed this one

	//console.log(markerImage)
    console.log('adding new marker');
    if (markerTitle == '###Enter Title###'){
        alert('You Have NOT Entered A Title, Enter One Now Before Coninuing')
    }

    //PURPOSE
    //  1) on marker click, the corresponding image and marker gps will display
    //INPUT
    //  1) marker lat/lng/title: these values are taken from NewMarker object paramters above
    //OUTPUT
    //  1) the display div now cahnges from display:none to display:inline
    this.display_markerData = function(){
        var curImage = document.getElementById('selected_img')
        var divImg = document.getElementById('divImg');
		var curLat = document.getElementById('lat_display');
        var curLng = document.getElementById('lng_display');
        curLat.setAttribute('value', this.GoogleMarker.latitude);
        curLng.setAttribute('value', this.GoogleMarker.longitude);
		console.log(this.GoogleMarker.latitude)
		console.log(this.GoogleMarker.title);
        curImage.src = this.GoogleMarker.imageLocation;   //=============changed this one
        //curImage.src = '/home/pi/Desktop/heroImages/m1.jpg'   //=============changed this one
        divImg.style.display = 'inline';
        current_MarkerArray.currentMarker = this.GoogleMarker; //tracker object
    };


    //PURPOSE
    //  1) Use google marker library to initiate a new marker object on UI w/ basic user-given params
    //INPUT
    //  1) markerTitle = String word/s (ie m1) that describe the marker: NOTE markerTitle has to ==
    //     the name of the markers image or the image will NOT pop up when you click on marker
    //  2) markerLocation = literal object that has 2 Number Properties: marker lat and lng
    //  4) status = either true or false => if true, target is Candidate target
    //OUTPUT
    //  1) marker is placed on the map
    //  2) marker and its properties pushed to our current_MarkerArray object
    this.GoogleMarker = new google.maps.Marker({
		latitude : markerLocation.lat,
		longitude : markerLocation.lng,
        position: {
            lat: markerLocation.lat,
            lng: markerLocation.lng
        },
        label: markerTitle,
		imageLocation: markerImage,
        title : markerTitle,
        time : timeOfPicture,
        status: status,
        icon : status ? 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png':'', //Ternary!!
        map:map //specififes the map you want the marker to go on
    });
    current_MarkerArray.pushMarker(this.GoogleMarker);//once marker is initiated, add it to array
    this.GoogleMarker.addListener("click", this.display_markerData.bind(this)); //NOTE the bind
}
