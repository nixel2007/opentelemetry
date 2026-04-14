#!/usr/bin/env python3
"""Сборка отчёта spec-compliance.md из JSON-результатов агентов верификации.

Читает структурированные JSON-файлы результатов и sections.json,
генерирует полный документ docs/spec-compliance.md с каждым требованием
как отдельной строкой таблицы.

Использование:
    python3 assemble_report.py <output_dir> [<report_path>]

Входные данные:
    <output_dir>/sections.json     - метаданные секций (из extract_requirements.py)
    <output_dir>/results/*.json    - результаты агентов (структурированный JSON)

Выходные данные:
    <report_path> (по умолчанию docs/spec-compliance.md)
"""

import glob
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date


STATUS_ICONS = {
    "found": "✅",
    "partial": "⚠️",
    "not_found": "❌",
    "n_a": "➖",
}

LEVEL_ORDER = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT"]


def load_results(results_dir):
    """Загружает все JSON-файлы результатов агентов.

    Возвращает словарь: section_id -> section_result
    При отсутствии section_id использует (page, subsection) как fallback.
    """
    merged = {}
    agents_loaded = []

    for filepath in sorted(glob.glob(os.path.join(results_dir, "*.json"))):
        with open(filepath, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"⚠️  Ошибка JSON в {filepath}: {e}")
                continue

        agent_name = data.get("agent", os.path.basename(filepath))
        agents_loaded.append(agent_name)

        for section in data.get("sections", []):
            key = section.get(
                "section_id",
                f"{section['page']}/{section['subsection']}",
            )
            if key in merged:
                print(
                    f"⚠️  Дубликат секции {key} "
                    f"(агенты: {merged[key].get('_agent')}, {agent_name})"
                )
            section["_agent"] = agent_name
            # Обеспечиваем наличие section_id для дальнейшей обработки
            section.setdefault("section_id", key)
            merged[key] = section

    return merged, agents_loaded


def load_sections_metadata(sections_file):
    """Загружает sections.json и строит индекс по section_id."""
    with open(sections_file, encoding="utf-8") as f:
        sections = json.load(f)
    index = {}
    for s in sections:
        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        index[key] = s
    return sections, index


def validate_completeness(sections, sections_index, merged):
    """Проверяет полноту результатов: все секции покрыты, keywords совпадают."""
    warnings = []

    for s in sections:
        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        if key not in merged:
            warnings.append(
                f"Секция {key} ({s['keywords']['total']} kw) "
                f"- нет результата от агента"
            )
            continue

        result = merged[key]
        actual_count = len(result.get("requirements", []))
        expected = s["keywords"]["total"]
        if actual_count == 0 and expected > 0:
            warnings.append(
                f"Секция {key}: "
                f"0 требований (ожидалось ~{expected})"
            )
        elif expected > 0 and actual_count != expected:
            warnings.append(
                f"Секция {key}: "
                f"{actual_count} требований (ожидалось ровно {expected})"
            )

    return warnings


def compute_stats(merged, sections):
    """Вычисляет статистику по доменам и общую."""
    # Группировка по страницам
    page_stats = defaultdict(lambda: Counter())
    page_must_stats = defaultdict(lambda: Counter())
    page_should_stats = defaultdict(lambda: Counter())
    total = Counter()
    total_must = Counter()
    total_should = Counter()

    for s in sections:
        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        result = merged.get(key)
        if not result:
            continue

        for req in result.get("requirements", []):
            status = req.get("status", "not_found")
            level = req.get("level", "MUST")
            stability = s.get("stability", "Stable")
            scope = s.get("scope", "universal")

            # Считаем только Stable + universal для основной статистики
            if stability != "Stable" or scope != "universal":
                continue

            page_stats[s["page"]][status] += 1
            total[status] += 1

            if "MUST" in level:
                page_must_stats[s["page"]][status] += 1
                total_must[status] += 1
            else:
                page_should_stats[s["page"]][status] += 1
                total_should[status] += 1

    return {
        "page_stats": dict(page_stats),
        "page_must_stats": dict(page_must_stats),
        "page_should_stats": dict(page_should_stats),
        "total": total,
        "total_must": total_must,
        "total_should": total_should,
    }


