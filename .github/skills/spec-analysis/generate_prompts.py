#!/usr/bin/env python3
"""Генерация промптов для агентов верификации спецификации OpenTelemetry.

Читает sections.json, группирует секции по доменам, генерирует файлы промптов
и конфигурацию агентов.

Использование:
    python3 generate_prompts.py <output_dir>

Входные данные:
    <output_dir>/sections.json - извлечённые секции (из extract_requirements.py)

Выходные данные:
    <output_dir>/agents.json        - конфигурация агентов (имя → секции)
    <output_dir>/prompts/<name>.md  - промпт для каждого агента
    <output_dir>/results/           - каталог для результатов агентов (создаётся пустым)
"""

import json
import math
import os
import sys

# Максимум секций на одного агента
MAX_SECTIONS_PER_AGENT = 8

# Домены: какие страницы спецификации → какие каталоги кода
DOMAIN_CONFIG = [
    {
        "domain": "core",
        "pages": ["Context", "Baggage Api"],
        "code_dirs": ["src/Ядро/"],
    },
    {
        "domain": "resource",
        "pages": ["Resource Sdk"],
        "code_dirs": ["src/Ядро/"],
    },
    {
        "domain": "propagators",
        "pages": ["Propagators"],
        "code_dirs": ["src/Пропагация/", "src/Ядро/"],
    },
    {
        "domain": "traces-api",
        "pages": ["Trace Api"],
        "code_dirs": ["src/Трассировка/"],
    },
    {
        "domain": "traces-sdk",
        "pages": ["Trace Sdk"],
        "code_dirs": ["src/Трассировка/"],
    },
    {
        "domain": "logs-api",
        "pages": ["Logs Api"],
        "code_dirs": ["src/Логирование/"],
    },
    {
        "domain": "logs-sdk",
        "pages": ["Logs Sdk"],
        "code_dirs": ["src/Логирование/"],
    },
    {
        "domain": "metrics-api",
        "pages": ["Metrics Api"],
        "code_dirs": ["src/Метрики/"],
    },
    {
        "domain": "metrics-sdk",
        "pages": ["Metrics Sdk"],
        "code_dirs": ["src/Метрики/"],
    },
    {
        "domain": "export",
        "pages": ["Otlp Exporter"],
        "code_dirs": ["src/Экспорт/"],
    },
    {
        "domain": "env-vars",
        "pages": ["Env Vars"],
        "code_dirs": ["src/Конфигурация/", "src/Экспорт/", "src/Ядро/"],
    },
]


