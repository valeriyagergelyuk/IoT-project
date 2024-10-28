
function changeFanImages(emailResult) {
    if(emailResult === "No") {
        document.getElementById('lightSwitch').src='../static/images/offSwitch.jpg';
         document.getElementById('fanState').src='../static/images/fanOff.jpg';
    } 
    else 
    {
        document.getElementById('lightSwitch').src='../static/images/onSwitch.jpg';
        document.getElementById('fanState').src='../static/images/fanOn.jpg';
    }
}

function toggleFan() {
    let emailResult;

    // Get result from a email somehow
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/offSwitch.jpg'){
        emailResult = 'Yes';
    }
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/onSwitch.jpg'){
        emailResult = 'No';
    }
    changeFanImages(emailResult);

    fetch('/toggle_motor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: emailResult }),
    });
}