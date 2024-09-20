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
}