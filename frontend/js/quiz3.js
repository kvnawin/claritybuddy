/* ═══════════════════════════════════════════════════
   ClarityBuddy — js/quiz3.js
   Quiz 3: The Relationship Clarity Report
   55 questions · 11 sections · weighted scoring engine
═══════════════════════════════════════════════════ */

/* ── 55 Questions with dimension weights ─────────── */
export const Q3_QUESTIONS = [

  /* ── Section 1: Identity & Values (Q1–Q5) ── */
  { id:'q1', section:'Identity & Values',
    text:'When you imagine married life, what matters MOST to you emotionally?',
    options:[
      {value:'a',label:'Feeling emotionally safe and peaceful'},
      {value:'b',label:'Building a successful life together'},
      {value:'c',label:'Feeling deeply desired and connected'},
      {value:'d',label:'Avoiding loneliness and social pressure'},
    ],
    w:{a:{identityClarity:2,emotionalStability:1,secureAttachment:2},b:{identityClarity:1,goodOnPaperBias:1},c:{anxiousAttachment:1,emotionalAvailabilityMismatch:1},d:{pressureVulnerability:2,anxiousAttachment:1,marriageReadiness:-1}}
  },
  { id:'q2', section:'Identity & Values',
    text:'If your family strongly approved of someone but your inner feeling felt uneasy, you would most likely:',
    options:[
      {value:'a',label:'Step back and trust my discomfort'},
      {value:'b',label:'Continue slowly while observing carefully'},
      {value:'c',label:'Doubt whether I\'m overthinking'},
      {value:'d',label:'Ignore my feelings because family experience matters more'},
    ],
    w:{a:{selfTrust:3,boundaryStrength:2,identityClarity:2},b:{selfTrust:1,identityClarity:1},c:{selfTrust:-2,overthinking:2,pressureVulnerability:1},d:{selfTrust:-3,pressureVulnerability:3,identityClarity:-2,boundaryStrength:-2}}
  },
  { id:'q3', section:'Identity & Values',
    text:'What usually makes relationship decisions difficult for you?',
    options:[
      {value:'a',label:'Balancing emotions with logic'},
      {value:'b',label:'Fear of making the wrong choice'},
      {value:'c',label:'Worrying about others\' opinions'},
      {value:'d',label:'Not fully knowing what I truly want'},
    ],
    w:{a:{identityClarity:1,overthinking:1},b:{pressureVulnerability:2,selfTrust:-1,anxiousAttachment:1},c:{pressureVulnerability:2,identityClarity:-1,selfTrust:-1},d:{identityClarity:-3,selfTrust:-2}}
  },
  { id:'q4', section:'Identity & Values',
    text:'How clearly can you describe your non-negotiables without mentioning looks, salary, or status?',
    options:[
      {value:'a',label:'Very clearly'},
      {value:'b',label:'Somewhat clearly'},
      {value:'c',label:'Only vaguely'},
      {value:'d',label:'I struggle to define them'},
    ],
    w:{a:{identityClarity:3,selfTrust:2,boundaryStrength:2},b:{identityClarity:1,selfTrust:1},c:{identityClarity:-1,selfTrust:-1},d:{identityClarity:-3,selfTrust:-2,boundaryStrength:-2}}
  },
  { id:'q5', section:'Identity & Values',
    text:'Have you ever stayed interested in someone mainly because they matched your "ideal checklist"?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Often'},
      {value:'d',label:'Almost always'},
    ],
    w:{a:{identityClarity:1},b:{goodOnPaperBias:1},c:{goodOnPaperBias:2,emotionalAvailabilityMismatch:1},d:{goodOnPaperBias:3,identityClarity:-1,selfTrust:-1}}
  },

  /* ── Section 2: Emotional World (Q6–Q10) ── */
  { id:'q6', section:'Emotional World',
    text:'When someone\'s texting pattern suddenly changes, your first emotional reaction is usually:',
    options:[
      {value:'a',label:'Curiosity without panic'},
      {value:'b',label:'Mild anxiety'},
      {value:'c',label:'Overthinking and emotional stress'},
      {value:'d',label:'Fear that I\'m being rejected'},
    ],
    w:{a:{emotionalStability:3,secureAttachment:2,selfTrust:1},b:{anxiousAttachment:1,emotionalStability:-1},c:{overthinking:3,anxiousAttachment:2,emotionalStability:-2},d:{anxiousAttachment:3,emotionalStability:-2,fearfulAvoidant:1}}
  },
  { id:'q7', section:'Emotional World',
    text:'After emotional disappointment, you usually:',
    options:[
      {value:'a',label:'Process it and recover steadily'},
      {value:'b',label:'Need time but eventually regain balance'},
      {value:'c',label:'Replay it repeatedly in my mind'},
      {value:'d',label:'Lose trust in relationships completely'},
    ],
    w:{a:{emotionalStability:3,secureAttachment:2},b:{emotionalStability:1,secureAttachment:1},c:{overthinking:3,emotionalStability:-2,anxiousAttachment:1},d:{avoidantAttachment:2,emotionalStability:-3,fearfulAvoidant:2}}
  },
  { id:'q8', section:'Emotional World',
    text:'When someone genuinely treats you well consistently, it feels:',
    options:[
      {value:'a',label:'Safe and comforting'},
      {value:'b',label:'Nice but unfamiliar'},
      {value:'c',label:'Suspicious or emotionally flat'},
      {value:'d',label:'Less exciting than emotionally intense connections'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,marriageReadiness:2},b:{anxiousAttachment:1,emotionalAvailabilityMismatch:1,fearfulAvoidant:1},c:{avoidantAttachment:2,emotionalAvailabilityMismatch:2,fearfulAvoidant:1},d:{emotionalAvailabilityMismatch:3,anxiousAttachment:2,redFlagBlindness:1}}
  },
  { id:'q9', section:'Emotional World',
    text:'How often do your emotions affect your ability to think clearly in relationships?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Frequently'},
      {value:'d',label:'Almost always'},
    ],
    w:{a:{emotionalStability:3,selfTrust:2},b:{emotionalStability:1},c:{emotionalStability:-2,overthinking:2,anxiousAttachment:1},d:{emotionalStability:-3,overthinking:3,selfTrust:-2}}
  },
  { id:'q10', section:'Emotional World',
    text:'What feels hardest emotionally?',
    options:[
      {value:'a',label:'Trusting slowly'},
      {value:'b',label:'Being vulnerable'},
      {value:'c',label:'Letting go after attachment'},
      {value:'d',label:'Being alone while waiting for the right person'},
    ],
    w:{a:{secureAttachment:1,emotionalStability:1},b:{avoidantAttachment:1,fearfulAvoidant:1},c:{anxiousAttachment:2,emotionalStability:-1},d:{pressureVulnerability:2,anxiousAttachment:1,marriageReadiness:-1}}
  },

  /* ── Section 3: Boundaries & Patterns (Q11–Q15) ── */
  { id:'q11', section:'Boundaries & Patterns',
    text:'If someone repeatedly crosses a boundary after apologizing, you usually:',
    options:[
      {value:'a',label:'Distance myself quickly'},
      {value:'b',label:'Give another chance cautiously'},
      {value:'c',label:'Keep hoping they\'ll change'},
      {value:'d',label:'Stay silent to avoid conflict'},
    ],
    w:{a:{boundaryStrength:3,selfTrust:2},b:{boundaryStrength:1},c:{boundaryStrength:-2,redFlagBlindness:2,anxiousAttachment:2},d:{boundaryStrength:-3,redFlagBlindness:2,fearfulAvoidant:1}}
  },
  { id:'q12', section:'Boundaries & Patterns',
    text:'Have you ever ignored behavior that bothered you because you feared losing the connection?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Often'},
      {value:'d',label:'Very frequently'},
    ],
    w:{a:{boundaryStrength:2,selfTrust:1},b:{redFlagBlindness:1},c:{boundaryStrength:-2,redFlagBlindness:2,anxiousAttachment:1},d:{boundaryStrength:-3,redFlagBlindness:3,anxiousAttachment:2}}
  },
  { id:'q13', section:'Boundaries & Patterns',
    text:'When saying "no" in relationships, you typically feel:',
    options:[
      {value:'a',label:'Clear and comfortable'},
      {value:'b',label:'Slightly guilty'},
      {value:'c',label:'Very anxious'},
      {value:'d',label:'Afraid they may leave'},
    ],
    w:{a:{boundaryStrength:3,selfTrust:2,identityClarity:1},b:{boundaryStrength:1,selfTrust:-1},c:{boundaryStrength:-2,anxiousAttachment:1,pressureVulnerability:1},d:{boundaryStrength:-3,anxiousAttachment:3,fearfulAvoidant:1}}
  },
  { id:'q14', section:'Boundaries & Patterns',
    text:'Which statement feels most true?',
    options:[
      {value:'a',label:'Respect matters more than emotional intensity'},
      {value:'b',label:'I try to balance both equally'},
      {value:'c',label:'I tolerate more than I should once attached'},
      {value:'d',label:'I avoid confrontation even when unhappy'},
    ],
    w:{a:{boundaryStrength:3,identityClarity:2,selfTrust:2},b:{boundaryStrength:1,identityClarity:1},c:{boundaryStrength:-2,anxiousAttachment:2,redFlagBlindness:1},d:{boundaryStrength:-3,avoidantAttachment:1,fearfulAvoidant:2}}
  },
  { id:'q15', section:'Boundaries & Patterns',
    text:'When someone disappoints you repeatedly, you tend to:',
    options:[
      {value:'a',label:'Re-evaluate the relationship logically'},
      {value:'b',label:'Communicate and observe change'},
      {value:'c',label:'Continue emotionally hoping'},
      {value:'d',label:'Blame yourself for expecting too much'},
    ],
    w:{a:{boundaryStrength:3,identityClarity:2,selfTrust:2},b:{boundaryStrength:2,secureAttachment:2},c:{boundaryStrength:-2,redFlagBlindness:2,anxiousAttachment:2},d:{boundaryStrength:-2,selfTrust:-2,anxiousAttachment:1,fearfulAvoidant:1}}
  },

  /* ── Section 4: External Pressures (Q16–Q20) ── */
  { id:'q16', section:'External Pressures',
    text:'What creates the MOST pressure in your marriage decisions?',
    options:[
      {value:'a',label:'Fear of choosing wrong'},
      {value:'b',label:'Family expectations'},
      {value:'c',label:'Age / timeline concerns'},
      {value:'d',label:'Seeing others move ahead'},
    ],
    w:{a:{pressureVulnerability:2,selfTrust:-1,overthinking:1},b:{pressureVulnerability:3,identityClarity:-1},c:{pressureVulnerability:3,marriageReadiness:-1},d:{pressureVulnerability:3,identityClarity:-2,selfTrust:-1}}
  },
  { id:'q17', section:'External Pressures',
    text:'If nobody around you asked about marriage, your decision-making would probably become:',
    options:[
      {value:'a',label:'Much calmer'},
      {value:'b',label:'Slightly clearer'},
      {value:'c',label:'Mostly unchanged'},
      {value:'d',label:'I\'m not sure'},
    ],
    w:{a:{pressureVulnerability:3},b:{pressureVulnerability:2},c:{selfTrust:2,identityClarity:1},d:{selfTrust:-1,pressureVulnerability:1}}
  },
  { id:'q18', section:'External Pressures',
    text:'Have you ever considered someone more seriously because you felt time was running out?',
    options:[
      {value:'a',label:'Never'},
      {value:'b',label:'Occasionally'},
      {value:'c',label:'Yes, multiple times'},
      {value:'d',label:'Very often'},
    ],
    w:{a:{selfTrust:2,identityClarity:2},b:{pressureVulnerability:1},c:{pressureVulnerability:3,selfTrust:-1,marriageReadiness:-1},d:{pressureVulnerability:3,selfTrust:-2,marriageReadiness:-2,identityClarity:-2}}
  },
  { id:'q19', section:'External Pressures',
    text:'Which situation feels more emotionally uncomfortable?',
    options:[
      {value:'a',label:'Staying single longer'},
      {value:'b',label:'Ending the wrong relationship'},
      {value:'c',label:'Disappointing family expectations'},
      {value:'d',label:'Starting over emotionally'},
    ],
    w:{a:{pressureVulnerability:2,marriageReadiness:-1},b:{boundaryStrength:-1,redFlagBlindness:1},c:{pressureVulnerability:3,identityClarity:-1},d:{emotionalStability:-1,fearfulAvoidant:1}}
  },
  { id:'q20', section:'External Pressures',
    text:'How much does comparison affect your emotional state?',
    options:[
      {value:'a',label:'Very little'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Quite a lot'},
      {value:'d',label:'Constantly'},
    ],
    w:{a:{identityClarity:2,selfTrust:1},b:{pressureVulnerability:1},c:{pressureVulnerability:2,identityClarity:-1,selfTrust:-1},d:{pressureVulnerability:3,identityClarity:-2,selfTrust:-2,emotionalStability:-1}}
  },

  /* ── Section 5: Self-Trust (Q21–Q25) ── */
  { id:'q21', section:'Self-Trust',
    text:'Looking back, how often was your intuition about someone eventually correct?',
    options:[
      {value:'a',label:'Most of the time'},
      {value:'b',label:'About half the time'},
      {value:'c',label:'Rarely'},
      {value:'d',label:'I usually ignored it'},
    ],
    w:{a:{intuitionTrust:3,selfTrust:2,identityClarity:1},b:{intuitionTrust:1,selfTrust:1},c:{intuitionTrust:-1,selfTrust:-1},d:{intuitionTrust:-2,selfTrust:-2,redFlagBlindness:2}}
  },
  { id:'q22', section:'Self-Trust',
    text:'When confused in relationships, you tend to:',
    options:[
      {value:'a',label:'Reflect internally first'},
      {value:'b',label:'Seek balanced advice'},
      {value:'c',label:'Ask many people for opinions'},
      {value:'d',label:'Depend heavily on external validation'},
    ],
    w:{a:{selfTrust:3,intuitionTrust:2,identityClarity:2},b:{selfTrust:1,identityClarity:1},c:{selfTrust:-2,overthinking:1,pressureVulnerability:1},d:{selfTrust:-3,pressureVulnerability:2,identityClarity:-2}}
  },
  { id:'q23', section:'Self-Trust',
    text:'What causes you to doubt yourself most?',
    options:[
      {value:'a',label:'Fear of missing something important'},
      {value:'b',label:'Past mistakes'},
      {value:'c',label:'Others questioning my judgment'},
      {value:'d',label:'Emotional attachment clouding logic'},
    ],
    w:{a:{overthinking:2,selfTrust:-1},b:{selfTrust:-1,emotionalStability:-1},c:{selfTrust:-2,pressureVulnerability:2,identityClarity:-1},d:{selfTrust:-1,redFlagBlindness:1,overthinking:1}}
  },
  { id:'q24', section:'Self-Trust',
    text:'Have you ever convinced yourself to stay despite inner discomfort?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Often'},
      {value:'d',label:'Repeatedly'},
    ],
    w:{a:{selfTrust:2,boundaryStrength:2,intuitionTrust:2},b:{redFlagBlindness:1},c:{selfTrust:-2,redFlagBlindness:2,boundaryStrength:-1,anxiousAttachment:1},d:{selfTrust:-3,redFlagBlindness:3,boundaryStrength:-2,anxiousAttachment:2}}
  },
  { id:'q25', section:'Self-Trust',
    text:'When making major emotional decisions, you trust:',
    options:[
      {value:'a',label:'My internal clarity'},
      {value:'b',label:'A balance of intuition and logic'},
      {value:'c',label:'Advice from trusted people'},
      {value:'d',label:'Whatever reduces anxiety fastest'},
    ],
    w:{a:{selfTrust:3,intuitionTrust:3,identityClarity:2},b:{selfTrust:2,identityClarity:1},c:{selfTrust:-1,pressureVulnerability:1},d:{selfTrust:-3,anxiousAttachment:2,emotionalStability:-2}}
  },

  /* ── Section 6: Attachment Style (Q26–Q30) ── */
  { id:'q26', section:'Attachment Style',
    text:'When someone becomes emotionally distant, your instinct is usually to:',
    options:[
      {value:'a',label:'Give space calmly'},
      {value:'b',label:'Seek reassurance'},
      {value:'c',label:'Overanalyze their behavior'},
      {value:'d',label:'Pull away emotionally first'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,selfTrust:2},b:{anxiousAttachment:2,selfTrust:-1},c:{overthinking:3,anxiousAttachment:2,emotionalStability:-2},d:{avoidantAttachment:3,fearfulAvoidant:1,emotionalAvailabilityMismatch:1}}
  },
  { id:'q27', section:'Attachment Style',
    text:'Which relationship dynamic feels most familiar?',
    options:[
      {value:'a',label:'Stable and balanced'},
      {value:'b',label:'Intense and uncertain'},
      {value:'c',label:'Emotionally distant'},
      {value:'d',label:'One-sided effort'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,marriageReadiness:2},b:{anxiousAttachment:2,emotionalAvailabilityMismatch:2,redFlagBlindness:1},c:{avoidantAttachment:3,emotionalAvailabilityMismatch:1},d:{anxiousAttachment:2,boundaryStrength:-2,redFlagBlindness:2}}
  },
  { id:'q28', section:'Attachment Style',
    text:'When someone likes you consistently, you usually:',
    options:[
      {value:'a',label:'Feel safe'},
      {value:'b',label:'Need time to trust it'},
      {value:'c',label:'Lose attraction slowly'},
      {value:'d',label:'Feel emotionally overwhelmed'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,marriageReadiness:2},b:{fearfulAvoidant:1,avoidantAttachment:1,emotionalStability:-1},c:{emotionalAvailabilityMismatch:3,avoidantAttachment:2},d:{anxiousAttachment:1,fearfulAvoidant:2,emotionalAvailabilityMismatch:1}}
  },
  { id:'q29', section:'Attachment Style',
    text:'Your biggest relationship fear is:',
    options:[
      {value:'a',label:'Choosing the wrong person'},
      {value:'b',label:'Being abandoned'},
      {value:'c',label:'Losing independence'},
      {value:'d',label:'Not being enough'},
    ],
    w:{a:{selfTrust:-1,overthinking:1},b:{anxiousAttachment:3,fearfulAvoidant:1},c:{avoidantAttachment:2,emotionalAvailabilityMismatch:1},d:{anxiousAttachment:2,fearfulAvoidant:2,selfTrust:-2}}
  },
  { id:'q30', section:'Attachment Style',
    text:'What usually creates emotional attraction for you?',
    options:[
      {value:'a',label:'Emotional safety'},
      {value:'b',label:'Chemistry and intensity'},
      {value:'c',label:'Mystery and unpredictability'},
      {value:'d',label:'Feeling needed emotionally'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,marriageReadiness:2},b:{emotionalAvailabilityMismatch:1,anxiousAttachment:1},c:{emotionalAvailabilityMismatch:3,redFlagBlindness:2,anxiousAttachment:1},d:{anxiousAttachment:3,boundaryStrength:-1,emotionalAvailabilityMismatch:1}}
  },

  /* ── Section 7: Pattern Recognition (Q31–Q35) ── */
  { id:'q31', section:'Pattern Recognition',
    text:'Have you ever explained away behavior that would concern you if it happened to a friend?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Often'},
      {value:'d',label:'Very frequently'},
    ],
    w:{a:{selfTrust:2,boundaryStrength:1},b:{redFlagBlindness:1},c:{redFlagBlindness:3,selfTrust:-1,boundaryStrength:-1},d:{redFlagBlindness:3,selfTrust:-2,boundaryStrength:-2,anxiousAttachment:1}}
  },
  { id:'q32', section:'Pattern Recognition',
    text:'When attracted emotionally, you tend to:',
    options:[
      {value:'a',label:'Stay observant'},
      {value:'b',label:'Ignore small concerns initially'},
      {value:'c',label:'Focus mostly on potential'},
      {value:'d',label:'Avoid acknowledging red flags'},
    ],
    w:{a:{selfTrust:2,identityClarity:2},b:{redFlagBlindness:2,selfTrust:-1},c:{redFlagBlindness:2,goodOnPaperBias:1,identityClarity:-1},d:{redFlagBlindness:3,selfTrust:-2,boundaryStrength:-1}}
  },
  { id:'q33', section:'Pattern Recognition',
    text:'What usually keeps you attached despite confusion?',
    options:[
      {value:'a',label:'Hope they\'ll improve'},
      {value:'b',label:'Emotional chemistry'},
      {value:'c',label:'Fear of losing connection'},
      {value:'d',label:'Fear of starting over'},
    ],
    w:{a:{redFlagBlindness:2,anxiousAttachment:1,boundaryStrength:-1},b:{emotionalAvailabilityMismatch:2,redFlagBlindness:1},c:{anxiousAttachment:3,fearfulAvoidant:1,redFlagBlindness:1},d:{anxiousAttachment:2,pressureVulnerability:2,redFlagBlindness:1}}
  },
  { id:'q34', section:'Pattern Recognition',
    text:'If someone gives mixed signals repeatedly, you usually:',
    options:[
      {value:'a',label:'Step back'},
      {value:'b',label:'Communicate directly'},
      {value:'c',label:'Try harder to understand them'},
      {value:'d',label:'Become more emotionally invested'},
    ],
    w:{a:{boundaryStrength:3,selfTrust:2},b:{secureAttachment:2,boundaryStrength:2,selfTrust:1},c:{anxiousAttachment:2,overthinking:2,redFlagBlindness:1},d:{anxiousAttachment:3,redFlagBlindness:2,emotionalAvailabilityMismatch:2}}
  },
  { id:'q35', section:'Pattern Recognition',
    text:'Have you mistaken emotional intensity for compatibility before?',
    options:[
      {value:'a',label:'Never'},
      {value:'b',label:'Once or twice'},
      {value:'c',label:'Multiple times'},
      {value:'d',label:'Almost always'},
    ],
    w:{a:{identityClarity:2},b:{redFlagBlindness:1,emotionalAvailabilityMismatch:1},c:{redFlagBlindness:2,emotionalAvailabilityMismatch:2,anxiousAttachment:1},d:{redFlagBlindness:3,emotionalAvailabilityMismatch:3,identityClarity:-2}}
  },

  /* ── Section 8: Mind Patterns (Q36–Q40) ── */
  { id:'q36', section:'Mind Patterns',
    text:'How long do relationship decisions usually stay in your mind?',
    options:[
      {value:'a',label:'Briefly'},
      {value:'b',label:'A few days'},
      {value:'c',label:'Weeks'},
      {value:'d',label:'Constantly'},
    ],
    w:{a:{emotionalStability:2,selfTrust:1},b:{overthinking:1,emotionalStability:-1},c:{overthinking:3,emotionalStability:-2},d:{overthinking:3,emotionalStability:-3,anxiousAttachment:1}}
  },
  { id:'q37', section:'Mind Patterns',
    text:'When confused about someone, you usually:',
    options:[
      {value:'a',label:'Observe behavior calmly'},
      {value:'b',label:'Analyze every interaction'},
      {value:'c',label:'Seek repeated reassurance'},
      {value:'d',label:'Swing between certainty and doubt'},
    ],
    w:{a:{selfTrust:2,emotionalStability:2},b:{overthinking:3,anxiousAttachment:1,emotionalStability:-1},c:{overthinking:2,anxiousAttachment:3,selfTrust:-2},d:{overthinking:3,fearfulAvoidant:2,emotionalStability:-2}}
  },
  { id:'q38', section:'Mind Patterns',
    text:'What happens when your intuition says "something feels off"?',
    options:[
      {value:'a',label:'I pay attention immediately'},
      {value:'b',label:'I investigate further'},
      {value:'c',label:'I suppress it unless I get proof'},
      {value:'d',label:'I ignore it due to emotional attachment'},
    ],
    w:{a:{intuitionTrust:3,selfTrust:3,boundaryStrength:2},b:{intuitionTrust:2,selfTrust:1},c:{intuitionTrust:-2,redFlagBlindness:2,selfTrust:-1},d:{intuitionTrust:-3,redFlagBlindness:3,boundaryStrength:-2,anxiousAttachment:1}}
  },
  { id:'q39', section:'Mind Patterns',
    text:'How often do you replay conversations mentally?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Frequently'},
      {value:'d',label:'Almost constantly'},
    ],
    w:{a:{emotionalStability:2,selfTrust:1},b:{overthinking:1},c:{overthinking:3,emotionalStability:-2},d:{overthinking:3,emotionalStability:-3,anxiousAttachment:1}}
  },
  { id:'q40', section:'Mind Patterns',
    text:'Which statement sounds most like you?',
    options:[
      {value:'a',label:'I usually know what I feel'},
      {value:'b',label:'I need time to understand my feelings'},
      {value:'c',label:'I confuse anxiety with intuition'},
      {value:'d',label:'My mind rarely feels emotionally quiet'},
    ],
    w:{a:{identityClarity:2,selfTrust:2,emotionalStability:2},b:{identityClarity:-1,overthinking:1},c:{overthinking:2,intuitionTrust:-2,emotionalStability:-1},d:{overthinking:3,emotionalStability:-3,anxiousAttachment:1}}
  },

  /* ── Section 9: Attraction Clarity (Q41–Q45) ── */
  { id:'q41', section:'Attraction Clarity',
    text:'What makes someone initially attractive to you?',
    options:[
      {value:'a',label:'Emotional maturity'},
      {value:'b',label:'Shared values and lifestyle'},
      {value:'c',label:'Achievement and stability'},
      {value:'d',label:'Strong chemistry and attention'},
    ],
    w:{a:{secureAttachment:2,identityClarity:2},b:{identityClarity:2,goodOnPaperBias:1},c:{goodOnPaperBias:3,identityClarity:-1},d:{emotionalAvailabilityMismatch:1,anxiousAttachment:1}}
  },
  { id:'q42', section:'Attraction Clarity',
    text:'Have you ever tried convincing yourself to like someone because they seemed "perfect"?',
    options:[
      {value:'a',label:'Never'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Often'},
      {value:'d',label:'Yes, even against my intuition'},
    ],
    w:{a:{identityClarity:2,selfTrust:2},b:{goodOnPaperBias:2,selfTrust:-1},c:{goodOnPaperBias:3,selfTrust:-2,identityClarity:-1},d:{goodOnPaperBias:3,selfTrust:-3,intuitionTrust:-2}}
  },
  { id:'q43', section:'Attraction Clarity',
    text:'Which creates more confusion for you?',
    options:[
      {value:'a',label:'Strong chemistry with instability'},
      {value:'b',label:'Stability without intense attraction'},
      {value:'c',label:'Balancing logic and emotion'},
      {value:'d',label:'Fear of rejecting a "good option"'},
    ],
    w:{a:{emotionalAvailabilityMismatch:2,redFlagBlindness:1},b:{emotionalAvailabilityMismatch:2,goodOnPaperBias:1},c:{overthinking:2,identityClarity:-1},d:{goodOnPaperBias:2,pressureVulnerability:2,selfTrust:-1}}
  },
  { id:'q44', section:'Attraction Clarity',
    text:'If someone checks every practical box but something emotionally feels missing, you usually:',
    options:[
      {value:'a',label:'Trust the emotional mismatch'},
      {value:'b',label:'Explore further carefully'},
      {value:'c',label:'Feel guilty for hesitating'},
      {value:'d',label:'Push myself to continue anyway'},
    ],
    w:{a:{selfTrust:3,identityClarity:2,intuitionTrust:3},b:{selfTrust:1,identityClarity:1},c:{goodOnPaperBias:2,pressureVulnerability:1,selfTrust:-1},d:{goodOnPaperBias:3,selfTrust:-2,boundaryStrength:-1,intuitionTrust:-2}}
  },
  { id:'q45', section:'Attraction Clarity',
    text:'How much does external approval affect attraction?',
    options:[
      {value:'a',label:'Very little'},
      {value:'b',label:'Somewhat'},
      {value:'c',label:'Quite a lot'},
      {value:'d',label:'More than I\'d like to admit'},
    ],
    w:{a:{identityClarity:2,selfTrust:2},b:{goodOnPaperBias:1,pressureVulnerability:1},c:{goodOnPaperBias:2,pressureVulnerability:2,selfTrust:-1,identityClarity:-1},d:{goodOnPaperBias:3,pressureVulnerability:2,selfTrust:-2,identityClarity:-2}}
  },

  /* ── Section 10: Emotional Availability (Q46–Q50) ── */
  { id:'q46', section:'Emotional Availability',
    text:'What type of connection feels most emotionally familiar?',
    options:[
      {value:'a',label:'Calm and emotionally consistent'},
      {value:'b',label:'Intense and unpredictable'},
      {value:'c',label:'Emotionally distant but exciting'},
      {value:'d',label:'One where I overgive emotionally'},
    ],
    w:{a:{secureAttachment:3,marriageReadiness:2},b:{emotionalAvailabilityMismatch:3,anxiousAttachment:2},c:{avoidantAttachment:2,emotionalAvailabilityMismatch:3},d:{anxiousAttachment:3,boundaryStrength:-2,emotionalAvailabilityMismatch:2}}
  },
  { id:'q47', section:'Emotional Availability',
    text:'When someone communicates clearly and consistently, you feel:',
    options:[
      {value:'a',label:'Secure'},
      {value:'b',label:'Relieved'},
      {value:'c',label:'Slightly bored'},
      {value:'d',label:'Suspicious'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,marriageReadiness:2},b:{anxiousAttachment:1,emotionalStability:1},c:{emotionalAvailabilityMismatch:3,avoidantAttachment:1},d:{fearfulAvoidant:3,emotionalAvailabilityMismatch:2,emotionalStability:-1}}
  },
  { id:'q48', section:'Emotional Availability',
    text:'Have you been more attracted to emotionally complicated people than emotionally healthy ones?',
    options:[
      {value:'a',label:'Rarely'},
      {value:'b',label:'Sometimes'},
      {value:'c',label:'Often'},
      {value:'d',label:'Almost always'},
    ],
    w:{a:{secureAttachment:2},b:{emotionalAvailabilityMismatch:1,anxiousAttachment:1},c:{emotionalAvailabilityMismatch:3,anxiousAttachment:2,redFlagBlindness:1},d:{emotionalAvailabilityMismatch:3,anxiousAttachment:2,redFlagBlindness:2,fearfulAvoidant:1}}
  },
  { id:'q49', section:'Emotional Availability',
    text:'What usually creates emotional excitement for you?',
    options:[
      {value:'a',label:'Deep trust and connection'},
      {value:'b',label:'Emotional intensity'},
      {value:'c',label:'Uncertainty and anticipation'},
      {value:'d',label:'Feeling emotionally chosen'},
    ],
    w:{a:{secureAttachment:3,marriageReadiness:2,emotionalStability:2},b:{anxiousAttachment:2,emotionalAvailabilityMismatch:1},c:{emotionalAvailabilityMismatch:3,anxiousAttachment:2,redFlagBlindness:1},d:{anxiousAttachment:3,selfTrust:-1,emotionalAvailabilityMismatch:1}}
  },
  { id:'q50', section:'Emotional Availability',
    text:'If a relationship feels peaceful, your mind tends to think:',
    options:[
      {value:'a',label:'This feels healthy'},
      {value:'b',label:'I hope this stays consistent'},
      {value:'c',label:'Something must be missing'},
      {value:'d',label:'I\'m waiting for things to change'},
    ],
    w:{a:{secureAttachment:3,emotionalStability:2,marriageReadiness:2},b:{anxiousAttachment:1,emotionalStability:1},c:{emotionalAvailabilityMismatch:3,fearfulAvoidant:1,redFlagBlindness:1},d:{emotionalAvailabilityMismatch:3,fearfulAvoidant:2,anxiousAttachment:1}}
  },

  /* ── Section 11: Relationship Readiness (Q51–Q55) ── */
  { id:'q51', section:'Relationship Readiness',
    text:'Why do you want marriage right now?',
    options:[
      {value:'a',label:'I feel emotionally ready to build a life'},
      {value:'b',label:'I want companionship and partnership'},
      {value:'c',label:'I feel pressure about time and future'},
      {value:'d',label:'I want emotional security and certainty'},
    ],
    w:{a:{marriageReadiness:3,emotionalStability:2,secureAttachment:2},b:{marriageReadiness:2,secureAttachment:1},c:{pressureVulnerability:3,marriageReadiness:-2},d:{anxiousAttachment:2,pressureVulnerability:1}}
  },
  { id:'q52', section:'Relationship Readiness',
    text:'If marriage was completely removed as a social expectation, would you still actively seek partnership now?',
    options:[
      {value:'a',label:'Absolutely'},
      {value:'b',label:'Probably'},
      {value:'c',label:'I\'m not sure'},
      {value:'d',label:'Maybe not'},
    ],
    w:{a:{marriageReadiness:3,selfTrust:2,identityClarity:2},b:{marriageReadiness:2,selfTrust:1},c:{pressureVulnerability:2,selfTrust:-1,marriageReadiness:-1},d:{pressureVulnerability:3,marriageReadiness:-2,identityClarity:-1}}
  },
  { id:'q53', section:'Relationship Readiness',
    text:'What matters most before saying "yes" to someone?',
    options:[
      {value:'a',label:'Emotional safety and trust'},
      {value:'b',label:'Shared long-term vision'},
      {value:'c',label:'Stability and commitment'},
      {value:'d',label:'Feeling certain enough quickly'},
    ],
    w:{a:{secureAttachment:3,marriageReadiness:2,identityClarity:2},b:{identityClarity:2,marriageReadiness:2},c:{goodOnPaperBias:1,marriageReadiness:1},d:{anxiousAttachment:1,pressureVulnerability:2,selfTrust:-1}}
  },
  { id:'q54', section:'Relationship Readiness',
    text:'Which statement feels most true?',
    options:[
      {value:'a',label:'I would rather wait than choose wrong'},
      {value:'b',label:'I want clarity before commitment'},
      {value:'c',label:'I fear waiting too long'},
      {value:'d',label:'I fear ending up alone'},
    ],
    w:{a:{selfTrust:2,identityClarity:2,marriageReadiness:1},b:{identityClarity:2,selfTrust:2,marriageReadiness:1},c:{pressureVulnerability:3,anxiousAttachment:1,marriageReadiness:-1},d:{anxiousAttachment:3,pressureVulnerability:2,marriageReadiness:-1}}
  },
  { id:'q55', section:'Relationship Readiness',
    text:'Right now, your emotional state around marriage feels:',
    options:[
      {value:'a',label:'Grounded and intentional'},
      {value:'b',label:'Hopeful but cautious'},
      {value:'c',label:'Confused and pressured'},
      {value:'d',label:'Emotionally exhausted'},
    ],
    w:{a:{marriageReadiness:3,emotionalStability:2,identityClarity:2},b:{marriageReadiness:2,emotionalStability:1},c:{pressureVulnerability:3,emotionalStability:-2,marriageReadiness:-2},d:{emotionalStability:-3,marriageReadiness:-2,anxiousAttachment:1}}
  },

  /* ── Email capture after all 55 questions ── */
  { id:'email', section:'Almost There',
    type:'email',
    text:'Where should we send your Relationship Clarity Report?',
    subtitle:'You\'ve answered all 55 questions. Your full personalised report will be ready in about 90 seconds — enter your details to receive it.',
  },
];