def generate_markdown(merged, sections, sections_index, stats, warnings):
    """Генерирует полный markdown-документ."""
    lines = []

    # Заголовок
    lines.append("# Анализ соответствия спецификации OpenTelemetry v1.55.0")
    lines.append("")
    lines.append(
        f"> **Версия спецификации**: "
        f"[v1.55.0](https://opentelemetry.io/docs/specs/otel/)"
    )
    lines.append(f"> **Дата анализа**: {date.today().isoformat()}")
    lines.append(
        "> **Методология**: spec-first - извлечены все MUST/SHOULD "
        "требования из спецификации, затем каждое прослежено до кода"
    )
    lines.append("")

    # Сводка
    t = stats["total"]
    tm = stats["total_must"]
    ts = stats["total_should"]

    applicable = t["found"] + t["partial"] + t["not_found"]
    must_applicable = tm["found"] + tm["partial"] + tm["not_found"]
    should_applicable = ts["found"] + ts["partial"] + ts["not_found"]

    # Подсчёт keywords
    stable_universal_kw = sum(
        s["keywords"]["total"]
        for s in sections
        if s["stability"] == "Stable" and s["scope"] == "universal"
    )
    dev_kw = sum(
        s["keywords"]["total"]
        for s in sections
        if s["stability"] == "Development"
    )
    cond_kw = sum(
        s["keywords"]["total"]
        for s in sections
        if "conditional" in s.get("scope", "")
    )
    total_kw = sum(s["keywords"]["total"] for s in sections)

    pct = lambda n, d: f"{n / d * 100:.1f}%" if d > 0 else "N/A"

    lines.append("## Сводка (Stable)")
    lines.append("")
    lines.append(
        "Учитываются только требования из стабильных разделов "
        "спецификации с универсальной областью применения."
    )
    lines.append("")
    lines.append("| Показатель | Значение |")
    lines.append("|---|---|")
    lines.append(f"| Всего keywords в спецификации | {total_kw} |")
    lines.append(f"| Stable + universal keywords | {stable_universal_kw} |")
    lines.append(f"| Conditional keywords | {cond_kw} |")
    lines.append(f"| Development keywords | {dev_kw} |")
    lines.append(f"| Найдено требований (Stable universal) | {applicable} |")
    lines.append(
        f"| ✅ Реализовано (found) | {t['found']} ({pct(t['found'], applicable)}) |"
    )
    lines.append(
        f"| ⚠️ Частично (partial) | {t['partial']} ({pct(t['partial'], applicable)}) |"
    )
    lines.append(
        f"| ❌ Не реализовано (not_found) | "
        f"{t['not_found']} ({pct(t['not_found'], applicable)}) |"
    )
    lines.append(f"| ➖ Неприменимо (n_a) | {t['n_a']} |")
    lines.append(
        f"| **MUST/MUST NOT found** | "
        f"{tm['found']}/{must_applicable} ({pct(tm['found'], must_applicable)}) |"
    )
    lines.append(
        f"| **SHOULD/SHOULD NOT found** | "
        f"{ts['found']}/{should_applicable} ({pct(ts['found'], should_applicable)}) |"
    )
    lines.append("")

    # Таблица по разделам
    lines.append("## Соответствие по разделам (Stable)")
    lines.append("")
    lines.append("| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |")
    lines.append("|---|---|---|---|---|---|---|")

    page_order = [
        "Context", "Baggage Api", "Resource Sdk", "Trace Api", "Trace Sdk",
        "Logs Api", "Logs Sdk", "Metrics Api", "Metrics Sdk",
        "Otlp Exporter", "Propagators", "Env Vars",
    ]
    for page in page_order:
        ps = stats["page_stats"].get(page, Counter())
        found = ps.get("found", 0)
        partial = ps.get("partial", 0)
        not_found = ps.get("not_found", 0)
        n_a = ps.get("n_a", 0)
        app = found + partial + not_found
        lines.append(
            f"| {page} | {found} | {partial} | {not_found} | {n_a} | "
            f"{app} | {pct(found, app)} |"
        )
    lines.append("")

    # Ключевые несоответствия
    lines.append("## Ключевые несоответствия (Stable)")
    lines.append("")

    # Собираем MUST нарушения
    must_violations = []
    should_violations = []
    for s in sections:
        if s["stability"] != "Stable" or s["scope"] != "universal":
            continue
        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        result = merged.get(key)
        if not result:
            continue
        for req in result.get("requirements", []):
            if req["status"] in ("not_found", "partial"):
                entry = {
                    "page": s["page"],
                    "subsection": s["subsection"],
                    "url": result.get("spec_url", s.get("url", "")),
                    **req,
                }
                if "MUST" in req.get("level", ""):
                    must_violations.append(entry)
                else:
                    should_violations.append(entry)

    lines.append("### MUST/MUST NOT нарушения")
    lines.append("")
    if must_violations:
        for v in must_violations:
            icon = STATUS_ICONS.get(v["status"], "?")
            loc = f"`{v['code_location']}`" if v.get("code_location", "-") != "-" else "-"
            expl = v.get("explanation", "")
            lines.append(
                f"- {icon} **[{v['page']}]** [{v['level']}] {v['spec_text']}  "
            )
            if expl:
                lines.append(f"  {expl} ({loc})")
            lines.append("")
    else:
        lines.append("Нет нарушений MUST/MUST NOT.")
        lines.append("")

    lines.append("### SHOULD/SHOULD NOT несоответствия")
    lines.append("")
    if should_violations:
        for v in should_violations:
            icon = STATUS_ICONS.get(v["status"], "?")
            loc = f"`{v['code_location']}`" if v.get("code_location", "-") != "-" else "-"
            expl = v.get("explanation", "")
            lines.append(
                f"- {icon} **[{v['page']}]** [{v['level']}] {v['spec_text']}  "
            )
            if expl:
                lines.append(f"  {expl} ({loc})")
            lines.append("")
    else:
        lines.append("Нет несоответствий SHOULD/SHOULD NOT.")
        lines.append("")

    # Детальный анализ по разделам
    lines.append("## Детальный анализ по разделам (Stable)")
    lines.append("")

    current_page = None
    req_counter = 0
    for s in sections:
        if s["stability"] != "Stable" or s["scope"] != "universal":
            continue

        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        result = merged.get(key)

        # Заголовок страницы
        if s["page"] != current_page:
            current_page = s["page"]
            req_counter = 0
            lines.append(f"### {current_page}")
            lines.append("")

        # Заголовок секции
        url = result.get("spec_url", s.get("url", "")) if result else s.get("url", "")
        lines.append(f"#### {s['subsection']}")
        lines.append("")
        lines.append(f"[Ссылка на спецификацию]({url})")
        lines.append("")

        if not result or not result.get("requirements"):
            lines.append(
                f"> ⚠️ Нет данных от агента (ожидалось ~{s['keywords']['total']} "
                f"требований)"
            )
            lines.append("")
            continue

        requirements = result["requirements"]

        lines.append(
            "| # | Уровень | Статус | Требование "
            "| Расположение в коде | Пояснение |"
        )
        lines.append("|---|---|---|---|---|---|")

        for req in requirements:
            req_counter += 1
            level = req.get("level", "?")
            status = req.get("status", "?")
            icon = STATUS_ICONS.get(status, "?")
            spec_text = req.get("spec_text", "").replace("|", "\\|").replace("\n", " ")
            loc = req.get("code_location", "-")
            if loc and loc != "-":
                loc = f"`{loc}`"
            explanation = (
                req.get("explanation", "").replace("|", "\\|").replace("\n", " ")
            )

            lines.append(
                f"| {req_counter} | {level} | {icon} {status} | {spec_text} "
                f"| {loc} | {explanation} |"
            )

        lines.append("")

    # Development-статус
    lines.append("## Требования Development-статуса")
    lines.append("")
    lines.append(
        "Эти требования находятся в секциях со статусом Development. "
        "Их реализация не обязательна для соответствия стабильной спецификации."
    )
    lines.append("")

    dev_sections = [s for s in sections if s["stability"] == "Development"]
    if dev_sections:
        current_page = None
        for s in dev_sections:
            key = s.get("section_id", f"{s['page']}/{s['subsection']}")
            result = merged.get(key)

            if s["page"] != current_page:
                current_page = s["page"]
                lines.append(f"### {current_page}")
                lines.append("")

            url = (
                result.get("spec_url", s.get("url", ""))
                if result
                else s.get("url", "")
            )
            lines.append(f"#### {s['subsection']}")
            lines.append("")
            lines.append(f"[Ссылка на спецификацию]({url})")
            lines.append("")

            if not result or not result.get("requirements"):
                lines.append(
                    f"> Нет данных от агента "
                    f"(ожидалось ~{s['keywords']['total']} требований)"
                )
                lines.append("")
                continue

            lines.append(
                "| # | Уровень | Статус | Требование "
                "| Расположение в коде | Пояснение |"
            )
            lines.append("|---|---|---|---|---|---|")

            for i, req in enumerate(result["requirements"], 1):
                level = req.get("level", "?")
                status = req.get("status", "?")
                icon = STATUS_ICONS.get(status, "?")
                spec_text = (
                    req.get("spec_text", "").replace("|", "\\|").replace("\n", " ")
                )
                loc = req.get("code_location", "-")
                if loc and loc != "-":
                    loc = f"`{loc}`"
                explanation = (
                    req.get("explanation", "").replace("|", "\\|").replace("\n", " ")
                )
                lines.append(
                    f"| {i} | {level} | {icon} {status} | {spec_text} "
                    f"| {loc} | {explanation} |"
                )

            lines.append("")

    # Условные требования - полные таблицы для Stable+conditional секций
    # (Development+conditional уже отображены в Development-секции)
    lines.append("## Условные требования (Conditional)")
    lines.append("")
    lines.append(
        "Требования из условных секций. Применяются только при реализации "
        "соответствующей опциональной фичи."
    )
    lines.append("")

    cond_stable_sections = [
        s for s in sections
        if "conditional" in s.get("scope", "") and s["stability"] == "Stable"
    ]
    if cond_stable_sections:
        current_page = None
        for s in cond_stable_sections:
            key = s.get("section_id", f"{s['page']}/{s['subsection']}")
            result = merged.get(key)

            if s["page"] != current_page:
                current_page = s["page"]
                lines.append(f"### {current_page}")
                lines.append("")

            url = (
                result.get("spec_url", s.get("url", ""))
                if result
                else s.get("url", "")
            )
            scope_label = s.get("scope", "conditional")
            lines.append(f"#### {s['subsection']}")
            lines.append("")
            lines.append(
                f"[Ссылка на спецификацию]({url}) | Scope: {scope_label}"
            )
            lines.append("")

            if not result or not result.get("requirements"):
                lines.append(
                    f"> ⚠️ Нет данных от агента "
                    f"(ожидалось ~{s['keywords']['total']} требований)"
                )
                lines.append("")
                continue

            lines.append(
                "| # | Уровень | Статус | Требование "
                "| Расположение в коде | Пояснение |"
            )
            lines.append("|---|---|---|---|---|---|")

            for i, req in enumerate(result["requirements"], 1):
                level = req.get("level", "?")
                status = req.get("status", "?")
                icon = STATUS_ICONS.get(status, "?")
                spec_text = (
                    req.get("spec_text", "").replace("|", "\\|").replace("\n", " ")
                )
                loc = req.get("code_location", "-")
                if loc and loc != "-":
                    loc = f"`{loc}`"
                explanation = (
                    req.get("explanation", "").replace("|", "\\|").replace("\n", " ")
                )
                lines.append(
                    f"| {i} | {level} | {icon} {status} | {spec_text} "
                    f"| {loc} | {explanation} |"
                )

            lines.append("")

    # Сводка условных секций (включая Development+conditional)
    all_cond_sections = [s for s in sections if "conditional" in s.get("scope", "")]
    if all_cond_sections:
        lines.append("### Сводка условных секций")
        lines.append("")
        lines.append("| Раздел | Секция | Scope | Stability | Keywords | Ссылка |")
        lines.append("|---|---|---|---|---|---|")
        for s in all_cond_sections:
            lines.append(
                f"| {s['page']} | {s['subsection']} | {s['scope']} | "
                f"{s['stability']} | {s['keywords']['total']} | "
                f"[spec]({s['url']}) |"
            )
        lines.append("")

    # Ограничения платформы
    lines.append("## Ограничения платформы OneScript")
    lines.append("")
    lines.append("| Ограничение | Влияние на спецификацию | Решение |")
    lines.append("|---|---|---|")
    lines.append(
        "| Нет наносекундной точности | Временные метки с точностью до миллисекунд "
        "| Используется миллисекундная точность |"
    )
    lines.append(
        "| Нет TLS/mTLS из SDK | Сертификаты конфигурируются вне SDK "
        "| Делегировано системе/прокси |"
    )
    lines.append(
        "| Нет opaque-объектов | Ключи контекста - строки "
        "| Строковые константы как ключи |"
    )
    lines.append(
        "| Нет thread-local | ФоновыеЗадания вместо goroutines "
        "| Передача контекста через параметры |"
    )
    lines.append("")

    # Предупреждения валидации
    if warnings:
        lines.append("## Предупреждения валидации")
        lines.append("")
        for w in warnings:
            lines.append(f"- ⚠️ {w}")
        lines.append("")

    # Методология
    lines.append("## Методология")
    lines.append("")
    lines.append("### Процесс анализа")
    lines.append("")
    lines.append(
        "1. **Извлечение требований** (`extract_requirements.py`): "
        "загрузка 12 страниц спецификации, разбиение на секции, "
        "подсчёт MUST/SHOULD keywords"
    )
    lines.append(
        "2. **Генерация промптов** (`generate_prompts.py`): "
        "группировка секций по доменам, генерация промптов "
        "с JSON-схемой вывода для агентов"
    )
    lines.append(
        "3. **Верификация** (general-purpose агенты): "
        "каждый агент анализирует 5-8 секций, записывает результат в JSON"
    )
    lines.append(
        "4. **Сборка отчёта** (`assemble_report.py`): "
        "детерминированная сборка markdown из JSON-результатов"
    )
    lines.append("")
    lines.append("### Статусы")
    lines.append("")
    lines.append("| Статус | Значение |")
    lines.append("|---|---|")
    lines.append(
        "| ✅ found | Требование полностью реализовано "
        "с корректной семантикой |"
    )
    lines.append(
        "| ⚠️ partial | Код существует, но не полностью "
        "соответствует спецификации |"
    )
    lines.append("| ❌ not_found | Реализация отсутствует |")
    lines.append(
        "| ➖ n_a | Неприменимо из-за ограничений платформы |"
    )
    lines.append("")

    # Статистика
    total_sections = len(sections)
    stable_sections = sum(1 for s in sections if s["stability"] == "Stable")
    dev_sections_count = sum(1 for s in sections if s["stability"] == "Development")
    cond_count = sum(1 for s in sections if "conditional" in s.get("scope", ""))

    lines.append("### Статистика извлечения")
    lines.append("")
    lines.append("| Метрика | Значение |")
    lines.append("|---|---|")
    lines.append("| Страниц спецификации | 12 |")
    lines.append(f"| Всего секций | {total_sections} |")
    lines.append(f"| Stable секций | {stable_sections} |")
    lines.append(f"| Development секций | {dev_sections_count} |")
    lines.append(f"| Conditional секций | {cond_count} |")
    lines.append(f"| Всего keywords | {total_kw} |")
    lines.append(f"| Stable universal keywords | {stable_universal_kw} |")
    lines.append("")

    return "\n".join(lines) + "\n"


