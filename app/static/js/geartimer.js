var gearCount = 0;
var autonGears = 0;
var teleOp = 2*60+15
var goal = 14;
var time = 2*60+15;

var timer = false


function incGear(){
    gearCount = gearCount + 1;
//    document.getElementById("timer").innerHTML = gearCount + autonGears;
    if (!timer){
        setInterval(incTimer, 1000);
        timer = true;
    }

}

function incAuton(){
    autonGears = autonGears + 1;

}

function incTimer(){
    console.log("Timer")
    time = time - 1;
    var minutes = Math.floor(time / 60);
    var seconds = time - minutes * 60;
    document.getElementById("timer").innerHTML = String(minutes) + ":" + String(seconds)

    var speedGoal = (goal - autonGears) / teleOp;
    var speedCurrent = (gearCount) / (teleOp - time)

    console.log(speedCurrent)
    if (speedCurrent > speedGoal){
        document.getElementById("gearProj").innerHTML = "On Target"
    } else {
        document.getElementById("gearProj").innerHTML = "Off Target"
    }
  z
    document.getElementById("currentSpeed").innerHTML = "Current rate: " + String(speedCurrent*teleOp) + " gears per round"
    document.getElementById("necessarySpeed").innerHTML = "Required rate for 12: " + String((goal-gearCount-autonGears)/(teleOp-time)) + " gears per round"





}

