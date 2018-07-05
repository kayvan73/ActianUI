//PURPOSE
//  1) Object gives you funtionality to maintain marker state

//NOTES - this.importMarkers
//  1) had to change the index letter in the convert function above to 'k' because it was messing
//     with the i values in the for loop here!!

//**************************************************************
//**************************************************************
//*************************************************************


var MarkerArray = function() {

    this.markerList = [];     //array of GoogleApiMarkers
    this.currentMarker = {};  // my way of managing state for which object is currently clicked


    //PURPOSE
    //  1) converts my googleApiMarker array, markerList, into JSON friendly list
    this.convertArray2_compatibleFormat = function() {
        var compatibleArray = [];
        for (k=0; k<this.markerList.length; k++) {
            var markerData = {
                lat : this.markerList[k].getPosition().lat(),  //NOTE how you obtain lat/lng
                lng : this.markerList[k].getPosition().lng(),
                title : this.markerList[k].title,
                time : this.markerList[k].time,
                markerType : this.markerList[k].status
            };
            compatibleArray.push(markerData);
        }
        return compatibleArray;
    }

    //PURPOSE
    //  1) uses convert_ function above to give console-friendly output of current marker array
    this.printMarkerList =  function () {
        convertedArray = this.convertArray2_compatibleFormat();
        var jsonTxt = JSON.stringify(convertedArray);
        console.log(jsonTxt);
    }

    //PURPOSE
    //  1) add each new googleAPiMarker into the markerList array
    //INPUT
    //  1) instantiated GoogleApiMarker
    //OUTPUT
    //  1) markerList array now has 1 more element
    this.pushMarker = function(markerObject) {
        this.markerList.push(markerObject);
        //this.updateLink();    //======commenting this out since no need for links ============
        //this.printMarkerList();
    }

    //PURPOSE
    //  1) creating a button that when clicked, initiates a file download on client computer
    //OUTPUT
    //  1) export.js downloaded on to user computer
    this.createExportLink = function () {
        var link = document.createElement('a');
        var linkText = document.createTextNode('Export Markers');
        link.appendChild(linkText);
        link.id = 'exportLink';
        link.setAttribute('href', '#');
        link.setAttribute('download', 'export.js');
        document.getElementById('divInput').appendChild(link);
    }

    //PURPOSE
    //  1) creatig a button that on click actives import algorith
    this.createImportButton = function () {
        var importButton = document.createElement('input');
        importButton.type = 'submit';
        importButton.addEventListener('click', this.importMarkers);
        importButton.setAttribute('value', 'Import Markers');
        importButton.style.color = 'blue';
        document.getElementById('divInput').appendChild(importButton);
    }

    //PURPOSE
    //  1) loop through each element in export.js file and create markers for each of those elements
    //INPUT
    //  1) export.js
    //OUTPUT
    //  1) markers placed on the map
    this.importMarkers = function () {
        console.log(imported.length);
        for (i=0; i<imported.length; i++){
            console.log(i);
            var importedMarker = new NewMarker(imported[i].title, {lat: imported[i].lat, lng: imported[i].lng}, imported[i].time, imported[i].markerType);
        };
    }


    //PURPOSE
    //  1) the easiest way to write to client computer is to download a "blob" object
    //     this function converts the just markerList into a blob so it can be downloaded
    //INPUT
    //  1) markerList that has been converted to JS friendly form
    //OUTPUT
    //  1) JSON blob
    this.convert2Blob = function() {
        var jsonTxt = JSON.stringify(this.convertArray2_compatibleFormat());
        var txt = 'var imported=' +  jsonTxt  + ';';
        var fileBlob = new Blob([txt], {type: 'application/javascript;charset=UTF-8'});
        return fileBlob;
    }

	//=================== dont need to update download link, w/ psql  the user no longer needs to ========
    //PURPOSE
    //  1) after each new marker, the new JSOn blib to download has to update to include new marker
    //INPUT
    //  1) JSOn blob
    //OUTPUT
    //  1) JSON blob
    //this.updateLink = function () {
    //    markerList_Blob = this.convert2Blob();
    //    //console.log('updating LInk');
    //    var exportLink = document.getElementById('exportLink');
    //    exportLink.setAttribute('href',  URL.createObjectURL(markerList_Blob));
    //}
}

console.log('initializing marker array')
var current_MarkerArray = new MarkerArray();
//======commenting these 2 out
//current_MarkerArray.createExportLink();
//current_MarkerArray.createImportButton();
