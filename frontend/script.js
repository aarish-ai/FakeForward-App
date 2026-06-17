const input = document.getElementById('message-input');
const charCount = document.getElementById('char-count');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsSection = document.getElementById('results-section');
const loadingState = document.getElementById('loading-state');
const stageLog = document.getElementById('stage-log');
const verdictContainer = document.getElementById('verdict-container');
const errorMessage = document.getElementById('error-message');

const MAX_CHARS = 3000;
// Update this URL before deploying
const API_URL = 'http://localhost:8000/analyze'; 

const mainHeader = document.getElementById('main-header');
const inputContainer = document.getElementById('input-container');
const controlsArea = document.getElementById('controls-area');
const mainContainer = document.querySelector('.container');

let hasInteracted = false;

input.addEventListener('input', () => {
    if (!hasInteracted && input.value.length > 0) {
        hasInteracted = true;
        mainContainer.classList.add('active-mode');
        mainHeader.classList.remove('hidden');
        controlsArea.classList.remove('hidden');
        inputContainer.classList.remove('idle');
    }

    // Auto-resize textarea
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 150) + 'px';

    const len = input.value.length;
    charCount.textContent = `${len} / ${MAX_CHARS}`;
    if (len > MAX_CHARS) {
        charCount.style.color = '#ef4444';
        analyzeBtn.disabled = true;
    } else {
        charCount.style.color = '#94a3b8';
        analyzeBtn.disabled = len === 0;
    }
});