/* ═══════════════════════════════════════════════════
   SCORING ENGINE
═══════════════════════════════════════════════════ */

const _DIMS = [
  'identityClarity','emotionalStability','boundaryStrength',
  'pressureVulnerability','selfTrust',
  'anxiousAttachment','avoidantAttachment','secureAttachment','fearfulAvoidant',
  'redFlagBlindness','overthinking','intuitionTrust',
  'goodOnPaperBias','emotionalAvailabilityMismatch','marriageReadiness',
];

/* Compute raw sums from answers */
function _computeRaw(answers) {
  const raw = Object.fromEntries(_DIMS.map(d => [d, 0]));
  for (const q of Q3_QUESTIONS) {
    if (q.type === 'email') continue;
    const ans = answers[q.id];
    if (!ans) continue;
    const w = q.w[ans] || {};
    for (const [dim, val] of Object.entries(w)) {
      raw[dim] = (raw[dim] || 0) + val;
    }
  }
  return raw;
}

/* Compute min/max possible scores across all questions */
const _MM = (() => {
  const mm = Object.fromEntries(_DIMS.map(d => [d, {min:0,max:0}]));
  for (const q of Q3_QUESTIONS) {
    if (q.type === 'email') continue;
    for (const dim of _DIMS) {
      const vals = ['a','b','c','d'].map(o => (q.w[o]||{})[dim]||0);
      mm[dim].min += Math.min(...vals);
      mm[dim].max += Math.max(...vals);
    }
  }
  return mm;
})();

