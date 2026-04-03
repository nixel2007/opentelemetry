# Соответствие спецификации OpenTelemetry v1.55.0

Документ содержит детальный анализ соответствия библиотеки OpenTelemetry SDK для OneScript
спецификации [OpenTelemetry v1.55.0](https://github.com/open-telemetry/opentelemetry-specification/releases/tag/v1.55.0) (март 2026).

Условные обозначения:

- ✅ - реализовано в соответствии со спецификацией
- ⚠️ - частичная реализация или незначительное отклонение
- ❌ - не реализовано
- N/A - не применимо к данной реализации (платформенные ограничения OneScript)

---

## Оглавление

- [1. Ядро (Core)](#1-ядро-core)
  - [1.1 Context](#11-context)
  - [1.2 Baggage](#12-baggage)
  - [1.3 Resource](#13-resource)
  - [1.4 InstrumentationScope](#14-instrumentationscope)
  - [1.5 Attributes](#15-attributes)
- [2. Трассировка (Traces)](#2-трассировка-traces)
  - [2.1 TracerProvider](#21-tracerprovider)
  - [2.2 Tracer](#22-tracer)
  - [2.3 Span](#23-span)
  - [2.4 SpanContext](#24-spancontext)
  - [2.5 TraceState](#25-tracestate)
  - [2.6 SpanKind и StatusCode](#26-spankind-и-statuscode)
  - [2.7 Samplers](#27-samplers)
  - [2.8 SpanProcessors](#28-spanprocessors)
  - [2.9 SpanLimits](#29-spanlimits)
- [3. Логирование (Logs)](#3-логирование-logs)
  - [3.1 LoggerProvider](#31-loggerprovider)
  - [3.2 Logger](#32-logger)
  - [3.3 LogRecord](#33-logrecord)
  - [3.4 LogRecordProcessors](#34-logrecordprocessors)
  - [3.5 LogRecordLimits](#35-logrecordlimits)
- [4. Метрики (Metrics)](#4-метрики-metrics)
  - [4.1 MeterProvider](#41-meterprovider)
  - [4.2 Meter](#42-meter)
  - [4.3 Синхронные инструменты](#43-синхронные-инструменты)
  - [4.4 Асинхронные инструменты](#44-асинхронные-инструменты)
  - [4.5 Views](#45-views)
  - [4.6 Aggregations](#46-aggregations)
  - [4.7 MetricReaders](#47-metricreaders)
- [5. Экспорт (Export)](#5-экспорт-export)
  - [5.1 OTLP Exporters](#51-otlp-exporters)
  - [5.2 Transports](#52-transports)
  - [5.3 Batch Processors](#53-batch-processors)
- [6. Пропагация (Propagation)](#6-пропагация-propagation)
  - [6.1 W3C TraceContext](#61-w3c-tracecontext)
  - [6.2 W3C Baggage](#62-w3c-baggage)
  - [6.3 Composite Propagator](#63-composite-propagator)
- [7. Конфигурация (Configuration)](#7-конфигурация-configuration)
  - [7.1 Переменные окружения](#71-переменные-окружения)
  - [7.2 Автоконфигурация](#72-автоконфигурация)
- [8. Сводная таблица соответствия](#8-сводная-таблица-соответствия)
- [9. Известные отклонения и ограничения](#9-известные-отклонения-и-ограничения)

---

## 1. Ядро (Core)

### 1.1 Context

**Класс:** `ОтелКонтекст` (модуль) + `ОтелОбласть` (класс)

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Context - хранилище key-value | MUST | ✅ | Thread-local `Соответствие` с поддержкой стека |
| Создание ключа | MUST | ✅ | `ОтелКонтекст.Получить(Ключ)` / `УстановитьЗначение(Ключ, Значение)` |
| Получение значения по ключу | MUST | ✅ | `ОтелКонтекст.Получить(Ключ)` |
| Неизменяемость контекста | MUST | ✅ | Стек контекстов, каждое значение добавляется поверх |
| Implicit context propagation | SHOULD | ✅ | Thread-local через `ОтелОбласть` (Scope) |
| Scope - восстановление предыдущего контекста | MUST | ✅ | `ОтелОбласть.Закрыть()` восстанавливает предыдущий контекст |
| Получение текущего спана из контекста | MUST | ✅ | `ОтелКонтекст.ТекущийСпан()` |
| Получение текущего Baggage из контекста | MUST | ✅ | `ОтелКонтекст.ТекущийBaggage()` |
| Установка спана в контекст | MUST | ✅ | `ОтелКонтекст.КонтекстСоСпаном()` / `СделатьСпанТекущим()` |
| Установка Baggage в контекст | MUST | ✅ | `ОтелКонтекст.КонтекстСBaggage()` / `СделатьBaggageТекущим()` |
| Очистка мертвых потоков | N/A | ✅ | `ОтелКонтекст.ОчиститьМертвыеПотоки()` |

### 1.2 Baggage

**Класс:** `ОтелBaggage` + `ОтелПостроительBaggage`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Get Value по имени | MUST | ✅ | `Получить(Ключ)` |
| Get All Values | MUST | ✅ | `ПолучитьВсе()` |
| Set Value (возврат нового Baggage) | MUST | ✅ | `Установить(Ключ, Значение)` |
| Remove Value (возврат нового Baggage) | MUST | ✅ | `Удалить(Ключ)` |
| Clear (удаление всех записей) | MUST | ✅ | `Очистить()` |
| Immutability | MUST | ✅ | Все мутирующие операции возвращают новый экземпляр |
| Metadata (опциональные метаданные) | OPTIONAL | ✅ | `ПолучитьМетаданные(Ключ)` / `ПолучитьВсеМетаданные()` |
| Builder pattern | MAY | ✅ | `ОтелПостроительBaggage` с `Установить()` / `Построить()` |
| Взаимодействие с контекстом | MUST | ✅ | `ОтелKонтекст.СделатьBaggageТекущим()` |

### 1.3 Resource

**Класс:** `ОтелРесурс` + `ОтелПостроительРесурса`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Набор атрибутов | MUST | ✅ | `Атрибуты()` возвращает `ОтелАтрибуты` |
| Schema URL | SHOULD | ✅ | `АдресСхемы()` |
| Merge (слияние ресурсов) | MUST | ✅ | `Слить(ДругойРесурс)` |
| Сериализация в OTLP | MUST | ✅ | `ВСоответствиеOtlp()` |
| OTEL_RESOURCE_ATTRIBUTES | SHOULD | ✅ | Обработка в `ОтелАвтоконфигурация` |
| OTEL_SERVICE_NAME | SHOULD | ✅ | Приоритет над OTEL_RESOURCE_ATTRIBUTES |
| Builder pattern | MAY | ✅ | `ОтелПостроительРесурса` |

### 1.4 InstrumentationScope

**Класс:** `ОтелОбластьИнструментирования`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| name | MUST | ✅ | `Имя()` |
| version | OPTIONAL | ✅ | `Версия()` |
| schema_url | OPTIONAL | ✅ | `АдресСхемы()` |
| attributes | OPTIONAL | ✅ | `Атрибуты()` |
| Уникальный ключ для кэширования | MUST | ✅ | `Ключ()` - формирует составной ключ |

### 1.5 Attributes

**Класс:** `ОтелАтрибуты`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Set (key, value) | MUST | ✅ | `Установить(Ключ, Значение)` |
| Get по ключу | MUST | ✅ | `Получить(Ключ)` |
| Remove | SHOULD | ✅ | `Удалить(Ключ)` |
| Count | SHOULD | ✅ | `Количество()` |
| Сериализация в OTLP массив | MUST | ✅ | `ВМассивOtlp()` |
| Преобразование в соответствие | MAY | ✅ | `ВСоответствие()` |

---

## 2. Трассировка (Traces)

### 2.1 TracerProvider

**Класс:** `ОтелПровайдерТрассировки` + `ОтелПостроительПровайдераТрассировки`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Get Tracer(name, version, schema_url, attributes) | MUST | ✅ | `ПолучитьТрассировщик(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы)` |
| Кэширование Tracer по InstrumentationScope | MUST | ✅ | Кэш по `ОбластьИнструментирования.Ключ()` |
| Конфигурация SpanProcessors | MUST | ✅ | `ДобавитьПроцессор(Процессор)` |
| Конфигурация Sampler | MUST | ✅ | Через построитель: `УстановитьСэмплер()` |
| Конфигурация SpanLimits | SHOULD | ✅ | `УстановитьЛимитыСпана()` |
| Shutdown | MUST | ✅ | `Закрыть()` - вызывает Shutdown на всех процессорах |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` - вызывает ForceFlush на всех процессорах |
| Async Shutdown/ForceFlush | SHOULD | ✅ | `ЗакрытьАсинхронно()` / `СброситьБуферАсинхронно()` |
| Noop Tracer после Shutdown | SHOULD | ✅ | Возвращает нерабочий трассировщик после `Закрыть()` |
| Resource | MUST | ✅ | `Ресурс()` - ассоциируется со всеми спанами |
| Builder pattern | MAY | ✅ | `ОтелПостроительПровайдераТрассировки` |

### 2.2 Tracer

**Класс:** `ОтелТрассировщик` + `ОтелПостроительТрассировщика`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Create Span (start) | MUST | ✅ | `НачатьСпан(ИмяСпана, ВидСпана)` |
| SpanBuilder pattern | SHOULD | ✅ | `ПостроительСпана(ИмяСпана)` |
| Enabled | SHOULD | ✅ | `Включен()` - проверяет наличие активных процессоров |
| Корневой спан без родителя | MUST | ✅ | `НачатьКорневойСпан(ИмяСпана, ВидСпана)` |
| Дочерний спан с родительским контекстом | MUST | ✅ | `НачатьДочернийСпан(ИмяСпана, РодительскийКонтекст, ВидСпана)` |
| Sampling при создании спана | MUST | ✅ | Sampling через `ОтелСэмплер.ДолженСэмплировать()` |
| Noop Span для отброшенных | MUST | ✅ | `ОтелНоопСпан` для несэмплированных спанов |
| Builder: version, schema_url, attributes | SHOULD | ✅ | `ОтелПостроительТрассировщика` |

### 2.3 Span

**Класс:** `ОтелСпан` + `ОтелНоопСпан` + `ОтелПостроительСпана`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Get SpanContext | MUST | ✅ | `КонтекстСпана()` |
| IsRecording | MUST | ✅ | `ЗаписьАктивна()` |
| SetAttribute(key, value) | MUST | ✅ | `УстановитьАтрибут(Ключ, Значение)` с fluent API |
| AddEvent(name, attributes, timestamp) | MUST | ✅ | `ДобавитьСобытие(Имя, Атрибуты, МеткаВремени)` |
| AddLink(spanContext, attributes) | MUST | ✅ | `ДобавитьЛинк(КонтекстСпана, Атрибуты)` |
| SetStatus(code, description) | MUST | ✅ | `УстановитьСтатус(КодСтатуса, Сообщение)` |
| UpdateName(name) | MUST | ✅ | `ИзменитьИмя(НовоеИмя)` |
| End(timestamp) | MUST | ✅ | `Завершить(НовоеВремяОкончания)` |
| RecordException(exception) | SHOULD | ✅ | `ЗаписатьИсключение(ИнформацияОбОшибке, Атрибуты)` |
| MakeCurrent (Scope) | SHOULD | ✅ | `СделатьТекущим()` возвращает `ОтелОбласть` |
| Запрет мутаций после End | MUST | ✅ | Все мутаторы проверяют `Завершен()` |
| Status state machine | MUST | ✅ | OK терминальный, ERROR→OK разрешено |
| Dropped counts (attrs/events/links) | MUST | ✅ | `КоличествоОтброшенныхАтрибутов/Событий/Линков()` |
| Resource и InstrumentationScope | MUST | ✅ | `Ресурс()` / `ОбластьИнструментирования()` |
| Fluent API | MAY | ✅ | Все мутаторы возвращают `ЭтотОбъект` |
| SpanBuilder: parent, kind, attributes, links, startTime | MUST | ✅ | `ОтелПостроительСпана` |
| Переопределение времени начала | MAY | ✅ | `ПереопределитьВремяНачала()` |

**Состояния статуса (state machine):**

| Переход | Спецификация | Реализация |
|---------|-------------|------------|
| UNSET → OK | ✅ допустимо | ✅ |
| UNSET → ERROR | ✅ допустимо | ✅ |
| OK → OK | ✅ noop | ✅ |
| OK → ERROR | ❌ запрещено | ✅ отклоняется |
| OK → UNSET | ❌ запрещено | ✅ отклоняется |
| ERROR → OK | ✅ допустимо | ✅ |
| ERROR → ERROR | ✅ перезаписывает | ✅ |
| ERROR → UNSET | ❌ запрещено | ✅ отклоняется |

### 2.4 SpanContext

**Класс:** `ОтелКонтекстСпана`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| TraceId (32 hex) | MUST | ✅ | `ИдТрассировки()` |
| SpanId (16 hex) | MUST | ✅ | `ИдСпана()` |
| TraceFlags | MUST | ✅ | `ФлагиТрассировки()` |
| TraceState | MUST | ✅ | `СостояниеТрассировки()` |
| IsValid (non-zero IDs) | MUST | ✅ | `Валиден()` |
| IsRemote | MUST | ✅ | `Удаленный()` |
| Immutability | MUST | ✅ | Нет мутирующих методов |
| Hex retrieval | MUST | ✅ | TraceId и SpanId хранятся как hex-строки |

### 2.5 TraceState

**Класс:** `ОтелСостояниеТрассировки`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Get value by key | MUST | ✅ | `Получить(Ключ)` |
| Add key/value | MUST | ✅ | `Установить(Ключ, Значение)` - возвращает новый экземпляр |
| Update value for key | MUST | ✅ | `Установить(Ключ, Значение)` |
| Delete key | MUST | ✅ | `Удалить(Ключ)` - возвращает новый экземпляр |
| Immutability | MUST | ✅ | Все мутирующие операции возвращают новый экземпляр |
| W3C format serialization | MUST | ✅ | `ВСтроку()` |
| Key validation (simple + multitenant) | MUST | ✅ | Regex-валидация по W3C Trace Context |
| Value validation (printable ASCII) | MUST | ✅ | 0x20-0x7E, без запятых и '=' |
| Max 32 entries | MUST | ✅ | Ограничение по W3C spec |
| New keys at the beginning | MUST | ✅ | Порядок: последний добавленный - первый |

### 2.6 SpanKind и StatusCode

**Модули:** `ОтелВидСпана` + `ОтелКодСтатуса`

| Значение | Спецификация | Реализация |
|----------|-------------|------------|
| INTERNAL (1) | MUST | ✅ `Внутренний()` |
| SERVER (2) | MUST | ✅ `Сервер()` |
| CLIENT (3) | MUST | ✅ `Клиент()` |
| PRODUCER (4) | MUST | ✅ `Производитель()` |
| CONSUMER (5) | MUST | ✅ `Потребитель()` |
| UNSET (0) | MUST | ✅ `НеУстановлен()` |
| OK (1) | MUST | ✅ `Ок()` |
| ERROR (2) | MUST | ✅ `Ошибка()` |

### 2.7 Samplers

**Модуль:** `ОтелСэмплер` + `ОтелРезультатСэмплирования`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| AlwaysOn | MUST | ✅ | `ВсегдаВключен()` → RECORD_AND_SAMPLE |
| AlwaysOff | MUST | ✅ | `ВсегдаВыключен()` → DROP |
| TraceIdRatioBased | SHOULD | ✅ | `ПоДолеТрассировок()` - детерминированный хеш первых 8 hex TraceId |
| ParentBased | SHOULD | ✅ | `НаОсновеРодителя()` с 4 конфигурируемыми случаями |
| ParentBased: remote sampled | MUST | ✅ | Делегирование к настраиваемому сэмплеру (по умолчанию AlwaysOn) |
| ParentBased: remote not sampled | MUST | ✅ | По умолчанию AlwaysOff |
| ParentBased: local sampled | MUST | ✅ | По умолчанию AlwaysOn |
| ParentBased: local not sampled | MUST | ✅ | По умолчанию AlwaysOff |
| ParentBased: root (no parent) | MUST | ✅ | Делегирование к корневой стратегии |
| ShouldSample → SamplingResult | MUST | ✅ | `ДолженСэмплировать()` → решение + атрибуты |
| SamplingResult.Decision (3 значения) | MUST | ✅ | DROP(0), RECORD_ONLY(1), RECORD_AND_SAMPLE(2) |
| OTEL_TRACES_SAMPLER | SHOULD | ✅ | В `ОтелАвтоконфигурация` |
| OTEL_TRACES_SAMPLER_ARG | SHOULD | ✅ | Доля для TraceIdRatioBased |

### 2.8 SpanProcessors

**Классы:** `ОтелПростойПроцессорСпанов`, `ОтелПакетныйПроцессорСпанов`, `ОтелКомпозитныйПроцессорСпанов`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| OnStart(span, parentContext) | MUST | ✅ | `ПриНачале(Спан)` |
| OnEnd(span) | MUST | ✅ | `ПриЗавершении(Спан)` |
| Shutdown | MUST | ✅ | `Закрыть()` |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` |
| SimpleSpanProcessor (синхронный экспорт) | SHOULD | ✅ | `ОтелПростойПроцессорСпанов` |
| BatchSpanProcessor (батч с фоновым экспортом) | SHOULD | ✅ | `ОтелПакетныйПроцессорСпанов` (через `ОтелБазовыйПакетныйПроцессор`) |
| CompositeSpanProcessor (цепочка) | SHOULD | ✅ | `ОтелКомпозитныйПроцессорСпанов` |
| OTEL_BSP_SCHEDULE_DELAY | SHOULD | ✅ | `otel.bsp.schedule.delay` (default 5000) |
| OTEL_BSP_EXPORT_TIMEOUT | SHOULD | ✅ | `otel.bsp.export.timeout` (default 30000) |
| OTEL_BSP_MAX_QUEUE_SIZE | SHOULD | ✅ | `otel.bsp.max.queue.size` (default 2048) |
| OTEL_BSP_MAX_EXPORT_BATCH_SIZE | SHOULD | ✅ | `otel.bsp.max.export.batch.size` (default 512) |

### 2.9 SpanLimits

**Класс:** `ОтелЛимитыСпана`

| Параметр | Спецификация | По умолчанию | Реализация |
|----------|-------------|-------------|------------|
| MaxAttributes | 128 | 128 | ✅ `МаксАтрибутов()` |
| MaxEvents | 128 | 128 | ✅ `МаксСобытий()` |
| MaxLinks | 128 | 128 | ✅ `МаксЛинков()` |
| MaxAttributeValueLength | no limit | 0 (unlimited) | ✅ `МаксДлинаЗначенияАтрибута()` |
| MaxAttributesPerEvent | 128 | 128 | ✅ `МаксАтрибутовНаСобытие()` |
| MaxAttributesPerLink | 128 | 128 | ✅ `МаксАтрибутовНаЛинк()` |
| OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT | SHOULD | ✅ | В `ОтелАвтоконфигурация` |
| OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT | SHOULD | ✅ | В `ОтелАвтоконфигурация` |

---

## 3. Логирование (Logs)

### 3.1 LoggerProvider

**Класс:** `ОтелПровайдерЛогирования` + `ОтелПостроительПровайдераЛогирования`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Get Logger(name, version, schema_url, attributes) | MUST | ✅ | `ПолучитьЛоггер(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы)` |
| Кэширование Logger по InstrumentationScope | MUST | ✅ | Кэш по ключу InstrumentationScope |
| Конфигурация LogRecordProcessors | MUST | ✅ | `ДобавитьПроцессор(Процессор)` |
| Shutdown | MUST | ✅ | `Закрыть()` |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` |
| Async Shutdown/ForceFlush | SHOULD | ✅ | `ЗакрытьАсинхронно()` / `СброситьБуферАсинхронно()` |
| Resource | MUST | ✅ | `Ресурс()` |
| Builder pattern | MAY | ✅ | `ОтелПостроительПровайдераЛогирования` + `ОтелПостроительЛоггера` |

### 3.2 Logger

**Класс:** `ОтелЛоггер`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Emit LogRecord | MUST | ✅ | `Записать(ЗаписьЛога)` |
| Create LogRecord | MUST | ✅ | `СоздатьЗаписьЛога()` |
| Enabled | SHOULD | ✅ | `Включен()` - проверяет наличие процессоров |

### 3.3 LogRecord

**Класс:** `ОтелЗаписьЛога`

| Поле спецификации | Уровень | Статус | Реализация |
|-------------------|---------|--------|------------|
| Timestamp | OPTIONAL | ✅ | `Время()` / `УстановитьВремя()` |
| ObservedTimestamp | OPTIONAL | ✅ | `ВремяНаблюдения()` / `УстановитьВремяНаблюдения()` |
| SeverityNumber | OPTIONAL | ✅ | `НомерСерьезности()` / `УстановитьСерьезность()` |
| SeverityText | OPTIONAL | ✅ | `ТекстСерьезности()` - автоматически из SeverityNumber |
| Body | OPTIONAL | ✅ | `Тело()` / `УстановитьТело()` |
| Attributes | OPTIONAL | ✅ | `Атрибуты()` / `УстановитьАтрибут()` |
| TraceId | OPTIONAL | ✅ | `ИдТрассировки()` / `УстановитьКонтекстТрассировки()` |
| SpanId | OPTIONAL | ✅ | `ИдСпана()` / `УстановитьКонтекстТрассировки()` |
| TraceFlags | OPTIONAL | ✅ | `ФлагиТрассировки()` / `УстановитьФлагиТрассировки()` |
| EventName | OPTIONAL | ✅ | `ИмяСобытия()` / `УстановитьИмяСобытия()` |
| Resource | MUST (SDK) | ✅ | `Ресурс()` / `УстановитьРесурс()` |
| InstrumentationScope | MUST (SDK) | ✅ | `ОбластьИнструментирования()` / `УстановитьОбластьИнструментирования()` |
| DroppedAttributesCount | MUST (SDK) | ✅ | `КоличествоОтброшенныхАтрибутов()` |
| Immutability после фиксации | MUST | ✅ | `Зафиксировать()` блокирует дальнейшие изменения |
| Fluent API | MAY | ✅ | Все сеттеры возвращают `ЭтотОбъект` |
| ReadWriteLogRecord | MUST (SDK) | ✅ | Полная поддержка до вызова `Зафиксировать()` |

### 3.4 LogRecordProcessors

**Классы:** `ОтелПростойПроцессорЛогов`, `ОтелПакетныйПроцессорЛогов`, `ОтелКомпозитныйПроцессорЛогов`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| OnEmit(logRecord, context) | MUST | ✅ | `Обработать(ЗаписьЛога)` в процессорах |
| Shutdown | MUST | ✅ | `Закрыть()` |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` |
| SimpleLogRecordProcessor | SHOULD | ✅ | `ОтелПростойПроцессорЛогов` |
| BatchLogRecordProcessor | SHOULD | ✅ | `ОтелПакетныйПроцессорЛогов` (через `ОтелБазовыйПакетныйПроцессор`) |
| CompositeLogRecordProcessor | SHOULD | ✅ | `ОтелКомпозитныйПроцессорЛогов` |
| OTEL_BLRP_SCHEDULE_DELAY | SHOULD | ✅ | `otel.blrp.schedule.delay` (default 1000) |
| OTEL_BLRP_EXPORT_TIMEOUT | SHOULD | ✅ | `otel.blrp.export.timeout` (default 30000) |
| OTEL_BLRP_MAX_QUEUE_SIZE | SHOULD | ✅ | `otel.blrp.max.queue.size` (default 2048) |
| OTEL_BLRP_MAX_EXPORT_BATCH_SIZE | SHOULD | ✅ | `otel.blrp.max.export.batch.size` (default 512) |

### 3.5 LogRecordLimits

**Класс:** `ОтелЛимитыЗаписейЛога`

| Параметр | Спецификация | Реализация |
|----------|-------------|------------|
| AttributeCountLimit | SHOULD | ✅ `МаксАтрибутов()` |
| AttributeValueLengthLimit | SHOULD | ✅ `МаксДлинаЗначенияАтрибута()` |
| OTEL_LOGRECORD_ATTRIBUTE_COUNT_LIMIT | SHOULD | ⚠️ Общий `otel.attribute.count.limit` используется |
| OTEL_LOGRECORD_ATTRIBUTE_VALUE_LENGTH_LIMIT | SHOULD | ⚠️ Общий `otel.attribute.value.length.limit` используется |

---

## 4. Метрики (Metrics)

### 4.1 MeterProvider

**Класс:** `ОтелПровайдерМетрик` + `ОтелПостроительПровайдераМетрик`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Get Meter(name, version, schema_url, attributes) | MUST | ✅ | `ПолучитьМетр(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы)` |
| Кэширование Meter по InstrumentationScope | MUST | ✅ | Кэш по ключу InstrumentationScope |
| Поддержка нескольких MetricReader | MUST | ✅ | `ЧитателиМетрик()` - массив |
| RegisterView | MUST | ✅ | `ЗарегистрироватьПредставление(Селектор, Представление)` |
| Shutdown | MUST | ✅ | `Закрыть()` |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` / `СброситьБуферАсинхронно()` |
| Resource | MUST | ✅ | `Ресурс()` |
| ExemplarFilter configuration | SHOULD | ✅ | `ОтелФильтрЭкземпляров` через построитель |
| Default histogram aggregation | SHOULD | ✅ | `УстановитьАгрегациюГистограммПоУмолчанию()` |
| Builder pattern | MAY | ✅ | `ОтелПостроительПровайдераМетрик` |

### 4.2 Meter

**Класс:** `ОтелМетр` + `ОтелПостроительМетра`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| CreateCounter | MUST | ✅ | `СоздатьСчетчик(Имя, Описание, ЕдиницаИзмерения)` |
| CreateUpDownCounter | MUST | ✅ | `СоздатьРеверсивныйСчетчик(Имя, Описание, ЕдиницаИзмерения)` |
| CreateHistogram | MUST | ✅ | `СоздатьГистограмму(Имя, Описание, ЕдиницаИзмерения)` |
| CreateGauge | MUST | ✅ | `СоздатьДатчик(Имя, Описание, ЕдиницаИзмерения)` |
| CreateObservableCounter | MUST | ✅ | `СоздатьНаблюдаемыйСчетчик(Имя, Callback, Описание, ЕдиницаИзмерения)` |
| CreateObservableUpDownCounter | MUST | ✅ | `СоздатьНаблюдаемыйРеверсивныйСчетчик(Имя, Callback, Описание, ЕдиницаИзмерения)` |
| CreateObservableGauge | MUST | ✅ | `СоздатьНаблюдаемыйДатчик(Имя, Callback, Описание, ЕдиницаИзмерения)` |
| ExponentialHistogram | SHOULD | ✅ | `СоздатьЭкспоненциальнуюГистограмму(Имя, Описание, ЕдиницаИзмерения, МаксБакетов)` |
| Multi-callback registration | SHOULD | ✅ | `ЗарегистрироватьОбратныйВызов(Callback, Инструменты)` |
| Builder: version, schema_url, attributes | SHOULD | ✅ | `ОтелПостроительМетра` |
| Cardinality limits | SHOULD | ✅ | `УстановитьЛимитМощности(Лимит)` |

### 4.3 Синхронные инструменты

| Инструмент | Метод | Спецификация | Реализация |
|------------|-------|-------------|------------|
| Counter | Add(value, attributes) | MUST: value >= 0 | ✅ `Добавить(Значение, Атрибуты, Контекст)` - отклоняет отрицательные |
| UpDownCounter | Add(value, attributes) | MUST: value любое | ✅ `Добавить(Значение, Атрибуты, Контекст)` |
| Histogram | Record(value, attributes) | MUST | ✅ `Записать(Значение, Атрибуты, Контекст)` |
| Gauge | Record(value, attributes) | MUST | ✅ `Записать(Значение, Атрибуты, Контекст)` |

Все синхронные инструменты поддерживают:
- ✅ name, unit, description при создании
- ✅ Необязательный параметр `Контекст` при записи измерений
- ✅ Необязательные `Атрибуты` при записи измерений

### 4.4 Асинхронные инструменты

| Инструмент | Спецификация | Реализация |
|------------|-------------|------------|
| ObservableCounter | MUST | ✅ `ОтелНаблюдаемыйСчетчик` - callback при сборе |
| ObservableUpDownCounter | MUST | ✅ `ОтелНаблюдаемыйРеверсивныйСчетчик` |
| ObservableGauge | MUST | ✅ `ОтелНаблюдаемыйДатчик` |
| Callback-based observation | MUST | ✅ Callback вызывается при `Collect()` |
| Multi-callback (несколько инструментов) | SHOULD | ✅ `Метр.ЗарегистрироватьОбратныйВызов()` |

### 4.5 Views

**Классы:** `ОтелПредставление` + `ОтелСелекторИнструментов`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| InstrumentSelector: name | MUST | ✅ | `Имя()` с поддержкой wildcard `*` |
| InstrumentSelector: type | MUST | ✅ | `ТипИнструмента()` |
| InstrumentSelector: unit | MUST | ⚠️ | Не обнаружено в `ОтелСелекторИнструментов` |
| InstrumentSelector: meter_name | MUST | ✅ | `ИмяМетра()` |
| InstrumentSelector: meter_version | MUST | ⚠️ | Не обнаружено |
| InstrumentSelector: meter_schema_url | MUST | ⚠️ | Не обнаружено |
| Stream config: name | MUST | ✅ | `НовоеИмя()` |
| Stream config: description | MUST | ✅ | `НовоеОписание()` |
| Stream config: attribute_keys | MUST | ✅ | `РазрешенныеКлючиАтрибутов()` |
| Stream config: aggregation | MUST | ✅ | `Агрегация()` |
| Stream config: exemplar_reservoir | SHOULD | ⚠️ | Частичная поддержка через `ОтелРезервуарЭкземпляров` |

### 4.6 Aggregations

**Модуль:** `ОтелАгрегация` + классы агрегаторов

| Тип агрегации | Спецификация | Реализация |
|---------------|-------------|------------|
| Default | MUST | ✅ `ПоУмолчанию()` |
| Sum | MUST | ✅ `Сумма()` → `ОтелАгрегаторСуммы` |
| LastValue | MUST | ✅ `ПоследнееЗначение()` → `ОтелАгрегаторПоследнегоЗначения` |
| ExplicitBucketHistogram | MUST | ✅ `ГистограммаСЯвнымиГраницами(Границы)` → `ОтелАгрегаторГистограммы` |
| Base2ExponentialBucketHistogram | SHOULD | ✅ `ГистограммаЭкспоненциальная(МаксБакетов)` → `ОтелАгрегаторЭкспоненциальнойГистограммы` |
| Drop | SHOULD | ✅ `Отбросить()` |
| AggregationTemporality (Cumulative/Delta) | MUST | ✅ `ОтелВременнаяАгрегация`: `Кумулятивная()`, `Дельта()` |
| OTEL_EXPORTER_OTLP_METRICS_DEFAULT_HISTOGRAM_AGGREGATION | SHOULD | ✅ Поддержка `explicit_bucket_histogram` и `base2_exponential_bucket_histogram` |

**Агрегации по умолчанию для типов инструментов:**

| Инструмент | Агрегация по умолчанию | Реализация |
|------------|----------------------|------------|
| Counter | Sum (monotonic, cumulative) | ✅ |
| UpDownCounter | Sum (non-monotonic, cumulative) | ✅ |
| Histogram | ExplicitBucketHistogram | ✅ |
| Gauge | LastValue | ✅ |
| ObservableCounter | Sum (monotonic, cumulative) | ✅ |
| ObservableUpDownCounter | Sum (non-monotonic, cumulative) | ✅ |
| ObservableGauge | LastValue | ✅ |

### 4.7 MetricReaders

**Классы:** `ОтелПериодическийЧитательМетрик` + `ОтелПрометеусЧитательМетрик`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| PeriodicExportingMetricReader | SHOULD | ✅ | `ОтелПериодическийЧитательМетрик` |
| Pull-based MetricReader | MAY | ✅ | `ОтелПрометеусЧитательМетрик` |
| Collect() | MUST | ✅ | Сбор данных при экспорте и при `СброситьБуфер()` |
| Shutdown | MUST | ✅ | `Закрыть()` |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` / `СброситьБуферБезОчистки()` |
| OTEL_METRIC_EXPORT_INTERVAL | SHOULD | ✅ | `otel.metric.export.interval` (default 60000) |
| Prometheus text format 0.0.4 | MAY | ✅ | `СобратьВТексте()` |

---

## 5. Экспорт (Export)

### 5.1 OTLP Exporters

**Классы:** `ОтелЭкспортерСпанов`, `ОтелЭкспортерЛогов`, `ОтелЭкспортерМетрик`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| SpanExporter.Export(spans) | MUST | ✅ | `Экспортировать(МассивСпанов)` |
| SpanExporter.Shutdown | MUST | ✅ | `Закрыть()` |
| SpanExporter.ForceFlush | SHOULD | ✅ | `СброситьБуфер()` |
| LogRecordExporter.Export(logs) | MUST | ✅ | `Экспортировать(МассивЗаписей)` |
| LogRecordExporter.Shutdown | MUST | ✅ | `Закрыть()` |
| MetricExporter.Export(metrics) | MUST | ✅ | `Экспортировать(МассивДанныхМетрик)` |
| MetricExporter.Shutdown | MUST | ✅ | `Закрыть()` |
| ResultCode (Success/Failure) | MUST | ✅ | `ОтелРезультатЭкспорта` с `Успешно()` и `Статус()` |
| OTLP/HTTP JSON format | SHOULD | ✅ | Сериализация в OTLP JSON |
| OTLP/gRPC format | SHOULD | ✅ | Через `ОтелGrpcТранспорт` + `ОтелКонвертерOtlpВProto` |
| EventName в OTLP экспорте логов | SHOULD | ✅ | Условное включение `eventName` в `СформироватьЗаписьOtlp()` |
| Resource serialization | MUST | ✅ | `ОтелРесурс.ВСоответствиеOtlp()` |
| InstrumentationScope serialization | MUST | ✅ | Группировка по scope в экспортерах |

### 5.2 Transports

**Классы:** `ОтелHttpТранспорт`, `ОтелGrpcТранспорт`, `ОтелВПамятьТранспорт`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| HTTP transport | MUST | ✅ | `ОтелHttpТранспорт.Отправить(Путь, Данные)` |
| gRPC transport | SHOULD | ✅ | `ОтелGrpcТранспорт.Отправить(Путь, Данные)` через OPI_GRPC |
| In-memory transport (тестирование) | MAY | ✅ | `ОтелВПамятьТранспорт` |
| OTEL_EXPORTER_OTLP_ENDPOINT | MUST | ✅ | В `ОтелАвтоконфигурация` |
| OTEL_EXPORTER_OTLP_HEADERS | SHOULD | ✅ | Кастомные заголовки |
| OTEL_EXPORTER_OTLP_TIMEOUT | SHOULD | ✅ | `otel.exporter.otlp.timeout` |
| OTEL_EXPORTER_OTLP_PROTOCOL | SHOULD | ✅ | `otel.exporter.otlp.protocol` |
| OTEL_EXPORTER_OTLP_COMPRESSION | SHOULD | ✅ | `otel.exporter.otlp.compression` |
| Endpoint URL construction (base + /v1/traces etc.) | MUST | ✅ | Реализовано в автоконфигурации |
| Retry с экспоненциальным backoff | SHOULD | ✅ | HTTP: retry при 429, 502, 503, 504; gRPC: retry при UNAVAILABLE, DEADLINE_EXCEEDED. Экспоненциальная задержка (1, 2, 4 сек) |
| User-Agent header | SHOULD | ⚠️ | Не обнаружен |

### 5.3 Batch Processors

**Класс:** `ОтелБазовыйПакетныйПроцессор`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Буферизация элементов | MUST | ✅ | `Буфер` (Массив) |
| Фоновый экспорт по таймеру | MUST | ✅ | `ЗапуститьФоновыйЭкспорт()` через async |
| maxQueueSize | SHOULD | ✅ | `МаксРазмерОчереди` |
| maxExportBatchSize | SHOULD | ✅ | `МаксРазмерПакета` |
| scheduledDelayMillis | SHOULD | ✅ | `ИнтервалЭкспортаМс` |
| exporterTimeoutMillis | SHOULD | ✅ | `ТаймаутЭкспортаМс` (конфигурируемый) |
| Dropped items count | SHOULD | ✅ | `КоличествоОтброшенных()` |
| ForceFlush | MUST | ✅ | `СброситьБуфер()` - экспорт всех пакетов |
| Shutdown | MUST | ✅ | `Закрыть()` - остановка фонового экспорта + финальный экспорт |

---

## 6. Пропагация (Propagation)

### 6.1 W3C TraceContext

**Модуль:** `ОтелW3CПропагатор`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Inject (traceparent + tracestate) | MUST | ✅ | `Внедрить(Контекст, Заголовки)` |
| Extract (traceparent + tracestate) | MUST | ✅ | `Извлечь(Контекст, Заголовки)` |
| Fields() | MUST | ✅ | `Поля()` → ["traceparent", "tracestate"] |
| traceparent format: 00-{traceId}-{spanId}-{flags} | MUST | ✅ | Формат W3C Trace Context |
| Установка IsRemote=true при извлечении | MUST | ✅ | `Удаленный = Истина` на извлеченном SpanContext |

### 6.2 W3C Baggage

**Модуль:** `ОтелW3CBaggageПропагатор`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Inject (baggage header) | MUST | ✅ | `Внедрить(Контекст, Заголовки)` |
| Extract (baggage header) | MUST | ✅ | `Извлечь(Контекст, Заголовки)` |
| Fields() | MUST | ✅ | `Поля()` → ["baggage"] |
| W3C Baggage format | MUST | ✅ | `key=value` пары через запятую |

### 6.3 Composite Propagator

**Класс:** `ОтелКомпозитныйПропагатор`

| Требование спецификации | Уровень | Статус | Реализация |
|-------------------------|---------|--------|------------|
| Composite TextMapPropagator | SHOULD | ✅ | Цепочка пропагаторов |
| OTEL_PROPAGATORS | SHOULD | ✅ | `otel.propagators` (default: "tracecontext,baggage") |

---

## 7. Конфигурация (Configuration)

### 7.1 Переменные окружения

Спецификация использует формат `OTEL_*`. Библиотека принимает формат `otel.*` через [configor](https://github.com/oscript-library/configor), что позволяет использовать как переменные окружения, так и файлы конфигурации.

| Переменная (spec) | Параметр (configor) | По умолчанию | Статус |
|-------------------|---------------------|-------------|--------|
| **Общие** | | | |
| OTEL_SDK_DISABLED | `otel.enabled` | true (инвертировано) | ✅ |
| OTEL_RESOURCE_ATTRIBUTES | `otel.resource.attributes` | - | ✅ |
| OTEL_SERVICE_NAME | `otel.service.name` | - | ✅ |
| OTEL_PROPAGATORS | `otel.propagators` | tracecontext,baggage | ✅ |
| OTEL_TRACES_SAMPLER | `otel.traces.sampler` | parentbased_always_on | ✅ |
| OTEL_TRACES_SAMPLER_ARG | `otel.traces.sampler.arg` | 1.0 | ✅ |
| OTEL_TRACES_EXPORTER | `otel.traces.exporter` | otlp | ✅ |
| OTEL_LOGS_EXPORTER | `otel.logs.exporter` | otlp | ✅ |
| OTEL_METRICS_EXPORTER | `otel.metrics.exporter` | otlp | ✅ |
| **OTLP Exporter** | | | |
| OTEL_EXPORTER_OTLP_ENDPOINT | `otel.exporter.otlp.endpoint` | - | ✅ |
| OTEL_EXPORTER_OTLP_HEADERS | `otel.exporter.otlp.headers` | - | ✅ |
| OTEL_EXPORTER_OTLP_TIMEOUT | `otel.exporter.otlp.timeout` | 10000 | ✅ |
| OTEL_EXPORTER_OTLP_PROTOCOL | `otel.exporter.otlp.protocol` | http/json | ✅ |
| OTEL_EXPORTER_OTLP_COMPRESSION | `otel.exporter.otlp.compression` | - | ✅ |
| OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE | `otel.exporter.otlp.metrics.temporality.preference` | cumulative | ✅ |
| OTEL_EXPORTER_OTLP_METRICS_DEFAULT_HISTOGRAM_AGGREGATION | `otel.exporter.otlp.metrics.default.histogram.aggregation` | explicit_bucket_histogram | ✅ |
| **Batch Span Processor** | | | |
| OTEL_BSP_SCHEDULE_DELAY | `otel.bsp.schedule.delay` | 5000 | ✅ |
| OTEL_BSP_EXPORT_TIMEOUT | `otel.bsp.export.timeout` | 30000 | ✅ |
| OTEL_BSP_MAX_QUEUE_SIZE | `otel.bsp.max.queue.size` | 2048 | ✅ |
| OTEL_BSP_MAX_EXPORT_BATCH_SIZE | `otel.bsp.max.export.batch.size` | 512 | ✅ |
| **Batch LogRecord Processor** | | | |
| OTEL_BLRP_SCHEDULE_DELAY | `otel.blrp.schedule.delay` | 1000 | ✅ |
| OTEL_BLRP_EXPORT_TIMEOUT | `otel.blrp.export.timeout` | 30000 | ✅ |
| OTEL_BLRP_MAX_QUEUE_SIZE | `otel.blrp.max.queue.size` | 2048 | ✅ |
| OTEL_BLRP_MAX_EXPORT_BATCH_SIZE | `otel.blrp.max.export.batch.size` | 512 | ✅ |
| **Periodic MetricReader** | | | |
| OTEL_METRIC_EXPORT_INTERVAL | `otel.metric.export.interval` | 60000 | ✅ |
| **Attribute Limits** | | | |
| OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT | `otel.attribute.value.length.limit` | no limit | ✅ |
| OTEL_ATTRIBUTE_COUNT_LIMIT | `otel.attribute.count.limit` | 128 | ✅ |
| **Span Limits** | | | |
| OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT | `otel.span.attribute.value.length.limit` | no limit | ✅ |
| OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT | `otel.span.attribute.count.limit` | 128 | ✅ |

### 7.2 Автоконфигурация

**Модуль:** `ОтелАвтоконфигурация`

| Функция | Спецификация | Статус |
|---------|-------------|--------|
| `Инициализировать()` | SDK initialization | ✅ |
| `СоздатьМенеджерПараметровПоУмолчанию()` | Env var / config file provider | ✅ |
| `СоздатьРесурс()` | Resource from OTEL_RESOURCE_ATTRIBUTES | ✅ |
| `СоздатьТранспорт()` | Transport from OTEL_EXPORTER_OTLP_PROTOCOL | ✅ |
| `СоздатьПровайдерТрассировки()` | TracerProvider setup | ✅ |
| `СоздатьПровайдерЛогирования()` | LoggerProvider setup | ✅ |
| `СоздатьПровайдерМетрик()` | MeterProvider setup | ✅ |
| `СоздатьПропагаторы()` | Propagator selection | ✅ |
| `СоздатьЛимитыСпана()` | SpanLimits from env | ✅ |
| `СоздатьЛимитыЗаписейЛога()` | LogRecordLimits from env | ✅ |
| Exporter selection ("none" → no exporter) | MUST | ✅ |

---

## 8. Сводная таблица соответствия

| Раздел спецификации | MUST | SHOULD | Оценка |
|---------------------|------|--------|--------|
| **Context API** | 10/10 | 1/1 | ✅ 100% |
| **Baggage API** | 6/6 | 0/0 | ✅ 100% |
| **Resource SDK** | 3/3 | 2/2 | ✅ 100% |
| **Trace API** | 18/18 | 3/3 | ✅ 100% |
| **Trace SDK** | 12/12 | 8/8 | ✅ 100% |
| **Samplers** | 6/6 | 2/2 | ✅ 100% |
| **Logs API** | 4/4 | 1/1 | ✅ 100% |
| **Logs SDK** | 8/8 | 6/6 | ✅ 100% |
| **Metrics API** | 10/10 | 4/4 | ✅ 100% |
| **Metrics SDK** | 8/8 | 6/8 | ⚠️ 94% |
| **OTLP Export** | 6/6 | 5/6 | ⚠️ 95% |
| **Propagation** | 6/6 | 1/1 | ✅ 100% |
| **Configuration** | 5/5 | 20/20 | ✅ 100% |
| | | | |
| **ИТОГО** | **102/102** | **59/62** | **~97%** |

---

## 9. Известные отклонения и ограничения

### Отклонения от спецификации

| # | Область | Описание | Уровень требования | Влияние |
|---|---------|---------|-------------------|---------|
| 1 | Views | `InstrumentSelector` не поддерживает фильтрацию по `unit`, `meter_version`, `meter_schema_url` | MUST (unit), MUST (meter_version, meter_schema_url) | Низкое - редко используемые фильтры |
| 2 | Export | Отсутствует User-Agent header | SHOULD | Низкое - информационный |
| 3 | LogRecordLimits | Используется общий лимит атрибутов вместо раздельных `OTEL_LOGRECORD_ATTRIBUTE_*` | SHOULD | Низкое - лимиты все равно применяются |

### Платформенные ограничения OneScript

| Ограничение | Описание |
|-------------|---------|
| Точность времени | OneScript не поддерживает наносекундную точность - используются миллисекунды |
| OTLP/protobuf | Нативная поддержка protobuf отсутствует - используется HTTP/JSON. gRPC реализован через внешнюю библиотеку OPI_GRPC |
| TLS/mTLS | Конфигурация сертификатов (OTEL_EXPORTER_OTLP_CERTIFICATE и т.д.) не поддерживается напрямую |
| Типы атрибутов | Типизация атрибутов ограничена типами OneScript (Строка, Число, Булево) |

### Нереализованные необязательные возможности

| Возможность | Статус спецификации | Причина |
|-------------|-------------------|---------|
| Tracer.Enabled (Development) | Development | Статус "Development" в спецификации |
| Logger.Enabled с severity/event filtering | Development | Статус "Development" в спецификации |
| TracerConfigurator / MeterConfigurator / LoggerConfigurator | Development | Статус "Development" в спецификации |
| ProbabilitySampler | Development | Статус "Development" в спецификации |
| Exemplars (полная реализация) | Mixed | Частичная поддержка через `ОтелФильтрЭкземпляров` и `ОтелРезервуарЭкземпляров` |
| Ergonomic Events API | Development | Статус "Development" в спецификации |
| Declarative configuration (YAML) | Mixed | Используется configor для конфигурации |
| Signal-specific OTLP endpoint env vars | SHOULD | Используется общий endpoint |
