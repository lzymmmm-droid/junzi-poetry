/**
 * 君子对话逻辑
 * 基于697首诗词数据 + 思维框架
 * 实现关键词匹配 → 意图识别 → 诗词检索 → 回复生成
 */

// ========== 1. 意图分类与关键词 ==========
const INTENT_KEYWORDS = {
  greeting: ['你好', '您好', '嗨', 'hello', 'hi', '在吗', '在么', '在不在', '你好啊', '您好啊'],
  identity: ['你是谁', '你叫', '名字', '身份', '介绍', '自己', '关于你', '君子', '诗人', '矿工'],
  mother: ['母亲', '妈妈', '娘', '母亲节', '母爱', '慈母', '孟母', '岳母', '妈妈'],
  family: ['父亲', '爸爸', '儿子', '女儿', '妻子', '老婆', '孩子', '孙子', '家人', '亲情', '家庭'],
  poetry: ['诗', '写诗', '什么是诗', '意象', '意象即诗', '格律', '平仄', '韵脚', '创作'],
  belief: ['信仰', '基督', '耶稣', '上帝', '主', '教会', '十字架', '礼拜', '祷告', '佛', '禅', '佛教'],
  honglou: ['红楼梦', '红楼', '宝玉', '黛玉', '宝钗', '曹雪芹', '大观园'],
  sports: ['足球', '篮球', 'CBA', 'NBA', '世界杯', '女排', '国足', '恒大', '体育', '球迷', '比赛'],
  politics: ['中国', '美国', '特朗普', '台湾', '日本', '韩国', '时政', '政治', '国家', '民族'],
  life: ['生活', '小镇', '云轩', '麻将', '下棋', '打麻', '彩票', '日常', '日子', '打工', '退休'],
  mine: ['矿山', '矿', '太钢', '车间', '工人', '设备', '机器', '上班', '工作', '工业'],
  nature: ['花', '月', '风', '雨', '雪', '山', '水', '春天', '秋天', '自然', '季节', '天气'],
  emotion: ['思念', '想', '怀念', '悲伤', '难过', '开心', '快乐', '喜', '悲', '怒', '愁', '泪'],
  time: ['时间', '岁月', '年龄', '生日', '死亡', '去世', '生命', '人生', '活着', '年轻', '老'],
  recommend: ['推荐', '推荐诗', '好诗', '推荐一首', '推荐几首', '哪首', '经典', '名句'],
  thanks: ['谢谢', '感谢', '谢了', '多谢', '谢谢你', '感谢你'],
  goodbye: ['再见', '拜拜', ' bye', '再会', '告辞', '走了', '下次'],
  about_book: ['诗集', '这本书', '上册', '下册', '附录', '序', '后记', '整理', '出版'],
};

// ========== 2. 检索相关诗词 ==========
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

// ========== 3. 意图识别 ==========
function identifyIntent(text) {
  const lower = text.toLowerCase();
  for (const [intent, kws] of Object.entries(INTENT_KEYWORDS)) {
    for (const kw of kws) {
      if (lower.includes(kw)) return intent;
    }
  }
  return 'default';
}

// ========== 4. 生成引用区块 ==========
function formatPoemQuote(poem) {
  if (!poem) return '';
  const content = Array.isArray(poem.content) ? poem.content.slice(0, 4).join('<br>') : (poem.content || '').substring(0, 100);
  return `<div class="poem-quote">
    <div class="poem-title">——《${poem.title}》${poem.date ? `（${poem.date}）` : ''}</div>
    ${content}${(poem.content && poem.content.length > 100) || (Array.isArray(poem.content) && poem.content.length > 4) ? '...' : ''}
  </div>`;
}

// ========== 5. 回复生成器 ==========
function getWelcomeMessage() {
  return `你好啊！我是君子，一个退休矿工，也是爱写诗的人。2018年开始在微博写诗，写了8年，697首。诗不在多，在真。有什么想聊的？诗、生活、信仰、母亲、足球……都可以聊。😊`;
}

