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

async function beginSession() {

    let payload={
        questionCount: Object.fromEntries(
            Array.from(selectedSubTopics).map(sub => [sub, subTopicAmounts[sub] || 10])
        ),
        difficulties: Array.from(selectedDifficulties),
        extraTime: extraTime
    };
    
    
    await pywebview.api.submitSettings(payload);

    const timerSeconds=await pywebview.api.getSessionTimer();

    document.getElementById('custom-practice').style.display='none';
    document.getElementById('session-container').style.display='block';

    startCountdown(timerSeconds, () => {
        alert("Time has ended. Terminating session...");
        // needs to add submition logic...
    });

    loadCurrentQuestion();
}