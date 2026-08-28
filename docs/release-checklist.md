# 发布检查清单

## 发布前（今天）

- [ ] 1. 本地跑通测试
  - [ ] 配置 .env 里的 DEEPSEEK_API_KEY
  - [ ] 双击 run.bat 启动
  - [ ] 浏览器打开 http://localhost:8000
  - [ ] 用 examples/sample-contract.txt 测试，确认审查结果正常
  - [ ] 测试文件上传功能
  - [ ] 测试错误处理（空文本、过长文本、无效API Key）

- [ ] 2. 代码检查
  - [ ] 确认没有硬编码的 API Key
  - [ ] 确认 .env 在 .gitignore 里（如果没有，创建 .gitignore）
  - [ ] 确认 README 里的链接和说明正确

- [ ] 3. 创建 .gitignore
  ```
  .env
  __pycache__/
  *.pyc
  .venv/
  venv/
  *.log
  .DS_Store
  ```

## 发布到 GitHub（第2天）

- [ ] 1. 注册/登录 GitHub
- [ ] 2. 创建新仓库，名字：contract-review-ai
- [ ] 3. 推送代码：
  ```bash
  cd contract-review-ai
  git init
  git add .
  git commit -m "feat: initial release - AI contract review tool"
  git branch -M main
  git remote add origin https://github.com/你的用户名/contract-review-ai.git
  git push -u origin main
  ```
- [ ] 4. 检查 GitHub 页面：
  - [ ] README 渲染正常
  - [ ] 所有文件都在
  - [ ] About 区域填写描述和标签（AI、contract-review、deepseek、fastapi）

## 推广发布（第3-4天）

- [ ] 1. 替换推广文案里的占位符
  - [ ] docs/v2ex-post.md 里的 hq20211124 替换成真实用户名
  - [ ] docs/juejin-post.md 里的 hq20211124 替换成真实用户名
  - [ ] README.md 里的 hq20211124 替换成真实用户名

- [ ] 2. V2EX 发帖
  - [ ] 节点：分享创造 或 程序员
  - [ ] 标题：做了个 AI 合同审查工具，开源了，帮你识别合同里的坑
  - [ ] 正文：docs/v2ex-post.md
  - [ ] 发帖后关注评论，及时回复

- [ ] 3. 掘金发文
  - [ ] 分类：后端 / Python / AI
  - [ ] 标题：我用 DeepSeek API 做了个 AI 合同审查工具，帮你避开合同里的坑（附完整实现）
  - [ ] 正文：docs/juejin-post.md
  - [ ] 标签：AI、DeepSeek、合同审查、FastAPI、Python、开源

- [ ] 4. 其他渠道（可选）
  - [ ] 朋友圈转发 GitHub 链接
  - [ ] 知乎回答相关问题（"有什么好用的合同审查工具"）
  - [ ] 小红书/公众号（如果有账号）

## 发布后（第1-2周）

- [ ] 1. 监控数据
  - [ ] GitHub Stars 数量
  - [ ] V2EX 帖子回复数
  - 掘金文章阅读量/点赞数
  - [ ] GitHub Issues 数量

- [ ] 2. 收集反馈
  - [ ] 有没有人说"这个功能我需要"
  - [ ] 有没有人问"能不能付费/能不能定制"
  - [ ] 有没有人提 Bug 或功能建议

- [ ] 3. 迭代优化
  - [ ] 修复反馈的 Bug
  - [ ] 加大家都在要的功能
  - [ ] 优化审查质量（调整 Prompt）

## 成功标准（2周后评估）

- [ ] GitHub Stars ≥ 100
- [ ] 收到 ≥ 3 个"能不能定制/能不能付费"的咨询
- [ ] V2EX 帖子回复 ≥ 20
- [ ] 掘金文章阅读 ≥ 1000

如果达到：说明需求验证成功，可以考虑做付费版/接定制单
如果没达到：分析原因（产品不行？渠道不对？文案不好？），调整方向
