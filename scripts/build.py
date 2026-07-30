#!/usr/bin/env python3
"""由 SKILL.md + references/ 生成各平台适配文件。

单一事实源是 SKILL.md 和 references/*.md。其余四个产物全部由本脚本生成：

    AGENTS.md                             Codex / Antigravity / 通用约定
    .cursor/rules/quick-learn-everything.mdc   Cursor 规则
    dist/PROMPT.md                        ChatGPT / WorkBuddy，粘贴进对话开头
    dist/PROMPT-compact.md                Custom GPT 指令框（≤8000 字符硬上限）

用法:
    python scripts/build.py            重新生成全部产物
    python scripts/build.py --check    校验产物与源一致（不一致则非零退出）
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Custom GPT 的指令框上限。超了不静默截断，直接报错。
COMPACT_CHAR_LIMIT = 8000

GENERATED_BANNER = (
    "本文件由 scripts/build.py 自动生成，请勿手动编辑。\n"
    "修改请改 SKILL.md 或 references/ 下的源文件，然后运行 `python scripts/build.py`。"
)

# 内联进自包含产物的参考文件，顺序即附录顺序。
REFERENCE_FILES = [
    "references/method.md",
    "references/source-quality.md",
    "references/prompts.md",
]

TEMPLATE_FILES = [
    "references/templates/learning-plan.md",
    "references/templates/glossary.md",
    "references/templates/sources.md",
    "references/templates/quiz.md",
    "references/templates/progress.md",
]

COMPACT_SKIP_RE = re.compile(
    r"[ \t]*<!--\s*compact:skip\s*-->.*?<!--\s*/compact:skip\s*-->[ \t]*\n?",
    re.DOTALL,
)
# 参考文件中标记为「精简版也要带上」的段落。
COMPACT_INCLUDE_RE = re.compile(
    r"<!--\s*compact:include\s*-->\n?(.*?)<!--\s*/compact:include\s*-->",
    re.DOTALL,
)
COMPACT_MARKER_RE = re.compile(
    r"[ \t]*<!--\s*/?compact:(?:skip|include)\s*-->[ \t]*\n?"
)


class BuildError(Exception):
    """构建失败，附带给人看的原因。"""


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise BuildError(f"缺少源文件：{rel}")
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """拆出 SKILL.md 的 YAML frontmatter 与正文。

    只解析顶层 `key: value`（支持折行续写），够用且不引入 PyYAML 依赖。
    """
    if not text.startswith("---\n"):
        raise BuildError("SKILL.md 必须以 YAML frontmatter (`---`) 开头")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise BuildError("SKILL.md 的 frontmatter 没有闭合的 `---`")

    fields: dict[str, str] = {}
    key = None
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match and not line.startswith((" ", "\t")):
            key, value = match.group(1), match.group(2).strip()
            fields[key] = value
        elif key:  # 折行续写
            fields[key] = f"{fields[key]} {line.strip()}".strip()

    for required in ("name", "description"):
        if not fields.get(required):
            raise BuildError(f"SKILL.md frontmatter 缺少 `{required}`")

    return fields, text[end + 5 :].lstrip("\n")


def strip_compact_markers(body: str) -> str:
    """去掉标记本身，保留被包裹的内容（用于全量产物）。"""
    return COMPACT_MARKER_RE.sub("", body)


def apply_compact(body: str) -> str:
    """删掉 compact:skip 包裹的整段（用于 compact 产物）。"""
    return COMPACT_SKIP_RE.sub("", body)


def demote_headings(text: str, levels: int = 1) -> str:
    """把 Markdown 标题降级，避免内联附录时抢占顶层结构。

    跳过 ``` 围栏代码块内的内容。
    """
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and (m := re.match(r"^(#{1,6})(\s)", line)):
            line = "#" * min(len(m.group(1)) + levels, 6) + line[len(m.group(1)) :]
        out.append(line)
    return "\n".join(out)


def strip_title(text: str) -> str:
    """去掉文件开头的 H1，标题由内联时的附录标题接管。"""
    return re.sub(r"\A#\s+.*\n+", "", text, count=1)


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def build_appendix(rel_paths: list[str], start_index: int = 0) -> tuple[str, int]:
    """把参考文件内联成附录小节。返回 (文本, 下一个可用序号)。"""
    parts = []
    for offset, rel in enumerate(rel_paths):
        letter = LETTERS[start_index + offset]
        content = demote_headings(strip_compact_markers(strip_title(read(rel))).strip())
        parts.append(f"## 附录 {letter}：{rel}\n\n{content}")
    return "\n\n---\n\n".join(parts), start_index + len(rel_paths)


def assert_no_dangling_refs(text: str, label: str) -> None:
    """自包含产物里不能残留指向仓库文件的引用——粘贴进 ChatGPT 后会指向虚空。

    只查带反引号的路径引用；附录标题里的裸路径是在说明来源，不是让 agent 去读。
    """
    dangling = re.findall(r"`(references/[^`]+)`", text)
    if dangling:
        raise BuildError(
            f"{label} 残留了 {len(dangling)} 处仓库路径引用：{sorted(set(dangling))}\n"
            f"自包含产物不能指向仓库文件。请在 build.py 的重写映射里处理它们，"
            f"或用 <!-- compact:skip --> 包裹相关段落。"
        )


def rewrite_ref_links(text: str, target: dict[str, str]) -> str:
    """把正文里的 `references/xxx.md` 换成产物内部的位置说明。

    行内代码前后惯例留空格，替换成中文短语后那个空格就多余了——紧跟中文字符时吃掉它。
    """
    for rel, replacement in target.items():
        text = re.sub(
            rf"(?<=[一-鿿]) `{re.escape(rel)}`", replacement, text
        )
        text = text.replace(f"`{rel}`", replacement)
    return text


def self_contained_body(body: str) -> str:
    """SKILL.md 正文 + 全部参考文件内联，无任何指向仓库路径的悬空引用。"""
    core = strip_compact_markers(body).strip()
    core = core.replace(
        "## 按需加载",
        "## 参考资料位置\n\n本文件是自包含的：下面提到的所有参考内容都已内联在文末附录中。",
        1,
    )
    first_tpl = LETTERS[len(REFERENCE_FILES)]
    last_tpl = LETTERS[len(REFERENCE_FILES) + len(TEMPLATE_FILES) - 1]
    core = rewrite_ref_links(
        core,
        {
            **{rel: f"文末附录 {LETTERS[i]}" for i, rel in enumerate(REFERENCE_FILES)},
            "references/templates/*.md": f"文末附录 {first_tpl}–{last_tpl}",
        },
    )
    refs, next_idx = build_appendix(REFERENCE_FILES)
    templates, _ = build_appendix(TEMPLATE_FILES, next_idx)
    text = (
        f"{core}\n\n---\n\n# 附录\n\n"
        f"以下内容原本是独立的参考文件，为便于单文件分发已内联于此。\n\n"
        f"{refs}\n\n---\n\n{templates}\n"
    )
    assert_no_dangling_refs(text, "自包含产物")
    return text


def compact_includes() -> str:
    """收集参考文件中标记为 compact:include 的段落，供精简版内联。"""
    blocks = []
    for rel in REFERENCE_FILES:
        for match in COMPACT_INCLUDE_RE.finditer(read(rel)):
            blocks.append(demote_headings(match.group(1).strip()))
    return "\n\n".join(blocks)


def build_agents_md(fields: dict[str, str], body: str) -> str:
    return (
        f"<!-- {GENERATED_BANNER} -->\n\n"
        f"# AGENTS.md · {fields['name']}\n\n"
        f"> **何时启用本指令**：{fields['description']}\n\n"
        f"> 面向遵循 AGENTS.md 约定的 agent（Codex、Antigravity 等）。"
        f"内容与 `SKILL.md` 完全一致，已内联全部参考资料。\n\n"
        f"---\n\n{self_contained_body(body)}"
    )


def build_cursor_rule(fields: dict[str, str], body: str) -> str:
    # Cursor 的 .mdc frontmatter 是单行 description + globs + alwaysApply。
    description = fields["description"].replace("\n", " ").strip()
    return (
        "---\n"
        f"description: {description}\n"
        "globs:\n"
        "alwaysApply: false\n"
        "---\n\n"
        f"<!-- {GENERATED_BANNER} -->\n\n"
        f"{self_contained_body(body)}"
    )


def build_prompt_full(fields: dict[str, str], body: str) -> str:
    return (
        f"<!-- {GENERATED_BANNER} -->\n\n"
        f"# {fields['name']} · 完整版\n\n"
        f"**用法**：把下面分隔线以下的全部内容粘贴到对话开头（ChatGPT、WorkBuddy "
        f"等无法读取仓库文件的环境），然后说出你想学的领域。\n\n"
        f"如果目标是填进 Custom GPT 的指令框（有 8000 字符上限），"
        f"请改用 `PROMPT-compact.md`。\n\n"
        f"---\n\n{self_contained_body(body)}"
    )


def compact_payload(body: str) -> str:
    """精简版真正会被粘贴的正文：SKILL 正文（去掉可省段落）+ 标记内联的参考段落。"""
    core = strip_compact_markers(apply_compact(body)).strip()
    core = rewrite_ref_links(core, {rel: "文末附录" for rel in REFERENCE_FILES})
    text = f"{core}\n\n---\n\n# 附录：信源与防幻觉\n\n{compact_includes()}"
    assert_no_dangling_refs(text, "精简版")
    return text


def build_prompt_compact(fields: dict[str, str], body: str) -> str:
    core = compact_payload(body)
    text = (
        f"<!-- {GENERATED_BANNER} -->\n\n"
        f"<!-- 精简版，用于 Custom GPT 指令框（{COMPACT_CHAR_LIMIT} 字符上限）。"
        f"完整版见 PROMPT.md。 -->\n\n"
        f"{core}\n"
    )
    # 上限只约束真正会被粘贴的正文，不含 HTML 注释形式的构建元信息。
    payload = len(core)
    if payload > COMPACT_CHAR_LIMIT:
        raise BuildError(
            f"PROMPT-compact.md 正文 {payload} 字符，超过 {COMPACT_CHAR_LIMIT} 上限"
            f"（超出 {payload - COMPACT_CHAR_LIMIT}）。\n"
            f"请在 SKILL.md 中用 <!-- compact:skip --> 包裹更多可省略的段落，"
            f"或精简正文——不要提高上限，那是 Custom GPT 的硬限制。"
        )
    return text


OUTPUTS = {
    "AGENTS.md": build_agents_md,
    ".cursor/rules/quick-learn-everything.mdc": build_cursor_rule,
    "dist/PROMPT.md": build_prompt_full,
    "dist/PROMPT-compact.md": build_prompt_compact,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="只校验产物是否与源一致，不写入；不一致则非零退出",
    )
    args = parser.parse_args()

    try:
        fields, body = split_frontmatter(read("SKILL.md"))
        generated = {rel: fn(fields, body) for rel, fn in OUTPUTS.items()}
    except BuildError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 1

    stale = []
    for rel, content in generated.items():
        path = ROOT / rel
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == content:
            continue
        if args.check:
            stale.append(rel if current is not None else f"{rel}（缺失）")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"  写入 {rel}（{len(content)} 字符）")

    if args.check:
        if stale:
            print("✗ 产物与源不一致：", file=sys.stderr)
            for rel in stale:
                print(f"    {rel}", file=sys.stderr)
            print("  运行 `python scripts/build.py` 重新生成。", file=sys.stderr)
            return 1
        print("✓ 全部产物与源一致")
        return 0

    compact = len(compact_payload(body))
    print(
        f"✓ 构建完成　compact 正文 {compact}/{COMPACT_CHAR_LIMIT} 字符"
        f"（余量 {COMPACT_CHAR_LIMIT - compact}）"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
