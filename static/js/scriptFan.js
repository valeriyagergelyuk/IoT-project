function changeFanImages(emailResult) {
    if(emailResult == true) {
        // document.getElementById('lightSwitch').src='../static/images/offSwitch.jpg';
        document.getElementById('fanState').src='../static/images/fanturn.png';
        //document.getElementById('fanState').style.transform='rotate(20deg)';
    } 
    else 
    {
        // document.getElementById('lightSwitch').src='../static/images/onSwitch.jpg';
        document.getElementById('fanState').src='../static/images/fanOff.jpg';
    }
}

function getTempResult() {
    fetch('/get_temp_data')
    .then(response => response.json())
    .then(data => {
        temp.refresh(data.Temperature);
        hum.refresh(data.Humidity);

        console.log(data);
        changeFanImages(data.IsFanMeantToBeOn);
    });
}