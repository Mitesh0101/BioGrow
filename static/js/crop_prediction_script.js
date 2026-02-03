lucide.createIcons()

const validSoilTypes = [
    "Alluvial Soil",
    "Black Cotton Soil",
    "Black Soil",
    "Brown Loamy Soil",
    "Clay Loamy Soil",
    "Clay Soil",
    "Cotton Soil",
    "Deep Soil",
    "Friable Soil",
    "Heavy Black Soil",
    "Heavy Soil",
    "Laterite Soil",
    "Light Loamy Soil",
    "Light Soil",
    "Loamy Soil",
    "Medium Black Soil",
    "Red Lateritic Loamy Soil",
    "Red Loamy Soil",
    "Red Soil",
    "Rich Red Loamy Soil",
    "Salty Clay Loamy Soil",
    "Sandy Clay Loamy Soil",
    "Sandy Loamy Soil",
    "Sandy Soil",
    "Shallow Black Soil",
    "Silty Loamy Soil",
    "Well-Drained Loamy Soil",
    "Well-Drained Soil",
    "Well-Grained Deep Loamy Moist Soil"
];

const n = document.getElementById("nitrogen");
const nitrogenError = document.getElementById("nitrogenError");

const p = document.getElementById("phosphorus");
const phosphorusError = document.getElementById("phosphorusError");

const k = document.getElementById("potassium");
const potassiumError = document.getElementById("potassiumError");

const ph = document.getElementById("ph");
const phError = document.getElementById("phError");

const humidity = document.getElementById("humidity");
const humidityError = document.getElementById("humidityError");

const temp = document.getElementById("temperature");
const tempError = document.getElementById("tempError");

const soil = document.getElementById("soil");
for (let soilType of validSoilTypes) {
    soil.innerHTML += `<option value='${soilType}'>${soilType}</option>`;
}

n.addEventListener("change", event => {
    validateData(n, nitrogenError, "Nitrogen", 0, 300);
});

p.addEventListener("change", event => {
    validateData(p, phosphorusError, "Phosphorus", 0, 300);
});

k.addEventListener("change", event => {
    validateData(k, potassiumError, "Potassium", 0, 300);
});

ph.addEventListener("change", event => {
    validateData(ph, phError, "pH", 0, 14);
});

humidity.addEventListener("change", event => {
    validateData(humidity, humidityError, "Humidity", 0, 100);
});

temp.addEventListener("change", event => {
    validateData(temp, tempError, "Temperature", 0, 60);
});

function validateData(field, errorField, featureName, lowerLimit, upperLimit) {
    if (field.value<lowerLimit || field.value>upperLimit) {
        errorField.innerHTML = `<p class='small text-danger'>${featureName} value should be between ${lowerLimit} and ${upperLimit}!</p>`;
    }
    else {
        errorField.innerHTML = ``;
    }
}

async function predictCrop(event) {
    event.preventDefault();

    const formData = {
        n: n.value,
        p: p.value,
        k: k.value,
        ph: ph.value,
        temp: temp.value,
        humidity: humidity.value,
        soil_type: soil.value
    }

    // const crop = getPrediction(formData);

    const response = await fetch("/api/predict-crop", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
    });

    const data = await response.json();

    // return data.result;


    // let cropData = null;

    // if (temp >= 25 && rainfall < 700 && p > 50) {
    //     cropData = {
    //         name: "Cotton",
    //         match: 86.3,
    //         fertilizer: "NPK 19:19:19 @ 25kg/acre + Urea @ 50kg/acre",
    //         season: "October - November",
    //         yield: "45-50 quintals/acre",
    //         water: "Moderate",
    //         price: "₹2,100/quintal"
    //     };
    // }
    // else if (rainfall > 800 && ph >= 6 && ph <= 7.5) {
    //     cropData = {
    //         name: "Rice",
    //         match: 89.1,
    //         fertilizer: "DAP @ 50kg/acre + Urea @ 40kg/acre",
    //         season: "June - July",
    //         yield: "50-60 quintals/acre",
    //         water: "High",
    //         price: "₹2,300/quintal"
    //     };
    // }
    // else {
    //     cropData = {
    //         name: "Wheat",
    //         match: 82.4,
    //         fertilizer: "Urea @ 45kg/acre + SSP @ 30kg/acre",
    //         season: "November - December",
    //         yield: "40-45 quintals/acre",
    //         water: "Low",
    //         price: "₹2,050/quintal"
    //     };
    // }

    document.getElementById("cropName").innerText = data.result;
    // document.getElementById("matchText").innerText = cropData.match + "% Match";
    // document.getElementById("matchBar").style.width = cropData.match + "%";
    // document.getElementById("fertilizer").innerText = cropData.fertilizer;
    // document.getElementById("season").innerText = cropData.season;
    // document.getElementById("yield").innerText = cropData.yield;
    // document.getElementById("water").innerText = cropData.water;
    // document.getElementById("price").innerText = cropData.price;

    document.getElementById("result-before").classList.add("d-none");
    document.getElementById("result-after").classList.remove("d-none");

}