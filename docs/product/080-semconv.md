---
title: Семантические соглашения
---

# Семантические соглашения

Какие атрибуты [семантических соглашений OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/)
заполняет SDK. В таблицах — stable-атрибуты semconv (версия 1.44.0); атрибуты в статусах
development и release candidate отмечены отдельно. Группы атрибутов названы так же, как в semconv.

## Ресурс

Автоконфигурация через переменные окружения и файловая конфигурация собирают ресурс SDK из
ресурса по умолчанию и атрибутов детекторов ([ОтелРесурсы](/api/opentelemetry/Ядро/ОтелРесурсы.md)).
Атрибуты детекторов ресурса описаны схемой `https://opentelemetry.io/schemas/1.44.0`. Провайдер,
которому ресурс не передан, получает только ресурс по умолчанию: `service.name` и `telemetry.sdk.*`.

### Service

[Service](https://opentelemetry.io/docs/specs/semconv/registry/entities/service/#service)

| Атрибут | Значение |
|---|---|
| `service.name` | `unknown_service:oscript`, если имя не задано через `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES` или `resource` файловой конфигурации |

### Service Instance

[Service Instance](https://opentelemetry.io/docs/specs/semconv/registry/entities/service/#service-instance)

| Атрибут | Значение |
|---|---|
| `service.instance.id` | детектор [ОтелДетекторРесурсаЭкземпляраСервиса](/api/opentelemetry/Ядро/ОтелДетекторРесурсаЭкземпляраСервиса.md): случайный UUID, один на процесс, если значение не задано через `OTEL_RESOURCE_ATTRIBUTES` или `resource` файловой конфигурации |

### Telemetry Sdk

[Telemetry Sdk](https://opentelemetry.io/docs/specs/semconv/registry/entities/telemetry/#telemetry-sdk)

| Атрибут | Значение |
|---|---|
| `telemetry.sdk.language` | `oscript` |
| `telemetry.sdk.name` | `oscript-opentelemetry`: значение `opentelemetry` по semconv зарезервировано за официальным SDK проекта OpenTelemetry |
| `telemetry.sdk.version` | версия пакета |

### Container

[Container](https://opentelemetry.io/docs/specs/semconv/registry/entities/container/#container)

| Атрибут | Значение |
|---|---|
| `container.id` | детектор [ОтелДетекторРесурсаКонтейнера](/api/opentelemetry/Ядро/ОтелДетекторРесурсаКонтейнера.md): только на Linux и только в контейнере |

### Атрибуты в статусах development и release candidate

Атрибуты, которые заполняют детекторы ресурса по умолчанию. Атрибуты Process — в статусе
release candidate, остальные — development.

#### Host

[Host](https://opentelemetry.io/docs/specs/semconv/registry/entities/host/#host)

| Атрибут | Детектор |
|---|---|
| `host.arch` | [ОтелДетекторРесурсаПроцессора](/api/opentelemetry/Ядро/ОтелДетекторРесурсаПроцессора.md) |
| `host.name` | [ОтелДетекторРесурсаХоста](/api/opentelemetry/Ядро/ОтелДетекторРесурсаХоста.md) |

#### Host CPU

[Host CPU](https://opentelemetry.io/docs/specs/semconv/registry/entities/host/#host-cpu)

| Атрибут | Детектор |
|---|---|
| `host.cpu.model.name` | [ОтелДетекторРесурсаПроцессора](/api/opentelemetry/Ядро/ОтелДетекторРесурсаПроцессора.md) |

#### OS

[OS](https://opentelemetry.io/docs/specs/semconv/registry/entities/os/#os)

| Атрибут | Детектор |
|---|---|
| `os.type` | [ОтелДетекторРесурсаХоста](/api/opentelemetry/Ядро/ОтелДетекторРесурсаХоста.md) |

#### Process

[Process](https://opentelemetry.io/docs/specs/semconv/registry/entities/process/#process)

| Атрибут | Детектор |
|---|---|
| `process.pid` | [ОтелДетекторРесурсаПроцесса](/api/opentelemetry/Ядро/ОтелДетекторРесурсаПроцесса.md) |

## Исключения

[Exceptions](https://opentelemetry.io/docs/specs/semconv/exceptions/)

[ОтелСпан.ЗаписатьИсключение](/api/opentelemetry/Трассировка/ОтелСпан.md) и запись лога с
исключением ([ОтелЗаписьЛога](/api/opentelemetry/Логирование/ОтелЗаписьЛога.md)) заполняют
атрибуты исключения:

| Атрибут | Значение |
|---|---|
| `exception.message` | описание ошибки |
| `exception.type` | код ошибки библиотеки errors или код нативной ошибки OneScript (native-errors); у нераспознанной ошибки не заполняется |
| `exception.stacktrace` | стек вызовов |

## Error

[Error](https://opentelemetry.io/docs/specs/semconv/registry/attributes/error/)

| Атрибут | Кто заполняет |
|---|---|
| `error.type` | библиотеки инструментирования в спанах и метриках: значение [ОтелУтилиты.ТипОшибки](/api/opentelemetry/Ядро/ОтелУтилиты.md) — тип ошибки или `_OTHER` |
