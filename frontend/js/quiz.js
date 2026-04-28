/* ═══════════════════════════════════════════════════
   ClarityBuddy — js/quiz.js
   Handles: progress bar, one-question-at-a-time nav,
   answer collection, email capture, submit.
   Used by both quiz.html and compatibility.html
═══════════════════════════════════════════════════ */

import { submitQuiz1, submitQuiz2 } from './api.js';

class ClarityQuiz {
  constructor(config) {
    this.quizType   = config.quizType;   // 'quiz1' | 'quiz2'
    this.questions  = config.questions;  // array of question objects
    this.onComplete = config.onComplete; // callback(reportId)

    this.currentIndex = 0;
    this.answers      = {};
    this.userData     = { name: '', email: '', partner_name: '' };
    this._totalQ      = this.questions.filter(q => q.type !== 'email').length;

    this._render();
    this._bindNav();
    this._showQuestion(0);
  }

  /* ── DOM refs ── */
  _render() {
    this.progressFill  = document.getElementById('progress-fill');
    this.progressText  = document.getElementById('progress-text');
    this.questionWrap  = document.getElementById('question-wrap');
    this.btnBack       = document.getElementById('btn-back');
    this.btnNext       = document.getElementById('btn-next');
    this.sectionLabel  = document.getElementById('section-label');
  }

  _bindNav() {
    this.btnNext.addEventListener('click', () => this._handleNext());
    this.btnBack.addEventListener('click', () => this._handleBack());
  }

