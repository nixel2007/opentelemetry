---
title: Семантические соглашения
---

# Семантические соглашения

Какие атрибуты [семантических соглашений OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/)
заполняет SDK, а какие задаёт приложение или коллектор. В таблицах — stable-атрибуты semconv
(версия 1.44.0); атрибуты в статусе development отмечены отдельно.

## Ресурс

Ресурс по умолчанию ([ОтелРесурс](/api/opentelemetry/Ядро/ОтелРесурс.md)) получают автоконфигурация
через переменные окружения, файловая конфигурация и `Новый ОтелРесурс()`. Атрибуты детекторов
ресурса в нём описаны схемой `https://opentelemetry.io/schemas/1.44.0`.

| Атрибут | Кто заполняет | Как задать самому |
|---|---|---|
| `service.name` | SDK: `unknown_service:oscript`, если имя не задано | `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES`, `resource` файловой конфигурации |
| `service.version`, `service.namespace`, `service.instance.id` | не заполняются | `OTEL_RESOURCE_ATTRIBUTES`, `resource` файловой конфигурации, [ОтелПостроительРесурса](/api/opentelemetry/Ядро/ОтелПостроительРесурса.md) |
| `telemetry.sdk.name`, `telemetry.sdk.version`, `telemetry.sdk.language` | SDK: `opentelemetry`, версия пакета, `oscript` | — |
| `deployment.environment.name` | не заполняется: окружение знает только приложение | как `service.version`. Для стандартных окружений используйте значения semconv: `production`, `staging`, `test`, `development` |
| `container.id` | детектор [ОтелДетекторРесурсаКонтейнера](/api/opentelemetry/Ядро/ОтелДетекторРесурсаКонтейнера.md): только на Linux и только в контейнере | — |
| `container.image.name`, `container.image.tags`, `container.image.repo_digests` | не заполняются: изнутри процесса их не узнать | имя — `OTEL_RESOURCE_ATTRIBUTES`; теги и дайджесты — массивы строк, только `resource.attributes` файловой конфигурации с типом `string_array`. В Kubernetes их может добавить коллектор (процессор `k8sattributes`) |

Прежнее имя `deployment.environment` в semconv устарело, используйте `deployment.environment.name`.

Атрибуты в статусе development, которые заполняют детекторы ресурса по умолчанию:

| Атрибут | Детектор |
|---|---|
| `host.name`, `os.type` | [ОтелДетекторРесурсаХоста](/api/opentelemetry/Ядро/ОтелДетекторРесурсаХоста.md) |
| `process.pid` | [ОтелДетекторРесурсаПроцесса](/api/opentelemetry/Ядро/ОтелДетекторРесурсаПроцесса.md) |
| `host.cpu.model.name`, `host.arch` | [ОтелДетекторРесурсаПроцессора](/api/opentelemetry/Ядро/ОтелДетекторРесурсаПроцессора.md) |

## Исключения

[ОтелСпан.ЗаписатьИсключение](/api/opentelemetry/Трассировка/ОтелСпан.md) и запись лога с
исключением ([ОтелЗаписьЛога](/api/opentelemetry/Логирование/ОтелЗаписьЛога.md)) заполняют
атрибуты исключения:

| Атрибут | Значение |
|---|---|
| `exception.message` | описание ошибки |
| `exception.type` | код ошибки библиотеки errors или код нативной ошибки OneScript (native-errors); у нераспознанной ошибки не заполняется |
| `exception.stacktrace` | стек вызовов |

Для `error.type` в спанах и метриках библиотеки инструментирования берут значение из
[ОтелУтилиты.ТипОшибки](/api/opentelemetry/Ядро/ОтелУтилиты.md): тот же тип или `_OTHER`.

В semconv запись исключения событием спана помечена устаревшей, stable-конвенция — исключения в
логах. SDK пока записывает исключение событием спана.
