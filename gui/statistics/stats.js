Chart.defaults.color='#adb5bd';
Chart.defaults.scale.grid.color='#343a40';
Chart.defaults.plugins.tooltip.backgroundColor='rgba(0, 0, 0, 0.85)';
Chart.defaults.plugins.tooltip.titleColor='#fff';

let charts={};
let globalConfig={ SUB_TOPIC_TIME:{}};

async function initializeDashboard(){
    try{
        const rawLogs=await pywebview.api.getLogs();

        const config=await pywebview.api.getConfig();
        if (config && config.SUB_TOPIC_TIME){
            globalConfig.SUB_TOPIC_TIME=config.SUB_TOPIC_TIME;
        }

        if (rawLogs && rawLogs.length>0){
            const sortedData=rawLogs.map((item,index)=>({...item,_originalIndex:index}))
                .sort((a,b)=>{
                    const dateDiff=new Date(a.date)-new Date(b.date);
                    if (dateDiff!==0) return dateDiff;

                    const sessionDiff=String(a.sessionId ?? '').localeCompare(
                        String(b.sessionId ?? ''),
                        undefined,
                       {numeric:true}
                    );
                    if (sessionDiff!==0) return sessionDiff;

                    return a._originalIndex-b._originalIndex;
                });

            buildDashboard(sortedData);
            setupFilters(sortedData);
        } else{
            document.getElementById('stats-content').innerHTML=`
                <div class="text-center mt-5">
                    <h4 class="text-muted">No practice data found.</h4>
                    <p class="text-muted">Complete a session to see your statistics!</p>
                </div>`;
        }
    } catch(error){
        console.error("Error communicating with Python API:", error);
    }
}

if (window.pywebview){
    initializeDashboard();
} else{
    window.addEventListener('pywebviewready', initializeDashboard);
}

const isCorrect=(d)=>{
    return d.correct==="True";
};

const parseTime=(d)=>{
    const t=parseFloat(d.timeSpent);
    return Number.isFinite(t) ? t:null;
};

const calcStats=(data)=>{
    if (!data || !data.length){
        return{
            total:0,
            accuracy:0,
            avgTime:0,
            medTime:0,
            correctCount:0
        };
    }

    const correctCount=data.filter(isCorrect).length;

    const times=data
        .map(parseTime)
        .filter(t=>t!==null)
        .sort((a,b)=>a-b);

    const avgTime=times.length
        ? times.reduce((a,b)=>a+b,0)/times.length
        :0;

    let medTime=0;
    if (times.length){
        medTime=times.length % 2!==0
            ? times[Math.floor(times.length/2)]
            :(times[times.length/2-1]+times[times.length/2])/2;
    }

    return{
        total:data.length,
        correctCount,
        accuracy:(correctCount/data.length)*100,
        avgTime:avgTime/1000,
        medTime:medTime/1000
    };
};

const groupBy=(data,key)=>{
    return data.reduce((acc,item)=>{
        const value=item[key] ?? "Unknown";
        if (!acc[value]) acc[value]=[];
        acc[value].push(item);
        return acc;
    },{});
};

const destroyChart=(canvasId)=>{
    if (charts[canvasId]){
        charts[canvasId].destroy();
        delete charts[canvasId];
    }
};

function buildDashboard(data){
    populateOverviewCards(data);
    populateRecentPerformance(data);
    populateCorrectVsIncorrectTime(data);

    const bySubject=groupBy(data,'subject');
    renderBarChart('chartSubject',bySubject,'Subject Accuracy','#0d6efd');

    const byDifficulty=groupBy(data,'difficulty');
    renderBarChart('chartDifficulty',byDifficulty,'Difficulty Accuracy','#198754');

    renderRollingAccuracyChart('chartTime',data);

    updateFilteredCharts(data);
    updateActionableInsights(data);
    buildDetailedTable(data);
}

