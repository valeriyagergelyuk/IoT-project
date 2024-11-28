let currentRFID = null;

function toggleLED() {
    let ledState;
    if (document.getElementById('lightSwitch').getAttribute('src') == '../static/images/offSwitch.jpg') {
        ledState = 'ON';
    }
    if (document.getElementById('lightSwitch').getAttribute('src') == '../static/images/onSwitch.jpg') {
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
    if (ledState === "OFF") {
        document.getElementById('lightSwitch').src = '../static/images/offSwitch.jpg';
        document.getElementById('lightbulb').src = '../static/images/lightOff.png';
    } else {
        document.getElementById('lightSwitch').src = '../static/images/onSwitch.jpg';
        document.getElementById('lightbulb').src = '../static/images/lightOn.png';
    }
}

function getEmailLightData() {
    fetch('/get_email_and_light_data')
    .then(response => response.json())
    .then(data => {
        document.getElementById("lightIntensity").innerText = "Light intensity: " + data["LightAmount"];
        document.getElementById("lightGauge").value = "" + data["LightAmount"];
        if (data["isEmailSent"]) {
            document.getElementById('lightbulb').src = '../static/images/lightOn.png';
            document.getElementById("emailText").innerText = data["emailBody"];
        } else {
            document.getElementById('lightbulb').src = '../static/images/lightOff.png';
            document.getElementById("emailText").innerText = "";
        }
        console.log(data);
    });
}

function getUserData() {
    fetch('/get_user')
    .then(response => response.json())
    .then(data => {
        if (!data["isUserLoggedIn"]) {
            document.getElementById("loggedIn").style.display = "block";
            document.getElementById("loggedIn").innerText = "Login";
            document.getElementById("profileId").innerText = "Profile ID:\nN/A";
            document.getElementById("rfidTag").innerText = "RFID tag ID:\nN/A";
        } else if (!data["correctUser"]) {
            document.getElementById("loggedIn").style.display = "block";
            document.getElementById("loggedIn").innerText = "Unknown Tag";
            setTimeout(function() {
                document.getElementById("loggedIn").style.display = "none";
            }, 3000);
            
        }else if (data["isUserLoggedIn"]) {
            document.getElementById("loggedIn").innerText = "Logged in";
            document.getElementById("profileId").innerText = "Profile ID: " + data["userID"];
            document.getElementById("rfidTag").innerText = "RFID tag ID: " + data["userRFID"];
            setTimeout(function() {
                document.getElementById("loggedIn").style.display = "none";
            }, 3000);
        } 
        document.getElementById("lightLevel").innerText = "Minimum Light Level: " + data["userLightThresh"];
        document.getElementById("tempLevel").innerText = "Maximum Temperature: " + data["userTempThresh"] + " C";
        //     document.getElementById("loggedIn").innerText = "Please scan a valid card to login";
        //     document.getElementById("profileId").innerText = "Profile ID: Unknown";
        //     document.getElementById("rfidTag").innerText = "RFID tag ID: Unknown"; // Display unknown if no user logged in
        // } else {
        //     document.getElementById("loggedIn").innerText = "Logged in";
        //     document.getElementById("profileId").innerText = "Profile ID: " + data["userID"];
            
        //     // Only show the RFID tag if it's valid (not 'none' or null)
        //     if (data["userRFID"] && data["userRFID"] !== "none") {
        //         document.getElementById("rfidTag").innerText = "RFID tag ID: " + data["userRFID"];
        //     } else {
        //         document.getElementById("rfidTag").innerText = "RFID tag ID: Unknown"; // Hide RFID tag if it's invalid
        //     }

        //     document.getElementById("lightLevel").innerText = "Minimum Light Level: " + data["userLightThresh"];
        //     document.getElementById("tempLevel").innerText = "Maximum Temperature: " + data["userTempThresh"] + " C";
        console.log(data);
    }); 
}
    

function onRFIDTagDetected(rfidTag) {
if (rfidTag !== currentRFID) {
        currentRFID = rfidTag;
        fetch('/login_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rfid: rfidTag }),
        })
        .then(response => response.json())
        .then(data => {
            getUserData();  
        });
    }
}