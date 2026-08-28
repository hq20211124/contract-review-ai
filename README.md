# ⚖️ AI 合同审查工具

基于 DeepSeek 大模型的智能合同风险审查工具，支持文本粘贴和文件上传，自动识别合同风险条款并给出修改建议。

> **本工具仅供参考，不构成法律意见。重要合同请咨询专业律师。**

## ✨ 功能特性

- **🔍 智能风险识别**：自动识别违约责任、争议解决、知识产权、保密条款、付款条款等高风险条款
- **📊 风险分级**：高/中/低三级风险标注，一目了然
- **💬 大白话解释**：用普通人能听懂的语言解释法律条款
- **✅ 修改建议**：每条风险都给出具体可操作的修改建议，甚至提供可直接替换的条款文本
- **📝 双输入方式**：支持粘贴文本和上传 .txt 文件
- **🎯 多合同类型**：支持服务合同、劳动合同、买卖合同、租赁合同、保密协议、合作协议等
- **🔒 隐私安全**：数据仅用于本次审查，不存储，不上传第三方（除 DeepSeek API）

## 📸 效果展示

以下是对一份**软件开发服务合同**的实际审查结果（完整示例见 `examples/sample-contract.txt`）：

**审查概览**：合同类型「软件开发服务合同」| 整体风险「🔴 高」| 高风险 9 项 | 中风险 5 项 | 低风险 3 项

### 典型风险识别示例

**🔴 高风险：验收标准甲方单方说了算**

> 原文：「如甲方认为项目未达到验收标准，有权拒绝支付任何费用，且乙方不得提出异议。」

**大白话**：甲方说不合格就不合格，说不给钱就不给钱，乙方连反对的权利都没有。

**风险**：甲方可以故意挑刺不验收，赖掉全部款项。「不得提出异议」剥夺乙方基本权利，虽可能因显失公平被撤销，但打官司耗时耗力。

**修改建议**：
> 验收标准以双方书面确认的《需求文档》为准。甲方应在收到交付物后 10 个工作日内完成验收并出具书面意见。逾期未提出书面异议的，视为验收合格。

---

**🔴 高风险：逾期违约金每日 5%（年化 1825%）**

> 原文：「乙方逾期交付的，每逾期一日，应向甲方支付项目总费用 5% 的违约金。」

**大白话**：晚一天交付赔 2500 元（5 万的 5%），晚 20 天赔完整个项目款。

**风险**：年化利率 1825%，远超法律保护上限（LPR 4 倍约 13.8%）。法院大概率会调低，但甲方可用此条款施压。

**修改建议**：
> 乙方逾期交付的，每逾期一日支付项目总费用 0.5‰ 的违约金（每日 25 元），累计不超过项目总费用的 20%。

---

**🔴 高风险：乙方已有技术被甲方无偿占有**

> 原文：「乙方在开发过程中使用的任何已有技术、代码、工具、框架，均视为乙方无偿授权甲方永久使用。」

**大白话**：乙方以前写的代码、用的开源框架、积累的工具，全部白送给甲方。

**风险**：范围极宽。React、Vue、Spring 等开源框架，乙方多年积累的代码库，都被「无偿授权」。甲方可拿着乙方代码库做别的项目。

**修改建议**：
> 项目定制开发的代码归甲方所有。开源组件、通用工具类、自有技术框架的知识产权归原作者或乙方所有，甲方获得在本项目中的使用权。

---

**🟡 中风险：违约金严重不对等**

> 原文：乙方逾期每日 5% vs 甲方逾期付款按「银行同期活期存款利率」（约 0.2%/年）

**风险**：相差 9000 倍。甲方可以放心拖欠款项，几乎没有成本。

**修改建议**：甲方逾期付款的，每逾期一日按应付未付金额的 0.5‰ 支付违约金，与乙方违约责任对等。

---

> 以上仅为部分展示，完整审查包含 17 个风险点的详细分析和修改建议。

## 🚀 快速开始

### 环境要求

