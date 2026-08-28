"""
AI 合同审查工具 - 后端服务
基于 DeepSeek API 的合同风险审查与修改建议生成
"""

import os
import json
import re
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx

# 加载环境变量
load_dotenv()

# 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="AI 合同审查工具", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ============================================================
# 数据模型
# ============================================================

class RiskItem(BaseModel):
    """单条风险项"""
    clause_type: str          # 条款类型
    risk_level: str           # 风险等级：高/中/低
    original_text: str        # 原文摘录
    plain_explanation: str    # 大白话解释
    risk_description: str     # 风险说明
    suggestion: str           # 修改建议


class ReviewResult(BaseModel):
    """审查结果"""
    contract_type: str                    # 合同类型
    summary: str                          # 总体评价
    overall_risk_level: str               # 整体风险等级
    risk_items: List[RiskItem]            # 风险项列表
    high_risk_count: int                  # 高风险数量
    medium_risk_count: int                # 中风险数量
    low_risk_count: int                   # 低风险数量
    key_advice: List[str]                 # 关键建议


# ============================================================
# 核心 Prompt 设计
# ============================================================

SYSTEM_PROMPT = """你是一位拥有15年执业经验的资深合同审查律师，精通《中华人民共和国民法典》合同编、《公司法》、《劳动法》等相关法律法规。

你的职责是对用户提供的合同进行专业、细致的风险审查，并给出：
1. 合同类型判断
2. 逐条风险识别（标注条款类型、风险等级）
3. 每条风险的大白话解释（让非法律专业人士也能看懂）
4. 具体的修改建议（给出可直接替换的条款文本）

审查重点关注以下高风险条款类型：
- 违约责任条款（违约金是否过高/过低、责任范围是否对等）
- 争议解决条款（管辖法院、仲裁机构、适用法律）
- 知识产权条款（归属、授权范围、侵权责任）
- 保密条款（范围、期限、违约责任）
- 付款条款（金额、时间、方式、发票、逾期责任）
- 期限与终止条款（合同期限、解除条件、终止后义务）
- 不可抗力条款（范围、通知义务、责任免除）
- 保证与担保条款
- 竞业限制条款
- 数据与个人信息保护条款
- 免责条款（是否显失公平、是否免除主要责任）
- 合同主体与签署条款（主体资格、授权代表、生效条件）

风险等级判定标准：
- 高风险：可能导致重大经济损失、合同无效、承担法律责任、丧失主要权利
- 中风险：可能导致经济损失、权利受限、履行困难，但有补救空间
- 低风险：表述不严谨、条款不完整、潜在争议，但影响较小

输出要求：
- 必须以严格的 JSON 格式输出，不要输出任何 JSON 之外的文字
- JSON 结构必须与给定的 schema 完全一致
- 风险项要具体，不要泛泛而谈
- 修改建议要可操作，最好给出具体的条款文本
- 如果合同文本过短或无法识别，如实说明，不要编造"""


def build_user_prompt(contract_text: str) -> str:
    """构建用户提示词"""
    return f"""请审查以下合同文本，进行专业的风险分析。

合同文本：
\"\"\"
{contract_text}
\"\"\"

请以 JSON 格式输出审查结果，结构如下：
{{
  "contract_type": "合同类型（如：服务合同、劳动合同、买卖合同、租赁合同、保密协议等）",
  "summary": "总体评价（200字以内，概括合同主要内容和整体风险状况）",
  "overall_risk_level": "整体风险等级（高/中/低）",
  "risk_items": [
    {{
      "clause_type": "条款类型",
      "risk_level": "高/中/低",
      "original_text": "原文摘录（从合同中摘录相关原文，不超过100字）",
      "plain_explanation": "大白话解释（用普通人能听懂的话解释这条在说什么）",
      "risk_description": "风险说明（这条有什么问题，可能导致什么后果）",
      "suggestion": "修改建议（具体怎么改，最好给出可直接替换的条款文本）"
    }}
  ],
  "key_advice": ["关键建议1", "关键建议2", "关键建议3"]
}}

注意：
1. 至少识别 5 条风险项，最多 15 条
2. 优先识别高风险和中风险条款
3. 如果某类条款不存在，不要编造
4. original_text 必须是合同中真实存在的文本
5. 输出必须是合法的 JSON，不要有注释、不要有 markdown 代码块标记"""


