lightSwitch = "off";

function toggleLED() {
    let ledState = document.getElementById('switch').checked ? 'ON' : 'OFF';
    fetch('/toggle_led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: ledState }),
    });

    document.getElementById('ledStatus').innerHTML = ledState === 'ON' ? 'LED is ON' : 'LED is OFF';

    //changeImages();
}

// function changeImages(){
//     if(lightSwitch == "off"){
//         document.getElementById('lightSwitch').scr='onSwitch.jpg';
//         document.getElementById('lightbulb').scr='lightOn.png';
//         lightSwitch = 'on';
//     }
//     else{
//         document.getElementById('lightSwitch').scr='offSwitch.jpg';
//         document.getElementById('lightbulb').scr='lightOff.png';
//         lightSwitch = 'off';
//     }
// }