var gearCount = 0;
var autonGears = 0;
var teleOp = 215
var goal = 14;
var myVar = setInterval(incTimer, 1000);
var time = 0;



function incGear(){
    gearCount = gearCount + 1;
    document.getElementById("incGear").value = gearCount + autonGears;

}

function incAuton(){
    autonGears = autonGears + 1;
}

function incTimer(){
    time = time + 1;
    var minutes = Math.floor(time / 60);
    var seconds = time - minutes * 60;
    var speedGoal = (goal - autonGears) / teleOp;
    var speedCurrent = (gearCount - autonGears) / (teleOp - seconds)


    if (speedCurrent < speedGoal){
        document.getElementById("gearProj").value = "On Target"
    } else {
        document.getElementById("gearProj").value = "Off Target"

    }



}