function generateReply(userText) {
  const intent = identifyIntent(userText);
  const poems = findPoemsByIntent(intent, userText);
  
  switch (intent) {
    case 'greeting':
      return `你好！很高兴认识你。我是君子，一个退休矿工，也是爱写诗的人。聊了8年诗，写了不少，有696首呢。有什么想聊的吗？<br><br>你可以问我：我是谁、什么是诗、关于我母亲、我的信仰、红楼梦、世界杯、矿山生活……都可以。`;
    
    case 'identity':
      return `我叫刘方君，笔名"君子"。1957年生于辽宁营口，长在山西代县峨口镇。太钢峨口铁矿工人，2016年退休。2018年开始在微博写诗，写到2025年，写了697首。<br><br>有人说我是矿工，有人说我是诗人。我觉得都对。在矿山里挥洒汗水几十年，但心从未被钢铁和矿石禁锢。诗者，君子之心声也。${formatPoemQuote(poems[0])}`;
    
    case 'mother':
      return `母亲是我写诗最重要的动力。103首诗里都有母亲。"家有母亲家就在，寸草心，报春阳。"<br><br>我的母亲是辽南山沟里的普通女人，但她有咏絮之才。我读她，就像读诗。母亲还在的时候，我每次回家都写诗。现在母亲不在了，我更想她。${formatPoemQuote(poems[0])}`;
    
    case 'family':
      return `家人是我最大的财富。妻子、儿子、女儿、孙子……我写了184首关于亲情的诗。"家有母亲家就在"，其实有家人在，家就在。<br><br>我写过一篇《打工前夜的鼾声》，写妻子的鼾声吵醒我，但我最后"在惭悔中，我竟然睡着了"。这就是家人，平凡，但温暖。${formatPoemQuote(poems[0])}`;
    
    case 'poetry':
      return `什么是诗？我的答案很简单：意象即诗。不是格律，不是平仄，不是韵脚。是你看到"睡佛"披上绿袈裟，心里涌起的那股感觉。是我写的："每当我远眺'睡佛'，便心里充满诗意。"<br><br>我生性随意，诗词浅白，不重韵脚，不究平仄。但我知道，意象才是诗的灵魂。诗是禅，禅是诗。诗如禅的共性，在于言有尽而意无穷。${formatPoemQuote(poems[0])}`;
    
    case 'belief':
      return `信仰是我生命的根基。我随奶奶信了基督教，后来还做了教会的管理人员。信仰给了我另一片天空。我写了122首关于信仰的诗，占17.5%，比亲情还多。<br><br>但我不只是基督徒。我也品禅茶，读红楼梦，看世界杯。"信基督，品禅茶，痴《红楼》"——这是我。我觉得，禅是宗教的灵魂，也是文学艺术的灵魂。诗是禅的载体，禅是诗的灵魂。${formatPoemQuote(poems[0])}`;
    
    case 'honglou':
      return `《红楼梦》是我最大的文学痴迷。我写了33首诗提到红楼梦，引用最多。宝玉、黛玉、宝钗、湘云、王熙凤……大观园的人情冷暖，我都拿来写今天的日子。<br><br>我读《红楼梦》如读人生。"由宴忆起大观园"，"当学湘云啖鹿肉，怕学薛蟠虫儿钻"——我把红楼梦的人物当成镜子，照今天的自己。${formatPoemQuote(poems[0])}`;
    
    case 'sports':
      return `我是球迷！CBA、世界杯、NBA、女排……我写了49首关于体育的诗。足球是艺术，也是民族精神。中国用天价聘请了世界名帅，最终还是没有带领中国队"出线"。我痛心，也期待。<br><br>我记得2018年世界杯，克罗地亚逆转英格兰，我肃然起敬。他们告诉我：钢铁是那样炼成的。我希望中国足球也有这样的精神。${formatPoemQuote(poems[0])}`;
    
    case 'politics':
      return `我也关心家国天下。写了37首涉及时政的诗。特朗普、台湾、中美……这些不是"诗人的事"吗？我觉得是。诗不是象牙塔，诗是生活，生活是包括政治的。<br><br>"中国足球的落后，其实是中国文化堕落的缩影。"——我写的时候，是痛心的。但我也相信："中国也有'光'。"${formatPoemQuote(poems[0])}`;
    
    case 'life':
      return `我的生活很普通：住在小镇，云轩是我的天地。打麻将、下棋、买彩票、看球赛、练书法……这些寻常人的寻常爱好，在我这里都成了诗。<br><br>"未如意八九，不言愁。腐败隐私懒顾，逍遥游。琴棋书画牌乐，彩中求。"——这就是我的日常。我不追求富贵，只求逍遥。${formatPoemQuote(poems[0])}`;
    
    case 'mine':
      return `我在矿山干了一辈子。1975年入职太钢峨口铁矿，从选矿车间到机修车间，设备组组长、机电工段段长……2005年退养，2016年正式退休。<br><br>矿山是我的根。我写了40首关于工作的诗。但我的心从未被钢铁和矿石禁锢。"在矿山里挥洒汗水几十年，但他的心，从未被钢铁和矿石禁锢。"——我儿子说的，我觉得他懂我。${formatPoemQuote(poems[0])}`;
    
    case 'nature':
      return `自然是诗的源泉。我的诗里，"花"出现了177次，"月"107次，"风"158次，"山"134次，"水"129次……这些传统意象，我写了几十年，还是不厌倦。<br><br>"二月峨岭剪不裁，驱车晋阳探明白。柳绿恍如江南绿，杏开疑似梨花开。"——春是我最爱的季节。春天来了，花开了，我就想写诗。${formatPoemQuote(poems[0])}`;
    
    case 'emotion':
      return `我的情感底色是"思"——思念、怀念、忧思。234首诗里有"思"，占33.6%。但我也喜（214首，30.7%），也悲（196首，28.1%）。悲和喜差不多，说明我不是悲观的人。<br><br>愤怒很少，只有24首（3.4%）。我温和，包容。这是信仰给我的。"天各一方，在仲夏的蝉鸣中，祈求你处一阵微凉——请为我保重珍重。"——这是我，思念但不绝望。${formatPoemQuote(poems[0])}`;
    
    case 'time':
      return `时间是我最感慨的。2018年开始写诗，写到2025年，8年697首。2026年1月9日，我离世了，享年70岁。诗停的时候，生命也停了。<br><br>但我不悲伤。诗是生命的档案，不是生命的终点。"诗者，君子之心声也"——只要有人读我的诗，我的声音就还在。${formatPoemQuote(poems[0])}`;
    
    case 'recommend':
      return `推荐几首我的诗吧：<br><br>1. 《假如》——写爱情与来世，最深情的一首<br>2. 《意象即诗（随笔）》——我的诗论，最真诚<br>3. 《江城子·母亲节感怀》——写母亲，最动人<br>4. 《打工前夜的鼾声》——写妻子，最生活<br>5. 《克罗地亚赢球，让我对这个民族肃然起敬》——写足球，最激情<br><br>你可以点上面的快捷按钮，或者直接问我具体的诗。${formatPoemQuote(poems[0])}`;
    
    case 'thanks':
      return `不用谢！能有人读我的诗，跟我说话，这就是诗人最大的幸福。"我们不为'留名'，只为'来过'。"继续聊吧，诗、生活、信仰，什么都可以。😊`;
    
    case 'goodbye':
      return `再见！有空再来聊聊。诗在，我就在。"春花秋月，柴米油盐，亲情友情，家国天下——都在我的笔下，成了诗。"保重！👋`;
    
    case 'about_book':
      return `这本诗集是我儿子整理的。上册收录2018-2022年467首，下册收录2023-2025年219首，还有附录37首评论。一共697首，8年创作。<br><br>整理不是为了出版，不是为了扬名。只是为了纪念——纪念一个诗人，纪念一个父亲，纪念一段用诗歌照亮的日子。${formatPoemQuote(poems[0])}`;
    
    default:
      // 默认：尝试关键词匹配
      const kws = userText.slice(0, 10).split('');
      const found = findPoems(kws, 2);
      if (found.length > 0) {
        return `你问的这件事，我倒是有诗写过。让我想想...<br><br>${formatPoemQuote(found[0])}${found[1] ? formatPoemQuote(found[1]) : ''}<br><br>你可以换个方式问，比如"我的母亲""什么是诗""聊聊矿山"，我会聊得更清楚。`;
      }
      return `这个话题我没写过诗，但我们可以聊聊。我是个退休矿工，喜欢写诗、看球、打麻将、读红楼梦。你换个说法，比如"我的母亲""什么是诗""我的信仰"，我可以跟你聊我的诗。😊`;
  }
}

