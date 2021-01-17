const axios = require('axios');

export default function getLastWaterBreak() {
    return axios.get('http://localhost:5000/lastwaterbreak');
}