/* Normalize a raw score to 0–100 */
function _norm(raw, dim) {
  const {min, max} = _MM[dim];
  if (max === min) return 50;
  return Math.max(0, Math.min(100, Math.round(((raw - min) / (max - min)) * 100)));
}

/* Derive dominant attachment style */
function _attachment(s) {
  const {secureAttachment:sec, anxiousAttachment:anx, avoidantAttachment:avo, fearfulAvoidant:fa} = s;
  if (fa >= 60 && anx >= 55) return 'Fearful-Avoidant';
  const top = Math.max(sec, anx, avo, fa);
  if (top === sec && sec >= 50) return 'Secure';
  if (top === avo) return 'Avoidant';
  if (top === anx) return 'Anxious';
  return 'Anxious'; // default
}

/* Derive marriage readiness type */
function _marriageType(s) {
  if (s.marriageReadiness >= 70 && s.pressureVulnerability < 50) return 'Grounded & Ready';
  if (s.pressureVulnerability >= 70) return 'Pressure-Driven';
  if (s.emotionalStability < 40 || s.redFlagBlindness >= 70) return 'Healing Before Commitment';
  if (s.anxiousAttachment >= 65 && s.marriageReadiness < 55) return 'Fear-Based Attachment Seeking';
  return 'Emotionally Hopeful but Cautious';
}

