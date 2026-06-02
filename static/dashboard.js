// =========================
// RELÓGIO
// =========================

function updateClock(){

    const now = new Date();

    document.getElementById("clock").innerHTML =
        now.toLocaleDateString("pt-BR")
        + " • "
        + now.toLocaleTimeString("pt-BR");
}

setInterval(updateClock, 1000);

updateClock();


// =========================
// CONTADORES
// =========================

const counters =
document.querySelectorAll(".counter");

counters.forEach(counter => {

    const target =
    Number(counter.dataset.target);

    let current = 0;

    const increment =
    Math.max(1, target / 30);

    const update = () => {

        if(current < target){

            current += increment;

            counter.innerText =
            Math.floor(current);

            requestAnimationFrame(update);

        }else{

            counter.innerText = target;
        }
    };

    update();
});