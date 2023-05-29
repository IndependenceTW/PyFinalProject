import Cookies from 'universal-cookie';

export default function record(id, choice) {
    const cookies = new Cookies();
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", "Bearer " + cookies.get('token'));

    var raw;
    if (choice !== -1) {
        raw = JSON.stringify({
            "restaurant_id": id,
            "choice": choice
        });
    }
    else {
        raw = JSON.stringify({
            "restaurant_id": id
        });
    }

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    if (choice === -1) {
        fetch("http://127.0.0.1:5000/restaurant/record", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));
    }
    else {
        fetch("http://127.0.0.1:5000/restaurant/recommend/record", requestOptions)
        .then (response => response.text())
        .then (result => console.log(result))
        .catch(error => console.log('error', error));
    }
}