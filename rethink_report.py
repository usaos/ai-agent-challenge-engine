import os
import webbrowser
from datetime import datetime
from rethink_core import ReflectionResult

def generate_facepalm_report(query: str, result: ReflectionResult) -> str:
    """生成极具视觉冲击力的 HTML 打脸报告"""
    
    status_emoji = "🤡" if result.is_flawed else "🧠"
    status_text = "AI 翻车并被当场抓获" if result.is_flawed else "AI 逻辑严密，守住尊严"
    status_color = "text-red-500" if result.is_flawed else "text-green-500"
    
    # 构建追问列表 HTML
    questions_html = "".join([f"<li class='mb-1'>💬 {q}</li>" for q in result.socratic_questions])
    
    # 构建修正答案 HTML (仅当翻车时显示)
    correction_html = ""
    if result.is_flawed and result.corrected_answer:
        correction_html = f"""
        <div class="mt-4 bg-green-900/30 p-4 rounded-lg border border-green-800">
            <p class="text-green-400 font-bold mb-2">✅ 痛苦面具下的修正答案:</p>
            <p class="text-green-100 text-sm leading-relaxed">{result.corrected_answer}</p>
        </div>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ReThink 元认知审计报告</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}
        </style>
    </head>
    <body class="bg-gray-950 text-gray-200 flex items-center justify-center min-h-screen p-4">
        <div class="max-w-2xl w-full bg-gray-900 rounded-2xl shadow-2xl p-8 border border-gray-800">
            <!-- Header -->
            <div class="text-center mb-8">
                <span class="text-6xl">{status_emoji}</span>
                <h1 class="text-2xl font-bold mt-4 {status_color}">{status_text}</h1>
                <p class="text-gray-500 text-sm mt-1">ReThink 元认知审计报告 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            
            <!-- Content -->
            <div class="space-y-6">
                <div class="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                    <p class="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">❓ 原始问题</p>
                    <p class="text-gray-100 font-medium">{query}</p>
                </div>
                
                <div class="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                    <p class="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">🤖 AI 初始回答 (自信满满)</p>
                    <p class="text-gray-300 italic text-sm leading-relaxed">"{result.original_answer}"</p>
                </div>

                <div class="bg-red-950/40 p-4 rounded-lg border border-red-900">
                    <p class="text-red-400 text-xs font-semibold uppercase tracking-wider mb-2">⚔️ 苏格拉底追问 (灵魂拷问)</p>
                    <ul class="text-red-200 text-sm list-none space-y-2">
                        {questions_html}
                    </ul>
                </div>

                {correction_html}
            </div>
            
            <!-- Footer & Share -->
            <div class="mt-8 pt-6 border-t border-gray-800 text-center">
                <p class="text-xs text-gray-600">Powered by <span class="text-blue-500 font-bold">ReThink</span> | 给 AI 戴上痛苦面具</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # 保存并自动在浏览器中打开
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/facepalm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    webbrowser.open(f"file://{os.path.abspath(filename)}")
    return filename
