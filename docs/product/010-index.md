---
title: OpenTelemetry SDK для OneScript
---

# OpenTelemetry SDK для OneScript

[![Quality Gate](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=alert_status)](https://sonar.openbsl.ru/dashboard?id=opentelemetry)
[![Coverage](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=coverage)](https://sonar.openbsl.ru/component_measures?id=opentelemetry&metric=coverage)
[![Bugs](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=bugs)](https://sonar.openbsl.ru/project/issues?id=opentelemetry&resolved=false&types=BUG)
[![Code Smells](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=code_smells)](https://sonar.openbsl.ru/project/issues?id=opentelemetry&resolved=false&types=CODE_SMELL)
[![Lines of Code](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=ncloc)](https://sonar.openbsl.ru/component_measures?id=opentelemetry&metric=ncloc)
[![OTel Spec](https://img.shields.io/badge/OTel_Spec-v1.55.0-blueviolet)](https://github.com/open-telemetry/opentelemetry-specification/releases/tag/v1.55.0)
[![Telegram](https://img.shields.io/badge/Telegram-чат-blue?logo=telegram)](https://t.me/autumn_winow)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/nixel2007/opentelemetry)

Библиотека на [OneScript](https://oscript.io) для использования [OpenTelemetry](https://opentelemetry.io) в оскриптовых проектах. Реализует [спецификацию OpenTelemetry v1.55.0](https://github.com/open-telemetry/opentelemetry-specification/releases/tag/v1.55.0).

Позволяет собирать и отправлять телеметрию (трассировку, логи, метрики) в формате OTLP в любой совместимый коллектор — [Grafana LGTM](https://grafana.com/oss/), [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) и другие.

## Возможности

| Подсистема | Описание |
|-----------|----------|
| **Автоконфигурация** | Настройка SDK из переменных окружения или файла конфигурации (через [configor](https://github.com/oscript-library/configor)) |
| **Трассировка** | Спаны, вложенные спаны, атрибуты, события, линки, статусы, семплирование |
| **Логирование** | Записи логов с уровнями серьёзности и корреляцией с трассировкой |
| **Метрики** | Счётчики, реверсивные счётчики, датчики, гистограммы, экспоненциальные гистограммы, наблюдаемые инструменты |
| **Пропагация** | W3C Trace Context, W3C Baggage, B3 (отдельный пакет), композитный пропагатор |
| **Экспорт** | OTLP/HTTP (JSON и Protobuf), OTLP/gRPC, InMemory (для тестов), TLS |
| **Интеграция с logos** | Аппендер для [logos](https://github.com/oscript-library/logos), перенаправляющий логи в OpenTelemetry |
| **Пакетная обработка** | Batch-процессоры для спанов и логов с фоновым экспортом |

## Установка

```bash
opm install opentelemetry
```

Все зависимости (logos, 1connector, collectionos, configor, async) устанавливаются автоматически.

## Быстрый старт

Самый простой способ настроить OpenTelemetry — через автоконфигурацию. Достаточно задать переменные окружения и вызвать `ОтелАвтоконфигурация.Инициализировать()`.

:::code-group

```bash [Переменные окружения]
export OTEL_SERVICE_NAME=my-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

```bsl [Код приложения]
#Использовать opentelemetry

// Автоконфигурация из переменных окружения
Сдк = ОтелАвтоконфигурация.Инициализировать();

// Получение трассировщика и метра через SDK
Трассировщик = Сдк.ПолучитьТрассировщик("my-library");
Метр = Сдк.ПолучитьМетр("my-library");

// Создание спана
Спан = Трассировщик.НачатьСпан("операция", ОтелВидСпана.Сервер());
Область = Спан.СделатьТекущим();
// ... работа ...
Область.Закрыть();
Спан.Завершить();

// Или через глобальный доступ из любого места кода
Трассировщик = ОтелГлобальный.ПолучитьТрассировщик("другая-библиотека");
```

```json [Файл конфигурации (configor)]
{
    "otel": {
        "service": { "name": "my-service" },
        "exporter": {
            "otlp": {
                "endpoint": "http://localhost:4318",
                "protocol": "http/protobuf"
            }
        }
    }
}
```

:::

## Требования

| Зависимость | Минимальная версия |
|-------------|-------------------|
| OneScript | 2.0.0+ |
| logos | 1.7.1+ |
| 1connector | 2.2.1+ |
| collectionos | 0.8.2+ |
| configor | 0.11.1+ |
| async | 0.3.0+ |
| oint | 1.33.0+ (только для gRPC-транспорта) |

## Дальнейшее изучение

- [Автоконфигурация](/opentelemetry/autoconfig.md) — настройка через переменные окружения и файл конфигурации
- [Трассировка](/opentelemetry/tracing.md) — спаны, атрибуты, события, семплирование
- [Логирование](/opentelemetry/logging.md) — записи логов, интеграция с logos
- [Метрики](/opentelemetry/metrics.md) — инструменты измерения, периодический экспорт
- [Пропагация](/opentelemetry/propagation.md) — W3C Trace Context, Baggage, B3
- [Экспорт](/opentelemetry/export.md) — транспорты HTTP, gRPC, InMemory, TLS