function populateOverviewCards(data){
    const overall=calcStats(data);

    document.getElementById('stat-total').innerText=overall.total;
    document.getElementById('stat-accuracy').innerText=overall.accuracy.toFixed(1)+'%';
    document.getElementById('stat-avg-time').innerText=overall.avgTime.toFixed(1)+'s';
    document.getElementById('stat-med-time').innerText=overall.medTime.toFixed(1)+'s';

    const last20=data.slice(-20);
    document.getElementById('stat-last20').innerText=
        calcStats(last20).accuracy.toFixed(1)+'%';

    let currentStreak=0;
    let maxStreak=0;

    for (let i=0;i<data.length;i++){
        if (isCorrect(data[i])){
            currentStreak++;
            maxStreak=Math.max(maxStreak,currentStreak);
        } else{
            currentStreak=0;
        }
    }

    document.getElementById('stat-cur-streak').innerText=currentStreak;
    document.getElementById('stat-max-streak').innerText=maxStreak;
}

function populateRecentPerformance(data){
    document.getElementById('acc-last10').innerText=
        calcStats(data.slice(-10)).accuracy.toFixed(1)+'%';

    document.getElementById('acc-last20').innerText=
        calcStats(data.slice(-20)).accuracy.toFixed(1)+'%';

    document.getElementById('acc-last50').innerText=
        calcStats(data.slice(-50)).accuracy.toFixed(1)+'%';

    const improvementEl=document.getElementById('acc-improvement');

    if (data.length>=40){
        const first20Acc=calcStats(data.slice(0,20)).accuracy;
        const last20Acc=calcStats(data.slice(-20)).accuracy;
        const diff=last20Acc-first20Acc;

        improvementEl.innerText=diff>=0
            ? `+${diff.toFixed(1)} pts`
            :`${diff.toFixed(1)} pts`;

        improvementEl.className=
            diff>=0
            ? 'fw-bold text-success'
            :'fw-bold text-danger';
    } else{
        improvementEl.innerText='Need 40+ Qs';
        improvementEl.className='fw-bold text-muted';
    }
}

function populateCorrectVsIncorrectTime(data){
    const correctData=data.filter(isCorrect);
    const wrongData=data.filter(d=>!isCorrect(d));

    const correctStats=calcStats(correctData);
    const wrongStats=calcStats(wrongData);

    document.getElementById('time-correct-avg').innerText=
        correctStats.avgTime.toFixed(1)+'s';
    document.getElementById('time-correct-med').innerText=
        correctStats.medTime.toFixed(1)+'s';

    document.getElementById('time-wrong-avg').innerText=
        wrongStats.avgTime.toFixed(1)+'s';
    document.getElementById('time-wrong-med').innerText=
        wrongStats.medTime.toFixed(1)+'s';
}

function renderBarChart(canvasId,groupedData,label,color,horizontal=false,isTime=false){
    const canvas=document.getElementById(canvasId);
    if (!canvas) return;

    const ctx=canvas.getContext('2d');
    destroyChart(canvasId);

    const labels=Object.keys(groupedData);
    const customMeta=labels.map(key=>calcStats(groupedData[key]));

    const displayLabels=labels.map((lbl,idx)=>{
        if (canvasId==='chartSubtopic' && customMeta[idx].total<5){
            return `${lbl} (Low sample)`;
        }
        return lbl;
    });

    const dataPoints=customMeta.map(meta=>isTime ? meta.avgTime :meta.accuracy);

    charts[canvasId]=new Chart(ctx,{
        type:'bar',
        data:{
            labels:displayLabels,
            datasets:[{
                label,
                data:dataPoints,
                backgroundColor:color,
                borderRadius:4,
                customMeta
            }]
        },
        options:{
            indexAxis:horizontal?'y':'x',
            responsive:true,
            maintainAspectRatio:false,
            scales:{
                [horizontal?'x':'y']:{
                    min:0,
                    max:isTime?undefined:100
                }
            },
            plugins:{
                tooltip:{
                    callbacks:{
                        label:(ctx)=>{
                            const meta=ctx.dataset.customMeta[ctx.dataIndex];

                            if (isTime){
                                return `Avg Time:${meta.avgTime.toFixed(1)}s (${meta.total} Qs)`;
                            }

                            return `${ctx.dataset.label}:${meta.accuracy.toFixed(1)}% (${meta.correctCount}/${meta.total})`;
                        }
                    }
                }
            }
        }
    });
}

