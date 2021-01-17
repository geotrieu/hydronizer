const start = 30;
let t = start * 60;

const device = 5843862085612977;

let currentMessageId = 0;
const countdown = document.getElementById('countdown');

function getLastWaterBreak() {
    return fetch(`http://localhost:5000/lastwaterbreak?deviceid=${device}`);
}

async function calculateTime() {
    let res = await getLastWaterBreak();
    let data = await res.json();
    console.log(currentMessageId);
    if (data.message_id == currentMessageId) return -1;
    let date = data.date;
    let time = data.time;
    let dateTime = Date.parse(date + " " + time);
    let differenceSeconds = Math.ceil((Date.now() - dateTime) / 1000);
    currentMessageId = data.message_id;
    console.log("dS:" + differenceSeconds)
    return differenceSeconds;
}

setInterval(updateCountdown, 1000);

chrome.runtime.onMessage.addListener(
    function(message, callback) {
      if (message == "changeColor"){
        chrome.tabs.executeScript({
          code: 'document.body.style.backgroundColor="orange"'
        });
      }
    });

async function updateCountdown() {
    let elapsedTimeSinceDrink = await calculateTime();
    if (elapsedTimeSinceDrink != -1) { // use cached message, message never changed
        t = start * 60 - elapsedTimeSinceDrink;
    }
    if (t <= 0) {
        t = 0;
        chrome.tabs.executeScript({
            code: 'document.getElementsByTagName("BODY")[0].style.filter = "blur(10px)"'
        });
        alert("DRINK");
    }
    const m = Math.floor(t/60);

    let s = t % 60;

    s = s < 10 ? '0' + s : s;

    countdown.innerHTML = `${m}:${s}`;
    t--;
}