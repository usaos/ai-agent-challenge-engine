import argparse
import sys
import json
from rethink_core import ReThinkEngine, MistakeArchive
from rethink_report import generate_facepalm_report

def main():
    parser = argparse.ArgumentParser(description="ReThink: 给 AI 戴上痛苦面具的元认知引擎")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 1. grill 命令 (核心拷问)
    grill_parser = subparsers.add_parser("grill", help="对 AI 的回答进行苏格拉底式追问")
    grill_parser.add_argument("-q", "--query", required=True, help="用户的原始问题")
    grill_parser.add_argument("-r", "--response", required=True, help="AI 的初始回答")
    grill_parser.add_argument("--model", default="gpt-4o-mini", help="使用的 LLM 模型 (默认: gpt-4o-mini)")

    # 2. history 命令 (查看错误档案)
    subparsers.add_parser("history", help="查看 AI 的历史翻车档案")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    archive = MistakeArchive()

    if args.command == "grill":
        print(f"🔍 正在启动 ReThink 引擎 (模型: {args.model})...")
        try:
            engine = ReThinkEngine(model=args.model)
        except ValueError as e:
            print(f"❌ 错误: {e}")
            sys.exit(1)

        print("⏳ 正在提取隐含假设并生成灵魂拷问...")
        result = engine.grill(args.query, args.response)
        
        # 记录到本地档案
        archive.record(args.query, result)

        # 终端输出摘要
        print("\n" + "="*50)
        if result.is_flawed:
            print("🤡 判定结果：AI 当场翻车！")
        else:
            print("🧠 判定结果：AI 逻辑严密，守住尊严。")
        
        print("\n⚔️ 苏格拉底追问：")
        for i, q in enumerate(result.socratic_questions, 1):
            print(f"  {i}. {q}")
        print("="*50 + "\n")

        # 生成 HTML 报告
        print("📄 正在生成打脸报告...")
        report_path = generate_facepalm_report(args.query, result)
        print(f"✅ 报告已在浏览器中打开: {report_path}")

    elif args.command == "history":
        print("📚 AI 历史翻车档案 (最近 5 条):")
        print("-" * 50)
        records = archive.get_history()
        if not records:
            print("暂无记录。你的 AI 还没被拷问过。")
        for q, assumptions, time in records:
            print(f"时间: {time}")
            print(f"问题: {q}")
            print(f"致命假设: {assumptions}")
            print("-" * 50)

if __name__ == "__main__":
    main()
