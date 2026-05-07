# OpenTelemetry SDK для OneScript

[![Quality Gate](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=alert_status)](https://sonar.openbsl.ru/dashboard?id=opentelemetry)
[![Coverage](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=coverage)](https://sonar.openbsl.ru/component_measures?id=opentelemetry&metric=coverage)
[![Bugs](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=bugs)](https://sonar.openbsl.ru/project/issues?id=opentelemetry&resolved=false&types=BUG)
[![Code Smells](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=code_smells)](https://sonar.openbsl.ru/project/issues?id=opentelemetry&resolved=false&types=CODE_SMELL)
[![Lines of Code](https://sonar.openbsl.ru/api/project_badges/measure?project=opentelemetry&metric=ncloc)](https://sonar.openbsl.ru/component_measures?id=opentelemetry&metric=ncloc)
[![OTel Spec](https://img.shields.io/badge/OTel_Spec-v1.55.0-blueviolet)](docs/spec-compliance.md)
[![Telegram](https://img.shields.io/badge/Telegram-чат-blue?logo=telegram)](https://t.me/autumn_winow)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/nixel2007/opentelemetry)

Библиотека на [OneScript](https://oscript.io) для использования [OpenTelemetry](https://opentelemetry.io) в оскриптовых проектах. Реализует [спецификацию OpenTelemetry v1.55.0](https://github.com/open-telemetry/opentelemetry-specification/releases/tag/v1.55.0).

Позволяет собирать и отправлять телеметрию (трассировку, логи, метрики) в формате OTLP в любой совместимый коллектор — [Grafana LGTM](https://grafana.com/oss/), [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) и другие. Поддерживает HTTP/JSON, HTTP/Protobuf и gRPC.

## Установка

```bash
opm install opentelemetry
```

## Быстрый старт

```bash
export OTEL_SERVICE_NAME=my-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

```bsl
#Использовать opentelemetry

Сдк = ОтелАвтоконфигурация.Инициализировать();

Трассировщик = Сдк.ПолучитьТрассировщик("my-library");

Спан = Трассировщик.НачатьСпан("операция", ОтелВидСпана.Сервер());
Область = Спан.СделатьТекущим();
// ... работа ...
Область.Закрыть();
Спан.Завершить();
```

## Совместимость

- OneScript 2.0.0+
- logos 1.7.1+, 1connector 2.2.1+, collectionos 0.8.2+, configor 0.11.1+, async 0.3.0+
- oint 1.33.0+ (для gRPC-транспорта)

## Документация

- [Руководство пользователя](https://autumn-library.github.io/opentelemetry/)
- [Справочник API](https://autumn-library.github.io/api/opentelemetry/)

## Лицензия

MIT
