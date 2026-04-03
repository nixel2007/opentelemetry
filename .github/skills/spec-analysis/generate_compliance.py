#!/usr/bin/env python3
"""Генерация docs/spec-compliance.md из результатов верификации.

Принимает JSON с требованиями и JSON с результатами верификации,
генерирует Markdown-документ с полным анализом соответствия.

Использование:
    python3 generate_compliance.py requirements.json verification.json output.md
"""

import json
import sys
from collections import Counter
from datetime import datetime


STATUS_ICONS = {
    "found": "✅",
    "partial": "⚠️",
    "not_found": "❌",
    "n_a": "➖",
}


def load_data(req_file, verif_file):
    """Загружает требования и результаты верификации."""
    with open(req_file, encoding="utf-8") as f:
        requirements = json.load(f)

    with open(verif_file, encoding="utf-8") as f:
        verification = json.load(f)

    # Объединяем: verification - dict {id: {status, location, notes}}
    for i, req in enumerate(requirements):
        req["id"] = i + 1
        v = verification.get(str(i + 1), {})
        req["status"] = v.get("status", "pending")
        req["code_location"] = v.get("location", "")
        req["notes"] = v.get("notes", "")

    return requirements


def generate_markdown(requirements, spec_version=None):
    """Генерирует Markdown-документ с разделением на Stable и Development."""
    if not spec_version:
        spec_version = "v1.55.0"

    pct = lambda n, d: round(100 * n / d, 1) if d > 0 else 0

    # Разделяем Stable и Development
    stable_reqs = [r for r in requirements if r.get("stability", "Stable") == "Stable"]
    dev_reqs = [r for r in requirements if r.get("stability", "Stable") == "Development"]

    total = len(requirements)

    md = []
    md.append(f"# Анализ соответствия спецификации OpenTelemetry {spec_version}")
    md.append("")
    md.append(f"> **Версия спецификации**: [{spec_version}](https://opentelemetry.io/docs/specs/otel/)")
    md.append(f"> **Дата анализа**: {datetime.now().strftime('%Y-%m-%d')}")
    md.append("> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода")
    md.append("")

    # === Stable summary ===
    s_found = sum(1 for r in stable_reqs if r["status"] == "found")
    s_partial = sum(1 for r in stable_reqs if r["status"] == "partial")
    s_not_found = sum(1 for r in stable_reqs if r["status"] == "not_found")
    s_na = sum(1 for r in stable_reqs if r["status"] == "n_a")
    s_applicable = len(stable_reqs) - s_na

    s_must = [r for r in stable_reqs if r["level"] in ("MUST", "MUST NOT") and r["status"] != "n_a"]
    s_must_found = sum(1 for r in s_must if r["status"] == "found")
    s_should = [r for r in stable_reqs if r["level"] in ("SHOULD", "SHOULD NOT") and r["status"] != "n_a"]
    s_should_found = sum(1 for r in s_should if r["status"] == "found")

    md.append("## Сводка (Stable)")
    md.append("")
    md.append("Учитываются только требования из стабильных разделов спецификации.")
    md.append("")
    md.append("| Показатель | Значение |")
    md.append("|---|---|")
    md.append(f"| Всего требований | {total} (Stable: {len(stable_reqs)}, Development: {len(dev_reqs)}) |")
    md.append(f"| Применимых Stable (без N/A) | {s_applicable} |")
    md.append(f"| ✅ Реализовано | {s_found} ({pct(s_found, s_applicable)}%) |")
    md.append(f"| ⚠️ Частично | {s_partial} ({pct(s_partial, s_applicable)}%) |")
    md.append(f"| ❌ Не реализовано | {s_not_found} ({pct(s_not_found, s_applicable)}%) |")
    md.append(f"| N/A (неприменимо) | {s_na} |")
    md.append(f"| **MUST/MUST NOT** | {s_must_found}/{len(s_must)} ({pct(s_must_found, len(s_must))}%) |")
    md.append(f"| **SHOULD/SHOULD NOT** | {s_should_found}/{len(s_should)} ({pct(s_should_found, len(s_should))}%) |")
    md.append("")

    # === Per-section summary (Stable only) ===
    sections = []
    seen = set()
    for r in requirements:
        if r["section"] not in seen:
            sections.append(r["section"])
            seen.add(r["section"])

    md.append("## Соответствие по разделам (Stable)")
    md.append("")
    md.append("| Раздел | Всего | ✅ | ⚠️ | ❌ | N/A | % | Dev |")
    md.append("|---|---|---|---|---|---|---|---|")

    for section in sections:
        sec_stable = [r for r in stable_reqs if r["section"] == section]
        sec_dev = [r for r in dev_reqs if r["section"] == section]
        t = len(sec_stable)
        f = sum(1 for r in sec_stable if r["status"] == "found")
        p = sum(1 for r in sec_stable if r["status"] == "partial")
        nf = sum(1 for r in sec_stable if r["status"] == "not_found")
        n = sum(1 for r in sec_stable if r["status"] == "n_a")
        appl = t - n
        md.append(f"| {section} | {t} | {f} | {p} | {nf} | {n} | {pct(f, appl)}% | {len(sec_dev)} |")

    md.append("")

    # === Key deviations (Stable only) ===
    md.append("## Ключевые несоответствия (Stable)")
    md.append("")
    md.append("### MUST/MUST NOT нарушения")
    md.append("")

    must_devs = [r for r in stable_reqs if r["level"] in ("MUST", "MUST NOT") and r["status"] in ("not_found", "partial")]
    must_devs.sort(key=lambda r: (r["section"], r["id"]))

    for r in must_devs:
        icon = "⚠️" if r["status"] == "partial" else "❌"
        short_req = r["requirement"][:150]
        if len(r["requirement"]) > 150:
            short_req += "..."
        loc = f" (`{r['code_location']}`)" if r["code_location"] else ""
        md.append(f"- {icon} **[{r['section']}]** [{r['level']}] {short_req}{loc}")
        if r["notes"]:
            md.append(f"  - {r['notes']}")

    md.append("")
    md.append("### SHOULD/SHOULD NOT несоответствия")
    md.append("")

    should_devs = [r for r in stable_reqs if r["level"] in ("SHOULD", "SHOULD NOT") and r["status"] in ("not_found", "partial")]
    should_devs.sort(key=lambda r: (r["section"], r["id"]))

    for r in should_devs:
        icon = "⚠️" if r["status"] == "partial" else "❌"
        short_req = r["requirement"][:150]
        if len(r["requirement"]) > 150:
            short_req += "..."
        loc = f" (`{r['code_location']}`)" if r["code_location"] else ""
        md.append(f"- {icon} **[{r['section']}]** [{r['level']}] {short_req}{loc}")
        if r["notes"]:
            md.append(f"  - {r['notes']}")

    md.append("")
    md.append("---")
    md.append("")

    # === Detailed per-section tables (Stable) ===
    md.append("## Детальный анализ по разделам (Stable)")
    md.append("")

    for section in sections:
        sec_reqs = [r for r in stable_reqs if r["section"] == section]
        if not sec_reqs:
            continue
        md.append(f"### {section}")
        md.append("")
        md.append("| # | Уровень | Статус | Требование | Расположение в коде |")
        md.append("|---|---|---|---|---|")

        for r in sec_reqs:
            icon = STATUS_ICONS.get(r["status"], "?")
            short_req = r["requirement"][:120].replace("|", "\\|").replace("\n", " ")
            if len(r["requirement"]) > 120:
                short_req += "..."
            loc = r["code_location"].replace("|", "\\|") if r["code_location"] else "-"
            if r["notes"] and r["status"] != "found":
                loc += f" ({r['notes']})" if r["code_location"] else r["notes"]
            md.append(f"| {r['id']} | {r['level']} | {icon} | {short_req} | {loc} |")

        md.append("")

    # === Development section ===
    if dev_reqs:
        md.append("---")
        md.append("")
        md.append("## Требования Development-статуса")
        md.append("")
        md.append("Эти требования находятся в нестабильных разделах спецификации (Status: Development).")
        md.append("Они не влияют на основной процент соответствия и могут измениться в будущих версиях спецификации.")
        md.append("")

        d_found = sum(1 for r in dev_reqs if r["status"] == "found")
        d_partial = sum(1 for r in dev_reqs if r["status"] == "partial")
        d_not_found = sum(1 for r in dev_reqs if r["status"] == "not_found")
        d_na = sum(1 for r in dev_reqs if r["status"] == "n_a")
        d_applicable = len(dev_reqs) - d_na

        md.append("| Показатель | Значение |")
        md.append("|---|---|")
        md.append(f"| Всего Development | {len(dev_reqs)} |")
        md.append(f"| ✅ Реализовано | {d_found} ({pct(d_found, d_applicable)}%) |")
        md.append(f"| ⚠️ Частично | {d_partial} ({pct(d_partial, d_applicable)}%) |")
        md.append(f"| ❌ Не реализовано | {d_not_found} ({pct(d_not_found, d_applicable)}%) |")
        md.append(f"| N/A | {d_na} |")
        md.append("")

        for section in sections:
            sec_dev = [r for r in dev_reqs if r["section"] == section]
            if not sec_dev:
                continue
            md.append(f"### {section} (Development)")
            md.append("")
            md.append("| # | Уровень | Статус | Требование | Расположение в коде |")
            md.append("|---|---|---|---|---|")

            for r in sec_dev:
                icon = STATUS_ICONS.get(r["status"], "?")
                short_req = r["requirement"][:120].replace("|", "\\|").replace("\n", " ")
                if len(r["requirement"]) > 120:
                    short_req += "..."
                loc = r["code_location"].replace("|", "\\|") if r["code_location"] else "-"
                if r["notes"] and r["status"] != "found":
                    loc += f" ({r['notes']})" if r["code_location"] else r["notes"]
                md.append(f"| {r['id']} | {r['level']} | {icon} | {short_req} | {loc} |")

            md.append("")

    # Platform limitations
    md.append("## Ограничения платформы OneScript")
    md.append("")
    md.append("Некоторые требования спецификации не могут быть полностью реализованы из-за ограничений платформы:")
    md.append("")
    md.append("| Ограничение | Влияние |")
    md.append("|---|---|")
    md.append("| Нет нативного protobuf | Используется HTTP/JSON вместо HTTP/protobuf. Протокол по умолчанию - http/json |")
    md.append("| Точность времени - миллисекунды | Спецификация требует наносекунды |")
    md.append("| Нет TLS/mTLS конфигурации | Нет поддержки сертификатов клиента |")
    md.append("| Нет поддержки B3/X-Ray пропагаторов | Реализованы только W3C TraceContext и W3C Baggage |")
    md.append("| Нет облачных детекторов ресурсов | Нет EKS/AKS/GKE детекторов |")
    md.append("")

    # Methodology
    md.append("## Методология")
    md.append("")
    md.append(f"1. Извлечены все предложения с ключевыми словами MUST/MUST NOT/SHOULD/SHOULD NOT из 12 страниц спецификации OTel {spec_version}:")
    md.append("   - Context, Baggage API, Resource SDK, Trace API, Trace SDK, Logs Bridge API, Logs SDK, Metrics API, Metrics SDK, OTLP Exporter, Propagators, SDK Environment Variables")
    md.append(f"2. Каждое из {total} требований классифицировано по стабильности (Stable/Development) на основе маркеров `Status:` в спецификации")
    md.append(f"3. Каждое требование прослежено до конкретного файла и строки в исходном коде")
    md.append("4. Статусы:")
    md.append("   - ✅ found - реализовано")
    md.append("   - ⚠️ partial - частично реализовано")
    md.append("   - ❌ not_found - не реализовано")
    md.append("   - ➖ n_a - неприменимо к платформе")
    md.append("5. Development-требования вынесены в отдельную секцию и не влияют на основной процент соответствия")
    md.append("")

    return "\n".join(md)


def main():
    if len(sys.argv) < 4:
        print("Использование: python3 generate_compliance.py requirements.json verification.json output.md")
        sys.exit(1)

    req_file = sys.argv[1]
    verif_file = sys.argv[2]
    output_file = sys.argv[3]

    spec_version = sys.argv[4] if len(sys.argv) > 4 else None

    requirements = load_data(req_file, verif_file)
    markdown = generate_markdown(requirements, spec_version)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    pending = sum(1 for r in requirements if r["status"] == "pending")
    found = sum(1 for r in requirements if r["status"] == "found")
    total = len(requirements)
    na = sum(1 for r in requirements if r["status"] == "n_a")

    print(f"Сгенерирован {output_file}")
    print(f"  Требований: {total}")
    print(f"  Реализовано: {found}/{total - na} ({round(100 * found / (total - na), 1) if total > na else 0}%)")
    if pending > 0:
        print(f"  ⚠️ Не верифицировано: {pending}")


if __name__ == "__main__":
    main()
