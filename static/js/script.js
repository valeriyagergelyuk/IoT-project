lightSwitch = "off";

function toggleLED() {
    //let ledState = document.getElementById('switch').checked ? 'ON' : 'OFF';

    let ledState;
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/offSwitch.jpg'){
        ledState = 'ON';
        //changeImages(ledState);
    }if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/onSwitch.jpg'){
        ledState = 'OFF';
        //changeImages(ledState);
    }
    changeImages(ledState);
    fetch('/toggle_led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: ledState }),
    });
    document.getElementById('ledStatus').innerHTML = ledState === 'ON' ? 'LED is ON' : 'LED is OFF';
    
}

function changeImages(ledState){
     if(ledState === "OFF"){
         document.getElementById('lightSwitch').src='../static/images/offSwitch.jpg';
         document.getElementById('lightbulb').src='../static/images/lightOff.png';
     }
     else{
         document.getElementById('lightSwitch').src='../static/images/onSwitch.jpg';
         document.getElementById('lightbulb').src='../static/images/lightOn.png';
     }
 }
