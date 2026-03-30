---
name: run-tests
description: >
  Запустить тесты проекта с помощью oneunit. Используй при необходимости
  прогнать юнит-тесты, e2e-тесты, отдельный файл, или получить отчёт покрытия.
---

## Предусловия

Перед первым запуском тестов установи зависимости (может занять 1+ минуту - не прерывай):

```bash
opm install opm && opm install -l --dev
```

## Запуск тестов

Все команды выполняются из **корня проекта**.

### Полный набор тестов

```bash
oneunit execute -d tests -r --mode none
```

> Флаг `--mode none` убирает интерактивный вывод.

### С JUnit-отчётом

```bash
oneunit execute -d tests -r --mode none --junit /tmp/report.xml
```

### Юнит-тесты по домену

```bash
oneunit execute -d tests/unit/Трассировка -r --mode none
oneunit execute -d tests/unit/Метрики -r --mode none
oneunit execute -d tests/unit/Логирование -r --mode none
oneunit execute -d tests/unit/Экспорт -r --mode none
oneunit execute -d tests/unit/Ядро -r --mode none
```

### Один тестовый файл

```bash
oneunit execute -f tests/unit/Ядро/ТестГлобальный.os --mode flat
```

> Для одиночных файлов используй `-f` и `--mode flat`.

### E2E-тесты

```bash
oneunit execute -d tests/e2e -r --mode none
```

### Покрытие кода (Cobertura)

```bash
oneunit execute -d tests -r --cobertura=coverage.xml
```

Целевой уровень покрытия - **95%**.

## Известные особенности

- `oneunit execute -d tests/unit -r` может не находить некоторые библиотеки (например, compressor). Используй `-d tests -r` (от корня tests/) - это надёжнее и совпадает с CI.
- Текущее количество тестов: ~672+.

## Структура тестов

```
tests/
├── unit/           # юнит-тесты по доменам
│   ├── Трассировка/
│   ├── Метрики/
│   ├── Логирование/
│   ├── Экспорт/
│   ├── Ядро/
│   └── Конфигурация/
├── e2e/            # интеграционные тесты
└── helpers/        # вспомогательные скрипты (mock-серверы и т.п.)
```