# Шаблон инструкции для агента верификации.
# Включается дословно в каждый промпт.
AGENT_INSTRUCTIONS = r"""
**Ты проводишь детальный анализ соответствия кода спецификации OpenTelemetry.**

### КРИТИЧЕСКИ ВАЖНО: Детерминированность

Каждая секция содержит поле `expected_keywords` - **точное** количество ключевых слов
MUST / MUST NOT / SHOULD / SHOULD NOT в тексте секции (блоки кода исключены из подсчёта).

**Количество записей requirements в твоём результате ОБЯЗАНО точно совпадать с `expected_keywords`.**

### Алгоритм извлечения (СТРОГО следуй)

1. Читай текст секции **строго сверху вниз**
2. При каждом появлении MUST NOT, SHOULD NOT, MUST или SHOULD создавай **ровно одну** запись:
   - MUST NOT - одно ключевое слово (не MUST + NOT отдельно)
   - SHOULD NOT - одно ключевое слово (не SHOULD + NOT отдельно)
   - `level` = тип ключевого слова (MUST / MUST NOT / SHOULD / SHOULD NOT)
   - `spec_text` = предложение или пункт списка с этим ключевым словом.
     **Цитируй дословно из спецификации**, не перефразируй.
3. Два ключевых слова в одном предложении = **два** требования (одинаковый spec_text, разные level)
4. **Пропускай** ключевые слова внутри блоков кода (``` ... ```) - они исключены из expected_keywords

> ⚠️ Если твой счёт не совпал с expected_keywords - ты ошибся. Перечитай текст:
> - Не пропустил ли ключевое слово?
> - Не посчитал ли слово из блока кода?
> - Правильно ли обработал MUST NOT / SHOULD NOT как одно слово?

### Верификация каждого требования

Для каждого извлечённого требования:
1. Найди в коде реализацию (grep по ключевым словам, просмотр файлов)
2. Определи статус: found / partial / not_found / n_a
3. Укажи файл:строка для found/partial
4. Укажи URL секции спецификации (поле `url`)

### Строгие критерии статуса

**found** - ВСЕ следующие условия выполнены:
- В коде есть метод/класс/интерфейс с **совпадающей сигнатурой** (имя, параметры, возвращаемый тип)
- Поведение метода соответствует описанному в спецификации
- Если спецификация требует **отдельную сущность** (интерфейс, класс, аргумент) - она СУЩЕСТВУЕТ как отдельная сущность

**partial** - одно из:
- Функциональность РЕАЛИЗОВАНА, но **архитектура не совпадает** с требуемой (например, inline-код вместо отдельного интерфейса)
- Метод существует, но **сигнатура не совпадает** (другие параметры, другой тип возврата)
- Поведение реализовано **не полностью** (часть кейсов не покрыта)
- Требование реализовано через **обходной путь**, а не так, как описано в спеке

**not_found** - реализация отсутствует полностью

### Стратегия верификации

Для каждого требования используй **правильную стратегию проверки**:

**Тип 1: Требование к API-интерфейсу** ("MUST accept parameter X", "MUST return Y", "MUST provide method Z")
→ Найди **конкретный метод**, проверь его **сигнатуру** (параметры + возврат). Если параметры не совпадают - `partial`.

**Тип 2: Требование к отдельной сущности** ("MUST provide a Getter", "MUST be implemented as separate packages", "MUST return an opaque object")
→ Ищи **отдельный класс/интерфейс/модуль**. Если функциональность inline в другом классе - `partial`.

**Тип 3: Требование к поведению** ("MUST NOT modify values", "MUST be thread-safe", "MUST propagate")
→ Прочитай реализацию, проверь что поведение соблюдается. Если есть но не полностью - `partial`.

**Тип 4: Требование к конфигурации** ("MUST support env variable X")
→ Найди `grep` по имени переменной. Проверь, что она читается и применяется.

### Примеры распространённых ошибок (false positive → partial)

**Ошибка 1: "Код есть → found"**
Спецификация: "Extract MUST accept an optional Getter argument with Keys, Get, GetAll methods"
Код: `Функция Извлечь(Контекст, Заголовки)` - Extract напрямую итерирует Заголовки (Соответствие)
❌ Неправильно: `found` - "код Extract существует"
✅ Правильно: `partial` - "Extract есть, но нет Getter-интерфейса как отдельного объекта с Keys/Get/GetAll"

**Ошибка 2: "Похожий код → found"**
Спецификация: "CreateKey MUST return an opaque object"
Код: `Ключ = "otel-span"` (строковая константа)
❌ Неправильно: `found` - "ключ используется"
✅ Правильно: `not_found` - "нет функции CreateKey, ключи - строки, а не опак-объекты"

**Ошибка 3: "Функция близкой семантики → found"**
Спецификация: "SetGlobalPropagator MUST exist as global API"
Код: `Установить(Сдк)` (устанавливает весь SDK, а не пропагатор отдельно)
❌ Неправильно: `found` - "установка глобального объекта есть"
✅ Правильно: `partial` - "пропагаторы задаются через SDK builder, нет отдельного SetGlobalPropagator"

**Ошибка 4: "Inline-код → found"**
Спецификация: "Resource detectors MUST be implemented as packages separate from the SDK"
Код: Детекция ресурсов захардкожена в `ОтелРесурс.ПриСозданииОбъекта()`
❌ Неправильно: `found` - "ресурсы детектятся"
✅ Правильно: `partial` - "детекция есть, но inline в классе ресурса, а не в отдельных пакетах"

### Общие правила

- **Количество требований ОБЯЗАНО точно совпадать с `expected_keywords` секции**
- Каждый MUST / MUST NOT / SHOULD / SHOULD NOT вне блоков кода - отдельное требование
- Два ключевых слова в одном предложении - два требования
- Текст в `spec_text` - **дословная цитата** из спецификации, не перефразируй
- **При каждом `partial` или `not_found` - добавь пояснение ПОЧЕМУ** в поле `explanation`
- Для `found` поле `explanation` оставь пустой строкой

### Строгие правила n_a

Агент **НЕ ИМЕЕТ ПРАВА** самостоятельно решать, что требование неприменимо.
Статус n_a допустим **ТОЛЬКО** в следующих случаях:

**Ограничения платформы OneScript** (известные, неустранимые):
- Наносекундная точность времени (OneScript поддерживает только миллисекунды)
- TLS/mTLS конфигурация сертификатов
- Многопоточная безопасность контекста на уровне goroutine/thread-local (OneScript использует ФоновыеЗадания)

**Условные фичи** (scope: conditional) - только если фича НЕ реализована:
- B3 Propagator (не реализован)
- Resource Detector Naming (не реализованы детекторы)

> **ЗАПРЕЩЕНО** ставить n_a по причинам вроде:
> - "Optional for OneScript" - если спецификация говорит MUST/SHOULD, это не optional
> - "Not needed for this platform" - не агент решает, что нужно
> - "Implementation choice" - выбор реализации не освобождает от требований спецификации
>
> Если требование находится в секции с заголовком "Optional ...", это НЕ значит n_a.
> Заголовок "Optional" в спецификации означает, что SDK МОЖЕТ реализовать эту функцию,
> но если реализует - ДОЛЖЕН следовать требованиям внутри секции.
> Проверяй код: если функция реализована, требование применимо.
""".strip()


