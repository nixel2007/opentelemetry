---
name: static-analysis
description: >
  Запустить статический анализ кода с помощью BSL Language Server (BSLLS)
  или проверку синтаксиса через oscript -check. Используй для проверки
  качества кода перед коммитом.
---

## BSL Language Server (BSLLS)

Статический анализ кода. Запускается из **корня проекта**.

> **ВАЖНО:** Анализ нужно запускать по ОБОИМ каталогам - `src` и `tests`. Не пропускай тесты!

### Порядок работы

Выходной файл SARIF один и тот же, поэтому **нельзя** запускать оба каталога подряд - второй запуск перетрёт результаты первого. Работай последовательно:

1. Анализ `src` → исправление замечаний
2. Анализ `tests` → исправление замечаний

### Анализ src

```bash
bsl-language-server analyze -s src -r sarif -o out
```

Прочитай результат, исправь замечания.

### Анализ tests

```bash
bsl-language-server analyze -s tests -r sarif -o out
```

Прочитай результат, исправь замечания.

### Анализ конкретной папки

```bash
bsl-language-server analyze -s src/Метрики -r sarif -o out
```

Результат сохраняется в `out/` в формате SARIF.

### Чтение результатов SARIF

```bash
python3 -c "
import json, glob
for f in glob.glob('out/*.sarif'):
    data = json.load(open(f))
    for run in data.get('runs', []):
        for r in run.get('results', []):
            loc = r.get('locations', [{}])[0].get('physicalLocation', {})
            path = loc.get('artifactLocation', {}).get('uri', '?')
            line = loc.get('region', {}).get('startLine', '?')
            print(f'{path}:{line}: [{r[\"ruleId\"]}] {r[\"message\"][\"text\"]}')
"
```

## Проверка синтаксиса (oscript -check)

```bash
find src -name "*.os" -exec oscript -check {} -env=src/fake-entrypoint.os \;
find tests -name "*.os" -exec oscript -check {} -env=src/fake-entrypoint.os \;
```

> `oscript -check` может ложно падать на неизвестных переменных и внешних типах - это особенность реализации интерпретатора. Для надёжной проверки используй запуск тестов.

## Правила обработки замечаний

| Правило | Действие |
|---------|----------|
| `MissingSpace` | **ВСЕГДА исправляй** добавлением пробела. Никогда не подавляй |
| `MagicNumber` | В продакшене - выноси в именованную константу. Не подавляй |
| `MagicNumber` в enum-модулях | Подавление допустимо |
| `NumberOfOptionalParams` | Подавление допустимо при необходимости (конструкторы с множеством параметров) |
| `Typo` | Исправляй опечатку. Добавление слова в словарь исключений - **только по согласованию с пользователем** |

### Подавление в тестах

В тестовых файлах допустимо подавлять в начале файла:

```bsl
// BSLLS:MagicNumber-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
```

**Никогда не подавляй `MissingSpace`** - всегда исправляй.

## Цели качества

- **0 новых замечаний** в добавляемом коде
- Покрытие тестами: **95%**
- Отчёты публикуются в SonarQube и Coveralls через CI (`qa.yml`)
