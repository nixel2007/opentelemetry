#!/usr/bin/env python3
"""Извлечение MUST/SHOULD требований из спецификации OpenTelemetry.

Загружает 12 страниц спецификации с opentelemetry.io, извлекает все строки
с ключевыми словами MUST/MUST NOT/SHOULD/SHOULD NOT и сохраняет в JSON.
Никакой дедупликации и фильтрации не производится - каждая строка спецификации
с ключевым словом сохраняется как отдельное требование.

Использование:
    python3 extract_requirements.py <output_dir>
"""

import html
import json
import os
import re
import sys
import urllib.request


SPEC_URLS = {
    "Context": "https://opentelemetry.io/docs/specs/otel/context/",
    "Baggage Api": "https://opentelemetry.io/docs/specs/otel/baggage/api/",
    "Resource Sdk": "https://opentelemetry.io/docs/specs/otel/resource/sdk/",
    "Trace Api": "https://opentelemetry.io/docs/specs/otel/trace/api/",
    "Trace Sdk": "https://opentelemetry.io/docs/specs/otel/trace/sdk/",
    "Logs Api": "https://opentelemetry.io/docs/specs/otel/logs/api/",
    "Logs Sdk": "https://opentelemetry.io/docs/specs/otel/logs/sdk/",
    "Metrics Api": "https://opentelemetry.io/docs/specs/otel/metrics/api/",
    "Metrics Sdk": "https://opentelemetry.io/docs/specs/otel/metrics/sdk/",
    "Otlp Exporter": "https://opentelemetry.io/docs/specs/otel/protocol/exporter/",
    "Propagators": "https://opentelemetry.io/docs/specs/otel/context/api-propagators/",
    "Env Vars": "https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/",
}

# Строки-шум, которые нужно пропускать
NOISE_PATTERNS = [
    r"^Status:",
    r"Copyright",
    r"[Ff]eedback",
    r"page helpful",
    r"document-status",
]

# Условные секции: подразделы, чьи MUST/SHOULD требования применяются
# только при реализации конкретной опциональной функциональности.
# Ключ - паттерн (regex) для сопоставления с subsection. Значение - название фичи.
CONDITIONAL_SUBSECTIONS = {
    # Propagators: B3 - extension package, не обязательный для SDK
    r"^B3": "B3 Propagator (extension)",
    # Propagators: GetAll - добавляется после stable релиза Getter
    r"^GetAll": "GetAll Getter (post-stable extension)",
    # Resource SDK: detector name conventions - только для SDK с детекторами
    r"^Resource detector name": "Resource Detector Naming (conditional)",
    # Env Vars: Prometheus exporter - отдельный пакет
    r"^Prometheus": "Prometheus Exporter (extension)",
}

# Deprecated секции: требования из них помечаются как deprecated
DEPRECATED_PATTERNS = [
    r"Jaeger",
    r"OT Trace",
    r"OpenTracing",
    r"OpenCensus",
]


def fetch_page(url, output_dir, name):
    """Загружает страницу, конвертирует HTML в текст, кеширует."""
    cache_file = os.path.join(output_dir, f"{name.lower().replace(' ', '_')}.txt")

    if os.path.exists(cache_file):
        with open(cache_file, encoding="utf-8") as f:
            return f.read()

    print(f"  Загрузка {name}: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "OTel-Spec-Analyzer/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")

    # Удаляем script/style/nav/header/footer блоки
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.DOTALL)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.DOTALL)
    raw = re.sub(r"<nav[^>]*>.*?</nav>", "", raw, flags=re.DOTALL)
    raw = re.sub(r"<header[^>]*>.*?</header>", "", raw, flags=re.DOTALL)
    raw = re.sub(r"<footer[^>]*>.*?</footer>", "", raw, flags=re.DOTALL)

    # Конвертируем HTML элементы в текст
    raw = re.sub(
        r"<h([1-6])[^>]*>(.*?)</h\1>",
        lambda m: "#" * int(m.group(1)) + " " + m.group(2),
        raw,
        flags=re.DOTALL,
    )
    raw = re.sub(r"<li[^>]*>", "* ", raw)
    raw = re.sub(r"<br\s*/?>", "\n", raw)
    raw = re.sub(r"<p[^>]*>", "\n", raw)
    raw = re.sub(r"</p>", "\n", raw)
    raw = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", raw, flags=re.DOTALL)
    raw = re.sub(r"<[^>]+>", "", raw)  # Убираем оставшиеся теги
    raw = html.unescape(raw)

    # Нормализуем пробелы
    lines = []
    for line in raw.split("\n"):
        line = line.strip()
        if line:
            lines.append(line)
    text = "\n".join(lines)

    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(text)

    return text