- Python 3.9+
- DeepSeek API Key（[免费申请](https://platform.deepseek.com/)）

### 安装步骤

**1. 克隆项目**

```bash
git clone https://github.com/hq20211124/contract-review-ai.git
cd contract-review-ai
```

**2. 安装依赖**

```bash
pip install -r requirements.txt
```

**3. 配置 API Key**

复制 `.env.example` 为 `.env`，填入你的 DeepSeek API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

**4. 启动服务**

```bash
# Windows 双击运行
run.bat

# 或命令行启动
python app.py
```

**5. 访问应用**

打开浏览器访问：http://localhost:8000

## 📖 使用说明

1. 选择输入方式（粘贴文本 / 上传文件）
2. 输入或上传合同内容（建议 50-20000 字）
3. 点击「开始审查」
4. 等待 10-30 秒（合同越长耗时越久）
5. 查看审查结果：
   - 概览：合同类型、整体风险等级、风险数量统计
   - 风险列表：按高/中/低排序，每条包含原文摘录、大白话解释、风险说明、修改建议
   - 关键建议：AI 给出的核心注意事项

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + Python 3.9+ |
| AI 模型 | DeepSeek Chat（deepseek-chat） |
| 前端 | 原生 HTML + CSS + JavaScript（无框架依赖） |
| 部署 | Uvicorn（可部署到任意支持 Python 的服务器） |

## 📁 项目结构

```
contract-review-ai/
├── app.py                  # 主应用（FastAPI 后端 + API 路由）
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量示例
├── run.bat                 # Windows 启动脚本
├── templates/
│   └── index.html          # 前端页面
├── static/
│   └── style.css           # 样式文件
└── examples/
    └── sample-contract.txt # 测试用示例合同
```

## 🌐 部署指南

### 本地运行

```bash
python app.py
```

### 服务器部署（以 Ubuntu 为例）

```bash
# 1. 安装 Python 3.9+
sudo apt update && sudo apt install python3 python3-pip

# 2. 克隆项目并安装依赖
git clone https://github.com/hq20211124/contract-review-ai.git
cd contract-review-ai
pip3 install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env 填入 API Key

# 4. 使用 systemd 后台运行
sudo nano /etc/systemd/system/contract-review.service
```

service 文件内容：

```ini
[Unit]
Description=AI Contract Review Tool
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/contract-review-ai
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable contract-review
sudo systemctl start contract-review
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "app.py"]
```

```bash
docker build -t contract-review .
docker run -d -p 8000:8000 -e DEEPSEEK_API_KEY=your_key contract-review
```

## 💼 定制开发服务

本项目为开源演示版本。如果你或你的企业需要以下服务，欢迎联系：

| 服务类型 | 说明 | 参考价格 |
|---------|------|---------|
| **私有化部署** | 部署到你的服务器，支持内网环境，数据完全自控 | ¥3,000 起 |
| **企业定制版** | 对接企业知识库、OA系统、合同管理系统，支持批量审查 | ¥10,000 起 |
| **垂直行业版** | 针对特定行业（电商/医疗/教育/建筑等）优化审查模型和条款库 | 面议 |
| **AI 工具定制** | 其他 AI 应用开发（智能客服、知识库问答、数据自动化等） | 面议 |

**服务流程**：需求沟通 → 方案报价 → 付定金 → 开发交付 → 验收尾款 → 1 个月免费维护

联系方式：见下方「📮 联系方式」

---

## ⚠️ 免责声明

1. 本工具由 AI 生成审查结果，**仅供参考，不构成法律意见**
2. 审查结果可能存在遗漏或错误，**重要合同请务必咨询专业律师**
3. 本工具不对因使用审查结果导致的任何损失承担责任
4. 用户上传的合同内容仅用于本次审查，通过 DeepSeek API 处理，开发者不存储用户数据

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- GitHub Issues
- Email: your-email@example.com

---

**如果这个工具对你有帮助，欢迎给个 Star ⭐**
