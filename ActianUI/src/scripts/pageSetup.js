//PURPOSE
//  0) DONT be intimidated by all the code - most of it is just me creating the imgs, textboxes, 
//     input boxes, checkboxes, and buttons that go into making any UI.  Besides the addListener 
//     methods, there is NO logic to pay attention to.
//  1) Initialize the Google Map on the Page
//  2) create basic elements/inputs/buttons for UI
//  3) create Listeners for the important buttons in creating markers and deleting markers

//NOTES - all
//  1) i use this form: document.getElementById(div_id).appendChild(input) as shrink code by 1 line
//  2) i solved the 'null' error from getElementById by appending div element to DOM before calling
//     with getElement function. 
//NOTES - specifyInputs method
//  1) I have to send the this.addInputs function a third param. putting 'na'
//     is just garabge so the function doesnt throw error
//NOTES - createDiv method
//  1) i had to create the if statement because i dont know how to pass body as a param

//*************************************************************
//*************************************************************
//*************************************************************


var map;

function NewPage() {

    //PURPOSE
    //  1) initMap creates an googleApi object that i call "map"
    //  2) the "map" object will start with the params I give below
    this.addMap = function() {
        mapOptions = {
            center: {lat: 30.3241499, lng: -97.6030111}, //centered right over KEDC
            zoom: 18.8,
            mapTypeId: 'satellite'
          }
        map = new google.maps.Map(document.getElementById('map'), mapOptions);
    };

    //this.divInput = document.createElement('div');
    //this.divInput.setAttribute('class' , 'divInput');


    //PURPOSE
    //  1) All 'input' elements (submit, number) are created and appended to DOM here
    //INPUT
    //  1) div_id is the parent div you want this input to be attached to 
    //OUTPUT
    //  1) a DOM object that will be attached to the DOM
    this.addInputs = function(div_id, input_id, input_type, default_value) {
        var input = document.createElement('input');
        input.id = input_id;
        input.type = input_type;
        input.setAttribute('value', default_value);
        document.getElementById(div_id).appendChild(input);
    };


    //PURPOSE
    //  1) same thing as addInputs() exept now its text Nodes
    this.addText = function(div_id, userText) {
        newText = document.createTextNode(userText);
        document.getElementById(div_id).appendChild(newText);
    }


    //PURPOSE
    //  1) same thing as addInputs() exept now its line breaks ie 'br'
    this.addLineBreak = function(div_id){
        var newLine = document.createElement('br');
        document.getElementById(div_id).appendChild(newLine);
    }


    //PURPOSE
    //  1) same thing as addInputs() exept now its 'img' elemetns
    this.createImg = function(div_id, img_src, img_id, img_height, img_width){
        var img = document.createElement('img');
        img.src = img_src;
        img.width = img_width;
        img.height = img_height;
        img.id = img_id;
        document.getElementById(div_id).appendChild(img);
    }


    //PURPOSE
    //  1) same thing as addInputs() exept now its 'div' elements
    this.createDiv = function(div_id, div_class, parent_divID){
        var newDiv = document.createElement('div');
        newDiv.id = div_id;
        newDiv.setAttribute('class', div_class);
        if (parent_divID == 'body'){
            document.body.appendChild(newDiv);
        }
        else
            document.getElementById(parent_divID).appendChild(newDiv);
    }


    //PURPOSE
    //  1) add a Listener to the delete button so when clicked it removes marker from map and array
    //OUTPUT
    //  1) marker no longer shows on map UI
    //  2) marker data is expunged from markerList array
    this.addListener2_deleteButt = function(){
        var deleteButt = document.getElementById('deleteButt');
        deleteButt.style.color = 'red';
        deleteButt.addEventListener('click', function(){
            for (j=0; j<current_MarkerArray.markerList.length; j++){
                if (current_MarkerArray.markerList[j] === current_MarkerArray.currentMarker){
                    console.log('deleting marker');
                    current_MarkerArray.markerList[j].setMap(null);//null b4 splice else it cant find
                    current_MarkerArray.markerList.splice(j, 1);
                }
            }
            divImg.style.display = 'none'; //after deleting marker, you want the img display to leave
            current_MarkerArray.printMarkerList();
            current_MarkerArray.updateLink();
        });
    };


    //=============== this is the OLD listerner for the create button ==============
    //this.addListener2_createButt = function() {
    //    var createButt = document.getElementById('submit');
    //    createButt.style.color = 'green';
    //    createButt.addEventListener('click', function() {
    //       var markerTitle = document.getElementById('titleInput').value; //NOTE the .value!
    //       var markerTime = document.getElementById('pictureTime').value; //NOTE the .value!
    //       var checkStatus = document.getElementById('CT_checkbox').checked;//NOTE .checked!
    //       var markerLocation = pageElements.calc_markerLocation();
    //       var markerObject = new NewMarker(markerTitle, markerLocation, markerTime, checkStatus);
    //    });
    //};


    //PURPOSE
    //  1) When use clicks on specific marker, correspding image/data will display bc of this method
    //OUTPUT
    //  1) before any clicks, there are hidden img/txt elements using display=none property
    this.createTarget_popUp = function() {
        this.createDiv('divImg', 'divImg', 'body');
        this.createImg('divImg', './heroImages/', 'selected_img', 200, 200);
        this.addLineBreak('divImg');
        var lat_display = this.addInputs('divImg', 'lat_display', 'number', '');
        var lng_display = this.addInputs('divImg', 'lng_display', 'number', '');
        this.addLineBreak('divImg');
        var deleteButt = this.addInputs('divImg', 'deleteButt', 'submit', 'Delete Marker');
        this.addListener2_deleteButt();
        document.getElementById('divImg').style.display = 'none';
    };


    //========================== this is the old add input implementation ====================
    //this.specify_newInputs = function() {
    //    this.createDiv('divInput', 'divInput', 'body');
    //    var lat_degrees = this.addInputs('divInput', 'lat_deg', 'number', '30');
    //    var lat_minutes = this.addInputs('divInput', 'lat_min', 'number', '19');
    //    var lat_seconds = this.addInputs('divInput', 'lat_sec', 'number', '4788');
    //    this.addLineBreak('divInput');
    //    var lng_degrees = this.addInputs('divInput', 'lng_deg', 'number', '97');
    //    var lng_minutes = this.addInputs('divInput', 'lng_min', 'number', '36');
    //    var lng_seconds = this.addInputs('divInput', 'lng_sec', 'number', '1950');
    //    this.addLineBreak('divInput');
    //    this.addText('divInput', 'Enter Time of Pic:  ')
    //    var pictureTime = this.addInputs('divInput', 'pictureTime', 'number', 'n/a');
    //    document.getElementById('pictureTime').style.width = '70px';
    //    this.addText('divInput', '  Enter Title:  ')
    //    var titleInput = this.addInputs('divInput', 'titleInput', 'string', '###Enter Title###');
    //    //I have to send the this.addInputs function a third param. putting 'na'
    //    //is just garabge so the function doesnt throw error
    //    this.addText('divInput', 'CT')
    //    var CT_checkbox = this.addInputs('divInput', 'CT_checkbox', 'checkbox', 'n/a');
    //    this.addLineBreak('divInput');
    //    var submit = this.addInputs('divInput', 'submit', 'submit', 'Create Marker');
    //    this.addListener2_createButt();
    //    this.addLineBreak('divInput');
    //    this.addLineBreak('divInput');
    //};

    this.specify_newInputs = function() {
        this.createDiv('divInput', 'divInput', 'body');
        //var submit = this.addInputs('divInput', 'submit', 'submit', 'Access PSQL');
        //this.addListener2_createButt();
        this.addLineBreak('divInput');
        this.addLineBreak('divInput');
    };

    //PURPOSE
    //  1) convert DD.MM.MMMM GPS user input into Decminal degrees (ie dds) for lat and lng
    //INPUT
    //  1) DD, MM, and MMMM, STRINGS
    //OUTPUT
    //  1) "location" which is an object having paramters for lng and lat as floating numbers
    //NOTES
    //  1) divide "seconds" value by 10000 bc it is decimal minutes out to ten thousands place
    //  2) multplying by -1 is easier here than making user input -1 for all value of lng
    this.calc_markerLocation = function () {
        var lat_deg = document.getElementById('lat_deg');
        var lat_min = document.getElementById('lat_min');
        var lat_sec = document.getElementById('lat_sec');
        var lng_deg = document.getElementById('lng_deg');
        var lng_min = document.getElementById('lng_min');
        var lng_sec = document.getElementById('lng_sec');
        var location = {
            lat : Number(lat_deg.value) + Number(lat_min.value/60) + Number(lat_sec.value)/10000/60,
            lng : -1*(Number(lng_deg.value) + Number(lng_min.value/60) + Number(lng_sec.value)/10000/60)
        };
        return location;
    };
};


//*****************************

console.log('creating page')
pageElements = new NewPage();
pageElements.addMap();
//======commented out the two line below
//pageElements.createTarget_popUp();
pageElements.specify_newInputs();
