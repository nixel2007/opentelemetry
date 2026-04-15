#!/usr/bin/env python3
"""Генерация промптов для агентов верификации спецификации OpenTelemetry.

Читает sections.json, группирует секции по доменам, генерирует файлы промптов
и конфигурацию агентов.

Использование:
    python3 generate_prompts.py <output_dir> [<codebase_root>]

Аргументы:
    <output_dir>      - каталог с sections.json (от extract_requirements.py)
    <codebase_root>   - корень репозитория (по умолчанию: определяется из расположения скрипта)

Входные данные:
    <output_dir>/sections.json - извлечённые секции (из extract_requirements.py)

Выходные данные:
    <output_dir>/agents.json        - конфигурация агентов (имя → секции, launch_prompt)
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
   - `spec_text` = **предложение целиком** от заглавной буквы до точки/перевода строки.
     **Цитируй дословно из спецификации**, не перефразируй.
     Если предложение длиннее 200 символов, обрезай после 200 символов с суффиксом "..."
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

### Специальные паттерны оценки

**Паттерн: "SHOULD complete or abort within some timeout"**
- Метод принимает параметр таймаута И прерывает операцию при превышении → `found`
- Метод НЕ принимает таймаут, но вызывает внутренний метод с таймаутом (который можно обернуть в async) → `partial`
- Нет механизма прерывания по таймауту → `not_found`

**Паттерн: "SHOULD provide a way to let the caller know whether it succeeded, failed or timed out"**
- Функция возвращает статус/Обещание → `found`
- Процедура (void), ошибки через исключения, но таймаут неотличим от успеха → `partial`
- Нет обработки ошибок → `not_found`

**Паттерн: "Default SHOULD be X" (значение по умолчанию)**
- Дефолтное значение = X → `found`
- Дефолтное значение ≠ X (даже если X поддерживается через конфигурацию) → `not_found`

**Паттерн: "API SHOULD be structured so a user is obligated to provide parameter X"**
- Параметр обязательный позиционный (без значения по умолчанию) → `found`
- Параметр есть, но опциональный (имеет значение по умолчанию) → `partial`
- Параметра нет в сигнатуре → `not_found`
> Спека говорит "obligated to **provide**", а не "validate the value". Валидация значения - отдельное требование.

**Паттерн: "API SHOULD be documented in a way to communicate X"**
- Документирующий комментарий (// перед Функция/Процедура) содержит информацию X → `found`
- Поведение очевидно из названия метода, но нет комментария с X → `partial`
- Нет ни комментария, ни очевидного именования → `not_found`
> Код-комментарий = документация в контексте OneScript.

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

### Примеры распространённых ошибок (false negative → not_found)

> ⚠️ Ложные `not_found` и `partial` так же вредны, как ложные `found`.
> Перед тем как поставить `not_found` - **тщательно поищи** реализацию.

**Ошибка 5: "Не нашёл код → not_found"**
Спецификация: "SHOULD log a message when span attributes/events/links are discarded due to limits"
Код: `Лог.Предупреждение("Спан..." + Имя + "...данные отброшены")` + флаг `ПредупреждениеОтброшенныхВыведено` для once-per-span
❌ Неправильно: `not_found` - "не нашёл логирования"
✅ Правильно: `found` - "Лог.Предупреждение с once-per-span guard через булев флаг"

**Ошибка 6: "Не вижу точного имени → not_found"**
Спецификация: "Values MUST be deduplicated when configuring propagators"
Код: `ВиденныеИмена = Новый Соответствие()` используется как Set для проверки дубликатов
❌ Неправильно: `not_found` - "не нашёл дедупликацию"
✅ Правильно: `found` - "дедупликация через Соответствие (как Set)"

**Ошибка 7: "Поведение по умолчанию → not_found"**
Спецификация: "If no View registered, instrument SHOULD be enabled with default aggregation"
Код: Инструмент без View просто работает с агрегацией по умолчанию - нет явной проверки "есть ли View"
❌ Неправильно: `not_found` - "нет явного fallback на default aggregation"
✅ Правильно: `found` - "инструменты без View автоматически используют агрегацию по умолчанию"

**Ошибка 8: "Мета-требование → not_found"**
Спецификация: "Renaming MUST NOT happen without major version bump"
Это процессное требование (версионная политика), а не функциональный код
❌ Неправильно: `not_found` - "нет кода, который запрещает переименование"
✅ Правильно: `found` - "проект следует семантическому версионированию"

**Ошибка 9: "Нет валидации значения → partial"**
Спецификация: "API SHOULD be structured so a user is obligated to provide this parameter"
Код: `Функция Добавить(Значение, Атрибуты = Неопределено)` - Значение обязательный позиционный
❌ Неправильно: `partial` - "можно передать 0 или пустую строку"
✅ Правильно: `found` - "параметр обязательный позиционный, пользователь обязан его передать"

> Спека говорит "obligated to **provide**", а не "validate". Позиционный параметр без default = пользователь обязан его передать.

**Ошибка 10: "Нет отдельной документации → partial"**
Спецификация: "API SHOULD be documented in a way to communicate X"
Код: метод имеет документирующий комментарий (`// Описание:`) перед определением
❌ Неправильно: `partial` - "нет отдельной документации"
✅ Правильно: `found` - "комментарий перед методом = документация"

> Код-комментарий (// перед Функция/Процедура) = документация в контексте OneScript. Отдельный docsite не требуется.

### Особенности платформы OneScript (ОБЯЗАТЕЛЬНО учитывай при верификации)

**Нативные гарантии платформы (не требуют явного кода):**
- Строки: .NET System.String, полный Unicode (BMP + дополнительные плоскости), длина до 2^31 символов
- Числа: System.Decimal, точность 28 значащих цифр

> Если спека говорит "MUST support BMP Unicode" или "MUST support at least 1023 characters",
> а код принимает строку без ограничений - это `found` (платформа гарантирует).
> Не ставь `not_found` из-за отсутствия явной проверки того, что и так обеспечено рантаймом.

**Встроенные функции для работы со строками:**
- `НРег(Строка)` = `Lower()` - приведение к **нижнему регистру** (case-insensitive). Пример: `НРег("TRUE")` → `"true"`
- `ВРег(Строка)` = `Upper()` - приведение к **верхнему регистру**
- Паттерн `НРег(Значение) = "true"` - это **корректная case-insensitive проверка** на значение "true"

**Сравнение строк:**
- Оператор `=` и `<>` для строк **регистрозависимый** (case-sensitive): `"kb" <> "kB"` → Истина
- Для case-insensitive сравнения используется `НРег()` или `ВРег()`

**Безопасное преобразование числа:**
- `Новый ОписаниеТипов("Число").ПривестиЗначение(Строка)` - возвращает 0 для невалидных строк (без исключения)
- Используется вместо `Число()` для безопасного парсинга

**Именование (русский язык):**
- **ВСЕ** имена классов, методов, переменных в этом SDK - **на русском языке** (это осознанное архитектурное решение)
- `ОтелЛимитыСпана` = SpanLimits, `СгенерироватьTraceId` = GenerateTraceId, `СгенерироватьSpanId` = GenerateSpanId
- Если спецификация требует "class SHOULD be named X" - проверяй по **семантике**, а не по английскому написанию
- Русское имя, **точно семантически совпадающее** с требуемым английским → `found`, НЕ `partial`
- Но если перевод **неточный** (например, `МаксСобытий` = MaxEvents ≠ EventCountLimit) → `partial` **корректен**

### Тщательность поиска (обязательные шаги перед not_found)

Перед тем как поставить `not_found` или `partial`:
1. **Используй grep** по нескольким вариантам ключевых слов (русским И английским)
2. **Прочитай полный файл** соответствующего класса, а не только grep-совпадения
3. **Проверь связанные классы** (например, View-логика может быть в Meter, а не в View; advisory params - в Meter, не в Instrument)
4. **Ищи реализацию "по умолчанию"** - если спека говорит "if X not set, use Y", и в коде Y является поведением по умолчанию без явного условия - это `found`
5. **Проверь приватные методы** (не-Экспорт) - реализация может быть в служебных методах класса

> **ПРАВИЛО**: Требования о версионной политике ("MUST NOT change without major version"),
> обратной совместимости ("SHOULD allow new parameters without breaking"),
> и именовании ("SHOULD be named X") - проверяй по **семантическому соответствию**.
> Процессные/политические требования (версионирование, релизный цикл) → `found` если проект следует семвер.

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
- Число = System.Decimal (не IEEE 754): NaN, Infinity, отрицательный ноль невозможны - операции выбрасывают исключение

**Условные фичи** (scope: conditional) - только если фича НЕ реализована:
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

    # Формируем JSON-литерал шаблона для записи результата
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

После анализа всех секций **запиши результат в JSON-файл**.
Это критически важно для воспроизводимости - результат должен быть машиночитаемым.

Путь файла результата: `{results_path}`

JSON-схема:
```json
{RESULT_JSON_SCHEMA}
```

**КРИТИЧЕСКИ ВАЖНО - как записать результат:**
- Используй инструмент `create` для создания файла `{results_path}` с JSON-содержимым.
- **НЕ создавай промежуточные Python-скрипты** (write_results.py и т.п.) - это засоряет проект.
- **НЕ создавай никаких файлов** кроме `{results_path}`.
- Просто вызови `create` tool с path=`{results_path}` и file_text= полный JSON-результат.

Формат JSON-файла:
```json
{{
  "agent": "{agent_name}",
  "sections": [
    // ... для каждой секции из метаданных ниже, добавь поле "requirements": [...]
  ]
}}
```

Метаданные секций (скопируй в результат, добавив `requirements`):
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
3. Запиши JSON-файл через `create` tool (НЕ через Python-скрипт!)
4. Выведи сводку в формате: `Секция <id>: expected=<N>, actual=<M>, found=<X>, partial=<Y>, not_found=<Z>, n_a=<W>`

---

## Секции для анализа

{sections_block}
""".strip()

    return prompt