# JSON-схема результата, которую агент должен записать в файл
RESULT_JSON_SCHEMA = r"""
{
  "agent": "<имя агента>",
  "sections": [
    {
      "page": "<страница спецификации>",
      "subsection": "<подраздел>",
      "section_id": "<уникальный идентификатор секции>",
      "spec_url": "<URL секции>",
      "stability": "Stable|Development",
      "scope": "universal|conditional:...",
      "expected_keywords": "<число>",
      "requirements": [
        {
          "level": "MUST|MUST NOT|SHOULD|SHOULD NOT",
          "status": "found|partial|not_found|n_a",
          "spec_text": "Полный текст требования из спецификации",
          "code_location": "path/to/file.os:line или - если не найдено",
          "explanation": "Пояснение для partial/not_found/n_a (пустая строка для found)"
        }
      ]
    }
  ]
}
""".strip()


def group_sections_into_agents(sections):
    """Группирует секции в агентов по доменам с учётом лимита секций.

    Возвращает список: [{"name": str, "code_dirs": [str], "sections": [dict]}]
    """
    agents = []

    for domain_cfg in DOMAIN_CONFIG:
        domain = domain_cfg["domain"]
        pages = domain_cfg["pages"]
        code_dirs = domain_cfg["code_dirs"]

        # Собираем секции для домена, сохраняя порядок из sections.json
        domain_sections = [s for s in sections if s["page"] in pages]
        if not domain_sections:
            continue

        # Разбиваем на группы по MAX_SECTIONS_PER_AGENT
        n_agents = math.ceil(len(domain_sections) / MAX_SECTIONS_PER_AGENT)
        chunk_size = math.ceil(len(domain_sections) / n_agents)

        for i in range(n_agents):
            chunk = domain_sections[i * chunk_size : (i + 1) * chunk_size]
            if not chunk:
                continue

            if n_agents > 1:
                agent_name = f"verify-{domain}-{i + 1}"
            else:
                agent_name = f"verify-{domain}"

            agents.append({
                "name": agent_name,
                "code_dirs": code_dirs,
                "sections": chunk,
            })

    return agents