/* Detect key contradictions */
function _contradictions(s) {
  const out = [];
  if (s.secureAttachment >= 50 && s.emotionalAvailabilityMismatch >= 60) out.push('desires_safety_but_attracted_inconsistency');
  if (s.selfTrust < 50 && s.overthinking >= 60) out.push('low_trust_high_overthinking');
  if (s.pressureVulnerability >= 65 && s.marriageReadiness < 55) out.push('pressure_driven_not_ready');
  if (s.identityClarity >= 65 && s.boundaryStrength < 50) out.push('knows_values_cant_enforce_boundaries');
  if (s.redFlagBlindness >= 60 && s.selfTrust >= 60) out.push('blind_spots_with_self_trust');
  if (s.avoidantAttachment >= 60 && s.marriageReadiness >= 65) out.push('avoidant_but_wants_commitment');
  return out;
}

/* Derive top 3 dominant patterns */
function _patterns(s) {
  const candidates = [
    {name:'Fear-Driven Attachment',        score: s.anxiousAttachment,                    threshold:62},
    {name:'Relationship Hyper-Analysis',   score: s.overthinking,                         threshold:62},
    {name:'Emotional Rationalisation',     score: s.redFlagBlindness,                     threshold:58},
    {name:'Stability vs Chemistry Conflict',score:s.emotionalAvailabilityMismatch,        threshold:62},
    {name:'Timeline Pressure',             score: s.pressureVulnerability,                threshold:62},
    {name:'Validation-Based Attraction',   score: s.goodOnPaperBias,                      threshold:58},
    {name:'Emotional Over-Responsibility', score: 100 - s.boundaryStrength,               threshold:55},
    {name:'Intuition Suppression',         score: 100 - s.selfTrust,                      threshold:55},
    {name:'Emotional Self-Protection',     score: s.avoidantAttachment,                   threshold:58},
    {name:'Push-Pull Attachment',          score: s.fearfulAvoidant,                      threshold:55},
    {name:'Clear Self-Awareness',          score: s.identityClarity,                      threshold:75},
    {name:'Grounded Emotional Clarity',    score: s.emotionalStability,                   threshold:75},
  ];
  return candidates
    .filter(c => c.score >= c.threshold)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map(c => c.name);
}

/* Compute overall clarity score (0–100) */
function _overall(s) {
  const components = [
    s.identityClarity,
    s.emotionalStability,
    s.boundaryStrength,
    100 - s.pressureVulnerability,
    s.selfTrust,
    s.secureAttachment,
    100 - s.redFlagBlindness,
    Math.round((s.intuitionTrust + (100 - s.overthinking)) / 2),
    100 - s.goodOnPaperBias,
    100 - s.emotionalAvailabilityMismatch,
    s.marriageReadiness,
  ];
  return Math.round(components.reduce((a, b) => a + b, 0) / components.length);
}

/* ── Main export: compute full scored profile from answers ── */
export function buildScoredProfile(answers) {
  const raw    = _computeRaw(answers);
  const scores = Object.fromEntries(_DIMS.map(d => [d, _norm(raw[d], d)]));

  return {
    scores,
    derived: {
      attachmentStyle:        _attachment(scores),
      marriageReadinessType:  _marriageType(scores),
      dominantPatterns:       _patterns(scores),
      contradictions:         _contradictions(scores),
      overallScore:           _overall(scores),
    },
  };
}
