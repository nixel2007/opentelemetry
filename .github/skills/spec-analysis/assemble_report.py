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

    Возвращает словарь: (page, subsection) -> section_result
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
            key = (section["page"], section["subsection"])
            if key in merged:
                print(
                    f"⚠️  Дубликат секции {key[0]}/{key[1]} "
                    f"(агенты: {merged[key].get('_agent')}, {agent_name})"
                )
            section["_agent"] = agent_name
            merged[key] = section

    return merged, agents_loaded


def load_sections_metadata(sections_file):
    """Загружает sections.json и строит индекс по (page, subsection)."""
    with open(sections_file, encoding="utf-8") as f:
        sections = json.load(f)
    index = {}
    for s in sections:
        key = (s["page"], s["subsection"])
        index[key] = s
    return sections, index


def validate_completeness(sections, sections_index, merged):
    """Проверяет полноту результатов: все секции покрыты, keywords совпадают."""
    warnings = []

    for s in sections:
        key = (s["page"], s["subsection"])
        if key not in merged:
            warnings.append(
                f"Секция {s['page']}/{s['subsection']} ({s['keywords']['total']} kw) "
                f"- нет результата от агента"
            )
            continue

        result = merged[key]
        actual_count = len(result.get("requirements", []))
        expected = s["keywords"]["total"]
        if actual_count == 0 and expected > 0:
            warnings.append(
                f"Секция {s['page']}/{s['subsection']}: "
                f"0 требований (ожидалось ~{expected})"
            )
        elif expected > 0 and abs(actual_count - expected) > expected * 0.5:
            warnings.append(
                f"Секция {s['page']}/{s['subsection']}: "
                f"{actual_count} требований (ожидалось ~{expected})"
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
        key = (s["page"], s["subsection"])
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
        key = (s["page"], s["subsection"])
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

        key = (s["page"], s["subsection"])
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
            key = (s["page"], s["subsection"])
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

    # Условные требования
    lines.append("## Условные требования (Conditional)")
    lines.append("")

    cond_sections = [s for s in sections if "conditional" in s.get("scope", "")]
    if cond_sections:
        lines.append("| Раздел | Секция | Scope | Keywords | Ссылка |")
        lines.append("|---|---|---|---|---|")
        for s in cond_sections:
            lines.append(
                f"| {s['page']} | {s['subsection']} | {s['scope']} | "
                f"{s['keywords']['total']} | [spec]({s['url']}) |"
            )
        lines.append("")

    # Ограничения платформы
    lines.append("## Ограничения платформы OneScript")
    lines.append("")
    lines.append("| Ограничение | Влияние на спецификацию | Решение |")
    lines.append("|---|---|---|")
    lines.append(
        "| Нет байтовых массивов | TraceId/SpanId хранятся как hex-строки "
        "| Функциональный эквивалент через строки |"
    )
    lines.append(
        "| Нет наносекундной точности | Временные метки с точностью до миллисекунд "
        "| Используется миллисекундная точность |"
    )
    lines.append(
        "| Нет нативного protobuf | HTTP/JSON вместо HTTP/protobuf "
        "| Полная поддержка через JSON-сериализацию |"
    )
    lines.append(
        "| Нет gRPC | Только HTTP транспорт "
        "| HTTP/JSON как основной протокол |"
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

    # Создаём каталог если нужно
    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    t = stats["total"]
    applicable = t["found"] + t["partial"] + t["not_found"]
    print(f"\n✅ Отчёт записан в {report_path}")
    print(f"   Stable universal: {t['found']} found, {t['partial']} partial, "
          f"{t['not_found']} not_found, {t['n_a']} n_a (из {applicable} применимых)")


if __name__ == "__main__":
    main()
