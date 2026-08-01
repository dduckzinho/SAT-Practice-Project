let countdownInterval;
let totalSecondsRemaining=0;

function startCountdown(durationInSeconds, onCompleteCallback) {
    totalSecondsRemaining=durationInSeconds;

    if (countdownInterval) clearInterval(countdownInterval);

    countdownInterval=setInterval(() => {
        if (totalSecondsRemaining <= 0) {
            clearInterval(countdownInterval);
            if (onCompleteCallback) onCompleteCallback();
            return;
        }

        totalSecondsRemaining--;
        let minutes=Math.floor(totalSecondsRemaining / 60);
        let seconds=totalSecondsRemaining % 60;
        
        let formattedTime=`${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        document.getElementById('countdown-timer').innerText=`Time Remaining: ${formattedTime}`;
    }, 1000);
}
