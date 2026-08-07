
let questionStartTime=0;
let currentQuestionId=null; 
let timeSpent={};

async function loadAndRenderCurrentQuestion(){
    let question=await pywebview.api.getCurrentQuestion();
    
    if (typeof question==='string'){
        try{
            question=JSON.parse(question);
        } catch (e){
            console.error("Failed to parse question JSON:", e);
            return;
        }
    }

    if (!question){
        alert("Session completed or no question available.");
        return;
    }

    currentQuestionId=question.id;
    await pywebview.api.debug("current question: "+currentQuestionId); 
    questionStartTime=Date.now();

    document.getElementById('question-stem-container').innerHTML=question.stem||"No stem provided.";

    const stimulusContainer=document.getElementById("stimulus-container");
    const stimulusPanel=document.getElementById("stimulus-panel");
    const questionPanel=document.getElementById("question-panel");
    
    if (question.resource){
        stimulusPanel.classList.remove("d-none");
        questionPanel.classList.remove("col-12");
        questionPanel.classList.add("col-md-6");

        if (question.resource.startsWith("data:image/")){
            stimulusContainer.innerHTML=`<img src="${question.resource}" class="img-fluid">`;
        } else if (question.resource.trim().startsWith("<svg")){
            stimulusContainer.innerHTML=question.resource;
        } else{
            stimulusContainer.innerHTML=question.resource;
        }
    } else{
        stimulusContainer.innerHTML="";
        stimulusPanel.classList.add("d-none");
        questionPanel.classList.remove("col-md-6");
        questionPanel.classList.add("col-12");
    }
    
    const optionsContainer=document.getElementById('answer-options-container');
    optionsContainer.innerHTML='';

    const qType=(question.type||"").toLowerCase();

    await pywebview.api.debug(question.options);
    await pywebview.api.debug(question.resource);
    await pywebview.api.debug("-------------------------------------");

    if (qType === "mcq") {
        if (question.options) {
            if (Array.isArray(question.options)) {
                const letters = ['A', 'B', 'C', 'D', 'E', 'F']; // Covers up to 6 options
                
                question.options.forEach((opt, index) => {
                    const assignedLetter = letters[index] || String.fromCharCode(65 + index);
                    
                    optionsContainer.innerHTML += `
                        <div class="form-check mb-2 p-2 rounded">
                            <input
                                class="form-check-input"
                                type="radio"
                                name="answerOption"
                                id="opt${index}"
                                value="${assignedLetter}"
                                onchange="saveAnswer('${assignedLetter}')">

                            <label class="form-check-label w-100" for="opt${index}">
                                <strong>${assignedLetter}.</strong> ${opt.content || opt.body || "Option text missing"}
                            </label>
                        </div>
                    `;
                });
            } else {
                Object.entries(question.options).forEach(([letter, opt], index) => {
                    optionsContainer.innerHTML += `
                        <div class="form-check mb-2 p-2 rounded">
                            <input
                                class="form-check-input"
                                type="radio"
                                name="answerOption"
                                id="opt${index}"
                                value="${letter}"
                                onchange="saveAnswer('${letter}')">

                            <label class="form-check-label w-100" for="opt${index}">
                                <strong>${letter}.</strong> ${opt.content || opt.body || "Option text missing"}
                            </label>
                        </div>
                    `;
                });
            }
        } else {
            optionsContainer.innerHTML = `<p class="text-danger">Error: 'options' array is missing from Python response.</p>`;
        }
        
    } else if (qType==="spr"||qType==="grid_in"){
        optionsContainer.innerHTML=`
            <div class="mb-3">
                <label for="spr-input" class="form-label text-light">Enter your response:</label>
                <input type="text" id="spr-input" class="form-control bg-dark text-white" placeholder="Type answer here..." oninput="saveAnswer(this.value)">
            </div>
        `;
    } else{
        optionsContainer.innerHTML=`<p class="text-warning">Warning: Unrecognized question type received: '${question.type}'</p>`;
    }

    const nextBtn=document.getElementById('next-btn');
    const submitBtn=document.getElementById('submit-btn');
    const prevBtn=document.getElementById('prev-btn');

    if (question.isLast){
        nextBtn.classList.add('d-none');
        submitBtn.classList.remove('d-none');
    } else{
        nextBtn.classList.remove('d-none');
        submitBtn.classList.add('d-none');
    }

    if (question.isFirst){
        prevBtn.disabled=true;
    } else{
        prevBtn.disabled=false;
    }
}

function recordAndSyncTime(){
    if (currentQuestionId && questionStartTime>0){
        const elapsed=Date.now()-questionStartTime;
        await pywebview.api.updateQuestionTime(elapsed);
        questionStartTime=Date.now(); 
    }
}

async function handleNextQuestion(){
    recordAndSyncTime();
    await pywebview.api.nextQuestion();
    await loadAndRenderCurrentQuestion();
}

async function handlePreviousQuestion(){
    recordAndSyncTime();
    await pywebview.api.previousQuestion();
    await loadAndRenderCurrentQuestion();
}

async function saveAnswer(userAnswer){
    await pywebview.api.submitAnswer(userAnswer);
}


async function submitFinalTest(){
    const submitBtn=document.getElementById('submit-btn');
    if (submitBtn){
        submitBtn.disabled=true;
        submitBtn.innerText="Submitting...";
    }

    await recordAndSyncTime();

    try{
        const result=await pywebview.api.finalizeSession();
        
        if (result && result.status==="success"){
            showResultsDashboard(result.score);
        } else{
            await pywebview.api.debug("No result or result was unsucessful.");
        }
    } catch (error){
        await pywebview.api.debug("Error: "+error);
    }
}

window.addEventListener('pywebviewready', async function(){
    await loadAndRenderCurrentQuestion();

    const timerSeconds=await pywebview.api.getSessionTimer();
    
    if (typeof startCountdown==='function'){
        startCountdown(timerSeconds, () =>{
            alert("Time has ended.");
            submitFinalTest();
        });
    } else{
        console.error("Timer function not found. Check timer.js path.");
    }
});