def build_prompt(agent_name, code_dirs, agent_sections, output_dir):
    """Строит полный промпт для одного агента."""
    results_path = os.path.join(output_dir, "results", f"{agent_name}.json")

    # Формируем блок секций
    sections_block = ""
    total_keywords = 0
    for s in agent_sections:
        total_keywords += s["keywords"]["total"]
        section_id = s.get("section_id", f"{s['page']}/{s['subsection']}")
        sections_block += f"\n{'=' * 60}\n"
        sections_block += (
            f"=== {section_id} "
            f"[{s['stability']}] [{s['scope']}] ===\n"
        )
        sections_block += f"section_id: {section_id}\n"
        sections_block += f"url: {s['url']}\n"
        kw = s["keywords"]
        sections_block += (
            f"expected_keywords: {kw['total']}"
            f" (MUST: {kw['must']}, MUST NOT: {kw['must_not']},"
            f" SHOULD: {kw['should']}, SHOULD NOT: {kw['should_not']})\n"
        )
        sections_block += (
            f"⚠️ Ожидается РОВНО {kw['total']} записей"
            f" requirements для этой секции.\n"
        )
        sections_block += f"{'=' * 60}\n\n"
        sections_block += s["text"] + "\n"

    # Формируем JSON-литерал шаблона для Python-записи
    sections_meta = []
    for s in agent_sections:
        section_id = s.get("section_id", f"{s['page']}/{s['subsection']}")
        sections_meta.append({
            "page": s["page"],
            "subsection": s["subsection"],
            "section_id": section_id,
            "spec_url": s["url"],
            "stability": s["stability"],
            "scope": s["scope"],
            "expected_keywords": s["keywords"]["total"],
            "keywords_breakdown": {
                "MUST": s["keywords"]["must"],
                "MUST NOT": s["keywords"]["must_not"],
                "SHOULD": s["keywords"]["should"],
                "SHOULD NOT": s["keywords"]["should_not"],
            },
        })

    prompt = f"""
{AGENT_INSTRUCTIONS}

---

## Твоё задание

Ты - агент **{agent_name}**.
Тебе назначены {len(agent_sections)} секций спецификации (ровно {total_keywords} keywords MUST/SHOULD).

### Каталоги исходного кода для поиска

{chr(10).join(f"- `{d}`" for d in code_dirs)}

### Формат вывода

После анализа всех секций **запиши результат в JSON-файл** используя Python.
Это критически важно для воспроизводимости - результат должен быть машиночитаемым.

Путь файла результата: `{results_path}`

JSON-схема:
```json
{RESULT_JSON_SCHEMA}
```

**Для записи используй Python** (гарантирует валидный JSON):

```python
import json
results = {{
    "agent": "{agent_name}",
    "sections": [
        # ... твои результаты по каждой секции ...
    ]
}}
with open("{results_path}", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Записано {{len(results['sections'])}} секций")
```

Метаданные секций для JSON (скопируй в результат, добавив `requirements`):
```json
{json.dumps(sections_meta, ensure_ascii=False, indent=2)}
```

### Порядок работы

1. Для каждой секции ниже:
   a. Прочитай полный текст секции **строго сверху вниз**
   b. Извлеки ВСЕ MUST / MUST NOT / SHOULD / SHOULD NOT ключевые слова (пропуская блоки кода)
   c. **Проверь**: количество найденных = `expected_keywords`. Если нет - перечитай и исправь
   d. Для каждого ключевого слова найди реализацию в коде через grep/view
   e. Определи статус (found/partial/not_found/n_a)
2. После анализа ВСЕХ секций - **перед записью проверь** количество requirements в каждой секции = expected_keywords
3. Запиши JSON-файл через Python
4. Выведи сводку в формате: `Секция <id>: expected=<N>, actual=<M>, found=<X>, partial=<Y>, not_found=<Z>, n_a=<W>`

---

## Секции для анализа

{sections_block}
""".strip()

    return prompt


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 generate_prompts.py <output_dir>")
        print()
        print("  <output_dir> - каталог с sections.json (от extract_requirements.py)")
        sys.exit(1)

    output_dir = sys.argv[1]
    sections_file = os.path.join(output_dir, "sections.json")

    if not os.path.exists(sections_file):
        print(f"Ошибка: {sections_file} не найден.")
        print("Сначала запусти extract_requirements.py")
        sys.exit(1)

    with open(sections_file, encoding="utf-8") as f:
        sections = json.load(f)

    print(f"Загружено {len(sections)} секций из {sections_file}")

    # Группируем секции в агентов
    agents = group_sections_into_agents(sections)

    # Создаём каталоги
    prompts_dir = os.path.join(output_dir, "prompts")
    results_dir = os.path.join(output_dir, "results")
    os.makedirs(prompts_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    # Генерируем промпты и конфигурацию
    agents_config = []
    for agent in agents:
        name = agent["name"]
        prompt = build_prompt(name, agent["code_dirs"], agent["sections"], output_dir)

        prompt_file = os.path.join(prompts_dir, f"{name}.md")
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)

        total_kw = sum(s["keywords"]["total"] for s in agent["sections"])
        agent_info = {
            "name": name,
            "code_dirs": agent["code_dirs"],
            "total_keywords": total_kw,
            "sections": [
                {
                    "page": s["page"],
                    "subsection": s["subsection"],
                    "section_id": s.get("section_id", f"{s['page']}/{s['subsection']}"),
                    "url": s["url"],
                    "stability": s["stability"],
                    "scope": s["scope"],
                    "keywords": s["keywords"]["total"],
                }
                for s in agent["sections"]
            ],
        }
        agents_config.append(agent_info)

        section_names = ", ".join(
            f"{s['page']}/{s['subsection']}" for s in agent["sections"]
        )
        print(f"  {name}: {len(agent['sections'])} секций, ~{total_kw} kw")

    # Сохраняем конфигурацию агентов
    agents_file = os.path.join(output_dir, "agents.json")
    with open(agents_file, "w", encoding="utf-8") as f:
        json.dump(agents_config, f, ensure_ascii=False, indent=2)

    print(f"\nСгенерировано {len(agents)} агентов")
    print(f"Промпты: {prompts_dir}/")
    print(f"Конфигурация: {agents_file}")
    print(f"Результаты будут в: {results_dir}/")

    # Итоговая статистика
    total_sections = sum(len(a["sections"]) for a in agents)
    total_keywords = sum(a["total_keywords"] for a in agents_config)
    print(f"\nВсего: {total_sections} секций, ~{total_keywords} keywords")
    print(f"Секций в sections.json: {len(sections)}")
    if total_sections != len(sections):
        missing = len(sections) - total_sections
        print(f"⚠️  {missing} секций не назначены агентам (проверь DOMAIN_CONFIG)")


if __name__ == "__main__":
    main()
