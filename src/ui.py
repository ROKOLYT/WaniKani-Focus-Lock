def get_progress_banner_script() -> str:
    return """
    if (!document.getElementById('wk-progress-banner')) {
        const banner = document.createElement('div');
        banner.id = 'wk-progress-banner';
        banner.style.position = 'fixed';
        banner.style.top = '40px';
        banner.style.right = '30px';
        banner.style.padding = '16px 20px';
        banner.style.backgroundColor = '#2c3e50';
        banner.style.color = '#ecf0f1';
        banner.style.borderRadius = '12px';
        banner.style.boxShadow = '0 8px 15px rgba(0,0,0,0.5)';
        banner.style.zIndex = '9999998';
        banner.style.fontFamily = '"Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif';
        banner.style.textAlign = 'left';
        banner.style.minWidth = '240px';
    
        const title = document.createElement('div');
        title.innerText = 'WaniKani Progress';
        title.style.fontSize = '16px';
        title.style.fontWeight = 'bold';
        title.style.marginBottom = '10px';
    
        const lessonsLine = document.createElement('div');
        lessonsLine.innerHTML = 'Lessons: <span id="wk-progress-lessons">0</span> / <span id="wk-progress-lessons-goal">0</span>';
        lessonsLine.style.marginBottom = '6px';
    
        const reviewsLine = document.createElement('div');
        reviewsLine.innerHTML = 'Reviews: <span id="wk-progress-reviews">0</span> / <span id="wk-progress-reviews-goal">0</span>';
        reviewsLine.style.marginBottom = '8px';
    
        const statusLine = document.createElement('div');
        statusLine.id = 'wk-progress-status';
        statusLine.style.fontSize = '13px';
        statusLine.style.opacity = '0.9';
    
        banner.appendChild(title);
        banner.appendChild(lessonsLine);
        banner.appendChild(reviewsLine);
        banner.appendChild(statusLine);
    
        if (document.body) {
            document.body.appendChild(banner);
        } else {
            window.addEventListener('DOMContentLoaded', () => {
                document.body.appendChild(banner);
            });
        }
    }
    
    window.updateWkProgress = (data) => {
        const lessonsEl = document.getElementById('wk-progress-lessons');
        const lessonsGoalEl = document.getElementById('wk-progress-lessons-goal');
        const reviewsEl = document.getElementById('wk-progress-reviews');
        const reviewsGoalEl = document.getElementById('wk-progress-reviews-goal');
        const statusEl = document.getElementById('wk-progress-status');
    
        if (lessonsEl) lessonsEl.innerText = String(data.lessons_done);
        if (lessonsGoalEl) lessonsGoalEl.innerText = String(data.lesson_goal);
        if (reviewsEl) reviewsEl.innerText = String(data.reviews_done);
        if (reviewsGoalEl) reviewsGoalEl.innerText = String(data.review_goal);
    
        if (statusEl) {
            if (data.lesson_goal_met && data.review_goal_met) {
                statusEl.innerText = 'Goals met! You can unlock your PC.';
            } else {
                statusEl.innerText = 'Goals in progress...';
            }
        }
    };

    undefined;
    """


def get_unlock_banner_script() -> str:
    return """
    if (!document.getElementById('wk-unlock-banner')) {
        const banner = document.createElement('div');
        banner.id = 'wk-unlock-banner';
        banner.style.position = 'fixed';
        banner.style.bottom = '30px';
        banner.style.right = '30px';
        banner.style.padding = '25px';
        banner.style.backgroundColor = '#2c3e50';
        banner.style.color = '#ecf0f1';
        banner.style.borderRadius = '12px';
        banner.style.boxShadow = '0 8px 15px rgba(0,0,0,0.5)';
        banner.style.zIndex = '9999999';
        banner.style.fontFamily = '"Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif';
        banner.style.textAlign = 'center';

        const msg = document.createElement('div');
        msg.innerText = '🎉 Goals met! You can keep studying or unlock your PC.';
        msg.style.marginBottom = '20px';
        msg.style.fontSize = '18px';
        msg.style.fontWeight = 'bold';

        const btn = document.createElement('button');
        btn.innerText = 'Unlock PC';
        btn.style.padding = '12px 24px';
        btn.style.border = 'none';
        btn.style.borderRadius = '6px';
        btn.style.backgroundColor = '#27ae60';
        btn.style.color = 'white';
        btn.style.fontSize = '16px';
        btn.style.fontWeight = 'bold';
        btn.style.cursor = 'pointer';
        
        btn.onclick = () => { window.triggerUnlock(); };

        banner.appendChild(msg);
        banner.appendChild(btn);
        
        if (document.body) {
            document.body.appendChild(banner);
        } else {
            window.addEventListener('DOMContentLoaded', () => {
                document.body.appendChild(banner);
            });
        }
    }
    """
