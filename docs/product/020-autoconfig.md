---
title: Автоконфигурация
---

# Автоконфигурация

Модуль `ОтелАвтоконфигурация` — рекомендуемый способ инициализации SDK. Он следует [спецификации переменных окружения OpenTelemetry](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/) и автоматически создаёт все необходимые провайдеры (трассировки, логирования, метрик), настраивает экспортеры, процессоры и пропагаторы.

## Как работает автоконфигурация

1. Читает параметры из переменных окружения (`OTEL_*`) и/или файла конфигурации через [configor](https://github.com/oscript-library/configor).
2. Создаёт транспорт (HTTP или gRPC) согласно `OTEL_EXPORTER_OTLP_PROTOCOL`.
3. Строит провайдеры трассировки, логирования и метрик с batch-процессорами.
4. Регистрирует SDK глобально через `ОтелГлобальный`.
5. Возвращает готовый объект `ОтелSdk`.

## Инициализация

```bsl
#Использовать opentelemetry

Сдк = ОтелАвтоконфигурация.Инициализировать();

// Получение трассировщика
Трассировщик = Сдк.ПолучитьТрассировщик("my-library");

// Получение метра
Метр = Сдк.ПолучитьМетр("my-library");

// Глобальный доступ из любого места кода
Трассировщик2 = ОтелГлобальный.ПолучитьТрассировщик("other-library");
```

## Настройка через переменные окружения

Переменные окружения читаются автоматически. Имена переменных соответствуют стандарту OpenTelemetry: `OTEL_FOO_BAR` → ключ configor `otel.foo.bar`.

:::code-group

```bash [Минимальная конфигурация]
export OTEL_SERVICE_NAME=my-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

```bash [HTTP/JSON транспорт]
export OTEL_SERVICE_NAME=my-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production,team=backend
```

```bash [gRPC транспорт]
export OTEL_SERVICE_NAME=my-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
```

```bash [Отключение SDK]
export OTEL_SDK_DISABLED=true
```

:::

## Настройка через файл конфигурации (configor)

Путь к файлу задаётся переменной `OTEL_CONFIG_FILE` или программно. Поддерживаются форматы JSON и YAML.

:::code-group

```json [JSON конфигурация]
{
    "otel": {
        "service": {
            "name": "my-service"
        },
        "exporter": {
            "otlp": {
                "endpoint": "http://otel-collector:4318",
                "protocol": "http/protobuf",
                "headers": "Authorization=Bearer token123",
                "compression": "gzip",
                "timeout": "10000"
            }
        },
        "traces": {
            "sampler": "parentbased_traceidratio",
            "sampler": {
                "arg": "0.1"
            }
        },
        "propagators": "tracecontext,baggage"
    }
}
```

```yaml [YAML конфигурация]
otel:
  service:
    name: my-service
  exporter:
    otlp:
      endpoint: http://otel-collector:4318
      protocol: http/protobuf
      compression: gzip
  traces:
    sampler: parentbased_always_on
  propagators: tracecontext,baggage
```

```bash [Указание пути к файлу]
export OTEL_CONFIG_FILE=/etc/myapp/otel-config.json
```

:::

## Полная таблица переменных окружения

### Общие параметры SDK

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_SDK_DISABLED` | `otel.sdk.disabled` | `false` | Отключить SDK. При `true` создаётся NoOp SDK |
| `OTEL_SERVICE_NAME` | `otel.service.name` | — | Имя сервиса (`service.name` в ресурсе) |
| `OTEL_RESOURCE_ATTRIBUTES` | `otel.resource.attributes` | — | Дополнительные атрибуты ресурса, формат: `key1=value1,key2=value2` |
| `OTEL_SDK_SHUTDOWN_TIMEOUT` | `otel.sdk.shutdown.timeout` | `30000` | Таймаут завершения SDK в миллисекундах |
| `OTEL_CONFIG_FILE` | `otel.config.file` | — | Путь к файлу конфигурации configor (YAML/JSON) |

### Экспортеры

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_TRACES_EXPORTER` | `otel.traces.exporter` | `otlp` | Экспортер трассировки: `otlp`, `none` |
| `OTEL_LOGS_EXPORTER` | `otel.logs.exporter` | `otlp` | Экспортер логов: `otlp`, `none` |
| `OTEL_METRICS_EXPORTER` | `otel.metrics.exporter` | `otlp` | Экспортер метрик: `otlp`, `none` |

### OTLP — общие параметры

Применяются ко всем сигналам, если не заданы per-signal переопределения.

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `otel.exporter.otlp.endpoint` | `http://localhost:4318` (HTTP) / `http://localhost:4317` (gRPC) | Адрес OTLP-коллектора |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `otel.exporter.otlp.protocol` | `http/protobuf` | Протокол: `http/json`, `http/protobuf`, `grpc` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `otel.exporter.otlp.headers` | — | Заголовки HTTP/gRPC, формат: `key1=value1,key2=value2` |
| `OTEL_EXPORTER_OTLP_COMPRESSION` | `otel.exporter.otlp.compression` | `none` | Сжатие: `gzip`, `none` |
| `OTEL_EXPORTER_OTLP_TIMEOUT` | `otel.exporter.otlp.timeout` | `10000` | Таймаут запроса в миллисекундах |
| `OTEL_EXPORTER_OTLP_CERTIFICATE` | `otel.exporter.otlp.certificate` | — | Путь к CA-сертификату (PEM) |
| `OTEL_EXPORTER_OTLP_CLIENT_KEY` | `otel.exporter.otlp.client.key` | — | Путь к клиентскому приватному ключу (PEM) |
| `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` | `otel.exporter.otlp.client.certificate` | — | Путь к клиентскому сертификату (PEM) |
| `OTEL_EXPORTER_OTLP_INSECURE` | `otel.exporter.otlp.insecure` | `false` | Отключить проверку TLS-сертификата |

### OTLP — трассировка (per-signal)

Переопределяют общие `OTEL_EXPORTER_OTLP_*` для сигнала трассировки.

| Переменная | Описание |
|------------|----------|
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Адрес коллектора |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL` | Протокол |
| `OTEL_EXPORTER_OTLP_TRACES_HEADERS` | Заголовки |
| `OTEL_EXPORTER_OTLP_TRACES_COMPRESSION` | Сжатие |
| `OTEL_EXPORTER_OTLP_TRACES_TIMEOUT` | Таймаут (мс) |
| `OTEL_EXPORTER_OTLP_TRACES_CERTIFICATE` | CA-сертификат (PEM) |
| `OTEL_EXPORTER_OTLP_TRACES_CLIENT_KEY` | Клиентский ключ (PEM) |
| `OTEL_EXPORTER_OTLP_TRACES_CLIENT_CERTIFICATE` | Клиентский сертификат (PEM) |

### OTLP — логирование (per-signal)

| Переменная | Описание |
|------------|----------|
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | Адрес коллектора |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL` | Протокол |
| `OTEL_EXPORTER_OTLP_LOGS_HEADERS` | Заголовки |
| `OTEL_EXPORTER_OTLP_LOGS_COMPRESSION` | Сжатие |
| `OTEL_EXPORTER_OTLP_LOGS_TIMEOUT` | Таймаут (мс) |
| `OTEL_EXPORTER_OTLP_LOGS_CERTIFICATE` | CA-сертификат (PEM) |
| `OTEL_EXPORTER_OTLP_LOGS_CLIENT_KEY` | Клиентский ключ (PEM) |
| `OTEL_EXPORTER_OTLP_LOGS_CLIENT_CERTIFICATE` | Клиентский сертификат (PEM) |

### OTLP — метрики (per-signal)

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` | — | Адрес коллектора |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL` | — | Протокол |
| `OTEL_EXPORTER_OTLP_METRICS_HEADERS` | — | Заголовки |
| `OTEL_EXPORTER_OTLP_METRICS_COMPRESSION` | — | Сжатие |
| `OTEL_EXPORTER_OTLP_METRICS_TIMEOUT` | — | Таймаут (мс) |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | `cumulative` | Временная агрегация: `cumulative`, `delta`, `lowmemory` |
| `OTEL_EXPORTER_OTLP_METRICS_DEFAULT_HISTOGRAM_AGGREGATION` | `explicit_bucket_histogram` | Агрегация гистограммы: `explicit_bucket_histogram`, `base2_exponential_bucket_histogram` |
| `OTEL_EXPORTER_OTLP_METRICS_CERTIFICATE` | — | CA-сертификат (PEM) |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` | — | Клиентский ключ (PEM) |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | — | Клиентский сертификат (PEM) |

### Семплирование трассировки

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_TRACES_SAMPLER` | `otel.traces.sampler` | `parentbased_always_on` | Стратегия сэмплирования |
| `OTEL_TRACES_SAMPLER_ARG` | `otel.traces.sampler.arg` | `1.0` | Аргумент сэмплера (доля для `traceidratio`) |

Поддерживаемые значения `OTEL_TRACES_SAMPLER`:

| Значение | Описание |
|----------|----------|
| `always_on` | Сэмплировать все спаны |
| `always_off` | Не сэмплировать ничего |
| `traceidratio` | Случайная доля (задаётся через `OTEL_TRACES_SAMPLER_ARG`) |
| `parentbased_always_on` | ParentBased(root=AlwaysOn) |
| `parentbased_always_off` | ParentBased(root=AlwaysOff) |
| `parentbased_traceidratio` | ParentBased(root=TraceIdRatio) |

### Пакетный процессор спанов (BatchSpanProcessor)

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_BSP_MAX_QUEUE_SIZE` | `otel.bsp.max.queue.size` | `2048` | Максимальный размер очереди |
| `OTEL_BSP_SCHEDULE_DELAY` | `otel.bsp.schedule.delay` | `5000` | Интервал запуска экспорта (мс) |
| `OTEL_BSP_MAX_EXPORT_BATCH_SIZE` | `otel.bsp.max.export.batch.size` | `512` | Максимальный размер пакета |
| `OTEL_BSP_EXPORT_TIMEOUT` | `otel.bsp.export.timeout` | `30000` | Таймаут экспорта (мс) |

> Пакетный процессор логов использует те же параметры, но со значением по умолчанию `OTEL_BSP_SCHEDULE_DELAY = 1000` мс.

### Периодический экспорт метрик

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_METRIC_EXPORT_INTERVAL` | `otel.metric.export.interval` | `60000` | Интервал экспорта метрик (мс) |
| `OTEL_METRICS_EXEMPLAR_FILTER` | `otel.metrics.exemplar.filter` | `trace_based` | Фильтр exemplars: `always_on`, `always_off`, `trace_based` |

### Пропагаторы контекста

| Переменная | Ключ configor | По умолчанию | Описание |
|------------|--------------|-------------|----------|
| `OTEL_PROPAGATORS` | `otel.propagators` | `tracecontext,baggage` | Пропагаторы через запятую |

Поддерживаемые значения:

| Значение | Описание |
|----------|----------|
| `tracecontext` | W3C Trace Context |
| `baggage` | W3C Baggage |
| `b3` | B3 Single Header (требуется пакет [`opentelemetry-propagator-b3`](https://github.com/nixel2007/opentelemetry-propagator-b3)) |
| `b3multi` | B3 Multi Header (требуется тот же пакет) |
| `none` | Отключить все пропагаторы |

### Ограничения атрибутов

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_ATTRIBUTE_COUNT_LIMIT` | `128` | Максимальное число атрибутов (все сигналы) |
| `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` | без ограничения | Максимальная длина строкового атрибута |
| `OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT` | наследует `OTEL_ATTRIBUTE_COUNT_LIMIT` | Переопределение для спанов |
| `OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT` | наследует `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` | Переопределение для спанов |
| `OTEL_SPAN_EVENT_COUNT_LIMIT` | `128` | Максимальное число событий в спане |
| `OTEL_SPAN_LINK_COUNT_LIMIT` | `128` | Максимальное число ссылок в спане |
| `OTEL_EVENT_ATTRIBUTE_COUNT_LIMIT` | `128` | Максимальное число атрибутов события |
| `OTEL_LINK_ATTRIBUTE_COUNT_LIMIT` | `128` | Максимальное число атрибутов ссылки |
| `OTEL_LOGRECORD_ATTRIBUTE_COUNT_LIMIT` | наследует `OTEL_ATTRIBUTE_COUNT_LIMIT` | Переопределение для записей лога |
| `OTEL_LOGRECORD_ATTRIBUTE_VALUE_LENGTH_LIMIT` | наследует `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` | Переопределение для записей лога |

## Смотрите также

- [Трассировка](/opentelemetry/tracing.md) — ручная настройка провайдера трассировки
- [Логирование](/opentelemetry/logging.md) — ручная настройка провайдера логирования
- [Метрики](/opentelemetry/metrics.md) — ручная настройка провайдера метрик
- [Экспорт](/opentelemetry/export.md) — транспорты и TLS
- [Пропагация](/opentelemetry/propagation.md) — пропагаторы контекста
