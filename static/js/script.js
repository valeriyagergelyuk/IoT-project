function toggleLED() {
    let ledState;
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/offSwitch.jpg'){
        ledState = 'ON';
    }
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/onSwitch.jpg'){
        ledState = 'OFF';
    }
    changeLedImages(ledState);
    
    fetch('/toggle_led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: ledState }),
    });
}

function changeLedImages(ledState) {
     if(ledState === "OFF"){
         document.getElementById('lightSwitch').src='../static/images/offSwitch.jpg';
         document.getElementById('lightbulb').src='../static/images/lightOff.png';
     }
     else{
         document.getElementById('lightSwitch').src='../static/images/onSwitch.jpg';
         document.getElementById('lightbulb').src='../static/images/lightOn.png';
     }
}

function getEmailLightData()
{
    fetch('/get_email_and_light_data')
    .then(response => response.json())
    .then(data => {
        document.getElementById("lightIntensity").innerText = "Light intensity: " + data["Light Amount"];
        document.getElementById("lightGauge").value = "" + data["Light Amount"];
        if (data["isEmailSent"]) {
            document.getElementById('lightbulb').src='../static/images/lightOn.png';
            document.getElementById("emailText").innerText = data["emailBody"];
        }
        else {
            document.getElementById('lightbulb').src='../static/images/lightOff.png';
            document.getElementById("emailText").innerText = "";
        }
        console.log(data);
    });
}

function getUserData(){
    fetch('/get_user_profile')
    .then(response => response.json())
    .then(data => {
        if(data["isUserLoggedIn"]){
            document.getElementById("loggedIn").innerText = "A new user has logged in";
        }
        if(data["isLoginFailed"]){
            document.getElementById("loggedIn").innerText = "Login failed";
        }
        document.getElementById("profileId").innerText = "Profile ID: " + data["userID"];
        document.getElementById("rfidTag").innerText = "RFID tag ID: " + data["userRFID"];
        document.getElementById("lightLevel").innerText = "Minimum Light Level: " + data["userLightThresh"];
        document.getElementById("tempLevel").innerText = "Maximum Temperature: " + data["userTempThresh"] + " C";
    });
}