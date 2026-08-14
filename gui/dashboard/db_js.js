let TOPICS, SUB_TOPICS, SUB_TOPIC_TIME, DIFFICULTY;

let selectedSubjects=new Set();
let selectedTopics=new Set();
let selectedSubTopics=new Set();
let subTopicAmounts={}; 
let extraTime=0;
let selectedDifficulties=new Set();

window.addEventListener('pywebviewready', async function(){
    const config=await pywebview.api.getConfig();
    
    TOPICS=config.TOPICS;
    SUB_TOPICS=config.SUB_TOPICS;
    SUB_TOPIC_TIME=config.SUB_TOPIC_TIME;
    DIFFICULTY=config.DIFFICULTY;
    
    selectedDifficulties=new Set(Object.keys(DIFFICULTY));

    renderUI();
    initializeFullTest()
});

function renderUI(){
    let subjHTML='';
    Object.keys(TOPICS).forEach(subj=>{
        subjHTML += `<div class="form-check form-check-inline fs-5">
            <input class="form-check-input subj-cb" type="checkbox" id="subj-${subj}" value="${subj}">
            <label class="form-check-label" for="subj-${subj}">${subj}</label>
        </div>`;
    });
    document.getElementById('subjects-container').innerHTML=subjHTML;

    document.querySelectorAll('.subj-cb').forEach(cb=>{
        cb.addEventListener('change', (e)=>{
            if(e.target.checked) selectedSubjects.add(e.target.value);
            else selectedSubjects.delete(e.target.value);
            renderTopics();
        });
    });

    let diffHTML='';
    Object.keys(DIFFICULTY).forEach(diff=>{
        diffHTML += `<div class="form-check fs-5">
            <input class="form-check-input diff-cb" type="checkbox" id="diff-${diff}" value="${diff}" checked>
            <label class="form-check-label" for="diff-${diff}">${diff}</label>
        </div>`;
    });
    document.getElementById('difficulty-container').innerHTML=diffHTML;
    
    document.querySelectorAll('.diff-cb').forEach(cb=>{
        cb.addEventListener('change', (e)=>{
            if(e.target.checked) selectedDifficulties.add(e.target.value);
            else selectedDifficulties.delete(e.target.value);
        });
    });
}

function renderTopics(){
    let html='';
    selectedSubjects.forEach(subj=>{
        html += `<h5 class="mt-4 border-bottom pb-2">${subj} Topics</h5><div class="d-flex flex-wrap gap-4 mt-2">`;
        TOPICS[subj].forEach(topic=>{
            let cleanId=topic.replace(/\s+/g, '');
            html += `<div class="form-check">
                <input class="form-check-input topic-cb" type="checkbox" id="topic-${cleanId}" value="${topic}">
                <label class="form-check-label" for="topic-${cleanId}">${topic}</label>
            </div>`;
        });
        html += `</div>`;
    });
    document.getElementById('topics-container').innerHTML=html;

    selectedTopics.clear();
    renderSubTopics();

    document.querySelectorAll('.topic-cb').forEach(cb=>{
        cb.addEventListener('change', (e)=>{
            if(e.target.checked) selectedTopics.add(e.target.value);
            else selectedTopics.delete(e.target.value);
            renderSubTopics();
        });
    });
}

function renderSubTopics(){
    let html='';
    selectedTopics.forEach(topic=>{
        html += `<div class="topic-card"><h6 class="topic-title">${topic}</h6><div class="ms-3 mt-2">`;
        if (SUB_TOPICS[topic]){
            SUB_TOPICS[topic].forEach(sub=>{
                let cleanId=sub.replace(/\W/g, '');
                let checked=selectedSubTopics.has(sub)? 'checked':'';
                html += `<div class="form-check">
                    <input class="form-check-input subtopic-cb" type="checkbox" id="sub-${cleanId}" value="${sub}" ${checked}>
                    <label class="form-check-label" for="sub-${cleanId}">${sub}</label>
                </div>`;
            });
        }
        html += `</div></div>`;
    });
    document.getElementById('subtopics-container').innerHTML=html;

    let validSubs=new Set();
    selectedTopics.forEach(topic=>{
        if(SUB_TOPICS[topic]) SUB_TOPICS[topic].forEach(s=>validSubs.add(s));
    });
    selectedSubTopics.forEach(s=>{
        if(!validSubs.has(s)) selectedSubTopics.delete(s);
    });

    document.querySelectorAll('.subtopic-cb').forEach(cb=>{
        cb.addEventListener('change', (e)=>{
            if(e.target.checked){
                selectedSubTopics.add(e.target.value);
                if(!subTopicAmounts[e.target.value]) subTopicAmounts[e.target.value]=10;
            } else{
                selectedSubTopics.delete(e.target.value);
            }
            renderSliders();
        });
    });
    renderSliders();
}

