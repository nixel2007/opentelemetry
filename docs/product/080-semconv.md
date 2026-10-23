---
title: Семантические соглашения
---

# Семантические соглашения

Какие атрибуты [семантических соглашений OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/)
заполняет SDK, а какие задаёт приложение или коллектор. В таблицах — stable-атрибуты semconv
(версия 1.44.0); атрибуты в статусе development отмечены отдельно. Группы атрибутов названы так же,
как в semconv.

## Ресурс

Ресурс по умолчанию ([ОтелРесурс](/api/opentelemetry/Ядро/ОтелРесурс.md)) получают автоконфигурация
через переменные окружения, файловая конфигурация и `Новый ОтелРесурс()`. Атрибуты детекторов
ресурса в нём описаны схемой `https://opentelemetry.io/schemas/1.44.0`.

Атрибуты, которые SDK не заполняет, задаются через `OTEL_RESOURCE_ATTRIBUTES`, `resource` файловой
конфигурации или [ОтелПостроительРесурса](/api/opentelemetry/Ядро/ОтелПостроительРесурса.md).

### Service

[Service](https://opentelemetry.io/docs/specs/semconv/registry/entities/service/#service)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `service.name` | SDK: `unknown_service:oscript`, если имя не задано | `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES`, `resource` |
| `service.version` | не заполняется | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |

### Service Instance

[Service Instance](https://opentelemetry.io/docs/specs/semconv/registry/entities/service/#service-instance)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `service.instance.id` | не заполняется | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |

### Service Namespace

[Service Namespace](https://opentelemetry.io/docs/specs/semconv/registry/entities/service/#service-namespace)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `service.namespace` | не заполняется | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |

### Telemetry Distro

[Telemetry Distro](https://opentelemetry.io/docs/specs/semconv/registry/entities/telemetry/#telemetry-distro)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `telemetry.distro.name` | не заполняется | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |
| `telemetry.distro.version` | не заполняется | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |

### Telemetry Sdk

[Telemetry Sdk](https://opentelemetry.io/docs/specs/semconv/registry/entities/telemetry/#telemetry-sdk)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `telemetry.sdk.language` | SDK: `oscript` | — |
| `telemetry.sdk.name` | SDK: `opentelemetry` | — |
| `telemetry.sdk.version` | SDK: версия пакета | — |

### Deployment

[Deployment](https://opentelemetry.io/docs/specs/semconv/registry/entities/deployment/#deployment)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `deployment.environment.name` | не заполняется: окружение знает только приложение | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |

Для стандартных окружений используйте значения semconv: `production`, `staging`, `test`,
`development`. Прежнее имя `deployment.environment` в semconv устарело.

### Container

[Container](https://opentelemetry.io/docs/specs/semconv/registry/entities/container/#container)

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `container.id` | детектор [ОтелДетекторРесурсаКонтейнера](/api/opentelemetry/Ядро/ОтелДетекторРесурсаКонтейнера.md): только на Linux и только в контейнере | — |

### Container Image

[Container Image](https://opentelemetry.io/docs/specs/semconv/registry/entities/container/#container-image)

Изнутри процесса атрибуты образа не узнать. В Kubernetes их может добавить коллектор
(процессор `k8sattributes`).

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `container.image.name` | не заполняется | `OTEL_RESOURCE_ATTRIBUTES`, `resource`, `ОтелПостроительРесурса` |
| `container.image.tags` | не заполняется | массив строк: `resource.attributes` файловой конфигурации с типом `string_array` |
| `container.image.repo_digests` | не заполняется | массив строк: `resource.attributes` файловой конфигурации с типом `string_array` |

### Атрибуты в статусе development

Атрибуты, которые заполняют детекторы ресурса по умолчанию.

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

В semconv запись исключения событием спана помечена устаревшей, stable-конвенция — исключения в
логах. SDK пока записывает исключение событием спана.

## Error

[Error](https://opentelemetry.io/docs/specs/semconv/registry/attributes/error/)

| Атрибут | Кто заполняет |
|---|---|
| `error.type` | библиотеки инструментирования в спанах и метриках: значение [ОтелУтилиты.ТипОшибки](/api/opentelemetry/Ядро/ОтелУтилиты.md) — тип ошибки или `_OTHER` |
