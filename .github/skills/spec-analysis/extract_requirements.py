#!/usr/bin/env python3
"""Извлечение секций спецификации OpenTelemetry для анализа соответствия.

Загружает 12 страниц спецификации с opentelemetry.io, разбивает на секции
по заголовкам (##/###), сохраняет полный текст каждой секции с метаданными.

Агенты верификации получают полные секции и сами идентифицируют
MUST/SHOULD требования в контексте окружающего текста.

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

# Условные подразделы - применяются только при реализации фичи
CONDITIONAL_SUBSECTIONS = {
    r"^B3": "B3 Propagator (extension)",
    r"^GetAll": "GetAll Getter (post-stable extension)",
    r"^Resource detector name": "Resource Detector Naming (conditional)",
    r"^Prometheus": "Prometheus Exporter (extension)",
}

# Deprecated секции
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


def _make_anchor(subsection):
    """Генерирует URL-якорь из заголовка (аналогично GitHub/Hugo)."""
    anchor = subsection.lower()
    anchor = re.sub(r"[^a-z0-9\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor).strip("-")
    return anchor


def _classify_subsection(subsection):
    """Определяет scope подраздела."""
    for pattern, feature in CONDITIONAL_SUBSECTIONS.items():
        if re.search(pattern, subsection):
            return f"conditional:{feature}"
    for pattern in DEPRECATED_PATTERNS:
        if re.search(pattern, subsection, re.IGNORECASE):
            return "deprecated"
    return "universal"


def _count_keywords(text):
    """Считает MUST/SHOULD ключевые слова в тексте."""
    must = len(re.findall(r"\bMUST\b", text))
    must_not = len(re.findall(r"\bMUST NOT\b", text))
    should = len(re.findall(r"\bSHOULD\b", text))
    should_not = len(re.findall(r"\bSHOULD NOT\b", text))
    return {
        "must": must - must_not,  # MUST без MUST NOT
        "must_not": must_not,
        "should": should - should_not,  # SHOULD без SHOULD NOT
        "should_not": should_not,
        "total": must + should,  # все ключевые слова
    }


def _detect_stability(text, page_default):
    """Определяет стабильность секции по маркерам Status:."""
    if re.search(r"Status:\s*Development", text):
        return "Development"
    return page_default


def extract_sections(text, page_name, page_url):
    """Разбивает текст страницы на секции по заголовкам.

    Возвращает список секций с полным текстом и метаданными.
    """
    sections = []
    lines = text.split("\n")

    # Стабильность по умолчанию для страницы
    page_default = "Stable"
    for line in lines:
        if re.search(r"Status:\s*(Stable|Development|Mixed)", line.strip()):
            if "Development" in line:
                page_default = "Development"
            break

    # Находим все заголовки ## и ###
    headings = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,4})\s+(.+)", line.strip())
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            title = re.sub(r"\[.*?\]", "", title).strip()
            headings.append((i, level, title))

    if not headings:
        # Страница без заголовков - одна секция
        kw = _count_keywords(text)
        if kw["total"] > 0:
            sections.append({
                "page": page_name,
                "subsection": page_name,
                "url": page_url,
                "stability": page_default,
                "scope": "universal",
                "text": text,
                "keywords": kw,
            })
        return sections

    # Разбиваем на секции между заголовками
    for idx, (line_idx, hlevel, title) in enumerate(headings):
        # Текст секции - от текущего заголовка до следующего того же или более высокого уровня
        if idx + 1 < len(headings):
            end_idx = headings[idx + 1][0]
        else:
            end_idx = len(lines)

        section_text = "\n".join(lines[line_idx:end_idx]).strip()
        kw = _count_keywords(section_text)

        # Пропускаем секции без требований
        if kw["total"] == 0:
            continue

        # Фильтруем шумные секции
        if any(
            p in title.lower()
            for p in ["feedback", "copyright", "on this page", "edit this page"]
        ):
            continue

        anchor = _make_anchor(title)
        stability = _detect_stability(section_text, page_default)
        scope = _classify_subsection(title)

        sections.append({
            "page": page_name,
            "subsection": title,
            "url": f"{page_url}#{anchor}",
            "stability": stability,
            "scope": scope,
            "text": section_text,
            "keywords": kw,
        })

    return sections


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 extract_requirements.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    os.makedirs(output_dir, exist_ok=True)

    print("Извлечение секций спецификации OpenTelemetry")
    print(f"Каталог: {output_dir}")
    print()

    all_sections = []
    total_keywords = 0

    for page_name, url in SPEC_URLS.items():
        text = fetch_page(url, output_dir, page_name)
        sections = extract_sections(text, page_name, url)
        page_kw = sum(s["keywords"]["total"] for s in sections)
        total_keywords += page_kw
        print(f"  {page_name}: {len(sections)} секций, ~{page_kw} требований")
        all_sections.extend(sections)

    print(f"\nВсего секций: {len(all_sections)}")
    print(f"Всего ключевых слов MUST/SHOULD: ~{total_keywords}")

    # Статистика
    from collections import Counter

    stability_counts = Counter(s["stability"] for s in all_sections)
    print(f"\nПо стабильности:")
    for stab, count in sorted(stability_counts.items()):
        print(f"  {stab}: {count} секций")

    scope_counts = Counter(s["scope"] for s in all_sections)
    print(f"\nПо области:")
    for scope, count in sorted(scope_counts.items()):
        print(f"  {scope}: {count} секций")

    page_counts = Counter(s["page"] for s in all_sections)
    print(f"\nПо страницам:")
    for page, count in sorted(page_counts.items(), key=lambda x: -x[1]):
        print(f"  {page}: {count} секций")

    output_file = os.path.join(output_dir, "sections.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_sections, f, ensure_ascii=False, indent=2)

    print(f"\nСохранено в {output_file}")


if __name__ == "__main__":
    main()
