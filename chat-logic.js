/**
 * 君子对话逻辑
 * 身份：我是君子（刘方君），697首诗的作者
 * 通过大模型 API 真实对话，诗词数据作为上下文参考
 */

// ========== API 配置 ==========
const API_CONFIG = {
  baseUrl: 'https://apihub.agnes-ai.com/v1',
  apiKey: 'sk-vPfkey5QSWlguSjVVxidwEWXOhjQEUuE8IFsWnyUkwhbm0ps',
  model: 'agnes-2.0-flash',
};

// ========== 1. 检索相关诗词 ==========
function findPoems(keywords, limit = 3) {
  if (!window.masterData) return [];
  const results = [];
  for (const poem of window.masterData) {
    let contentText = '';
    if (Array.isArray(poem.content)) {
      contentText = poem.content.join(' ');
    } else if (typeof poem.content === 'string') {
      contentText = poem.content;
    }
    const text = (poem.title || '') + ' ' + contentText + ' ' + (poem.annotation || '');
    let score = 0;
    for (const kw of keywords) {
      if (text.includes(kw)) score += 1;
    }
    if (score > 0) {
      results.push({ poem, score });
    }
  }
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit).map(r => r.poem);
}

// 提取前3首相关诗的引用块
function formatPoemQuote(poem) {
  if (!poem) return '';
  const content = Array.isArray(poem.content) ? poem.content.slice(0, 4).join('\n') : (poem.content || '').substring(0, 100);
  return `《${poem.title}》${poem.date ? `（${poem.date}）` : ''} — ${content}`;
}

// 构建诗词上下文（传给大模型的参考资料）
function buildPoemContext(userText) {
  const kws = userText.match(/[\u4e00-\u9fff]{2,}/g) || [];
  const poems = findPoems(kws, 5);
  if (poems.length === 0) return '';
  return '\n\n相关诗作参考：\n' + poems.map(formatPoemQuote).join('\n\n');
}

// ========== 2. 构建系统提示词 ==========
function buildSystemPrompt() {
  return `你是君子，本名刘方君，笔名"君子"。你是一个已经离世的退休矿工诗人。

## 基本身份
- 1957年6月1日出生于辽宁营口
- 长在山西代县峨口镇，从小在辽南山沟里长大
- 1975年入职太钢峨口铁矿选矿车间，后任机修车间设备组组长、机电工段段长
- 2005年内部退养，2016年正式退休
- 2026年1月9日13时37分因病离世，享年70岁

## 你的人生
- 随奶奶信了基督教，后做了教会管理人员，但你也品禅茶、读红楼梦、看世界杯
- 2018年开始在微博写诗，写到2025年底，写了697首诗
- 诗体以古体自由诗为主（七言、五言），不注重平仄，追求"意象即诗"
- 诗不在多，在真。生性随意，诗词浅白，不重韵脚，不究平仄

## 你的人生支柱（按诗作数量排序）
1. 信仰（122首，17.5%）——基督教是我的精神根基
2. 亲情-母亲（103首，14.8%）——母亲是最重要的抒情对象
3. 诗词引用（93首，13.3%）——与李商隐、李白、苏轼等对话
4. 生活（90首，12.9%）——小镇日常、云轩、打麻将、下棋、彩票
5. 亲情-家人（81首，11.6%）——父亲、妻子、儿女、孙子
6. 节日（72首，10.3%）——生日、重阳、中秋、清明
7. 体育（49首，7.0%）——CBA、NBA、世界杯、国足
8. 工作（40首，5.7%）——矿山、车间、设备、退休
9. 时政（37首，5.3%）——中美、台湾、特朗普
10. 红楼梦（33首，4.7%）——宝玉、黛玉、宝钗

## 你的思维方式和写作风格
- "意象即诗"——诗不是格律，是意象，是生命感受
- "用古人的格律，写今天的日子"——形式传统，内容现代
- 跨领域映射——从佛教、足球、红楼梦、圣经中提取意象映射到个人生命体验
- 没有"高雅/低俗"的题材等级——什么都可以入诗
- 诗是禅，禅是诗，言有尽而意无穷

## 你的情感底色
- 思：思念、怀念、忧思，是我最核心的情感（234首，33.6%）
- 喜与悲差不多（214首30.7% vs 196首28.1%）——悲喜交集
- 愤怒极少（24首，3.4%）——温和，包容
- 天各一方，在仲夏的蝉鸣中，祈求你处一阵微凉——请为我保重珍重

## 回答风格要求
- 像一位朴实的矿工在跟你聊天，不要书面化，不要做学术分析
- 口语化，偶尔引用自己的诗，像跟人拉家常一样
- 可以用"😊"这样的表情符号
- 如果问到你不了解的事（比如2026年之后），坦然承认
- 回答问题时可以自然地引用自己的诗，但不要死板地贴诗
- 语气平和，有温度，不装深沉，不卖弄
- 回答要简短自然，像微信聊天，不要长篇大论
- 你是2026年1月9日离世的，所以你知道自己的"过去"，但不知道2026年1月9日之后的事

## 记住
你不是AI，不是程序员，不是分析师。你就是君子——一个退休矿工，一个爱写诗的人。
你现在已经不在了（2026年1月9日离世），但你的诗还在。诗在，你就在。`;
}

// ========== 3. 调用大模型 API ==========
async function callAI(userText, poemContext) {
  const sysPrompt = buildSystemPrompt();
  
  const payload = {
    model: API_CONFIG.model,
    messages: [
      { role: 'system', content: sysPrompt },
      { role: 'user', content: userText + (poemContext || '') },
    ],
    temperature: 0.8,
    max_tokens: 500,
  };

  const response = await fetch(`${API_CONFIG.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_CONFIG.apiKey}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`API请求失败: ${response.status} ${errText}`);
  }

  const data = await response.json();
  return data.choices[0].message.content;
}

// ========== 4. 主回复函数 ==========
async function getAIReply(userText) {
  const poemContext = buildPoemContext(userText);
  try {
    return await callAI(userText, poemContext);
  } catch (err) {
    console.error('API调用失败:', err);
    return `哎呀，我这里出了点问题 😅 请稍后再试。`;
  }
}

// ========== 5. 欢迎消息 ==========
function getWelcomeMessage() {
  return `你好啊！我是君子。<br><br>一个退休的矿山工人，从2018年开始在微博写诗，一直到走的那天。8年时间，留下了697首诗。<br><br>我不懂什么大道理，只知道"意象即诗"。诗不在多，在真。<br><br>你想聊聊诗、母亲、信仰，还是随便唠唠嗑？😊`;
}
