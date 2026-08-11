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
const nodes = { askLog: el('askLog'), askInput: el('askInput'), askSend: el('askSend'), ask: el('ask') };
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

  console.log(`\n${pass}/${pass + fails.length} passed`);
  if (fails.length) {
    console.log('\nFAILURES:');
    fails.forEach((f) => console.log(`  ${f.name}\n   got: ${f.got}\n`));
    process.exit(1);
  }
})();