  /* ── Show a question ── */
  _showQuestion(index) {
    const q = this.questions[index];
    this.currentIndex = index;

    /* progress — email step is not counted as a question */
    if (q.type === 'email') {
      this.progressText.textContent = 'Your details';
    } else {
      const qNum = this.questions.slice(0, index + 1).filter(q => q.type !== 'email').length;
      const pct  = Math.round(((qNum - 1) / this._totalQ) * 100);
      this.progressFill.style.width = pct + '%';
      this.progressText.textContent = `${qNum} of ${this._totalQ}`;
    }

    /* section label */
    if (this.sectionLabel && q.section) {
      this.sectionLabel.textContent = q.section;
    }

    /* back button */
    this.btnBack.classList.toggle('hidden', index === 0);

    /* render question */
    this.questionWrap.innerHTML = '';
    this.questionWrap.classList.remove('animate-fadeup');
    void this.questionWrap.offsetWidth; /* reflow to restart animation */
    this.questionWrap.classList.add('animate-fadeup');

    if (q.type === 'email') {
      this._renderEmailCapture(q);
    } else {
      this._renderChoiceQuestion(q);
    }

    /* scroll to top on mobile */
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  _renderChoiceQuestion(q) {
    const selected = this.answers[q.id] || null;

    this.questionWrap.innerHTML = `
      <p class="quiz-q-num text-xs text-soft mb-8">Question ${this.currentIndex + 1}</p>
      <h2 class="quiz-question mb-24">${q.text}</h2>
      <div class="quiz-options" role="radiogroup" aria-label="${q.text}">
        ${q.options.map((opt, i) => `
          <button
            class="quiz-option ${selected === opt.value ? 'selected' : ''}"
            data-value="${opt.value}"
            role="radio"
            aria-checked="${selected === opt.value}"
          >
            <span class="quiz-option__dot"></span>
            <span class="quiz-option__text">${opt.label}</span>
          </button>
        `).join('')}
      </div>
    `;

    /* bind option clicks */
    this.questionWrap.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', () => {
        this.questionWrap.querySelectorAll('.quiz-option').forEach(b => {
          b.classList.remove('selected');
          b.setAttribute('aria-checked', 'false');
        });
        btn.classList.add('selected');
        btn.setAttribute('aria-checked', 'true');
        this.answers[q.id] = btn.dataset.value;

        /* auto-advance after short delay */
        setTimeout(() => this._handleNext(), 300);
      });
    });
  }

  _renderEmailCapture(q) {
    this.questionWrap.innerHTML = `
      <div class="email-capture-wrap">
        <h2 class="quiz-question mb-12">${q.text}</h2>
        <p class="mb-24 text-sm text-soft">${q.subtitle || ''}</p>
        <div class="form-group">
          <label class="form-label" for="user-name">Your first name</label>
          <input
            class="form-input"
            type="text"
            id="user-name"
            placeholder="e.g. Priya"
            value="${this.userData.name}"
            autocomplete="given-name"
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="user-email">Your email address</label>
          <input
            class="form-input"
            type="email"
            id="user-email"
            placeholder="you@example.com"
            value="${this.userData.email}"
            autocomplete="email"
          />
        </div>
        ${this.quizType === 'quiz2' ? `
        <div class="form-group">
          <label class="form-label" for="partner-name">His first name (optional)</label>
          <input
            class="form-input"
            type="text"
            id="partner-name"
            placeholder="e.g. Arjun"
            value="${this.userData.partner_name}"
          />
        </div>
        ` : ''}
        <p class="text-xs text-soft mt-8">
          Your report will be sent here. We don't share your details.
        </p>
      </div>
    `;
  }

  /* ── Navigation ── */
  _handleNext() {
    const q = this.questions[this.currentIndex];

    if (q.type === 'email') {
      if (!this._validateEmail()) return;
      this._captureEmail();
    } else {
      if (!this.answers[q.id]) {
        this._shake();
        return;
      }
    }

    if (this.currentIndex < this.questions.length - 1) {
      this._showQuestion(this.currentIndex + 1);
    } else {
      this._submit();
    }
  }

  _handleBack() {
    if (this.currentIndex > 0) {
      this._showQuestion(this.currentIndex - 1);
    }
  }

  /* ── Validation ── */
  _validateEmail() {
    const name  = document.getElementById('user-name')?.value.trim();
    const email = document.getElementById('user-email')?.value.trim();
    if (!name) { this._showError('Please enter your first name.'); return false; }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      this._showError('Please enter a valid email address.'); return false;
    }
    return true;
  }

  _captureEmail() {
    this.userData.name  = document.getElementById('user-name')?.value.trim() || '';
    this.userData.email = document.getElementById('user-email')?.value.trim() || '';
    if (this.quizType === 'quiz2') {
      this.userData.partner_name = document.getElementById('partner-name')?.value.trim() || '';
    }
  }

  /* ── Submit ── */
  async _submit() {
    /* show loader */
    this._showLoader();
    console.log('[Quiz] Submitting answers...', { quizType: this.quizType, answers: this.answers });

    try {
      let result;
      const payload = {
        name:    this.userData.name,
        email:   this.userData.email,
        answers: this.answers,
      };

      if (this.quizType === 'quiz1') {
        console.log('[Quiz] Calling submitQuiz1...');
        result = await submitQuiz1(payload);
      } else {
        console.log('[Quiz] Calling submitQuiz2...');
        result = await submitQuiz2({
          ...payload,
          partner_name: this.userData.partner_name,
        });
      }

      console.log('[Quiz] Submission successful:', result);
      /* store report id locally so payment page can use it */
      localStorage.setItem('cb_report_id', result.report_id);
      localStorage.setItem('cb_persona', result.archetype || '');
      localStorage.setItem('cb_score',     result.score || '');
      localStorage.setItem('cb_quiz_type', this.quizType);

      if (this.onComplete) {
        console.log('[Quiz] Calling onComplete callback');
        this.onComplete(result.report_id);
      } else {
        const redirectUrl = `report.html?id=${result.report_id}`;
        console.log('[Quiz] Redirecting to:', redirectUrl);
        window.location.href = redirectUrl;
      }
    } catch (err) {
      console.error('[Quiz] Submission failed:', err);
      this._hideLoader();
      this._showError(err.message || 'Something went wrong. Please try again.');
    }
  }

  /* ── UI helpers ── */
  _showLoader() {
    document.getElementById('quiz-body')?.classList.add('hidden');
    document.getElementById('quiz-loader')?.classList.remove('hidden');
  }

  _hideLoader() {
    document.getElementById('quiz-body')?.classList.remove('hidden');
    document.getElementById('quiz-loader')?.classList.add('hidden');
  }

  _shake() {
    const wrap = this.questionWrap;
    wrap.style.animation = 'none';
    void wrap.offsetWidth;
    wrap.style.animation = 'shake 0.4s ease';
  }

  _showError(msg) {
    let toast = document.getElementById('cb-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'cb-toast';
      toast.className = 'toast toast--error';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3500);
  }
}

/* ── Shake keyframe (injected once) ── */
const style = document.createElement('style');
style.textContent = `
  @keyframes shake {
    0%,100% { transform: translateX(0); }
    20%      { transform: translateX(-8px); }
    40%      { transform: translateX(8px); }
    60%      { transform: translateX(-5px); }
    80%      { transform: translateX(5px); }
  }
`;
document.head.appendChild(style);

export default ClarityQuiz;