function renderAttemptsChart(canvasId,groupedData){
    const canvas=document.getElementById(canvasId);
    if (!canvas) return;

    const ctx=canvas.getContext('2d');
    destroyChart(canvasId);

    const labels=Object.keys(groupedData);
    const dataPoints=labels.map(key=>groupedData[key].length);

    charts[canvasId]=new Chart(ctx,{
        type:'bar',
        data:{
            labels,
            datasets:[{
                label:'Questions Attempted',
                data:dataPoints,
                backgroundColor:'#6c757d'
            }]
        },
        options:{
            indexAxis:'y',
            responsive:true,
            maintainAspectRatio:false,
            plugins:{
                tooltip:{
                    callbacks:{
                        label:(ctx)=>`Attempted:${ctx.raw}`
                    }
                }
            }
        }
    });
}

function renderRollingAccuracyChart(canvasId,data){
    const canvas=document.getElementById(canvasId);
    if (!canvas) return;

    const ctx=canvas.getContext('2d');
    destroyChart(canvasId);

    const rollingData=[];
    const labels=[];
    const windowSize=20;

    data.forEach((q,index)=>{
        labels.push(index+1);

        const start=Math.max(0,index-windowSize+1);
        const window=data.slice(start,index+1);

        rollingData.push(calcStats(window).accuracy);
    });

    charts[canvasId]=new Chart(ctx,{
        type:'line',
        data:{
            labels,
            datasets:[{
                label:`Rolling Accuracy (Last ${windowSize})`,
                data:rollingData,
                borderColor:'#0dcaf0',
                tension:0.1,
                fill:false,
                pointRadius:1
            }]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false,
            scales:{
                y:{
                    min:0,
                    max:100,
                    title:{
                        display:true,
                        text:'Accuracy (%)'
                    }
                },
                x:{
                    title:{
                        display:true,
                        text:'Question Number'
                    }
                }
            }
        }
    });
}

function setupFilters(data){
    const subjectFilter=document.getElementById('filter-subject');
    const topicFilter=document.getElementById('filter-topic');

    if (!subjectFilter || !topicFilter) return;

    const updateTopics=()=>{
        const selectedSubject=subjectFilter.value;

        topicFilter.innerHTML='<option value="All">All Topics</option>';

        const relevantTopics=[
            ...new Set(
                data
                    .filter(d=>selectedSubject==='All' || d.subject===selectedSubject)
                    .map(d=>d.topic)
                    .filter(Boolean)
            )
        ];

        relevantTopics.forEach(topic=>{
            topicFilter.innerHTML+=
                `<option value="${escapeHtml(topic)}">${escapeHtml(topic)}</option>`;
        });

        updateFilteredCharts(data);
    };

    subjectFilter.addEventListener('change',updateTopics);
    topicFilter.addEventListener('change',()=>updateFilteredCharts(data));

    updateTopics();
}

function updateFilteredCharts(data){
    const subjFilter=document.getElementById('filter-subject');
    const topicFilter=document.getElementById('filter-topic');

    if (!subjFilter || !topicFilter) return;

    const selectedSubject=subjFilter.value;
    const selectedTopic=topicFilter.value;

    let filteredData=data;

    if (selectedSubject!=='All'){
        filteredData=filteredData.filter(d=>d.subject===selectedSubject);
    }

    const byTopic=groupBy(filteredData,'topic');

    renderBarChart(
        'chartTopic',
        byTopic,
        'Topic Accuracy (%)',
        '#6f42c1',
        true,
        false
    );

    if (selectedTopic!=='All'){
        filteredData=filteredData.filter(d=>d.topic===selectedTopic);
    }

    const bySubtopic=groupBy(filteredData,'subtopic');

    renderBarChart(
        'chartSubtopic',
        bySubtopic,
        'Subtopic Accuracy (%)',
        '#20c997',
        true,
        false
    );

    renderAttemptsChart('chartAttempts',bySubtopic);
}