# ============================================================
# DeepSeek API 调用
# ============================================================

async def call_deepseek(prompt: str, temperature: float = 0.1) -> str:
    """调用 DeepSeek API"""
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="未配置 DEEPSEEK_API_KEY，请在 .env 文件中配置你的 DeepSeek API Key"
        )

    url = f"{DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 4000,
        "response_format": {"type": "json_object"}
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if e.response else str(e)
            raise HTTPException(
                status_code=502,
                detail=f"DeepSeek API 调用失败: {error_detail}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"网络请求失败: {str(e)}"
            )


def parse_review_result(raw_json: str) -> ReviewResult:
    """解析 API 返回的 JSON，处理可能的格式问题"""
    try:
        # 尝试直接解析
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        # 尝试提取 JSON 部分
        json_match = re.search(r'\{[\s\S]*\}', raw_json)
        if json_match:
            try:
                data = json.loads(json_match.group())
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="API 返回的 JSON 格式无法解析")
        else:
            raise HTTPException(status_code=500, detail="API 未返回有效的 JSON 数据")

    # 构建风险项列表
    risk_items = []
    for item in data.get("risk_items", []):
        risk_items.append(RiskItem(
            clause_type=item.get("clause_type", "未分类"),
            risk_level=item.get("risk_level", "低"),
            original_text=item.get("original_text", ""),
            plain_explanation=item.get("plain_explanation", ""),
            risk_description=item.get("risk_description", ""),
            suggestion=item.get("suggestion", "")
        ))

    # 统计风险数量
    high_count = sum(1 for r in risk_items if r.risk_level == "高")
    medium_count = sum(1 for r in risk_items if r.risk_level == "中")
    low_count = sum(1 for r in risk_items if r.risk_level == "低")

    return ReviewResult(
        contract_type=data.get("contract_type", "未识别"),
        summary=data.get("summary", ""),
        overall_risk_level=data.get("overall_risk_level", "中"),
        risk_items=risk_items,
        high_risk_count=high_count,
        medium_risk_count=medium_count,
        low_risk_count=low_count,
        key_advice=data.get("key_advice", [])
    )


# ============================================================
# 路由
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """首页"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/review", response_model=ReviewResult)
async def review_contract(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """审查合同接口"""
    # 获取合同文本
    contract_text = ""

    if file and file.filename:
        # 从上传文件读取
        content = await file.read()
        try:
            contract_text = content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                contract_text = content.decode("gbk")
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="文件编码不支持，请使用 UTF-8 或 GBK 编码的文本文件")
    elif text:
        contract_text = text
    else:
        raise HTTPException(status_code=400, detail="请提供合同文本（粘贴或上传 .txt 文件）")

    # 文本长度检查
    contract_text = contract_text.strip()
    if len(contract_text) < 50:
        raise HTTPException(status_code=400, detail="合同文本过短，请提供完整的合同内容（至少50字）")
    if len(contract_text) > 20000:
        raise HTTPException(status_code=400, detail="合同文本过长（超过20000字），请精简后再试")

    # 调用 DeepSeek 审查
    prompt = build_user_prompt(contract_text)
    raw_result = await call_deepseek(prompt)

    # 解析结果
    result = parse_review_result(raw_result)

    return result


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "api_key_configured": bool(DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your_api_key_here"),
        "model": DEEPSEEK_MODEL
    }


# ============================================================
# 启动
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 AI 合同审查工具启动中...")
    print(f"📡 访问地址: http://localhost:{PORT}")
    print(f"🔑 API Key 已配置: {'是' if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != 'your_api_key_here' else '否（请在 .env 中配置）'}")
    uvicorn.run(app, host=HOST, port=PORT)
