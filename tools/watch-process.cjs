const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');

const root = process.cwd();
const pending = new Set();
const contents = new Map();
let timer;
let running = false;

function updateProcess() {
  if (running || pending.size === 0) return;
  const files = [...pending].sort();
  pending.clear();
  running = true;
  console.log('DOC_EVENT', JSON.stringify(files));
  const log = fs.openSync(path.join(root, '.git/process-agent.log'), 'a');
  const prompt = [
    '这是代码/JSON编辑事件触发的文档维护任务。',
    '读取AGENTS.md和docs/README.md，再检查这些文件的当前内容和Git差异：',
    JSON.stringify(files),
    '从docs/design中找对应游戏设计，只更新已有事实所需的docs/process/json或docs/process/code同名文档。',
    'JSON实现和代码实现分别维护，各自引用同名design，单向依赖。',
    '只做Bug排查或Bug修复时不入档；没有明确对应设计或没有可归档实现事实时，不创建占位文档，输出原因。',
    '按标题重写完整相关章节，删除矛盾结论，不追加日期流水。未执行的验证明确写未执行。',
    '只允许修改docs/process，不修改源码、JSON、design、vanilla、归档或其他文件。',
    '不提交Git，不启动其他agent，不启动监听器。'
  ].join('\n');
  const child = spawn('codex', [
    'exec', '--ephemeral', '--sandbox', 'workspace-write', '-C', root, prompt
  ], { cwd: root, stdio: ['ignore', log, log] });
  child.on('error', error => console.error('AGENT_ERROR', error.message));
  child.on('close', code => {
    fs.closeSync(log);
    running = false;
    console.log('AGENT_EXIT', code);
    if (pending.size) timer = setTimeout(updateProcess, 1000);
  });
}

fs.watch(root, { recursive: true }, (_event, filename) => {
  const file = String(filename);
  if (!/^(src|data|tests|tools|build-scripts)\//.test(file)) return;
  if (!/\.(c|cc|cpp|cxx|h|hh|hpp|hxx|py|js|mjs|cjs|ts|tsx|sh|json)$/.test(file)) return;
  const full = path.join(root, file);
  const text = fs.existsSync(full) ? fs.readFileSync(full, 'utf8') : null;
  if (contents.has(file) && contents.get(file) === text) return;
  contents.set(file, text);
  pending.add(file);
  clearTimeout(timer);
  timer = setTimeout(updateProcess, 1000);
});

console.log('READY', root);
