const start = 30;
let t = start * 60;

const countdown = document.getElementById('countdown');

setInterval(updateCountdown, 1000);

function updateCountdown() {
    const m = Math.floor(t/60);

    let s = t % 60;

    s = s < 10 ? '0' + s : s;

    countdown.innerHTML = `${m}:${s}`;
    t--;
}