function spawnBubbleBurst(originElement) {
    const rect = originElement.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;

    for (let i = 0; i < 8; i++) {
        const bubble = document.createElement('div');
        bubble.className = 'bubble-pop';
        
        const size = Math.random() * 12 + 8; // 8-20px
        const angle = Math.random() * Math.PI * 2;
        const dist = Math.random() * 40 + 20; // 20-60px distance
        const dx = Math.cos(angle) * dist;
        const dy = Math.sin(angle) * dist;

        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${x - size/2}px`;
        bubble.style.top = `${y - size/2}px`;
        bubble.style.setProperty('--dx', `${dx}px`);
        bubble.style.setProperty('--dy', `${dy}px`);
        bubble.style.animation = `popOut ${Math.random() * 200 + 400}ms ease-out forwards`;

        document.body.appendChild(bubble);
        setTimeout(() => bubble.remove(), 700);
    }
}

let progressIntervals = [];

function startSimulatedProgress() {
    // Reset all bars
    for(let i=0; i<4; i++) {
        const bar = document.getElementById(`stage-${i}`);
        bar.style.transition = 'none';
        bar.style.width = '0%';
        bar.classList.remove('pulsing');
        // Force reflow
        void bar.offsetWidth;
    }

    const durations = [2500, 4000, 3000, 1500];
    let currentStage = 0;

    function nextStage() {
        if (currentStage >= 4) return;
        const bar = document.getElementById(`stage-${currentStage}`);
        bar.style.transition = `width ${durations[currentStage]}ms linear`;
        bar.style.width = '100%';

        if (currentStage === 3) {
            // Last stage pulses until real data arrives
            setTimeout(() => {
                if (bar.style.width === '100%') {
                    bar.classList.add('pulsing');
                }
            }, durations[currentStage]);
        }

        const interval = setTimeout(() => {
            currentStage++;
            nextStage();
        }, durations[currentStage]);
        progressIntervals.push(interval);
    }
    nextStage();
}

function snapProgressToEnd() {
    progressIntervals.forEach(clearTimeout);
    progressIntervals = [];
    for(let i=0; i<4; i++) {
        const bar = document.getElementById(`stage-${i}`);
        bar.style.transition = 'width 0.2s ease-out';
        bar.style.width = '100%';
        bar.classList.remove('pulsing');
    }
}

analyzeBtn.addEventListener('click', async () => {
    const text = input.value.trim();
    if (!text || text.length > MAX_CHARS) return;

    spawnBubbleBurst(analyzeBtn);

    // UI Reset
    analyzeBtn.disabled = true;
    errorMessage.classList.add('hidden');
    verdictContainer.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    loadingState.classList.remove('hidden');
    
    startSimulatedProgress();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        snapProgressToEnd();
        setTimeout(() => renderResults(data), 300); // Wait a tiny bit for snap to finish visually
    } catch (err) {
        console.error(err);
        snapProgressToEnd();
        errorMessage.textContent = "Something went wrong — please try again.";
        errorMessage.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    } finally {
        analyzeBtn.disabled = false;
        loadingState.classList.add('hidden');
    }
});

function renderResults(data) {
    // Render final stage logs briefly if needed, but we mostly just show the result
    verdictContainer.classList.remove('hidden');

    const overallCard = document.getElementById('overall-verdict-card');
    const overallText = document.getElementById('overall-verdict-text');
    const overallScore = document.getElementById('overall-score-text');
    
    // Add show-anim for entrance
    overallCard.className = `verdict-card verdict-${data.overall_verdict} show-anim`;
    overallText.textContent = data.overall_verdict.replace('_', ' ');
    overallScore.textContent = data.overall_score;

    const claimsList = document.getElementById('claims-list');
    claimsList.innerHTML = '';

    if (data.claims.length === 0) {
        claimsList.innerHTML = '<p>No objective claims found to analyze.</p>';
    } else {
        data.claims.forEach(claim => {
            const el = document.createElement('div');
            el.className = `claim-card`;
            
            const floatWrap = document.createElement('div');
            floatWrap.className = 'claim-inner-float';
            // Randomize float animation delay
            const floatDelay = -(Math.random() * 6);
            floatWrap.style.animationDelay = `${floatDelay}s`;
            
            const h4 = document.createElement('h4');
            h4.className = 'typewriter-text';
            h4.dataset.fullText = `"${claim.claim}"`;
            h4.textContent = ''; // empty initially
            h4.style.minHeight = '1.5em'; // prevent massive vertical jump

            const badgeWrapper = document.createElement('div');
            badgeWrapper.className = 'badge-wrapper';
            badgeWrapper.style.opacity = '0';
            badgeWrapper.style.transform = 'scale(0)';
            badgeWrapper.style.transformOrigin = 'left center';
            badgeWrapper.innerHTML = `<div class="claim-verdict bg-${claim.verdict}">${claim.verdict} (${claim.score}/100)</div>`;

            const evidence = document.createElement('p');
            evidence.className = 'evidence-text';
            evidence.style.opacity = '0';
            evidence.textContent = claim.evidence_summary;

            floatWrap.appendChild(h4);
            floatWrap.appendChild(badgeWrapper);
            floatWrap.appendChild(evidence);
            el.appendChild(floatWrap);

            claimsList.appendChild(el);
            observeCard(el);
        });
    }

    // Setup Copy button
    document.getElementById('copy-btn').onclick = () => {
        let copyText = `FakeForward Verdict: ${data.overall_verdict.replace('_', ' ')} (${data.overall_score}/100)\n\n`;
        data.claims.forEach((c, i) => {
            copyText += `${i+1}. ${c.claim}\nVerdict: ${c.verdict}\n\n`;
        });
        navigator.clipboard.writeText(copyText).then(() => {
            const btn = document.getElementById('copy-btn');
            btn.innerHTML = '✔ Copied!';
            btn.classList.add('copied-active');
            setTimeout(() => {
                btn.innerHTML = 'Copy Result';
                btn.classList.remove('copied-active');
            }, 1500);
        });
    };
}

const cardObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const card = entry.target;
            if (card.dataset.animated === 'true') return;
            card.dataset.animated = 'true';
            observer.unobserve(card);

            const h4 = card.querySelector('h4');
            const badge = card.querySelector('.badge-wrapper');
            const ev = card.querySelector('.evidence-text');

            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

            if (prefersReducedMotion) {
                h4.textContent = h4.dataset.fullText;
                badge.style.transition = 'none';
                badge.style.opacity = '1';
                badge.style.transform = 'scale(1)';
                ev.style.transition = 'none';
                ev.style.opacity = '1';
                return;
            }

            // Typewriter
            const text = h4.dataset.fullText;
            let i = 0;
            h4.textContent = '|';
            const typeInterval = setInterval(() => {
                h4.textContent = text.substring(0, i) + '|';
                i++;
                if (i > text.length) {
                    clearInterval(typeInterval);
                    h4.textContent = text;
                    
                    // Pop Badge
                    badge.style.transition = 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.2s';
                    badge.style.opacity = '1';
                    badge.style.transform = 'scale(1)';

                    setTimeout(() => {
                        ev.style.transition = 'opacity 0.3s ease';
                        ev.style.opacity = '1';
                    }, 400); // after badge pops
                }
            }, 20); // 20ms per char
        }
    });
}, { threshold: 0.4 });

function observeCard(el) {
    cardObserver.observe(el);
}
