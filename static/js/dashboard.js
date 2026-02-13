document.addEventListener("DOMContentLoaded", function() {

    let city = document.getElementById("city").value;

    function getWeather(city) {
        let apiKey = "WEATHER_API";

        fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerHTML =
                data.main.temp + "°C";
        })
        .catch(() => {
            document.getElementById("result").innerHTML =
                "Weather unavailable";
        });
    }

    getWeather(city);
});