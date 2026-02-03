lucide.createIcons()

function predictCrop(event) {
    event.preventDefault();

    const n = document.getElementById("nitrogen").value;
    const p = document.getElementById("phosphorus").value;
    const k = document.getElementById("potassium").value;
    const ph = document.getElementById("ph").value;
    const rainfall = document.getElementById("rainfall").value;
    const temp = document.getElementById("temperature").value;

    let cropData = null;

    if (temp >= 25 && rainfall < 700 && p > 50) {
        cropData = {
            name: "Cotton",
            match: 86.3,
            fertilizer: "NPK 19:19:19 @ 25kg/acre + Urea @ 50kg/acre",
            season: "October - November",
            yield: "45-50 quintals/acre",
            water: "Moderate",
            price: "₹2,100/quintal"
        };
    }
    else if (rainfall > 800 && ph >= 6 && ph <= 7.5) {
        cropData = {
            name: "Rice",
            match: 89.1,
            fertilizer: "DAP @ 50kg/acre + Urea @ 40kg/acre",
            season: "June - July",
            yield: "50-60 quintals/acre",
            water: "High",
            price: "₹2,300/quintal"
        };
    }
    else {
        cropData = {
            name: "Wheat",
            match: 82.4,
            fertilizer: "Urea @ 45kg/acre + SSP @ 30kg/acre",
            season: "November - December",
            yield: "40-45 quintals/acre",
            water: "Low",
            price: "₹2,050/quintal"
        };
    }

    document.getElementById("cropName").innerText = cropData.name;
    document.getElementById("matchText").innerText = cropData.match + "% Match";
    document.getElementById("matchBar").style.width = cropData.match + "%";
    document.getElementById("fertilizer").innerText = cropData.fertilizer;
    document.getElementById("season").innerText = cropData.season;
    document.getElementById("yield").innerText = cropData.yield;
    document.getElementById("water").innerText = cropData.water;
    document.getElementById("price").innerText = cropData.price;

    document.getElementById("result-before").classList.add("d-none");
    document.getElementById("result-after").classList.remove("d-none");

}