function renderSliders(){
    let html='';
    if (selectedSubTopics.size===0){
        html='<p class="empty-message">Select subtopics in the Filters tab to see options here.</p>';
    } else{
        selectedSubTopics.forEach(sub=>{
            let val=subTopicAmounts[sub] || 10;
            let cleanId=sub.replace(/\W/g, '');
            html+=`
            <div class="slider-container">
                <div class="slider-label">${sub}</div>
                <input type="range" class="form-range q-slider" min="1" max="50" step="1" value="${val}" data-sub="${sub}">
                <div class="slider-value" id="val-${cleanId}">${val}</div>
            </div>`;
        });
    }
    document.getElementById('sliders-container').innerHTML=html;

    document.querySelectorAll('.q-slider').forEach(slider=>{
        slider.addEventListener('input', (e)=>{
            let sub=e.target.getAttribute('data-sub');
            let val=parseInt(e.target.value);
            subTopicAmounts[sub]=val;
            document.getElementById(`val-${sub.replace(/\W/g, '')}`).innerText=val;
            updateTime();
        });
    });
    updateTime();
}

document.getElementById('extra-time-slider').addEventListener('input', (e)=>{
    extraTime=parseInt(e.target.value);
    document.getElementById('extra-time-val').innerText=extraTime > 0 ? `+${extraTime} minutes` : 'No extra time';
    updateTime();
});

function updateTime(){
    let seconds=0;
    selectedSubTopics.forEach(sub=>{
        let amt=subTopicAmounts[sub] || 10;
        seconds+=(SUB_TOPIC_TIME[sub]*amt);
    });
    let totalSeconds=(seconds * 1.05) + (extraTime * 60);
    let mins=Math.floor(totalSeconds / 60);
    let secs=Math.floor(totalSeconds % 60);
    document.getElementById('timeDisplay').innerText=`Time: ${mins} minutes and ${secs} seconds.`;
}

async function beginCustomSession(){
    let payload={
        mode: 'custom',
        questionCount: Object.fromEntries(
            Array.from(selectedSubTopics).map(sub=>[sub, subTopicAmounts[sub]||10])
        ),
        difficulties: Array.from(selectedDifficulties),
        extraTime: extraTime
    };
    
    let targetUrl=await pywebview.api.submitSettings(payload);

    window.location.href='../qv_window.html';
}

// full test

let fullTestSubjects=new Set(['Math', 'English']);
let fullTestExtraTime=0;


function initializeFullTest(){
    const mathCB=document.getElementById('full-test-math');
    const englishCB=document.getElementById('full-test-english');

    const skipMathCB=document.getElementById('skip-module-math');
    const skipEnglishCB=document.getElementById('skip-module-english');

    mathCB.addEventListener('change', ()=>{
        if (mathCB.checked){
            fullTestSubjects.add('Math');
        } else{
            fullTestSubjects.delete('Math');

            skipMathCB.checked=false;
        }

        updateFullTestSkipControls();
    });

    englishCB.addEventListener('change', ()=>{
        if (englishCB.checked){
            fullTestSubjects.add('English');
        } else{
            fullTestSubjects.delete('English');

            skipEnglishCB.checked=false;
        }

        updateFullTestSkipControls();
    });

    document
        .getElementById('full-test-extra-time-slider')
        .addEventListener('input', (e)=>{

            fullTestExtraTime=parseInt(e.target.value);

            document.getElementById('full-test-extra-time-val').innerText=
                fullTestExtraTime > 0
                    ? `+${fullTestExtraTime} minutes`
                    : 'No extra time';

            document.getElementById('full-test-timeDisplay').innerText=
                `Extra Time: ${fullTestExtraTime} minutes`;
        });

    updateFullTestSkipControls();
}


function updateFullTestSkipControls(){
    const mathSelected=document.getElementById('full-test-math').checked;
    const englishSelected=document.getElementById('full-test-english').checked;

    const skipMathCB=document.getElementById('skip-module-math');
    const skipEnglishCB=document.getElementById('skip-module-english');

    skipMathCB.disabled=!mathSelected;
    skipEnglishCB.disabled=!englishSelected;

    if (!mathSelected){
        skipMathCB.checked=false;
    }

    if (!englishSelected){
        skipEnglishCB.checked=false;
    }
}


async function beginFullTestSession(){
    const mathSelected=
        document.getElementById('full-test-math').checked;

    const englishSelected=
        document.getElementById('full-test-english').checked;

    const skipMath=
        document.getElementById('skip-module-math').checked;

    const skipEnglish=
        document.getElementById('skip-module-english').checked;


    if (!mathSelected && !englishSelected){
        alert('Please select at least one module.');
        return;
    }


    const payload={
        mode: 'full_test',

        subjects:{
            Math: mathSelected,
            English: englishSelected
        },

        skipModuleOne:{
            Math: mathSelected && skipMath,
            English: englishSelected && skipEnglish
        },

        extraTime: fullTestExtraTime
    };


    const targetUrl=
        await pywebview.api.submitSettings(payload);

    window.location.href='../qv_window.html';
}
