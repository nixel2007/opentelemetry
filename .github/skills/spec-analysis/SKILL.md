---
name: spec-analysis
description: >
  Провести полный анализ соответствия спецификации OpenTelemetry.
  Парсит спецификацию с сайта, извлекает MUST/SHOULD требования,
  проверяет каждое требование по коду и генерирует docs/spec-compliance.md.
---

## Обзор

Скилл выполняет **spec-first анализ соответствия** реализации спецификации OpenTelemetry.
Результат - файл `docs/spec-compliance.md` с трассируемым чеклистом: каждое MUST/SHOULD требование привязано к конкретному файлу и строке в коде.

## Шаг 1: Извлечение требований из спецификации

Запусти Python-скрипт для парсинга всех страниц спецификации OTel.

> **ВАЖНО:** Скрипт загружает 12 страниц с opentelemetry.io. Убедись, что есть доступ в интернет.

```bash
python3 .github/skills/spec-analysis/extract_requirements.py /tmp/otel-specs
```

Скрипт:
1. Загружает 12 страниц спецификации (Context, Baggage API, Resource SDK, Trace API, Trace SDK, Logs Bridge API, Logs SDK, Metrics API, Metrics SDK, OTLP Exporter, Propagators, SDK Environment Variables)
2. Извлекает все предложения с MUST/MUST NOT/SHOULD/SHOULD NOT
3. Фильтрует Development-статус требования и дедуплицирует
4. Сохраняет результат в `/tmp/otel-specs/requirements.json`

Ожидаемый результат: ~750+ требований в JSON. Никакой дедупликации не производится - каждая строка спецификации с ключевым словом сохраняется как отдельное требование.

## Шаг 2: Верификация требований по коду

Для каждого раздела спецификации запусти **параллельных explore-агентов** (до 5 одновременно), каждый получает:
- Список требований из `requirements.json` для своего раздела
- Путь к исходникам (`src/`)

Разделение на агентов:

| Агент | Разделы спецификации | Каталоги кода |
|---|---|---|
| verify-core | Context, Baggage Api, Resource Sdk, Propagators | `src/Ядро/`, `src/Пропагация/` |
| verify-traces | Trace Api, Trace Sdk | `src/Трассировка/` |
| verify-logs | Logs Api, Logs Sdk | `src/Логирование/` |
| verify-metrics | Metrics Api, Metrics Sdk | `src/Метрики/` |
| verify-export | Otlp Exporter, Env Vars | `src/Экспорт/`, `src/Конфигурация/` |

Каждый агент должен для **каждого** требования определить статус:
- **found** - реализовано. Указать файл:строка
- **partial** - частично. Указать что отсутствует
- **not_found** - не реализовано
- **n_a** - неприменимо к платформе

Формат вывода агента:
```
[ID] STATUS | file:line | краткое пояснение
```

## Шаг 3: Генерация документа

Запусти скрипт генерации, передав JSON с результатами верификации:

```bash
python3 .github/skills/spec-analysis/generate_compliance.py /tmp/otel-specs/requirements.json /tmp/otel-specs/verification.json docs/spec-compliance.md
```

Скрипт генерирует `docs/spec-compliance.md` со следующей структурой:
- Сводка (общий процент, MUST/SHOULD отдельно)
- Таблица по разделам
- Ключевые несоответствия (MUST отдельно, SHOULD отдельно)
- Детальные таблицы по каждому разделу (требование -> статус -> код)
- Ограничения платформы OneScript
- Методология

## Шаг 4: Сравнение с предыдущей версией

Если `docs/spec-compliance.md` уже существует в git, сравни старую и новую версии:

```bash
git --no-pager diff docs/spec-compliance.md
```

Обрати внимание на:
- Изменения в общем проценте соответствия
- Новые несоответствия (регрессии)
- Исправленные несоответствия (прогресс)

## Шаг 5: Коммит

```bash
git add docs/spec-compliance.md
git commit -m "docs: обновить анализ соответствия спецификации OpenTelemetry vX.Y.Z

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

## Ограничения платформы OneScript

При анализе учитывай, что OneScript не поддерживает:
- Нативный protobuf (HTTP/JSON вместо HTTP/protobuf)
- Наносекундную точность времени (только миллисекунды)
- TLS/mTLS конфигурацию сертификатов
- B3/X-Ray пропагаторы (только W3C TraceContext и W3C Baggage)

## Версия спецификации

Текущая версия спецификации определяется автоматически из заголовка страницы при парсинге. Если версия изменилась, обнови бейдж в README.md:

```markdown
[![OTel Spec](https://img.shields.io/badge/OTel_Spec-vX.Y.Z-blueviolet)](docs/spec-compliance.md)
```