def extract_requirements(text, section):
    """Извлекает требования построчно: каждая строка с MUST/SHOULD = требование.

    Отслеживает маркеры 'Status: Development' и 'Status: Stable' в тексте.
    Status-маркеры привязаны к подразделам: при появлении нового заголовка
    статус сбрасывается к значению по умолчанию для страницы.

    Определяет scope требования:
    - universal: обязательно для любой реализации SDK
    - conditional:<feature>: обязательно только при реализации <feature>
    - deprecated: относится к устаревшей функциональности
    """
    reqs = []
    current_subsection = section

    # Определяем стабильность по умолчанию для страницы (первый Status: ...)
    page_default = "Stable"
    for line in text.split("\n"):
        if re.search(r"Status:\s*(Stable|Development|Mixed)", line.strip()):
            if "Development" in line:
                page_default = "Development"
            else:
                page_default = "Stable"
            break

    current_stability = page_default
    current_scope = "universal"

    for line in text.split("\n"):
        stripped = line.strip()

        # Определяем подразделы по заголовкам - сбрасываем статус к умолчанию
        m = re.match(r"^#{1,4}\s+(.+)", stripped)
        if m:
            current_subsection = m.group(1).strip()
            current_subsection = re.sub(r"\[.*?\]", "", current_subsection).strip()
            current_stability = page_default

            # Определяем scope по подразделу
            current_scope = "universal"
            for pattern, feature in CONDITIONAL_SUBSECTIONS.items():
                if re.search(pattern, current_subsection):
                    current_scope = f"conditional:{feature}"
                    break
            for pattern in DEPRECATED_PATTERNS:
                if re.search(pattern, current_subsection, re.IGNORECASE):
                    current_scope = "deprecated"
                    break
            continue

        # Отслеживаем маркеры стабильности секций
        if re.search(r"Status:\s*Development", stripped):
            current_stability = "Development"
            if re.match(r"^Status:\s*Development\s*$", stripped):
                continue
        elif re.search(r"Status:\s*Stable", stripped):
            current_stability = "Stable"
            if re.match(r"^Status:\s*Stable", stripped):
                continue

        # Inline Development/Deprecated маркеры - для конкретной строки
        line_stability = current_stability
        line_scope = current_scope
        if "Status: Development" in stripped or "(Development)" in stripped:
            line_stability = "Development"
        if "Status: Deprecated" in stripped:
            line_scope = "deprecated"
        for pattern in DEPRECATED_PATTERNS:
            if re.search(pattern, stripped, re.IGNORECASE) and current_scope == "universal":
                # Только если встречается в контексте описания deprecated фичи
                if "Deprecated" in stripped:
                    line_scope = "deprecated"

        # Пропускаем короткие строки
        if len(stripped) < 30:
            continue

        # Определяем уровень требования (приоритет: NOT-варианты первые)
        level = None
        if re.search(r"\bMUST NOT\b", stripped):
            level = "MUST NOT"
        elif re.search(r"\bSHOULD NOT\b", stripped):
            level = "SHOULD NOT"
        elif re.search(r"\bMUST\b", stripped):
            level = "MUST"
        elif re.search(r"\bSHOULD\b", stripped):
            level = "SHOULD"

        if not level:
            continue

        # Нормализуем пробелы
        clean = re.sub(r"\s+", " ", stripped)[:450]

        # Пропускаем шум
        if any(re.search(p, clean, re.IGNORECASE) for p in NOISE_PATTERNS):
            continue

        reqs.append(
            {
                "section": section,
                "subsection": current_subsection,
                "level": level,
                "requirement": clean,
                "stability": line_stability,
                "scope": line_scope,
            }
        )

    return reqs


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 extract_requirements.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    os.makedirs(output_dir, exist_ok=True)

    print("Извлечение требований из спецификации OpenTelemetry")
    print(f"Каталог: {output_dir}")
    print()

    all_requirements = []

    for section, url in SPEC_URLS.items():
        text = fetch_page(url, output_dir, section)
        reqs = extract_requirements(text, section)
        print(f"  {section}: {len(reqs)} требований из {len(text)} символов текста")
        all_requirements.extend(reqs)

    print(f"\nВсего извлечено: {len(all_requirements)}")

    # Статистика по уровням
    from collections import Counter

    counts = Counter(r["level"] for r in all_requirements)
    for level, count in sorted(counts.items()):
        print(f"  {level}: {count}")

    # Статистика по стабильности
    stability_counts = Counter(r["stability"] for r in all_requirements)
    print(f"\nПо стабильности:")
    for stab, count in sorted(stability_counts.items()):
        print(f"  {stab}: {count}")

    # Статистика по scope
    scope_counts = Counter(r["scope"] for r in all_requirements)
    print(f"\nПо области применения:")
    for scope, count in sorted(scope_counts.items()):
        print(f"  {scope}: {count}")

    # Статистика по разделам
    print("\nПо разделам:")
    section_counts = Counter(r["section"] for r in all_requirements)
    for section, count in sorted(section_counts.items(), key=lambda x: -x[1]):
        print(f"  {section}: {count}")

    output_file = os.path.join(output_dir, "requirements.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_requirements, f, ensure_ascii=False, indent=2)

    print(f"\nСохранено в {output_file}")


if __name__ == "__main__":
    main()
