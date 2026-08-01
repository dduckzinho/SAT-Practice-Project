

async function loadAndRenderCurrentQuestion(){
    let question=await pywebview.api.getCurrentQuestion();
    
    if (typeof question==='string'){
        try{
            question=JSON.parse(question);
        }catch (e){
            console.error("Failed to parse question JSON:", e);
            return;
        }
    }

    if (!question){
        alert("Session completed or no question available.");
        return;
    }


    document.getElementById('question-stem-container').innerHTML=question.stem || "No stem provided.";

    const optionsContainer=document.getElementById('answer-options-container');
    optionsContainer.innerHTML='';

    const qType=(question.type || "").toLowerCase();

    await pywebview.api.debug(question.options);

    if (qType==="mcq"){

        if (question.options){

            if (Array.isArray(question.options)) {

                question.options.forEach((opt, index) => {
                    optionsContainer.innerHTML += `
                        <div class="form-check mb-2 p-2 border border-secondary rounded">
                            <input
                                class="form-check-input"
                                type="radio"
                                name="answerOption"
                                id="opt${index}"
                                value="${opt.id}"
                                onchange="saveAnswer('${opt.id}')">

                            <label class="form-check-label w-100" for="opt${index}">
                                ${opt.content || opt.body || "Option text missing"}
                            </label>
                        </div>
                    `;
                });

            }else{

                Object.entries(question.options).forEach(([letter, opt], index) => {
                    optionsContainer.innerHTML += `
                        <div class="form-check mb-2 p-2 border border-secondary rounded">
                            <input
                                class="form-check-input"
                                type="radio"
                                name="answerOption"
                                id="opt${index}"
                                value="${letter}"
                                onchange="saveAnswer('${letter}')">

                            <label class="form-check-label w-100" for="opt${index}">
                                ${opt.content || opt.body || "Option text missing"}
                            </label>
                        </div>
                    `;
                });

            };
        }else{
            optionsContainer.innerHTML=`<p class="text-danger">Error: 'options' array is missing from Python response.</p>`;
        }
    }else if (qType==="spr" || qType==="grid_in"){
        optionsContainer.innerHTML=`
            <div class="mb-3">
                <label for="spr-input" class="form-label text-light">Enter your response:</label>
                <input type="text" id="spr-input" class="form-control bg-dark text-white border-secondary" placeholder="Type answer here..." oninput="saveAnswer(this.value)">
            </div>
        `;
    }else{
        optionsContainer.innerHTML=`<p class="text-warning">Warning: Unrecognized question type received: '${question.type}'</p>`;
    }
}

async function handleNextQuestion(){
    await pywebview.api.nextQuestion();
    await loadAndRenderCurrentQuestion();
}

async function handlePreviousQuestion(){
    await pywebview.api.previousQuestion();
    await loadAndRenderCurrentQuestion();
}

async function saveAnswer(userAnswer){
    // sends answer back to python to record in the session class
    await pywebview.api.submitAnswer(userAnswer);
}

window.addEventListener('pywebviewready', async function(){

    await loadAndRenderCurrentQuestion();

    const timerSeconds=await pywebview.api.getSessionTimer();
    
    if (typeof startCountdown === 'function') {
        startCountdown(timerSeconds, () => {
            alert("Time has ended.");
            // auto submit code todo
        });
    } else {
        console.error("Timer function not found. Check timer.js path.");
    }
});