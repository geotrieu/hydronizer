const axios = require('axios');

export function getWaterLeft(device) {
    return axios.get('http://localhost:5000/lastwaterbreak?deviceid=' + device);
}

export function getMetrics(device) {
    return axios.get('http://localhost:5000/metrics?deviceid=' + device);
}