function getExpectedSubtopicTime(subtopic){
    if (!globalConfig.SUB_TOPIC_TIME) return null;

    const target=globalConfig.SUB_TOPIC_TIME[subtopic];

    return Number.isFinite(Number(target))
        ? Number(target)
        :null;
}

function getExpectedTopicTime(topicData){
    const validTargets=topicData
        .map(q=>getExpectedSubtopicTime(q.subtopic))
        .filter(t=>t!==null);

    if (!validTargets.length) return null;

    return validTargets.reduce((sum,t)=>sum+t,0)/validTargets.length;
}

function getTimeMetrics(data){
    const stats=calcStats(data);
    const target=getExpectedTopicTime(data);

    if (!target || !stats.total || !stats.avgTime){
        return{
            target:null,
            ratio:null,
            difference:null,
            differencePct:null
        };
    }

    const ratio=stats.avgTime/target;
    const difference=stats.avgTime-target;
    const differencePct=(difference/target)*100;

    return{
        target,
        ratio,
        difference,
        differencePct
    };
}

function getQuadrant(stats,timeMetrics){
    if (stats.total<5 || timeMetrics.ratio===null){
        return 'insufficient';
    }

    const highAccuracy=stats.accuracy>=75;
    const slow=timeMetrics.ratio>1.15;

    if (highAccuracy && !slow) return 'strong';
    if (highAccuracy && slow) return 'speed';
    if (!highAccuracy && !slow) return 'knowledge';
    return 'priority';
}

function updateActionableInsights(data){
    const bySubtopic=groupBy(data,'subtopic');

    const allSubtopics=Object.keys(bySubtopic)
        .map(subtopic=>{
            const stats=calcStats(bySubtopic[subtopic]);
            const time=getTimeMetrics(bySubtopic[subtopic]);

            return{
                name:subtopic,
                data:bySubtopic[subtopic],
                stats,
                time,
                quadrant:getQuadrant(stats,time)
            };
        });

    const sufficient=allSubtopics
        .filter(item=>item.stats.total>=5);

    const insufficient=allSubtopics
        .filter(item=>item.stats.total<5)
        .sort((a,b)=>b.stats.total-a.stats.total);

    const weakest=[...sufficient]
        .sort((a,b)=>a.stats.accuracy-b.stats.accuracy)
        .slice(0,5);

    const strongest=[...sufficient]
        .sort((a,b)=>b.stats.accuracy-a.stats.accuracy)
        .slice(0,5);

    const lists={
        insufficient:document.getElementById('list-insufficient'),
        weakest:document.getElementById('list-weakest'),
        strongest:document.getElementById('list-strongest'),
        strong:document.getElementById('quad-strong'),
        speed:document.getElementById('quad-speed'),
        knowledge:document.getElementById('quad-knowledge'),
        priority:document.getElementById('quad-priority')
    };

    Object.values(lists).forEach(el=>{
        if (el) el.innerHTML='';
    });

    insufficient.forEach(item=>{
        lists.insufficient.innerHTML+=`
            <li class="list-group-item bg-transparent text-light">
                <div class="fw-bold">${escapeHtml(item.name)}</div>
                <small class="text-muted">${item.stats.total} question${item.stats.total===1?'':'s'} attempted</small>
            </li>`;
    });

    if (!insufficient.length){
        lists.insufficient.innerHTML=
            `<li class="list-group-item bg-transparent text-muted">None</li>`;
    }

    weakest.forEach((item,index)=>{
        lists.weakest.innerHTML+=createRankingItem(item,index+1,'danger');
    });

    strongest.forEach((item,index)=>{
        lists.strongest.innerHTML+=createRankingItem(item,index+1,'success');
    });

    if (!weakest.length){
        lists.weakest.innerHTML=
            `<li class="list-group-item bg-transparent text-muted">Need at least 5 questions.</li>`;
    }

    if (!strongest.length){
        lists.strongest.innerHTML=
            `<li class="list-group-item bg-transparent text-muted">Need at least 5 questions.</li>`;
    }

    const quadrantGroups={
        strong:[],
        speed:[],
        knowledge:[],
        priority:[]
    };

    sufficient.forEach(item=>{
        if (quadrantGroups[item.quadrant]){
            quadrantGroups[item.quadrant].push(item);
        }
    });

    Object.entries(quadrantGroups).forEach(([quadrant,items])=>{
        items.sort((a,b)=>a.stats.accuracy-b.stats.accuracy);

        items.forEach(item=>{
            lists[quadrant].innerHTML+=createQuadrantListItem(item);
        });

        if (!items.length){
            lists[quadrant].innerHTML=
                `<li class="text-muted">None</li>`;
        }
    });

    renderQuadrantBubbleChart(sufficient);
}