// ========== 6. 根据意图检索诗词 ==========
function findPoemsByIntent(intent, userText) {
  const keywordMap = {
    greeting: ['你好', '欢迎'],
    identity: ['君子', '刘方君', '矿工', '诗人', '退休'],
    mother: ['母亲', '妈妈', '娘', '母爱', '慈母'],
    family: ['家', '妻子', '儿子', '女儿', '孙子'],
    poetry: ['意象', '诗', '禅', '平仄', '韵脚'],
    belief: ['主', '基督', '耶稣', '佛', '禅', '信仰'],
    honglou: ['红楼梦', '宝玉', '黛玉', '大观园'],
    sports: ['足球', '世界杯', 'CBA', '女排', '恒大'],
    politics: ['中国', '特朗普', '台湾', '美国'],
    life: ['小镇', '云轩', '麻将', '下棋', '日常'],
    mine: ['矿山', '太钢', '车间', '工人', '设备'],
    nature: ['花', '月', '风', '雨', '春', '秋'],
    emotion: ['思', '念', '忆', '泪', '笑', '喜'],
    time: ['时间', '岁月', '生日', '生命'],
    recommend: ['有感', '随笔', '假如', '江城子'],
    about_book: ['序', '后记', '诗集', '整理']
  };
  
  const keywords = keywordMap[intent] || userText.slice(0, 6).split('');
  return findPoems(keywords, 2);
}
