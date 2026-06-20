import os
import sqlite3
import json
from typing import List, Optional
from pydantic import BaseModel, Field

try:
    import instructor
    from openai import OpenAI
except ImportError:
    raise ImportError("请先运行: pip install -r requirements.txt")

# --- 1. 数据结构定义 ---
class ReflectionResult(BaseModel):
    original_answer: str = Field(description="AI最初的回答原文")
    hidden_assumptions: List[str] = Field(description="回答中隐含的、未经验证的 2-3 个前提假设")
    socratic_questions: List[str] = Field(description="针对假设提出的 2 个尖锐的反事实/苏格拉底式追问")
    is_flawed: bool = Field(description="经过追问后，判断原始回答是否存在逻辑缺陷、幻觉或过度顺从")
    corrected_answer: Optional[str] = Field(description="如果有缺陷，修正后的最终答案；如果没有，填 None")
    confidence_score: int = Field(ge=1, le=10, description="修正后答案的置信度(1-10)")

# --- 2. 核心反思引擎 ---
class ReThinkEngine:
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("未找到 OPENAI_API_KEY 环境变量。请设置后重试。")
        
        # 使用 instructor 强制 LLM 输出符合 Pydantic 结构的 JSON
        self.client = instructor.from_openai(OpenAI(api_key=api_key))
        self.model = model

    def grill(self, user_query: str, ai_response: str) -> ReflectionResult:
        prompt = f"""你是一位严苛的逻辑学教授和苏格拉底式导师。
        用户提出了问题："{user_query}"
        AI 给出了初步回答："{ai_response}"
        
        你的任务是审视 AI 的回答：
        1. 找出 AI 回答中隐藏的、可能不成立的前提假设（特别是过度顺从用户、虚假权威或因果倒置）。
        2. 提出尖锐的反事实问题来攻击这些假设。
        3. 判定 AI 的初始回答是否存在逻辑漏洞或幻觉。
        4. 如果有缺陷，给出修正后更严谨的答案。
        """
        
        return self.client.chat.completions.create(
            model=self.model,
            response_model=ReflectionResult,
            messages=[{"role": "user", "content": prompt}],
        )

# --- 3. 极简本地记忆库 (SQLite) ---
class MistakeArchive:
    def __init__(self, db_path: str = "rethink_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT, 
                assumptions TEXT, 
                correction TEXT, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        
    def record(self, query: str, result: ReflectionResult):
        if result.is_flawed:
            self.conn.execute(
                "INSERT INTO mistakes (query, assumptions, correction) VALUES (?, ?, ?)",
                (query, json.dumps(result.hidden_assumptions, ensure_ascii=False), result.corrected_answer)
            )
            self.conn.commit()
            
    def get_history(self, limit: int = 5) -> list:
        cursor = self.conn.execute(
            "SELECT query, assumptions, created_at FROM mistakes ORDER BY created_at DESC LIMIT ?", 
            (limit,)
        )
        return cursor.fetchall()