STATUS_WEIGHT = {"found": 0, "partial": 1, "not_found": 2, "n_a": 3}

ICON_TO_STATUS = {"✅": "found", "⚠️": "partial", "❌": "not_found", "➖": "n_a"}


def load_previous_report(report_path):
    """Загружает предыдущую версию spec-compliance.md из git (HEAD).

    Возвращает None если файл не существует в git.
    """
    try:
        git_path = os.path.relpath(report_path)
        result = subprocess.run(
            ["git", "show", f"HEAD:{git_path}"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def parse_report_requirements(markdown_text):
    """Парсит spec-compliance.md и извлекает требования по секциям.

    Возвращает dict: (page, subsection) -> [
        {"level": ..., "status": ..., "spec_text": ...,
         "code_location": ..., "explanation": ...}
    ]
    """
    sections = {}
    current_page = None
    current_subsection = None
    in_table = False

    for line in markdown_text.split("\n"):
        stripped = line.strip()

        # Заголовок страницы: ### Page
        if stripped.startswith("### ") and not stripped.startswith("#### "):
            current_page = stripped[4:].strip()
            current_subsection = None
            in_table = False
            continue

        # Заголовок секции: #### Subsection
        if stripped.startswith("#### "):
            current_subsection = stripped[5:].strip()
            in_table = False
            continue

        # Строка-заголовок таблицы - пропускаем
        if stripped.startswith("| # |") or stripped.startswith("|---|"):
            in_table = True
            continue

        # Строка таблицы с требованием
        if in_table and stripped.startswith("| ") and current_page and current_subsection:
            parts = stripped.split("|")
            # | # | Уровень | Статус | Требование | Код | Пояснение |
            if len(parts) >= 7:
                level = parts[2].strip()
                status_raw = parts[3].strip()
                spec_text = parts[4].strip()
                code_loc = parts[5].strip().strip("`")
                explanation = parts[6].strip()

                # Парсим статус: "✅ found" -> "found"
                status = "found"
                for icon, st in ICON_TO_STATUS.items():
                    if icon in status_raw:
                        status = st
                        break

                key = (current_page, current_subsection)
                if key not in sections:
                    sections[key] = []
                sections[key].append({
                    "level": level,
                    "status": status,
                    "spec_text": spec_text,
                    "code_location": code_loc,
                    "explanation": explanation,
                })
        elif not stripped.startswith("|"):
            in_table = False

    return sections


def _build_current_sections(merged, sections_meta):
    """Строит dict (page, subsection) -> [req...] из текущих результатов."""
    result = {}
    for s in sections_meta:
        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        sec_result = merged.get(key)
        if not sec_result or not sec_result.get("requirements"):
            continue

        sec_key = (s["page"], s["subsection"])
        reqs = []
        for req in sec_result["requirements"]:
            reqs.append({
                "level": req.get("level", "MUST"),
                "status": req.get("status", "not_found"),
                "spec_text": req.get("spec_text", ""),
                "code_location": req.get("code_location", "-"),
                "explanation": req.get("explanation", ""),
            })
        result[sec_key] = reqs
    return result


def _match_requirement(old_req, new_reqs, excluded=None):
    """Находит наилучшее совпадение по level + spec_text.

    excluded - множество уже занятых индексов в new_reqs.
    Возвращает (индекс, score) или (None, 0).
    """
    if excluded is None:
        excluded = set()

    old_text = old_req["spec_text"].lower()
    old_prefix = old_text[:60]

    best_idx = None
    best_score = 0.0

    for i, nr in enumerate(new_reqs):
        if i in excluded:
            continue

        new_text = nr["spec_text"].lower()
        new_prefix = new_text[:60]

        if old_req["level"] == nr["level"] and old_prefix == new_prefix:
            return i, 1.0

        old_words = set(old_text.split())
        new_words = set(new_text.split())
        if not old_words or not new_words:
            continue
        intersection = old_words & new_words
        score = len(intersection) / max(len(old_words), len(new_words))
        if score > best_score and score > 0.5 and old_req["level"] == nr["level"]:
            best_score = score
            best_idx = i

    return best_idx, best_score


def compare_with_previous(old_sections, new_sections):
    """Сравнивает текущие и предыдущие результаты, выводит анализ расхождений.

    Оба аргумента - dict: (page, subsection) -> [req...].
    Возвращает список строк для вывода в терминал.
    """
    lines = []

    # Общая статистика
    old_total = Counter()
    new_total = Counter()
    for reqs in old_sections.values():
        for r in reqs:
            old_total[r["status"]] += 1
    for reqs in new_sections.values():
        for r in reqs:
            new_total[r["status"]] += 1

    old_app = old_total["found"] + old_total["partial"] + old_total["not_found"] + old_total["n_a"]
    new_app = new_total["found"] + new_total["partial"] + new_total["not_found"] + new_total["n_a"]

    lines.append("")
    lines.append("=" * 70)
    lines.append("📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  {'Статус':<14} {'Было':>6} {'Стало':>6} {'Δ':>6}")
    lines.append(f"  {'-' * 38}")
    for st in ["found", "partial", "not_found", "n_a"]:
        old_v = old_total.get(st, 0)
        new_v = new_total.get(st, 0)
        delta = new_v - old_v
        sign = "+" if delta > 0 else ""
        marker = ""
        if st == "found" and delta < 0:
            marker = " ⚠️  РЕГРЕССИЯ"
        elif st == "not_found" and delta > 0:
            marker = " ⚠️  РЕГРЕССИЯ"
        elif st == "found" and delta > 0:
            marker = " ✅"
        lines.append(
            f"  {st:<14} {old_v:>6} {new_v:>6} {sign}{delta:>5}{marker}"
        )
    lines.append(f"  {'Всего':<14} {old_app:>6} {new_app:>6} "
                 f"{'+'if new_app - old_app >= 0 else ''}{new_app - old_app:>5}")
    lines.append("")

    # Построчное сравнение
    all_keys = sorted(set(old_sections.keys()) | set(new_sections.keys()))

    upgrades = []     # partial/not_found -> found
    downgrades = []   # found -> partial/not_found
    lateral = []      # partial <-> not_found
    added_reqs = []   # новые требования
    removed_reqs = [] # пропавшие
    new_secs = []
    removed_secs = []

    for key in all_keys:
        old_reqs = old_sections.get(key)
        new_reqs = new_sections.get(key)
        page, subsection = key

        if old_reqs is None:
            new_secs.append((key, len(new_reqs)))
            continue
        if new_reqs is None:
            removed_secs.append((key, len(old_reqs)))
            continue

        matched_new = set()
        for old_r in old_reqs:
            match_idx, score = _match_requirement(old_r, new_reqs, matched_new)
            if match_idx is not None:
                new_r = new_reqs[match_idx]
                matched_new.add(match_idx)
                if old_r["status"] != new_r["status"]:
                    old_w = STATUS_WEIGHT.get(old_r["status"], 99)
                    new_w = STATUS_WEIGHT.get(new_r["status"], 99)
                    entry = (page, subsection, old_r, new_r)
                    if new_w < old_w:
                        upgrades.append(entry)
                    elif new_w > old_w:
                        downgrades.append(entry)
                    else:
                        lateral.append(entry)
            else:
                removed_reqs.append((page, subsection, old_r))

        for i, new_r in enumerate(new_reqs):
            if i not in matched_new:
                added_reqs.append((page, subsection, new_r))

    # Вывод: сначала понижения (самое критичное)
    if downgrades:
        lines.append(
            f"  🔴 ПОНИЖЕНИЕ СТАТУСА ({len(downgrades)}) "
            f"- требует перепроверки:"
        )
        lines.append("")
        for page, sub, old_r, new_r in downgrades:
            lines.append(f"     [{page} / {sub}]")
            lines.append(f"       {old_r['status']} → {new_r['status']}")
            lines.append(f"       Текст: {old_r['spec_text'][:100]}")
            if old_r.get("code_location", "-") != new_r.get("code_location", "-"):
                lines.append(
                    f"       Расположение: {old_r.get('code_location', '-')} → "
                    f"{new_r.get('code_location', '-')}"
                )
            if new_r.get("explanation"):
                lines.append(f"       Пояснение: {new_r['explanation'][:150]}")
            lines.append(
                f"       ⚠️  Возможные причины: 1) регрессия в коде; "
                f"2) агент строже оценил; 3) ложное срабатывание"
            )
            lines.append("")

    if upgrades:
        lines.append(
            f"  🟢 ПОВЫШЕНИЕ СТАТУСА ({len(upgrades)}) "
            f"- требует перепроверки:"
        )
        lines.append("")
        for page, sub, old_r, new_r in upgrades:
            lines.append(f"     [{page} / {sub}]")
            lines.append(f"       {old_r['status']} → {new_r['status']}")
            lines.append(f"       Текст: {old_r['spec_text'][:100]}")
            if new_r.get("code_location", "-") != "-":
                lines.append(f"       Код: {new_r['code_location']}")
            if old_r.get("explanation"):
                lines.append(f"       Было: {old_r['explanation'][:100]}")
            lines.append(
                f"       ⚠️  Возможные причины: 1) код добавлен/исправлен; "
                f"2) агент мягче оценил; 3) ложное повышение"
            )
            lines.append("")

    if lateral:
        lines.append(
            f"  🔄 БОКОВОЕ ИЗМЕНЕНИЕ ({len(lateral)}) "
            f"- статус изменён на равнозначный:"
        )
        lines.append("")
        for page, sub, old_r, new_r in lateral:
            lines.append(
                f"     [{page}] {old_r['status']} → {new_r['status']}: "
                f"{old_r['spec_text'][:80]}"
            )
        lines.append("")

    if new_secs:
        lines.append(f"  📋 Новые секции ({len(new_secs)}):")
        for (page, sub), cnt in new_secs:
            lines.append(f"     + [{page}] {sub} ({cnt} req)")
        lines.append("")

    if removed_secs:
        lines.append(f"  📋 Исчезнувшие секции ({len(removed_secs)}):")
        for (page, sub), cnt in removed_secs:
            lines.append(f"     - [{page}] {sub} ({cnt} req)")
        lines.append("")

    if added_reqs:
        lines.append(
            f"  ➕ НОВЫЕ ТРЕБОВАНИЯ ({len(added_reqs)}) "
            f"- агент нашёл дополнительные:"
        )
        lines.append("")
        for page, sub, r in added_reqs[:20]:
            lines.append(
                f"     [{page}] {r['level']} {r['status']}: "
                f"{r['spec_text'][:80]}"
            )
        if len(added_reqs) > 20:
            lines.append(f"     ... и ещё {len(added_reqs) - 20}")
        lines.append("")

    if removed_reqs:
        lines.append(
            f"  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ ({len(removed_reqs)}) "
            f"- были раньше, теперь нет:"
        )
        lines.append("")
        for page, sub, r in removed_reqs[:20]:
            lines.append(
                f"     [{page}] {r['level']} {r['status']}: "
                f"{r['spec_text'][:80]}"
            )
        if len(removed_reqs) > 20:
            lines.append(f"     ... и ещё {len(removed_reqs) - 20}")
        lines.append("")

    # Итог
    total_changes = (
        len(downgrades) + len(upgrades) + len(lateral)
        + len(added_reqs) + len(removed_reqs)
    )
    lines.append(f"  Итого изменений: {total_changes}")
    lines.append(
        f"    Понижений: {len(downgrades)}, Повышений: {len(upgrades)}, "
        f"Боковых: {len(lateral)}"
    )
    lines.append(
        f"    Новых req: {len(added_reqs)}, Пропущенных req: {len(removed_reqs)}"
    )
    lines.append(
        f"    Новых секций: {len(new_secs)}, "
        f"Исчезнувших секций: {len(removed_secs)}"
    )
    if len(downgrades) > 0 or len(removed_reqs) > 5:
        lines.append("")
        lines.append(
            "  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные "
            "требования вручную, чтобы отличить реальные регрессии от "
            "вариативности агентов."
        )
    lines.append("")
    lines.append("=" * 70)

    return lines


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 assemble_report.py <output_dir> [<report_path>]")
        print()
        print("  <output_dir>   - каталог с sections.json и results/")
        print("  <report_path>  - путь к выходному файлу (по умолчанию docs/spec-compliance.md)")
        sys.exit(1)

    output_dir = sys.argv[1]
    report_path = sys.argv[2] if len(sys.argv) > 2 else "docs/spec-compliance.md"

    sections_file = os.path.join(output_dir, "sections.json")
    results_dir = os.path.join(output_dir, "results")

    if not os.path.exists(sections_file):
        print(f"Ошибка: {sections_file} не найден")
        sys.exit(1)

    if not os.path.exists(results_dir):
        print(f"Ошибка: каталог {results_dir} не найден")
        sys.exit(1)

    result_files = glob.glob(os.path.join(results_dir, "*.json"))
    if not result_files:
        print(f"Ошибка: нет JSON-файлов в {results_dir}")
        sys.exit(1)

    print(f"Загрузка результатов из {results_dir}")

    # Загрузка данных
    sections, sections_index = load_sections_metadata(sections_file)
    merged, agents_loaded = load_results(results_dir)

    print(f"Загружено {len(agents_loaded)} агентов, {len(merged)} секций с результатами")

    # Валидация
    warnings = validate_completeness(sections, sections_index, merged)
    if warnings:
        print(f"\n⚠️  {len(warnings)} предупреждений валидации:")
        for w in warnings:
            print(f"  - {w}")

    # Статистика
    stats = compute_stats(merged, sections)

    # Генерация markdown
    markdown = generate_markdown(merged, sections, sections_index, stats, warnings)

    # Сравнение с предыдущей версией
    # Файл сравнения лежит рядом с отчётом: docs/spec-compliance.md -> docs/spec-comparison-report.md
    report_dir = os.path.dirname(os.path.abspath(report_path))
    comparison_path = os.path.join(report_dir, "spec-comparison-report.md")
    old_markdown = load_previous_report(report_path)
    if old_markdown:
        old_sections_parsed = parse_report_requirements(old_markdown)
        new_sections_parsed = parse_report_requirements(markdown)
        diff_lines = compare_with_previous(old_sections_parsed, new_sections_parsed)
        comparison_text = "# Отчёт сравнения spec-compliance\n\n```\n" + "\n".join(diff_lines) + "\n```\n"
        os.makedirs(report_dir, exist_ok=True)
        with open(comparison_path, "w", encoding="utf-8") as f:
            f.write(comparison_text)
        print(f"\n📋 Отчёт сравнения записан в {comparison_path}")
    else:
        print("\nПредыдущая версия отчёта не найдена в git - сравнение пропущено.")
        os.makedirs(report_dir, exist_ok=True)
        with open(comparison_path, "w", encoding="utf-8") as f:
            f.write("# Отчёт сравнения spec-compliance\n\nПредыдущая версия отчёта не найдена в git - сравнение пропущено.\n")

    # Создаём каталог если нужно
    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    t = stats["total"]
    applicable = t["found"] + t["partial"] + t["not_found"]
    print(f"\n✅ Отчёт записан в {report_path}")
    print(f"   Stable universal: {t['found']} found, {t['partial']} partial, "
          f"{t['not_found']} not_found, {t['n_a']} n_a (из {applicable} применимых)")

    # Финальная валидация: total requirements в markdown == total keywords в sections
    expected_kw = sum(s["keywords"]["total"] for s in sections)
    actual_reqs = 0
    for s in sections:
        key = s.get("section_id", f"{s['page']}/{s['subsection']}")
        result = merged.get(key)
        if result:
            actual_reqs += len(result.get("requirements", []))

    # Проверяем также, что markdown содержит все требования (через парсинг)
    parsed_sections = parse_report_requirements(markdown)
    md_reqs = sum(len(reqs) for reqs in parsed_sections.values())

    print(f"\n📊 Валидация полноты:")
    print(f"   Keywords в спецификации: {expected_kw}")
    print(f"   Требований от агентов (JSON): {actual_reqs}")
    print(f"   Требований в markdown: {md_reqs}")

    if actual_reqs != expected_kw:
        delta = expected_kw - actual_reqs
        print(f"   ❌ ОШИБКА: Разница агенты vs спецификация: {delta} "
              f"(агенты вернули {actual_reqs}, ожидалось {expected_kw})")
        # Показываем какие секции не совпали
        for s in sections:
            key = s.get("section_id", f"{s['page']}/{s['subsection']}")
            result = merged.get(key)
            if not result:
                print(f"      Нет результата: {key} ({s['keywords']['total']} kw)")
            elif len(result.get("requirements", [])) != s["keywords"]["total"]:
                print(f"      Несовпадение: {key} "
                      f"(ожидалось {s['keywords']['total']}, "
                      f"получено {len(result.get('requirements', []))})")
    elif md_reqs != expected_kw:
        print(f"   ❌ ОШИБКА: Разница markdown vs спецификация: "
              f"{expected_kw - md_reqs}")
    else:
        print(f"   ✅ Все {expected_kw} требований присутствуют "
              f"(JSON: {actual_reqs}, markdown: {md_reqs})")


if __name__ == "__main__":
    main()