def detect_codebase_root():
    """Определяет корень репозитория из расположения скрипта.

    Скрипт находится в .github/skills/spec-analysis/scripts/,
    поэтому корень - на 4 уровня выше.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(script_dir, "..", "..", "..", ".."))
    if os.path.exists(os.path.join(root, "lib.config")):
        return root
    return os.getcwd()


def build_launch_prompt(agent_name, codebase_root, output_dir):
    """Строит короткий промпт для запуска агента через task tool.

    Агент получает этот промпт и сам читает свой файл инструкций.
    """
    prompt_path = os.path.join(output_dir, "prompts", f"{agent_name}.md")
    results_path = os.path.join(output_dir, "results", f"{agent_name}.json")
    return (
        f"Read your full instructions from the file {prompt_path} "
        f"and follow them precisely.\n\n"
        f"The codebase is at {codebase_root} (src/, tests/, lib.config).\n"
        f"Write your JSON result to {results_path} "
        f"exactly as specified in the instructions."
    )


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 generate_prompts.py <output_dir> [<codebase_root>]")
        print()
        print("  <output_dir>    - каталог с sections.json (от extract_requirements.py)")
        print("  <codebase_root> - корень репозитория (опционально)")
        sys.exit(1)

    output_dir = sys.argv[1]
    codebase_root = sys.argv[2] if len(sys.argv) > 2 else detect_codebase_root()
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
        launch_prompt = build_launch_prompt(name, codebase_root, output_dir)
        agent_info = {
            "name": name,
            "launch_prompt": launch_prompt,
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
