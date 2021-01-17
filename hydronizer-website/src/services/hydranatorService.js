const axios = require('axios');

const serverAddress = "http://35.185.60.243:5000";

export function getWaterLeft(device) {
    return axios.get(serverAddress + '/lastwaterbreak?deviceid=' + device);
}

export function getMetrics(device) {
    return axios.get(serverAddress + '/metrics?deviceid=' + device);
}