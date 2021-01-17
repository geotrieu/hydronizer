const serverAddress = "http://35.185.60.243:5000";

let t = 30 * 60;

function setTime() {
    var hours = document.getElementById("hours");
    var minutes = document.getElementById("minutes");
    if (hours && minutes) {
        t = hours * 60 + minutes
    }
}
    

const el = document.getElementById("set")
if (el){
    el.addEventListener('click', setTimeToDrink);
}


let device = "5843862085612977";

let currentMessageId = 0;
let blurred = false;
const countdown = document.getElementById('countdown');



function getLastWaterBreak() {
    return fetch(`${serverAddress}/lastwaterbreak?deviceid=${device}`);
}

function getTimeToDrink() {
    return fetch(`${serverAddress}/userTimer?deviceid=${device}`);
}

async function setTimeToDrink() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', `${serverAddress}/postNewTime`);
    xhr.setRequestHeader('Content-Type', 'application/json');

    let deviceName = await getDeviceName();
    let minutes = document.getElementById("minutes").value;
    let seconds = document.getElementById("seconds").value;

    xhr.send(JSON.stringify({"device_id": device, "device_name": deviceName, "new_time": minutes*60 + seconds}));
    currentMessageId = 0;
}

async function calculateTimeToDrink() {
    let res = await getTimeToDrink();
    let data = await res.json();
    return data.timer;
}

async function getDeviceName() {
    let res = await getTimeToDrink();
    let data = await res.json();
    return data.device_name;
}

async function calculateTime() {
    let res = await getLastWaterBreak();
    let data = await res.json();
    if (data.message_id == currentMessageId) return -100;
    let date = data.date;
    let time = data.time;
    let dateTime = Date.parse(date + " " + time);
    let differenceSeconds = Math.ceil((Date.now() - dateTime) / 1000);
    console.log(differenceSeconds);
    currentMessageId = data.message_id;
    return differenceSeconds;
}

setInterval(updateCountdown, 1000);

async function updateCountdown() {
    let elapsedTimeSinceDrink = await calculateTime();
    if (elapsedTimeSinceDrink != -100) { // message changed
        let timeToDrink = await calculateTimeToDrink();
        if (timeToDrink == null) return currentMessageId = 0;
        t = timeToDrink - elapsedTimeSinceDrink;
    }
    if (t <= 0) {
        t = 0;
        chrome.tabs.executeScript({
            code: 'document.getElementsByTagName("BODY")[0].style.filter = "blur(10px)"'
        });
        if (!blurred) {
            alert("The time is up. Please drink some water :)");
            blurred = true;
        }
    } else if (blurred) {
        chrome.tabs.executeScript({
            code: 'document.getElementsByTagName("BODY")[0].style.filter = ""'
        });
    }
    const m = Math.floor(t/60);

    let s = t % 60;

    s = s < 10 ? '0' + s : s;

    countdown.innerHTML = `${m}:${s}`;
    t--;
}