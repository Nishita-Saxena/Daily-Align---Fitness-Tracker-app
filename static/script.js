// script.js

function calculateBMI() {
    let height = parseFloat(document.getElementById('height').value) / 100;
    let weight = parseFloat(document.getElementById('weight').value);

    if (!height || !weight) return;

    let bmi = weight / (height * height);
    document.getElementById('bmi-result').innerText = "BMI: " + bmi.toFixed(2);

    let category = "";
    if (bmi < 18.5) category = "Underweight";
    else if (bmi < 25) category = "Normal";
    else if (bmi < 30) category = "Overweight";
    else category = "Obese";

    document.getElementById('bmi-category').innerText = "Category: " + category;
}