# Переменные окружения OpenTelemetry SDK

Полный список поддерживаемых переменных окружения `OTEL_*`.

Переменные читаются через [configor](https://github.com/oscript-library/configor): `OTEL_FOO_BAR` → ключ `otel.foo.bar`.  
Альтернативно параметры можно задать через файл конфигурации configor или программно через `МенеджерПараметров`.

---

## Общие параметры SDK

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_SDK_DISABLED` | `false` | Отключить SDK. При `true` создаётся NoOp SDK (без экспортеров, сэмплер `always_off`) |
| `OTEL_SERVICE_NAME` | - | Имя сервиса (`service.name` в ресурсе) |
| `OTEL_RESOURCE_ATTRIBUTES` | - | Дополнительные атрибуты ресурса, формат: `key1=value1,key2=value2` |
| `OTEL_SDK_SHUTDOWN_TIMEOUT` | `30000` | Таймаут завершения SDK в миллисекундах |
| `OTEL_CONFIG_FILE` | - | Путь к файлу конфигурации configor (YAML/JSON) |
| `OTEL_EXPERIMENTAL_CONFIG_FILE` | - | **Устарела.** Используйте `OTEL_CONFIG_FILE` |

---

## Экспортеры

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_TRACES_EXPORTER` | `otlp` | Экспортер трассировки: `otlp`, `none` |
| `OTEL_LOGS_EXPORTER` | `otlp` | Экспортер логов: `otlp`, `none` |
| `OTEL_METRICS_EXPORTER` | `otlp` | Экспортер метрик: `otlp`, `none` |

---

## OTLP - общие параметры

Применяются ко всем сигналам, если не заданы per-signal переопределения.

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318` (HTTP) / `http://localhost:4317` (gRPC) | Адрес OTLP-коллектора |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | Протокол: `http/json`, `http/protobuf`, `grpc` |
| `OTEL_EXPORTER_OTLP_HEADERS` | - | Заголовки HTTP/gRPC, формат: `key1=value1,key2=value2` |
| `OTEL_EXPORTER_OTLP_COMPRESSION` | `none` | Сжатие: `gzip`, `none` |
| `OTEL_EXPORTER_OTLP_TIMEOUT` | `10000` | Таймаут запроса в миллисекундах |
| `OTEL_EXPORTER_OTLP_CERTIFICATE` | - | Путь к CA-сертификату (PEM) |
| `OTEL_EXPORTER_OTLP_CLIENT_KEY` | - | Путь к клиентскому приватному ключу (PEM) |
| `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` | - | Путь к клиентскому сертификату (PEM) |
| `OTEL_EXPORTER_OTLP_INSECURE` | `false` | Отключить проверку TLS-сертификата |

---

## OTLP - трассировка (per-signal)

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

---

## OTLP - логирование (per-signal)

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

---

## OTLP - метрики (per-signal)

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` | - | Адрес коллектора |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL` | - | Протокол |
| `OTEL_EXPORTER_OTLP_METRICS_HEADERS` | - | Заголовки |
| `OTEL_EXPORTER_OTLP_METRICS_COMPRESSION` | - | Сжатие |
| `OTEL_EXPORTER_OTLP_METRICS_TIMEOUT` | - | Таймаут (мс) |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | `cumulative` | Временная агрегация: `cumulative`, `delta`, `lowmemory` |
| `OTEL_EXPORTER_OTLP_METRICS_DEFAULT_HISTOGRAM_AGGREGATION` | `explicit_bucket_histogram` | Агрегация гистограммы: `explicit_bucket_histogram`, `base2_exponential_bucket_histogram` |
| `OTEL_EXPORTER_OTLP_METRICS_CERTIFICATE` | - | CA-сертификат (PEM) |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` | - | Клиентский ключ (PEM) |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | - | Клиентский сертификат (PEM) |

---

## Семплирование трассировки

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_TRACES_SAMPLER` | `always_on` | Стратегия сэмплирования |
| `OTEL_TRACES_SAMPLER_ARG` | `1.0` | Аргумент сэмплера (доля для `traceidratio`) |

Поддерживаемые значения `OTEL_TRACES_SAMPLER`:

| Значение | Описание |
|----------|----------|
| `always_on` | Сэмплировать все спаны |
| `always_off` | Не сэмплировать ничего |
| `traceidratio` | Случайная доля (задаётся через `OTEL_TRACES_SAMPLER_ARG`, по умолчанию `1.0`) |
| `parentbased_always_on` | ParentBased(root=AlwaysOn) |
| `parentbased_always_off` | ParentBased(root=AlwaysOff) |
| `parentbased_traceidratio` | ParentBased(root=TraceIdRatio) |
| `jaeger_remote` | Jaeger Remote (только с предупреждением, не реализован) |
| `parentbased_jaeger_remote` | ParentBased(root=JaegerRemote) (только с предупреждением, не реализован) |

---

## Пакетный процессор спанов (BatchSpanProcessor)

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_BSP_MAX_QUEUE_SIZE` | `2048` | Максимальный размер очереди |
| `OTEL_BSP_SCHEDULE_DELAY` | `5000` | Интервал запуска экспорта (мс) |
| `OTEL_BSP_MAX_EXPORT_BATCH_SIZE` | `512` | Максимальный размер пакета |
| `OTEL_BSP_EXPORT_TIMEOUT` | `30000` | Таймаут экспорта (мс) |

> Пакетный процессор логов использует те же параметры, но с дефолтом `OTEL_BSP_SCHEDULE_DELAY = 1000` мс.

---

## Периодический экспорт метрик

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_METRIC_EXPORT_INTERVAL` | `60000` | Интервал экспорта метрик (мс) |
| `OTEL_METRICS_EXEMPLAR_FILTER` | `trace_based` | Фильтр exemplars: `always_on`, `always_off`, `trace_based` |

---

## Пропагаторы контекста

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `OTEL_PROPAGATORS` | `tracecontext,baggage` | Пропагаторы через запятую |

Поддерживаемые значения:

| Значение | Описание |
|----------|----------|
| `tracecontext` | W3C Trace Context |
| `baggage` | W3C Baggage |
| `b3` | B3 Single Header (требуется пакет [`opentelemetry-propagator-b3`](https://github.com/nixel2007/opentelemetry-propagator-b3)) |
| `b3multi` | B3 Multi Header (требуется тот же пакет) |
| `none` | Отключить все пропагаторы |

---

## Ограничения атрибутов

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
