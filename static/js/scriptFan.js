setInterval(getEmailResult,9000);


function changeFanImages(emailResult) {
    if(emailResult == 'Yes') {
        // document.getElementById('lightSwitch').src='../static/images/offSwitch.jpg';
         document.getElementById('fanState').src='../static/images/fanOn.jpg';
    } 
    else 
    {
        // document.getElementById('lightSwitch').src='../static/images/onSwitch.jpg';
        document.getElementById('fanState').src='../static/images/fanOff.jpg';
    }
}

// function getEmailResult() {
//     fetch('/get_DHT_11')
//         .then(response => response.json())
//         .then(data => {
//             changeFanImages(data.fanStatus);
//             // temp.refresh(data.temperature);
//             // hum.refresh(data.humidity);
//             // document.getElementById('temp').getAttribute('value')==data.temperature;
//             // document.getElementById('hum').getAttribute('value')==data.humidity;
//         });
// }

function getEmailResult() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log(data.IsFanMeantToBeOn);
            changeFanImages(data.IsFanMeantToBeOn);

        });
}

function toggleFan(emailResult) {

    // Get result from a email somehow
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/offSwitch.jpg'){
        emailResult = 'Yes';
    }
    if(document.getElementById('lightSwitch').getAttribute('src')=='../static/images/onSwitch.jpg'){
        emailResult = 'No';
    }
    changeFanImages(emailResult);

    // fetch('/toggle_motor', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ state: emailResult }),
    // });
}