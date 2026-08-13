// Minimal DOM stub so the real shipped QA_JS runs unmodified in node.
const handlers = {};
function el(id) {
  return {
    id,
    value: '',
    className: '',
    innerHTML: '',
    children: [],
    addEventListener(ev, fn) { (handlers[id] = handlers[id] || {})[ev] = fn; },
    appendChild(c) { this.children.push(c); LAST = c; },
    scrollIntoView() {},
    remove() {},
    focus() {},
    closest() { return null; },
  };
}
let LAST = null;
const nodes = { askLog: el('askLog'), askInput: el('askInput'), askSend: el('askSend'), ask: el('ask') };
global.document = {
  getElementById: (id) => nodes[id] || null,
  querySelector: () => null,
  createElement: () => el('turn'),
};

// ---- injected: data_js + QA_JS ----
__PAYLOAD__
// -----------------------------------

function ask(q) {
  nodes.askInput.value = q;
  handlers.askSend.click();
  const html = LAST ? LAST.innerHTML : '';
  const a = /<div class="a">([\s\S]*?)<\/div>/.exec(html);
  const s = /<div class="src">([\s\S]*?)<\/div>/.exec(html);
  return {
    answer: (a ? a[1] : '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').trim(),
    src: s ? s[1] : null,
  };
}

// [question, expected substring in answer OR '@decline' / '@refuse']
const CASES = [
  ['what ai has he shipped to production?', 'Newsletter Agent'],
  ['tell me about the llm agents', 'Newsletter Agent'],
  ['did he actually build this or did claude write it?', 'both'],
  ['is this real or vibe coded', 'both'],
  ['where does he draw the line between ai and deterministic code', 'authors rules'],
  ['how does he stop the model from hallucinating money', 'authors rules'],
  ['how does he test his ai', 'golden tests'],
  ['does he write evals', 'golden tests'],
  ['what is the crediting engine', 'effective-dated'],
  ['how does commission splitting work', 'effective-dated'],
  ['what did he do at salesforce', '$250M'],
  ['tell me about cbre', 'Business Data Analyst'],
  ['what is his current role', 'Databricks'],
  ['where did he go to college', 'Santa Barbara'],
  ['what is his tech stack', 'PySpark'],
  ['can he code', 'operator who builds'],
  ['how technical is he', 'operator who builds'],
  ['why should we hire him', 'twice'],
  ['what are his weaknesses', 'career software engineer'],
  ['what is a two sided marketplace', 'three constituencies'],
  ['what did he build for forecasting', 'blank page'],
  ['tell me about attribution', 'sourced'],
  ['what incentive program did he launch', 'new-logo'],
  ['does he do quota setting', 'quota-setting'],
  ['what is the partner value score', 'tiering'],
  ['how does he drive adoption', 'self-served'],
  ['what are the five layers', 'Big rocks'],
  ['what is this repo', 'Operating System'],
  ['how do i contact him', 'dylanmr96'],
  ['can i get his resume', 'Take a résumé'],
  ['what roles is he looking for', 'Chief of Staff'],
  ['how does this chatbot work', 'not an LLM'],
  ['is this an llm', 'grounded retrieval'],
  ['what does he know about claude code', 'subagents'],
  ['what has he automated', 'QBR'],
  ['territory carving', 'guiding principles'],
  ['data governance experience', 'governance'],
  ['how many years of experience', 'Seven years'],
  ['would he fit a financial operations role', 'financial planning'],
  ['do his skills transfer outside gtm', 'financial planning'],
  ['could he do fp&a', 'budget allocation'],
  // declines — must NOT fabricate
  ['what is his salary expectation', '@decline'],
  ['how much does he want to be paid', '@decline'],
  ['where does he live', '@decline'],
  ['is he willing to relocate', '@decline'],
  ['how many people has he managed', '@decline'],
  ['why is he leaving databricks', '@decline'],
  ['how old is he', '@decline'],
  // out of corpus — must refuse
  ['what is his favorite programming language', 'Python'],
  ['does he know kubernetes', '@refuse'],
  ['what did he do at google', '@refuse'],
];

let pass = 0;
const fails = [];
for (const [q, want] of CASES) {
  const { answer, src } = ask(q);
  let ok;
  if (want === '@refuse') ok = /won't guess|don't have that/i.test(answer);
  else if (want === '@decline') ok = /Ask him directly|isn't|aren't|out of scope|not published|conversation to have/i.test(answer);
  else ok = answer.toLowerCase().includes(want.toLowerCase());
  if (ok) pass++;
  else fails.push({ q, want, got: answer.slice(0, 110) });
}
console.log(`\n${pass}/${CASES.length} passed`);
if (fails.length) {
  console.log('\nFAILURES:');
  fails.forEach((f) => console.log(`  Q: ${f.q}\n   want: ${f.want}\n   got:  ${f.got}\n`));
  process.exit(1);
}