function createRankingItem(item,rank,badgeColor){
    return `
        <li class="list-group-item bg-transparent text-light d-flex justify-content-between align-items-center">
            <div>
                <span class="fw-bold">${rank}. ${escapeHtml(item.name)}</span><br>
                <small class="text-muted">
                    ${item.stats.accuracy.toFixed(0)}% ·
                    ${item.stats.correctCount}/${item.stats.total} ·
                    ${item.stats.avgTime.toFixed(0)}s avg
                </small>
            </div>
            <span class="badge bg-${badgeColor} rounded-pill fs-6">
                ${item.stats.accuracy.toFixed(0)}%
            </span>
        </li>`;
}

function createQuadrantListItem(item){
    const timeText=item.time.ratio===null
        ? 'N/A'
        :`${item.time.ratio.toFixed(2)}× target`;

    return `
        <li class="mb-2">
            <span class="fw-bold">${escapeHtml(item.name)}</span>
            <small class="text-muted d-block">
                ${item.stats.accuracy.toFixed(0)}% ·
                ${item.stats.correctCount}/${item.stats.total} ·
                ${item.stats.avgTime.toFixed(0)}s ·
                ${timeText}
            </small>
        </li>`;
}

function renderQuadrantBubbleChart(items){
    const canvas=document.getElementById('chartQuadrantBubble');
    if (!canvas) return;

    const ctx=canvas.getContext('2d');
    destroyChart('chartQuadrantBubble');

    const colors={
        strong:'#198754',
        speed:'#0dcaf0',
        knowledge:'#ffc107',
        priority:'#dc3545'
    };

    const datasets=['strong','speed','knowledge','priority'].map(quadrant=>{
        const quadrantItems=items.filter(item=>item.quadrant===quadrant);

        return{
            label:quadrantLabel(quadrant),
            data:quadrantItems.map(item=>({
                x:item.time.ratio,
                y:item.stats.accuracy,
                r:Math.max(5,Math.min(16,5+item.stats.total/4)),
                name:item.name,
                count:item.stats.total,
                avgTime:item.stats.avgTime,
                target:item.time.target,
                ratio:item.time.ratio
            })),
            backgroundColor:colors[quadrant],
            borderColor:colors[quadrant],
            borderWidth:1
        };
    });

    charts['chartQuadrantBubble']=new Chart(ctx,{
        type:'bubble',
        data:{ datasets },

        options:{
            responsive: true,
            maintainAspectRatio: false,

            animation:{
                duration: 800
            },

            transitions:{
                zoom:{
                    animation:{
                        duration: 0
                    }
                },
                resize:{
                    animation:{
                        duration: 0
                    }
                }
            },

            scales:{
                x:{
                    min:0.5,
                    title:{
                        display:true,
                        text:'Time Ratio (Actual/Target)'
                    },
                    ticks:{
                        callback:value=>`${Number(value).toFixed(1)}×`
                    },
                    grid:{
                        color:'#343a40'
                    }
                },

                y:{
                    min:0,
                    max:100,
                    title:{
                        display:true,
                        text:'Accuracy (%)'
                    }
                }
            },

            plugins:{
                zoom:{
                    pan:{
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom:{
                        wheel:{
                            enabled: true
                        },
                        pinch:{
                            enabled: true
                        },
                        mode: 'xy'
                    }
                },

                tooltip:{
                    callbacks:{
                        title:()=>[],
                        label:(ctx)=>{
                            const p=ctx.raw;

                            return [
                                p.name,
                                `Accuracy:${p.y.toFixed(1)}%`,
                                `Average:${p.avgTime.toFixed(1)}s`,
                                `Target:${p.target.toFixed(1)}s`,
                                `Time Ratio:${p.ratio.toFixed(2)}×`,
                                `Questions:${p.count}`
                            ];
                        }
                    }
                },

                zoom:{
                    pan:{
                        enabled:true,
                        mode:'xy'
                    },

                    zoom:{
                        wheel:{
                            enabled:true
                        },
                        pinch:{
                            enabled:true
                        },
                        mode:'xy'
                    }
                }
            }
        },

        plugins:[{
            id:'quadrantLines',

            afterDraw(chart){
                const{ ctx, chartArea, scales }=chart;

                if (!chartArea) return;

                const xThreshold=scales.x.getPixelForValue(1.15);
                const yThreshold=scales.y.getPixelForValue(75);

                ctx.save();

                ctx.setLineDash([6, 6]);
                ctx.lineWidth=1;
                ctx.strokeStyle='#94546a';

                ctx.beginPath();
                ctx.moveTo(xThreshold, chartArea.top);
                ctx.lineTo(xThreshold, chartArea.bottom);
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(chartArea.left, yThreshold);
                ctx.lineTo(chartArea.right, yThreshold);
                ctx.stroke();

                ctx.restore();
            }
        }]
    });
}

function quadrantLabel(quadrant){
    const labels={
        strong:'Strong',
        speed:'Speed Practice',
        knowledge:'Knowledge Gap',
        priority:'Priority'
    };

    return labels[quadrant];
}

function buildDetailedTable(data){
    const tbody=document.querySelector('#detailed-table tbody');
    if (!tbody) return;

    tbody.innerHTML='';

    const byTopic=groupBy(data,'topic');

    Object.keys(byTopic).forEach(topic=>{
        const topicData=byTopic[topic];
        const stats=calcStats(topicData);
        const time=getTimeMetrics(topicData);

        let ratioText='N/A';
        let statusBadge='<span class="badge bg-secondary">Unknown</span>';

        if (time.ratio!==null){
            ratioText=`${time.ratio.toFixed(2)}×`;

            if (time.ratio>1.15){
                statusBadge='<span class="badge bg-danger">Slow</span>';
            } else if (time.ratio<0.85){
                statusBadge='<span class="badge bg-success">Fast</span>';
            } else{
                statusBadge='<span class="badge bg-info">On target</span>';
            }
        }

        const tr=document.createElement('tr');

        tr.innerHTML=`
            <td>${escapeHtml(topic)}</td>
            <td>${stats.total}</td>
            <td>${stats.accuracy.toFixed(1)}%</td>
            <td>${stats.avgTime.toFixed(1)}s</td>
            <td>${time.target!==null ? time.target.toFixed(1)+'s' :'N/A'}</td>
            <td>${ratioText}</td>
            <td>${statusBadge}</td>
        `;

        tbody.appendChild(tr);
    });
}

function escapeHtml(value){
    return String(value)
        .replaceAll('&','&amp;')
        .replaceAll('<','&lt;')
        .replaceAll('>','&gt;')
        .replaceAll('"','&quot;')
        .replaceAll("'","&#039;");
}