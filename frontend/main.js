let t = 30 * 60;

const device = 5843862085612977;

let currentMessageId = 0;
const countdown = document.getElementById('countdown');

function getLastWaterBreak() {
    return fetch(`http://localhost:5000/lastwaterbreak?deviceid=${device}`);
}

function getTimeToDrink() {
    return fetch(`http://localhost:5000/userTimer?deviceid=${device}`);
}

async function calculateTimeToDrink() {
    let res = await getTimeToDrink();
    let data = await res.json();
    return data.time;
}

async function calculateTime() {
    let res = await getLastWaterBreak();
    let data = await res.json();
    if (data.message_id == currentMessageId) return -1;
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
    if (elapsedTimeSinceDrink != -1) { // message changed
        let timeToDrink = await calculateTimeToDrink();
        t = timeToDrink - elapsedTimeSinceDrink;
    }
    if (t < 0) {
        t = 0;
        alert("DRINK");
        chrome.tabs.executeScript({
            code: 'document.getElementsByTagName("BODY")[0].style.filter = "blur(10px)"'
        });
    }
    const m = Math.floor(t/60);

    let s = t % 60;

    s = s < 10 ? '0' + s : s;

    countdown.innerHTML = `${m}:${s}`;
    t--;
}