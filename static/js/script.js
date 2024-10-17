function toggleLED() {
    let ledState;
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/offSwitch.jpg'){
        ledState = 'ON';
    }
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/onSwitch.jpg'){
        ledState = 'OFF';
    }
    changeImages(ledState);
    
    fetch('/toggle_led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: ledState }),
    });
}

function changeImages(ledState) {
     if(ledState === "OFF"){
         document.getElementById('lightSwitch').src='../static/images/offSwitch.jpg';
         document.getElementById('lightbulb').src='../static/images/lightOff.png';
     }
     else{
         document.getElementById('lightSwitch').src='../static/images/onSwitch.jpg';
         document.getElementById('lightbulb').src='../static/images/lightOn.png';
     }
 }

 function turnOnFan() {
    let emailResult;

    // Get result from a email somehow
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/offSwitch.jpg'){
        emailResult = 'ON';
    }
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/onSwitch.jpg'){
        emailResult = 'OFF';
    }

    fetch('/toggle_motor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: emailResult }),
    });
 }
