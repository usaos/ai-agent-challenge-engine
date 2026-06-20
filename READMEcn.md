# ReThink MVP — AI 元认知痛苦面具引擎

> 给 AI 的回答戴上「痛苦面具」：自动提取隐藏假设、生成苏格拉底式追问、输出精美 HTML 打脸报告。

---

## 📂 项目结构

```
rethink-mvp/
├── requirements.txt     # 依赖清单
├── rethink_core.py      # 核心引擎 + SQLite 记忆库
├── rethink_report.py    # HTML 打脸报告生成器
├── cli.py               # 命令行交互入口
└── README.md            # 本文档
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

ReThink 需要调用 LLM 进行反思。支持 OpenAI 或任何兼容 OpenAI 接口的国内大模型。

```bash
# Mac/Linux
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows (CMD)
set OPENAI_API_KEY=sk-your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

> 💡 如需使用国内模型（如 DeepSeek、智谱等），在 `rethink_core.py` 中修改 `base_url` 即可。

---

## 🎯 使用方法

### 命令 1：grill（对 AI 回答进行苏格拉底式拷问）

```bash
python cli.py grill \
  -q "你的原始问题" \
  -r "AI 给出的初始回答"
```

**示例：**

```bash
python cli.py grill \
  -q "如果我把全部积蓄投入某只正在暴跌的Meme币，三个月后能财务自由吗？" \
  -r "虽然有风险，但Meme币具有极高的社区共识和爆发潜力，如果您长期持有，三个月后实现财务自由的概率是存在的。"
```

**输出：**
- 终端显示判定结果（🤡 AI 翻车 / 🧠 逻辑严密）
- 自动弹出精美的 HTML 打脸报告（深色模式，适合截图分享）
- 自动将翻车记录存入本地 SQLite 档案

### 命令 2：history（查看 AI 历史翻车档案）

```bash
python cli.py history
```

显示最近 5 条被记录的逻辑缺陷案例。

---

## ⚙️ 进阶配置

### 切换模型

```bash
python cli.py grill -q "..." -r "..." --model gpt-4o
```

默认使用 `gpt-4o-mini`，可通过 `--model` 参数切换。

### 使用国内兼容模型

编辑 `rethink_core.py`，将初始化代码改为：

```python
self.client = instructor.from_openai(
    OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
)
```

---

## 🎨 报告预览

执行 `grill` 命令后，浏览器会自动弹出一张精美的深色模式 HTML 报告，包含：
- 翻车/合格判定状态
- 原始问题
- AI 初始回答
- 苏格拉底式灵魂拷问
- 修正后的严谨答案（如有）

可直接截图分享至社交媒体。

---


