const axios = require('axios');

function getLastWaterBreak() {
    axios.get('http://localhost:5000/lastwaterbreak')
    .then(function (response) {
        // handle success
        console.log(response);
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    })
    .then(function () {
        // always executed
    });
}

export default getLastWaterBreak;
