// Drives the shipped chat client through a stubbed DOM + fetch, so the live
// path and its fallback are exercised as written rather than reimplemented.
const handlers = {};
let LOG = [];

function el(id) {
  const node = {
    id, value: '', className: '', innerHTML: '', disabled: false, children: [],
    classList: { add() {}, remove() {} },
    addEventListener(ev, fn) { (handlers[id] = handlers[id] || {})[ev] = fn; },
    appendChild(c) { this.children.push(c); LOG.push(c); },
    scrollIntoView() {}, remove() { LOG = LOG.filter((n) => n !== this); },
    focus() {}, closest() { return null; },
  };
  return node;
}
const nodes = {
  askLog: el('askLog'), askInput: el('askInput'), askSend: el('askSend'), ask: el('ask'),
  jdToggle: el('jdToggle'), jdBar: el('jdBar'), jdInput: el('jdInput'), jdSend: el('jdSend'),
};
global.document = {
  getElementById: (id) => nodes[id] || null,
  querySelector: () => null,
  createElement: () => el('turn'),
};

let FETCH_IMPL = null;
global.fetch = (...args) => FETCH_IMPL(...args);

// ---- injected: data_js + QA_JS ----
__PAYLOAD__
// -----------------------------------

const tick = () => new Promise((r) => setTimeout(r, 0));

async function send(q) {
  LOG = [];
  nodes.askInput.value = q;
  handlers.askSend.click();
  for (let i = 0; i < 12; i++) await tick(); // let promise chains settle
  const html = LOG.map((n) => n.innerHTML).join('\n');
  return html.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
}

function ok(name, cond, got) {
  if (cond) { pass++; return; }
  fails.push({ name, got: (got || '').slice(0, 120) });
}

let pass = 0;
const fails = [];

(async () => {
  // 1. live model answers -> its reply is rendered, retrieval is not used
  FETCH_IMPL = async () => ({
    ok: true,
    json: async () => ({ reply: 'I was the first Partner S&O hire at Databricks.' }),
  });
  let out = await send('walk me through your background');
  ok('live reply rendered', out.includes('first Partner S&O hire'), out);

  // 2. multi-turn -> history is sent, and grows
  let seenBody = null;
  FETCH_IMPL = async (_url, opts) => {
    seenBody = JSON.parse(opts.body);
    return { ok: true, json: async () => ({ reply: 'Second answer.' }) };
  };
  out = await send('and after that?');
  ok('history carries prior turns', seenBody.messages.length >= 3, JSON.stringify(seenBody));
  ok('history ends on the user', seenBody.messages[seenBody.messages.length - 1].role === 'user');

  // 3. rate limited -> falls back to retrieval, says why, still answers
  FETCH_IMPL = async () => ({ ok: false, json: async () => ({ error: 'rate_limited' }) });
  out = await send('what is the crediting engine');
  ok('rate-limit note shown', /Busy right now/i.test(out), out);
  ok('rate-limit still answers', /effective-dated/i.test(out), out);

  // 4. network failure -> falls back, different note, still answers
  FETCH_IMPL = async () => { throw new Error('network down'); };
  out = await send('where did you go to school');
  ok('outage note shown', /unreachable/i.test(out), out);
  ok('outage still answers', /Santa Barbara/i.test(out), out);

  // 5. a failed turn must not poison the next request's history
  FETCH_IMPL = async (_url, opts) => {
    seenBody = JSON.parse(opts.body);
    return { ok: true, json: async () => ({ reply: 'Recovered.' }) };
  };
  out = await send('are you still there');
  const roles = seenBody.messages.map((m) => m.role).join(',');
  ok('no orphaned turn after failure', !/user,user/.test(roles), roles);
  ok('recovers after failure', out.includes('Recovered'), out);

  // ---- JD fit check ----
  const JD = 'We need a revenue operations lead with forecasting experience. '.repeat(10);
  async function sendJd(jd) {
    LOG = [];
    nodes.jdInput.value = jd;
    handlers.jdSend.click();
    for (let i = 0; i < 12; i++) await tick();
    return LOG.map((n) => n.innerHTML).join('\n')
      .replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
  }

  // 6. toggle is revealed only when an endpoint exists (it is in this run)
  ok('jd toggle revealed with endpoint', nodes.jdToggle.hidden === false,
    String(nodes.jdToggle.hidden));

  // 7. success: mapping rendered, both sides pushed into history
  let jdBody = null;
  FETCH_IMPL = async (_url, opts) => {
    jdBody = JSON.parse(opts.body);
    return { ok: true, json: async () => ({ reply: 'Forecasting — LISTED. Kubernetes — NOT LISTED.' }) };
  };
  out = await sendJd(JD);
  ok('jd request uses jd mode', jdBody.mode === 'jd' && jdBody.jd.length > 100, JSON.stringify(jdBody).slice(0, 80));
  ok('jd mapping rendered', out.includes('NOT LISTED'), out);
  FETCH_IMPL = async (_url, opts) => {
    seenBody = JSON.parse(opts.body);
    return { ok: true, json: async () => ({ reply: 'Follow-up answered.' }) };
  };
  out = await send('what about the second requirement?');
  const joined = seenBody.messages.map((m) => m.content).join(' ');
  ok('follow-up carries the fit-check context', /Fit check against this job description/.test(joined),
    joined.slice(0, 120));

  // 8. failure: honest note, no retrieval fake, history untouched
  const before = seenBody.messages.length;
  FETCH_IMPL = async () => { throw new Error('down'); };
  out = await sendJd(JD);
  ok('jd failure is honest (no retrieval fallback)', /email me the JD/i.test(out), out);
  FETCH_IMPL = async (_url, opts) => {
    seenBody = JSON.parse(opts.body);
    return { ok: true, json: async () => ({ reply: 'ok' }) };
  };
  // Expected growth since `before` (captured at the follow-up SEND): the
  // follow-up's assistant reply (+1) and this new user turn (+1). A failed JD
  // contributing anything would make it +3 or more.
  await send('still with me?');
  ok('failed jd left no orphaned history', seenBody.messages.length === before + 2,
    `${seenBody.messages.length} vs ${before}+2`);

  // 9. jd-specific rate limit message
  FETCH_IMPL = async () => ({ ok: false, json: async () => ({ error: 'rate_limited', scope: 'jd' }) });
  out = await sendJd(JD);
  ok('jd rate-limit message shown', /few per hour/i.test(out), out);

  console.log(`\n${pass}/${pass + fails.length} passed`);
  if (fails.length) {
    console.log('\nFAILURES:');
    fails.forEach((f) => console.log(`  ${f.name}\n   got: ${f.got}\n`));
    process.exit(1);
  }
})();
