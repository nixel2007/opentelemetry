# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-20
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего keywords в спецификации | 824 |
| Stable + universal keywords | 701 |
| Conditional keywords | 6 |
| Development keywords | 123 |
| Найдено требований (Stable universal) | 697 |
| ✅ Реализовано (found) | 595 (85.4%) |
| ⚠️ Частично (partial) | 77 (11.0%) |
| ❌ Не реализовано (not_found) | 25 (3.6%) |
| ➖ Неприменимо (n_a) | 4 |
| **MUST/MUST NOT found** | 407/423 (96.2%) |
| **SHOULD/SHOULD NOT found** | 188/274 (68.6%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 15 | 0 | 0 | 0 | 15 | 100.0% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 17 | 2 | 1 | 0 | 20 | 85.0% |
| Trace Api | 109 | 11 | 2 | 0 | 122 | 89.3% |
| Trace Sdk | 68 | 12 | 2 | 0 | 82 | 82.9% |
| Logs Api | 19 | 2 | 0 | 0 | 21 | 90.5% |
| Logs Sdk | 55 | 8 | 1 | 0 | 64 | 85.9% |
| Metrics Api | 88 | 11 | 0 | 1 | 99 | 88.9% |
| Metrics Sdk | 134 | 23 | 11 | 3 | 168 | 79.8% |
| Otlp Exporter | 14 | 4 | 7 | 0 | 25 | 56.0% |
| Propagators | 38 | 2 | 0 | 0 | 40 | 95.0% |
| Env Vars | 22 | 1 | 1 | 0 | 24 | 91.7% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Trace Api]** [MUST NOT] However, alternative implementations MUST NOT allow callers to create Spans directly.  
  Конструктор ОтелСпан публичный, OneScript не поддерживает ограничение видимости конструктора. Пользователь может вызвать Новый ОтелСпан(...) напрямую, обходя Tracer. Документированный путь - через Tracer.ПостроительСпана(). (`src/Трассировка/Классы/ОтелСпан.os:599`)

- ⚠️ **[Trace Api]** [MUST NOT] There MUST NOT be any API for creating a Span other than with a Tracer.  
  Публичный конструктор ОтелСпан доступен для прямого вызова (Новый ОтелСпан(...)). Платформа OneScript не позволяет ограничить видимость конструктора. Фактический документированный путь - только через Tracer, но запрет прямого создания не форсируется кодом. (`src/Трассировка/Классы/ОтелСпан.os:599`)

- ⚠️ **[Trace Api]** [MUST NOT] This operation itself MUST NOT perform blocking I/O on the calling thread.  
  Сам Завершить() не выполняет I/O напрямую, но синхронно вызывает Процессор.ПриЗавершении(), и ОтелПростойПроцессорСпанов экспортирует спан синхронно в вызывающем потоке, что эквивалентно блокирующему I/O на calling thread. (`src/Трассировка/Классы/ОтелСпан.os:459`)

- ⚠️ **[Trace Api]** [MUST] The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface.  
  Операция реализована через конструктор Новый ОтелНоопСпан(КонтекстСпана), но отдельного метода API (например, Tracer.WrapSpanContext) не существует. Используется в пропагаторах (W3C/B3), но публично оформленного wrap-метода нет. (`src/Трассировка/Классы/ОтелНоопСпан.os:279`)

- ⚠️ **[Trace Api]** [MUST] The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current).  
  При отсутствии SDK ПолучитьАктивныйСдк() возвращает кэшированный SDK с сэмплером ВсегдаВыключен, НачатьСпан возвращает ОтелНоопСпан с контекстом, унаследованным от родителя, но с НОВЫМ SpanId (СоздатьНоопСпанДляОтброшенного в ОтелТрассировщик.os:213). Спека требует вернуть non-recording span с тем же SpanContext, что в parent Context, а не генерировать новый SpanId. (`src/Ядро/Модули/ОтелГлобальный.os:143-160`)

- ⚠️ **[Trace Api]** [MUST] If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags).  
  В noop-режиме (AlwaysOff) без родителя генерируются НЕ нулевые TraceId/SpanId, а полноценные идентификаторы (Провайдер.СгенерироватьИдТрассировки/СгенерироватьИдСпана), затем возвращается NoopSpan. Спека требует all-zero IDs. (`src/Трассировка/Классы/ОтелТрассировщик.os:56-68`)

- ⚠️ **[Logs Api]** [MUST] When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context.  
  Контекст = Неопределено разрешается в текущий контекст только внутри ТрассировкаНеСэмплирована (ветка trace-based фильтрации), но в процессор Включен передаётся исходное Неопределено без явного вызова ОтелКонтекст.Текущий(); разрешение контекста не универсально для всех веток API. (`src/Логирование/Классы/ОтелЛоггер.os:68`)

- ⚠️ **[Metrics Api]** [MUST] Therefore, this API MUST be structured to accept a variable number of attributes, including none.  
  Параметр АтрибутыОбласти принимает ОтелАтрибуты-контейнер (или Неопределено) - т.е. 'переменное число атрибутов, включая ноль' поддерживается через объект-контейнер, а не через варargs/массив. Семантически соответствует, но не через variadic-параметр. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:62`)

- ⚠️ **[Metrics Api]** [MUST] It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string.  
  Строки в OneScript регистрозависимы по умолчанию (сравнение '=' case-sensitive), поэтому case-sensitivity обеспечивается платформой. Однако проверки на ASCII-only (отклонение/валидация не-ASCII символов) нет - единица измерения принимается как произвольная строка. (`src/Метрики/Классы/ОтелМетр.os:621`)

- ⚠️ **[Metrics Api]** [MUST] Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Потокобезопасность документирована только для синхронных инструментов (ОтелБазовыйСинхронныйИнструмент:49-50). Базовый класс наблюдаемых инструментов (ОтелБазовыйНаблюдаемыйИнструмент) не содержит комментария о thread-safety на уровне класса. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:49`)

- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collecti...  
  Callback вызывается при сборе конкретным reader, но состояние инструмента общее для всех reader'ов — нет явной изоляции наблюдений по reader'у. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:226`)

- ⚠️ **[Metrics Sdk]** [MUST] This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additi...  
  Параметр АтрибутыСерии передаётся в Предложить(), но в документирующем комментарии не подчёркнуто, что филтрованный набор атрибутов может расходиться с таймсерией. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41`)

- ⚠️ **[Metrics Sdk]** [MUST] This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additi...  
  Атрибуты таймсерии не передаются в резервуар при конструировании - они передаются пер-вызов в Предложить(АтрибутыСерии). Обходной путь, а не "at construction" как требует спека. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:174`)

- ⚠️ **[Otlp Exporter]** [MUST] Options MUST be one of: grpc, http/protobuf, http/json.  
  Валидация значений выполняется (grpc, http/protobuf, http/json), однако http/protobuf фактически обрабатывается как http/json — ОтелHttpТранспорт всегда сериализует тело в JSON (ЗаписатьJSON), отдельной реализации http/protobuf нет. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:612`)

- ⚠️ **[Propagators]** [MUST] A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2.  
  Парсинг и валидация traceparent/tracestate реализованы (версия ff отклоняется, проверка длин id, all-zeros отклоняются), но комментарий заявляет соответствие W3C Trace Context Level 1. Level 2 добавляет дополнительные требования (random trace flag), которые не проверяются. (`src/Пропагация/Классы/ОтелW3CПропагатор.os:81`)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Предупреждение и безопасное игнорирование реализовано для otel.traces.sampler (строка 293) и otel.propagators (строка 529), но для otel.traces.exporter / otel.logs.exporter / otel.metrics.exporter неизвестное значение не логируется - оно молча трактуется как otlp (строки 238, 363, 431). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:293`)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Ключ контекста Baggage экспортирован через Функция КлючBaggage() Экспорт, то есть доступен API-пользователям. Это нарушает рекомендацию скрывать ключ - правильнее оставить его внутренним (не-Экспорт) и работать через BaggageИзКонтекста/КонтекстСBaggage. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ⚠️ **[Resource Sdk]** [SHOULD] Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error.  
  Исключения при детекции логируются на уровне Отладка (Debug), а не Ошибка. Ошибка поглощается без сообщения об ошибке согласно Error Handling. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:25`)

- ⚠️ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles.  
  При сбое декодирования пропускается только некорректная пара (пропуск по отсутствию '='), вся строка целиком не отбрасывается, как требует спецификация. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:742`)

- ❌ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles.  
  Ошибки декодирования не логируются и не репортятся через Error Handling; некорректные пары молча пропускаются без сообщения об ошибке. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation.  
  КлючСпана() экспортирован из модуля ОтелКонтекст, то есть ключ контекста технически доступен внешнему коду. Основной API (СпанИзКонтекста/КонтекстСоСпаном/ТекущийСпан) абстрагирует ключ, но сам ключ не скрыт. (`src/Ядро/Модули/ОтелКонтекст.os:44`)

- ⚠️ **[Trace Api]** [SHOULD NOT] To prevent misuse, implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext.  
  Метод Атрибуты() экспортирован и доступен внешнему коду (не только процессорам/экспортерам), что нарушает рекомендацию скрывать атрибуты. Публичный геттер позволяет читать атрибуты после установки. (`src/Трассировка/Классы/ОтелСпан.os:146`)

- ⚠️ **[Trace Api]** [SHOULD] An attempt to set value `Unset` SHOULD be ignored.  
  Явной проверки на попытку установить Unset нет; при текущем КодСтатуса=НеУстановлен вызов УстановитьСтатус(НеУстановлен) эффективно no-op (присвоение того же значения), но при КодСтатуса=Ошибка переход в Unset явно блокируется, а в других веток код Unset всё же переприсваивается, что формально отличается от требования 'ignored'. (`src/Трассировка/Классы/ОтелСпан.os:425`)

- ❌ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type).  
  Тип ОтелНоопСпан зарегистрирован как публичный класс в lib.config и напрямую инстанциируется снаружи (пропагаторы, Tracer). Нет скрытой/пакетной видимости. (-)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`.  
  Класс назван ОтелНоопСпан (NoopSpan), не NonRecordingSpan. Семантически эквивалентно, но имена различаются. (`src/Трассировка/Классы/ОтелНоопСпан.os`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Линк хранится как Соответствие (не отдельный иммутабельный класс). После добавления в массив Линки не изменяется, но формальной документации иммутабельности и конкурентной безопасности для Link нет. (`src/Трассировка/Классы/ОтелСпан.os:384-389`)

- ❌ **[Trace Api]** [SHOULD] If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`.  
  Нет проверки ЗаписьАктивна()/IsRecording у родительского спана в ОтелТрассировщик.НачатьСпан - всегда создаётся новый экземпляр (ОтелСпан или ОтелНоопСпан), даже если родитель уже non-recording. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] SDKs SHOULD return a valid no-op Tracer for these calls, if possible.  
  После Закрыть() ПолучитьТрассировщик возвращает новый экземпляр ОтелТрассировщик, а не NoOp-трассировщик. Спаны могут всё ещё создаваться, хотя процессоры уже закрыты. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:78`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный Закрыть - процедура без возврата статуса. Асинхронный ЗакрытьАсинхронно возвращает Обещание, но таймаут контролируется только вызывающей стороной через Обещание.Получить(таймаут); внутреннего таймаута нет. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:154`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Сама процедура Закрыть не принимает параметр таймаута и не прерывается. Таймаут возможен только через внешнее Обещание.Получить(timeout) при использовании ЗакрытьАсинхронно. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:128`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный СброситьБуфер - процедура без возврата статуса. Асинхронный СброситьБуферАсинхронно возвращает Обещание, но таймаут контролируется только вызывающей стороной через Обещание.Получить(таймаут); внутреннего таймаута нет. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:143`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Сама процедура СброситьБуфер не принимает параметр таймаута и не прерывается. Таймаут возможен только через внешнее Обещание.Получить(timeout) при использовании СброситьБуферАсинхронно. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set.  
  Процессоры (ОтелПростойПроцессорСпанов, ОтелПакетныйПроцессорСпанов) передают экспортеру все завершённые спаны без фильтрации по Sampled-флагу TraceFlags. RECORD_ONLY-спан (IsRecording=true, Sampled=false) был бы отправлен экспортеру. На практике встроенные сэмплеры не возвращают RECORD_ONLY, но механизм фильтрации отсутствует. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not.  
  Процессоры не фильтруют по Sampled-флагу перед вызовом экспортера. RECORD_ONLY-спан (IsRecording=true, Sampled=false) будет отправлен экспортеру, нарушая SHOULD NOT. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  ФлагиТрассировки используют только бит sampled (0x01): для корневых спанов не устанавливается бит Random (0x02) W3C Trace Context Level 2 - см. ОтелТрассировщик.ВычислитьФлагиТрассировки (возвращает 0 или 1) и ОтелКонтекстСпана (ФлагиТрассировки=1). (-)

- ❌ **[Trace Sdk]** [SHOULD] If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated.  
  IdGenerator расширение есть (ОтелПровайдерТрассировки.УстановитьГенераторИд), но механизм задания W3C Trace Context Level 2 Random flag отсутствует - TraceFlags random bit не поддерживается и не пробрасывается из IdGenerator. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.  
  Опции названы МаксСобытий (MaxEvents) и МаксЛинков (MaxLinks) - семантика корректна, но дословный перевод имён не совпадает с EventCountLimit/LinkCountLimit (отсутствует 'Count' в имени). (`src/Трассировка/Классы/ОтелЛимитыСпана.os:40`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть - процедура без возвращаемого значения. Вызывающий не может отличить успех, ошибку или таймаут; ошибки передаются только через исключения, а таймаут тихо логируется без индикатора результата. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:77; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер - процедура без возвращаемого значения. Таймаут только логируется (Лог.Предупреждение), успех/неудача/таймаут неразличимы для вызывающего. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() объявлена как Процедура (void) - не возвращает статус успеха/неудачи/таймаута. Ошибки всплывают исключениями, но таймаут неотличим от успеха. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер() экспортера не принимает параметр таймаута. Для синхронного экспортера это no-op (завершается мгновенно), но механизма прерывания по таймауту нет. На уровне процессора таймаут поддержан (ОтелБазовыйПакетныйПроцессор.СброситьБуфер(ТаймаутМс)). (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57`)

- ⚠️ **[Logs Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Комментарий к методу описывает назначение Включен (пропустить создание LogRecord если логгер ничего не сделает) и упоминает, что возвращаемое значение не статично, но отсутствует явное указание вызывать API каждый раз перед эмиссией LogRecord для получения актуального ответа. (`src/Логирование/Классы/ОтелЛоггер.os:28`)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Метод Закрыть() не принимает таймаут и вызывает Процессор.Закрыть() без таймаута. Таймаут доступен только косвенно через ЗакрытьАсинхронно().Получить(таймаут), что прерывает ожидание, но не саму операцию закрытия процессоров. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:132`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ...  
  СброситьБуфер() - процедура (void). ERROR-сигнал доступен только косвенно через СброситьБуферАсинхронно() (Обещание). Явного возврата ERROR/NO ERROR из синхронного API нет. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:122`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ...  
  Синхронный СброситьБуфер() ничего не возвращает (NO ERROR/успех неотличим). Статус доступен только через СброситьБуферАсинхронно(). (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:122`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Provider.СброситьБуфер() вызывает Процессор.СброситьБуфер() без параметра таймаута. Композитный процессор поддерживает таймаут внутри, но провайдер передаёт 0 (без ограничения). Прерывание возможно только через Обещание.Получить(таймаут). (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:122`)

- ❌ **[Logs Sdk]** [SHOULD] To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor.  
  В документации процессоров/логгера нет рекомендации клонировать ЗаписьЛога для конкурентной обработки. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть - Процедура (void), без возврата статуса. Асинхронная обёртка ЗакрытьАсинхронно возвращает Обещание на уровне провайдера, но у самого процессора статус успех/отказ/таймаут не возвращается.   (`src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:87`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер - Процедура без возврата статуса. Провайдер предоставляет СброситьБуферАсинхронно → Обещание, но у самого процессора статус операции не возвращается. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  ОтелЭкспортерЛогов.СброситьБуфер() - Процедура (void), не возвращает статус успеха/ошибки/таймаута. На уровне Провайдера есть СброситьБуферАсинхронно() с Обещанием, но у самого экспортера возврата статуса нет. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  ОтелЭкспортерЛогов.СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по таймауту (синхронный экспортер, сам экспорт уже ограничен таймаутом в Экспортировать). (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62`)

- ⚠️ **[Metrics Api]** [SHOULD] Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`.  
  Глобальный доступ к Meter осуществляется через ОтелГлобальный.ПолучитьМетр(), установка провайдера метрик - через билдер SDK (ОтелПостроительSdk.УстановитьПровайдерМетрик) и ОтелГлобальный.Установить(Сдк). Отдельного global MeterProvider getter/setter (как SetGlobalMeterProvider/GetGlobalMeterProvider) нет - доступ опосредован через глобальный SDK. (`src/Ядро/Модули/ОтелГлобальный.os:100`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  Комментарии к методам СоздатьСчетчик/СоздатьГистограмму/СоздатьДатчик описывают параметр Имя, но не упоминают правила синтаксиса имён инструментов (instrument name syntax). (`src/Метрики/Классы/ОтелМетр.os:42`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] The API SHOULD NOT validate `advisory` parameters.  
  ПроверитьСовет() выполняет лёгкую валидацию типов advisory (Структура, Массив) с логированием предупреждений, тогда как спека говорит SHOULD NOT validate. (`src/Метрики/Классы/ОтелМетр.os:796`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  Комментарии к СоздатьНаблюдаемый* описывают параметр Имя, но не упоминают правила синтаксиса имён инструментов. (`src/Метрики/Классы/ОтелМетр.os:272`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] The API SHOULD NOT validate `advisory` parameters.  
  ПроверитьСовет() выполняет лёгкую валидацию типов advisory с логированием предупреждений, что противоречит SHOULD NOT validate. (`src/Метрики/Классы/ОтелМетр.os:796`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response.  
  Документация метода Включен() описывает, что значение может изменяться, но не содержит явной рекомендации вызывать API при каждом измерении для получения актуального значения. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:248`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] This API SHOULD NOT validate this value, that is left to implementations of the API.  
  Добавить() проверяет Значение < 0 и молча игнорирует отрицательные значения — это валидация на уровне API, тогда как спека говорит SHOULD NOT validate. (`src/Метрики/Классы/ОтелСчетчик.os:22`)

- ⚠️ **[Metrics Api]** [SHOULD] This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative.  
  Документирующий комментарий метода Записать описывает параметр как 'измеренное значение', но не упоминает явно что значение должно быть неотрицательным. (`src/Метрики/Классы/ОтелГистограмма.os:13`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Синхронный метод Закрыть() не принимает таймаут. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, таймаут задаётся снаружи через Обещание.Получить(), но внутренняя операция Закрыть() не прерывается при превышении. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:179`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERRO...  
  Асинхронный СброситьБуферАсинхронно() возвращает Обещание, которое может быть отклонено при исключении, но явного ERROR/NO ERROR статус-объекта нет. Синхронная СброситьБуфер() - процедура без возвращаемого статуса. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:167`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Синхронная СброситьБуфер() не принимает таймаут. Асинхронная СброситьБуферАсинхронно() возвращает Обещание, таймаут можно задать через Обещание.Получить(), но сама операция не прерывается при превышении. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:167`)

- ⚠️ **[Metrics Sdk]** [SHOULD] In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument.  
  Нет явной проверки/предупреждения, что при заданном NewName селектор не должен сопоставляться более чем с одним инструментом (no fail-fast). (-)

- ❌ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  View применяется, но нет диагностики 'conflicting metric identities' (когда несколько View дают одинаковый идентификатор потока). (-)

- ❌ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warnin...  
  Нет проверки семантических ошибок конфигурации View (например, histogram-агрегация для асинхронного инструмента) и соответствующего warning. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD NOT] Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`).  
  Sum собирается всегда без условного отключения для UpDownCounter/ObservableGauge. По умолчанию эти инструменты не используют гистограмму, но при явной настройке через View нет fallback. (`src/Метрики/Классы/ОтелАгрегаторГистограммы.os:51`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  Есть ДобавитьВнешниеНаблюдения, разрешающая наблюдения вне зарегистрированного callback, что противоречит SHOULD-disregard (однако используется интеграциями как дополнительный механизм). (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:81`)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Вызов ТекущееДействие.Выполнить в ВызватьCallbackИСобрать не ограничен таймаутом, зависшая callback блокирует сбор. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент не содержит логики ограничения кардинальности (нет ЛимитМощности, нет overflow, нет предпочтения первых наблюдений). Async-инструменты собирают все наблюдения без лимита. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Предупреждение содержит сравнение старых и новых параметров и факт возврата ранее зарегистрированного инструмента, но не содержит конкретных рекомендаций (например, View-рецепта) по устранению конфликта. (`src/Метрики/Классы/ОтелМетр.os:727`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning.  
  В ПроверитьКонфликтДескриптора нет логики, проверяющей, что конфликт описания разрешён через View: предупреждение выдаётся при любом различии Описание. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the war...  
  Текст предупреждения не содержит View-рецепта для переименования; лог выводит только описание конфликта. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument regist...  
  Код возвращает ранее зарегистрированный инструмент (ОтелМетр.os:59), а не регистрирует второй Metric объект с другой единицей. Второй инструмент не создаётся и его данные не проходят отдельным потоком. (-)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax.  
  В ОтелМетр.СоздатьСчетчик/СоздатьГистограмму/… имя нормализуется через НРег(), но не валидируется против синтаксиса имени (regex [A-Za-z][A-Za-z0-9_.\-/]{0,254}). Проверок нет ни в одном из методов создания инструмента. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Поскольку валидации имени нет, соответствующее предупреждение о неверном синтаксисе не эмитируется. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided.  
  ПроверитьСовет эмитирует предупреждения и при некорректном типе Совет (не Структура) фактически игнорирует его (ПолучитьГраницыИзСовета/ПолучитьКлючиАтрибутовИзСовета возвращают Неопределено). Однако для невалидных вложенных полей (ГраницыГистограммы не Массив, КлючиАтрибутов не Массив) код только логирует, но всё равно возвращает исходное значение в дальнейшие вычисления - т.е. не «proceed as if not provided». (`src/Метрики/Классы/ОтелМетр.os:796`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.  
  СоздатьЭкземпляр создаёт новый Соответствие и новые объекты отфильтрованных атрибутов при каждом вызове Предложить - аллокации не оптимизированы. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:121`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер/СобратьИЭкспортировать - процедуры (void), ошибки логируются, но каллеру не возвращается статус успеха/ошибки/таймаута. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ⚠️ **[Metrics Sdk]** [SHOULD] SDKs SHOULD return some failure for these calls, if possible.  
  Reader's СброситьБуфер/СобратьИЭкспортировать не проверяет флаг Закрыт явно; подавление делегируется экспортёру (Экспортировать возвращает Ложь после Закрыть). Нет прямой сигнализации отказа из ридера. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() - Процедура (void), не возвращает статус succ/fail/timeout; таймаут финального ожидания логируется, но не различим от успеха. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:111`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter.  
  СброситьБуфер ридера собирает метрики и вызывает Экспортер.Экспортировать, но НЕ вызывает Экспортер.СброситьБуфер() (ForceFlush) после этого. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер - Процедура (void), без возврата статуса; ошибки логируются, но не различимы с таймаутом для вызывающего. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to mod...  
  Статус ERROR/NO ERROR не возвращается - метод void; ошибки только логируются. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Явного параметра таймаута у СброситьБуфер нет; прерывание делегируется внутреннему Экспортер.Экспортировать (таймаут экспортёра), но собственного таймаута у ридера нет. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `Metr...  
  ОтелЭкспортерМетрик не проверяет совместимость агрегации/временности данных и не сообщает об ошибке при неподдерживаемой комбинации. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this me...  
  СброситьБуфер экспортёра - пустая реализация (no-op), потому что экспортёр синхронный и не буферизует данные. Формально "hint" выполняется тривиально, но без явной работы по отправке прежних метрик. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер - Процедура (void), не возвращает статус succ/fail/timeout. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер - пустая процедура без параметра таймаута; прерывание по таймауту не реализовано явно, но операция тривиальна (завершается мгновенно). (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `MetricExporter` instance.  
  Закрыть() идемпотентен (Закрыт.Установить(Истина) можно вызывать повторно без побочных эффектов), но явной защиты/проверки повторного вызова (как в ридере через СравнитьИУстановить) нет. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64`)

- ❌ **[Metrics Sdk]** [SHOULD] `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics.  
  В интерфейсе ИнтерфейсПродюсерМетрик нет параметров/конфигурации AggregationTemporality; продюсеры не принимают этот параметр. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The option SHOULD accept any form allowed by the underlying gRPC client implementation.  
  gRPC транспорт принимает адрес и передаёт его в oint/api/grpc клиент, но специальная обработка форм адреса (unix:, dns:, etc.) не реализована — URL разбирается как http/https. (`src/Экспорт/Классы/ОтелGrpcТранспорт.os:1`)

- ❌ **[Otlp Exporter]** [SHOULD] If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format for that implementation.  
  Преобразование URL http/https в альтернативную форму для gRPC-клиента не реализовано — адрес передаётся как есть. (-)

- ❌ **[Otlp Exporter]** [SHOULD] However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification.  
  Obsolete-переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE не реализованы и, следовательно, требование о сохранении совместимости неприменимо к их наличию; однако в коде нет поддержки этих устаревших имён. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default.  
  Значение по умолчанию для otel.exporter.otlp.protocol = http/json, а не http/protobuf как требует спецификация. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:606`)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD support both grpc and http/protobuf transports and MUST support at least one of them.  
  Реализованы grpc (ОтелGrpcТранспорт) и http/json (ОтелHttpТранспорт). Значение http/protobuf принимается, но транспорт http всегда сериализует тело в JSON (ЗаписатьJSON в ОтелHttpТранспорт), отдельной реализации http/protobuf нет. (`src/Экспорт/Классы/ОтелGrpcТранспорт.os:1`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one, it SHOULD be http/protobuf.  
  SDK поддерживает более одного транспорта (grpc и http/json), поэтому условие «если поддерживается только один» формально не активно; однако реального http/protobuf нет, а http/json технически не соответствует названию. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:64`)

- ❌ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default (e.g.  
  Значение по умолчанию otel.exporter.otlp.protocol = http/json (см. ПротоколHttpJson), а не http/protobuf, как требует спецификация. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:606`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  Заголовок User-Agent не устанавливается ни в ОтелHttpТранспорт, ни в ОтелGrpcТранспорт — поиск по коду (grep по 'User-Agent'/'userAgent') не нашёл реализации. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231.  
  Заголовок User-Agent не формируется, следовательно формат RFC 7231 не применяется. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string.  
  Конфигурационной опции для product identifier в User-Agent нет, так как сам User-Agent не реализован. (-)

- ⚠️ **[Propagators]** [SHOULD] If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API.  
  В SDK нет pre-configured пропагаторов: если пользователь не задал, ПолучитьПропагаторы возвращает ОтелНоопПропагатор вместо композита W3C Trace Context + W3C Baggage. Классы W3C-пропагаторов существуют (ОтелW3CПропагатор, ОтелW3CBaggageПропагатор), но не используются по умолчанию. (`src/Ядро/Модули/ОтелГлобальный.os:132`)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  В функциях парсинга Boolean (Отключён в Автоконфигурации и Insecure в настройках TLS) отсутствует логирование предупреждения при получении невалидного значения - функции просто возвращают false без вывода warning. (-)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 3 | MUST | ✅ found | In the cases where an extremely clear, pre-existing option is not available, OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: | `src/Ядро/Модули/ОтелКонтекст.os:35` |  |
| 5 | SHOULD NOT | ✅ found | Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. | `src/Ядро/Модули/ОтелКонтекст.os:36` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key. | `src/Ядро/Классы/ОтелКлючКонтекста.os:1` |  |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:113` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the `Context` for the specified key. | `src/Ядро/Модули/ОтелКонтекст.os:114` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 10 | MUST | ✅ found | The API MUST return a new `Context` containing the new value. | `src/Ядро/Модули/ОтелКонтекст.os:130` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries. | `src/Ядро/Модули/ОтелКонтекст.os:203` |  |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the `Context` associated with the caller's current execution unit. | `src/Ядро/Модули/ОтелКонтекст.os:63` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:246` |  |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:252` |  |

#### Detach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#detach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API MUST accept the following parameters: * A `Token` that was returned by a previous call to attach a `Context`. | `src/Ядро/Классы/ОтелОбласть.os:22` |  |

### Baggage Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Each name in `Baggage` MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелBaggage.os:3` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:1` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:152` |  |

#### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | To access the value for a name/value pair set by a prior event, the Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if th... | `src/Ядро/Классы/ОтелBaggage.os:38` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. | `src/Ядро/Классы/ОтелBaggage.os:103` |  |

#### Set Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | To record the value for a name/value pair, the Baggage API MUST provide a function which takes a name, and a value as input. | `src/Ядро/Классы/ОтелBaggage.os:68` |  |

#### Remove Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#remove-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | To delete a name/value pair, the Baggage API MUST provide a function which takes a name as input. | `src/Ядро/Классы/ОтелBaggage.os:82` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the `Context`, it MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Ключ контекста Baggage экспортирован через Функция КлючBaggage() Экспорт, то есть доступен API-пользователям. Это нарушает рекомендацию скрывать ключ - правильнее оставить его внутренним (не-Экспорт) и работать через BaggageИзКонтекста/КонтекстСBaggage. |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:100` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:100` |  |

#### Clear Baggage in the Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#clear-baggage-in-the-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | To avoid sending any name/value pairs to an untrusted process, the Baggage API MUST provide a way to remove all baggage entries from a context. | `src/Ядро/Классы/ОтелBaggage.os:94` |  |

#### Propagation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#propagation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following `Propagator`s: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |

#### Conflict Resolution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#conflict-resolution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:99, src/Ядро/Классы/ОтелПостроительРесурса.os:61` |  |
| 2 | MUST | ✅ found | When associated with a `TracerProvider`, all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:346` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:107` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a `TracerProvider` or `MeterProvider` if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:356, src/Метрики/Классы/ОтелПровайдерМетрик.os:303` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource, from `Attributes`. | `src/Ядро/Классы/ОтелПостроительРесурса.os:61` |  |

#### Merge

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:41` |  |
| 7 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:58` |  |
| 8 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:61` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17, src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:17, src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:17` |  |
| 11 | MUST NOT | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:20` |  |
| 12 | SHOULD | ⚠️ partial | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:25` | Исключения при детекции логируются на уровне Отладка (Debug), а не Ошибка. Ошибка поглощается без сообщения об ошибке согласно Error Handling. |
| 13 | MUST | ✅ found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18, src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:18, src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:18` |  |
| 14 | SHOULD | ✅ found | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate... | `src/Ядро/Классы/ОтелРесурс.os:99` |  |
| 15 | MUST | ✅ found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:43` |  |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:151` |  |
| 17 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:754` |  |
| 18 | MUST | ✅ found | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:755` |  |
| 19 | SHOULD | ⚠️ partial | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:742` | При сбое декодирования пропускается только некорректная пара (пропуск по отсутствию '='), вся строка целиком не отбрасывается, как требует спецификация. |
| 20 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | Ошибки декодирования не логируются и не репортятся через Error Handling; некорректные пары молча пропускаются без сообщения об ошибке. |

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:33` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:345` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: Get a `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: `name` (required), `version` (optional), `schema_url` (optional), `attributes` (optional). | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library, package, module or class name. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:53` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:70` |  |
| 7 | SHOULD | ✅ found | its `name` property SHOULD be set to an empty string. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:73` |  |
| 8 | SHOULD | ✅ found | a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71` |  |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:318` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: Extract the `Span` from a `Context` instance; Combine the `Span` with a `Context` instance, creating a new `Context` instance. | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:44` | КлючСпана() экспортирован из модуля ОтелКонтекст, то есть ключ контекста технически доступен внешнему коду. Основной API (СпанИзКонтекста/КонтекстСоСпаном/ТекущийСпан) абстрагирует ключ, но сам ключ не скрыт. |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context`, the API SHOULD also provide the following functionality: Get the currently active span from the implicit context; Set the currently active span into a new context. | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The `Tracer` MUST provide functions to: Create a new `Span`. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 15 | SHOULD | ✅ found | The `Tracer` SHOULD provide functions to: Report if `Tracer` is `Enabled`. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API MUST implement methods to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252` |  |
| 17 | SHOULD | ✅ found | These methods SHOULD be the only way to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252` |  |
| 18 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |
| 19 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | The API MUST allow retrieving the TraceId and SpanId in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 21 | MUST | ✅ found | Hex - returns the lowercase hex encoded TraceId (result MUST be a 32-hex-character lowercase string) or SpanId (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 22 | MUST | ✅ found | Hex - returns the lowercase hex encoded TraceId (result MUST be a 32-hex-character lowercase string) or SpanId (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 23 | MUST | ✅ found | Binary - returns the binary representation of the TraceId (result MUST be a 16-byte array) or SpanId (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84` |  |
| 24 | MUST | ✅ found | Binary - returns the binary representation of the TraceId (result MUST be a 16-byte array) or SpanId (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:93` |  |
| 25 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:3` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ✅ found | An API called IsValid, that returns a boolean value, which is true if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST | ✅ found | An API called IsRemote, that returns a boolean value, which is true if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` |  |
| 28 | MUST | ✅ found | When extracting a SpanContext through the Propagators API, IsRemote MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:126` |  |
| 29 | MUST | ✅ found | When extracting a SpanContext through the Propagators API, IsRemote MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Tracing API MUST provide at least the following operations on TraceState: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:52` |  |
| 31 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:364` |  |
| 32 | MUST | ✅ found | All mutating operations MUST return a new TraceState with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:112` |  |
| 33 | MUST | ✅ found | TraceState MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:74` |  |
| 34 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:75` |  |
| 35 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return TraceState containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:75` |  |
| 36 | MUST | ✅ found | If invalid value is passed the operation MUST NOT return TraceState containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:76` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | `src/Трассировка/Классы/ОтелПостроительСпана.os:129` |  |
| 38 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability. | `src/Трассировка/Классы/ОтелПостроительСпана.os:129` |  |
| 39 | SHOULD | ✅ found | A Span's start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:632` |  |
| 40 | SHOULD | ✅ found | After the Span is created, it SHOULD be possible to change its name, set its Attributes, add Events, and set the Status. | `src/Трассировка/Классы/ОтелСпан.os:259` |  |
| 41 | MUST NOT | ✅ found | These MUST NOT be changed after the Span's end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:260` |  |
| 42 | SHOULD NOT | ⚠️ partial | To prevent misuse, implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:146` | Метод Атрибуты() экспортирован и доступен внешнему коду (не только процессорам/экспортерам), что нарушает рекомендацию скрывать атрибуты. Публичный геттер позволяет читать атрибуты после установки. |
| 43 | MUST NOT | ⚠️ partial | However, alternative implementations MUST NOT allow callers to create Spans directly. | `src/Трассировка/Классы/ОтелСпан.os:599` | Конструктор ОтелСпан публичный, OneScript не поддерживает ограничение видимости конструктора. Пользователь может вызвать Новый ОтелСпан(...) напрямую, обходя Tracer. Документированный путь - через Tracer.ПостроительСпана(). |
| 44 | MUST | ✅ found | All Spans MUST be created via a Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ⚠️ partial | There MUST NOT be any API for creating a Span other than with a Tracer. | `src/Трассировка/Классы/ОтелСпан.os:599` | Публичный конструктор ОтелСпан доступен для прямого вызова (Новый ОтелСпан(...)). Платформа OneScript не позволяет ограничить видимость конструктора. Фактический документированный путь - только через Tracer, но запрет прямого создания не форсируется кодом. |
| 46 | MUST NOT | ✅ found | In languages with implicit Context propagation, Span creation MUST NOT set the newly created Span as the active Span in the current Context by default, but this functionality MAY be offered additionally as a separate operation. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 47 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` |  |
| 48 | MUST NOT | ✅ found | This API MUST NOT accept a Span or SpanContext as parent, only a full Context. | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` |  |
| 49 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелПостроительСпана.os:36` |  |
| 50 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:70` |  |
| 51 | SHOULD | ✅ found | This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:108` |  |
| 52 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:108` |  |
| 53 | MUST | ✅ found | Implementations MUST provide an option to create a Span as a root span, and MUST generate a new TraceId for each root span created. | `src/Трассировка/Классы/ОтелПостроительСпана.os:50` |  |
| 54 | MUST | ✅ found | Implementations MUST provide an option to create a Span as a root span, and MUST generate a new TraceId for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:124` |  |
| 55 | MUST | ✅ found | For a Span with a parent, the TraceId MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:159` |  |
| 56 | MUST | ✅ found | Also, the child span MUST inherit all TraceState values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:289` |  |
| 57 | MUST | ✅ found | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | During Span creation, a user MUST have the ability to record links to other Spans. | `src/Трассировка/Классы/ОтелПостроительСпана.os:97` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The Span interface MUST provide: An API that returns the `SpanContext` for the given `Span`. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 60 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |

#### IsRecording

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:246` |  |
| 62 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:246` |  |
| 63 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:246` |  |
| 64 | SHOULD | ✅ found | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | `src/Трассировка/Классы/ОтелСпан.os:246` |  |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:275` |  |
| 66 | MUST | ✅ found | The Span interface MUST provide: An API to set a single `Attribute` where the attribute properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:275` |  |
| 67 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute's value. | `src/Трассировка/Классы/ОтелСпан.os:290` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST | ✅ found | A `Span` MUST have the ability to add events. | `src/Трассировка/Классы/ОтелСпан.os:305` |  |
| 69 | MUST | ✅ found | The Span interface MUST provide: An API to record a single `Event` where the `Event` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:305` |  |
| 70 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:309` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:373` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | `Description` MUST only be used with the `Error` `StatusCode` value. | `src/Трассировка/Классы/ОтелСпан.os:441` |  |
| 73 | MUST | ✅ found | The Span interface MUST provide: An API to set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 74 | SHOULD | ✅ found | This SHOULD be called `SetStatus`. | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 75 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:441` |  |
| 76 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 77 | SHOULD | ⚠️ partial | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:425` | Явной проверки на попытку установить Unset нет; при текущем КодСтатуса=НеУстановлен вызов УстановитьСтатус(НеУстановлен) эффективно no-op (присвоение того же значения), но при КодСтатуса=Ошибка переход в Unset явно блокируется, а в других веток код Unset всё же переприсваивается, что формально отличается от требования 'ignored'. |
| 78 | SHOULD | ✅ found | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 79 | SHOULD | ✅ found | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | - |  |
| 80 | SHOULD NOT | ✅ found | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | - |  |
| 81 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | - |  |
| 82 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:431` |  |
| 83 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:431` |  |
| 84 | SHOULD | ✅ found | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | - |  |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended. | `src/Трассировка/Классы/ОтелСпан.os:460` |  |
| 86 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 87 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 88 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 89 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 90 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:410` |  |
| 91 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:461` |  |
| 92 | MUST NOT | ⚠️ partial | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:459` | Сам Завершить() не выполняет I/O напрямую, но синхронно вызывает Процессор.ПриЗавершении(), и ОтелПростойПроцессорСпанов экспортирует спан синхронно в вызывающем потоке, что эквивалентно блокирующему I/O на calling thread. |
| 93 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a `RecordException` method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:329` |  |
| 95 | MUST | ✅ found | The method MUST record an exception as an `Event` with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:358` |  |
| 96 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:329` |  |
| 97 | MUST | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:329` |  |
| 98 | SHOULD | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:352-358` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:632` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ⚠️ partial | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | `src/Трассировка/Классы/ОтелНоопСпан.os:279` | Операция реализована через конструктор Новый ОтелНоопСпан(КонтекстСпана), но отдельного метода API (например, Tracer.WrapSpanContext) не существует. Используется в пропагаторах (W3C/B3), но публично оформленного wrap-метода нет. |
| 101 | SHOULD NOT | ❌ not_found | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | - | Тип ОтелНоопСпан зарегистрирован как публичный класс в lib.config и напрямую инстанциируется снаружи (пропагаторы, Tracer). Нет скрытой/пакетной видимости. |
| 102 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | `src/Трассировка/Классы/ОтелНоопСпан.os` | Класс назван ОтелНоопСпан (NoopSpan), не NonRecordingSpan. Семантически эквивалентно, но имена различаются. |
| 103 | MUST | ✅ found | `GetContext` MUST return the wrapped `SpanContext`. | `src/Трассировка/Классы/ОтелНоопСпан.os:30` |  |
| 104 | MUST | ✅ found | `IsRecording` MUST return `false` to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНоопСпан.os:148-150` |  |
| 105 | MUST | ✅ found | The remaining functionality of `Span` MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:159-253` |  |
| 106 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os` |  |
| 107 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | SHOULD | ✅ found | In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | `src/Трассировка/Модули/ОтелВидСпана.os` |  |
| 109 | SHOULD NOT | ✅ found | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | `src/Трассировка/Модули/ОтелВидСпана.os` |  |

#### Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 110 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:373` |  |
| 111 | MUST | ✅ found | The API MUST provide: An API to record a single `Link` where the `Link` properties are passed as arguments. | `src/Трассировка/Классы/ОтелПостроительСпана.os:97` |  |
| 112 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:373-391` |  |
| 113 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:389` |  |
| 114 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can only consider information present during s... | `src/Трассировка/Классы/ОтелПостроительСпана.os:87-88` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 115 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:7` |  |
| 116 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3-4` |  |
| 117 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3-4` |  |
| 118 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 119 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:384-389` | Линк хранится как Соответствие (не отдельный иммутабельный класс). После добавления в массив Линки не изменяется, но формальной документации иммутабельности и конкурентной безопасности для Link нет. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 120 | MUST | ⚠️ partial | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Ядро/Модули/ОтелГлобальный.os:143-160` | При отсутствии SDK ПолучитьАктивныйСдк() возвращает кэшированный SDK с сэмплером ВсегдаВыключен, НачатьСпан возвращает ОтелНоопСпан с контекстом, унаследованным от родителя, но с НОВЫМ SpanId (СоздатьНоопСпанДляОтброшенного в ОтелТрассировщик.os:213). Спека требует вернуть non-recording span с тем же SpanContext, что в parent Context, а не генерировать новый SpanId. |
| 121 | SHOULD | ❌ not_found | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | - | Нет проверки ЗаписьАктивна()/IsRecording у родительского спана в ОтелТрассировщик.НачатьСпан - всегда создаётся новый экземпляр (ОтелСпан или ОтелНоопСпан), даже если родитель уже non-recording. |
| 122 | MUST | ⚠️ partial | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелТрассировщик.os:56-68` | В noop-режиме (AlwaysOff) без родителя генерируются НЕ нулевые TraceId/SpanId, а полноценные идентификаторы (Провайдер.СгенерироватьИдТрассировки/СгенерироватьИдСпана), затем возвращается NoopSpan. Спека требует all-zero IDs. |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:10` |  |
| 2 | MUST | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:96` |  |
| 3 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:367` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:129` |  |
| 5 | SHOULD | ⚠️ partial | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:78` | После Закрыть() ПолучитьТрассировщик возвращает новый экземпляр ОтелТрассировщик, а не NoOp-трассировщик. Спаны могут всё ещё создаваться, хотя процессоры уже закрыты. |
| 6 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:154` | Синхронный Закрыть - процедура без возврата статуса. Асинхронный ЗакрытьАсинхронно возвращает Обещание, но таймаут контролируется только вызывающей стороной через Обещание.Получить(таймаут); внутреннего таймаута нет. |
| 7 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:128` | Сама процедура Закрыть не принимает параметр таймаута и не прерывается. Таймаут возможен только через внешнее Обещание.Получить(timeout) при использовании ЗакрытьАсинхронно. |
| 8 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:132` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:143` | Синхронный СброситьБуфер - процедура без возврата статуса. Асинхронный СброситьБуферАсинхронно возвращает Обещание, но таймаут контролируется только вызывающей стороной через Обещание.Получить(таймаут); внутреннего таймаута нет. |
| 10 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118` | Сама процедура СброситьБуфер не принимает параметр таймаута и не прерывается. Таймаут возможен только через внешнее Обещание.Получить(timeout) при использовании СброситьБуферАсинхронно. |
| 11 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:71` |  |
| 13 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:173` |  |
| 14 | MUST | ✅ found | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:68` |  |
| 15 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended (some languages might implement this by having an end timestamp of `null`, others might have an explicit `hasEnded` boolean). | `src/Трассировка/Классы/ОтелСпан.os:209` |  |
| 16 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:218` |  |
| 17 | MUST | ✅ found | As an exception to the authoritative set of span properties defined in the API spec, implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST ex... | `src/Трассировка/Классы/ОтелСпан.os:101` |  |
| 18 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user (for example, th... | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to true. | `src/Трассировка/Классы/ОтелТрассировщик.os:84` |  |
| 20 | SHOULD NOT | ⚠️ partial | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42` | Процессоры (ОтелПростойПроцессорСпанов, ОтелПакетныйПроцессорСпанов) передают экспортеру все завершённые спаны без фильтрации по Sampled-флагу TraceFlags. RECORD_ONLY-спан (IsRecording=true, Sampled=false) был бы отправлен экспортеру. На практике встроенные сэмплеры не возвращают RECORD_ONLY, но механизм фильтрации отсутствует. |
| 21 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42` |  |
| 22 | SHOULD NOT | ⚠️ partial | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42` | Процессоры не фильтруют по Sampled-флагу перед вызовом экспортера. RECORD_ONLY-спан (IsRecording=true, Sampled=false) будет отправлен экспортеру, нарушая SHOULD NOT. |
| 23 | MUST NOT | ✅ found | The flag combination `SampledFlag == true` and `IsRecording == false` could cause gaps in the distributed trace, and because of this the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:272` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:64` |  |
| 26 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:272` |  |
| 27 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:272` |  |
| 28 | SHOULD | ✅ found | If the sampler returns an empty `Tracestate` here, the `Tracestate` will be cleared, so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Модули/ОтелСэмплер.os:141` |  |

#### GetDescription

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#getdescription)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD NOT | ✅ found | Callers SHOULD NOT cache the returned value. | `src/Трассировка/Модули/ОтелСэмплер.os:106` |  |

#### AlwaysOn

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Description MUST be `AlwaysOnSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:109` |  |

#### AlwaysOff

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysoff)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 31 | MUST | ✅ found | Description MUST be `AlwaysOffSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:111` |  |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 32 | SHOULD | ✅ found | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | ФлагиТрассировки используют только бит sampled (0x01): для корневых спанов не устанавливается бит Random (0x02) W3C Trace Context Level 2 - см. ОтелТрассировщик.ВычислитьФлагиТрассировки (возвращает 0 или 1) и ОтелКонтекстСпана (ФлагиТрассировки=1). |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST NOT | ✅ found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:189` |  |

#### Presumption of TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#presumption-of-traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ✅ found | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState. | `src/Трассировка/Модули/ОтелСэмплер.os:139` |  |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | SHOULD | ❌ not_found | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated. | - | IdGenerator расширение есть (ОтелПровайдерТрассировки.УстановитьГенераторИд), но механизм задания W3C Trace Context Level 2 Random flag отсутствует - TraceFlags random bit не поддерживается и не пробрасывается из IdGenerator. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 38 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java example bellow. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:76` |  |
| 39 | SHOULD | ⚠️ partial | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:40` | Опции названы МаксСобытий (MaxEvents) и МаксЛинков (MaxLinks) - семантика корректна, но дословный перевод имён не совпадает с EventCountLimit/LinkCountLimit (отсутствует 'Count' в имени). |
| 40 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 41 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK’s log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:480` |  |
| 42 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:481` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 44 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:93` |  |
| 45 | MUST | ✅ found | The SDK MAY provide this functionality by allowing custom implementations of an interface like the java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with SpanContext), which provides extension points... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:234` |  |
| 46 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | `src/Трассировка/` |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:90` |  |
| 48 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:44` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: OnStart OnEnd Shutdown ForceFlush. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11-46` |  |
| 50 | SHOULD | ✅ found | The `SpanProcessor` interface SHOULD declare the following methods: OnEnding method. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |

#### OnStart

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onstart)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 52 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:459-474` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:470-472` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:78` |  |
| 55 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:43-45` |  |
| 56 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:77; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80` | Закрыть - процедура без возвращаемого значения. Вызывающий не может отличить успех, ошибку или таймаут; ошибки передаются только через исключения, а таймаут тихо логируется без индикатора результата. |
| 57 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80-87` |  |
| 58 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80-87, 126-146` |  |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73, 126-146` |  |
| 60 | SHOULD | ✅ found | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:148-166` |  |
| 61 | MUST | ✅ found | The built-in SpanProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:66-70` |  |
| 62 | MUST | ✅ found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:126-146` |  |
| 63 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73` | СброситьБуфер - процедура без возвращаемого значения. Таймаут только логируется (Лог.Предупреждение), успех/неудача/таймаут неразличимы для вызывающего. |
| 64 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73` |  |
| 65 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73, 126-146` |  |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:49` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:155` |  |
| 69 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:61` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:7` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:14` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:48` |  |
| 73 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47` |  |
| 74 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:159` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57` |  |
| 76 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57` | СброситьБуфер() объявлена как Процедура (void) - не возвращает статус успеха/неудачи/таймаута. Ошибки всплывают исключениями, но таймаут неотличим от успеха. |
| 77 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports ... | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57` |  |
| 78 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57` | СброситьБуфер() экспортера не принимает параметр таймаута. Для синхронного экспортера это no-op (завершается мгновенно), но механизма прерывания по таймауту нет. На уровне процессора таймаут поддержан (ОтелБазовыйПакетныйПроцессор.СброситьБуфер(ТаймаутМс)). |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:368` |  |
| 80 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:106` |  |
| 81 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:49` |  |
| 82 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:63` |  |

### Logs Api

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:33` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: Get a `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:56` |  |

#### Get a Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#get-a-logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: name, version (optional), schema_url (optional), attributes (optional). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:56` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: Emit a `LogRecord`. | `src/Логирование/Классы/ОтелЛоггер.os:94` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: Report if `Logger` is `Enabled`. | `src/Логирование/Классы/ОтелЛоггер.os:49` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: Timestamp (optional), Observed Timestamp (optional), The Context associated with the `LogRecord`, Severity Number (optional), Severity Text (optional), Body (optional), Attributes (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЗаписьЛога.os:308` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:94` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:100` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:94` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:49` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:49` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:50` |  |
| 14 | MUST | ⚠️ partial | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:68` | Контекст = Неопределено разрешается в текущий контекст только внутри ТрассировкаНеСэмплирована (ветка trace-based фильтрации), но в процессор Включен передаётся исходное Неопределено без явного вызова ОтелКонтекст.Текущий(); разрешение контекста не универсально для всех веток API. |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:47` |  |
| 16 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28` | Комментарий к методу описывает назначение Включен (пропустить создание LogRecord если логгер ничего не сделает) и упоминает, что возвращаемое значение не статично, но отсутствует явное указание вызывать API каждый раз перед эмиссией LogRecord для получения актуального ответа. |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:49` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:49` |  |
| 19 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:56` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7` |  |
| 21 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:273` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:269` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `LoggerProvider` MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:269` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the `LogRecord`s produced by any `Logger` from the `LoggerProvider`. | `src/Логирование/Классы/ОтелЛоггер.os:96` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:269` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:281` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained f... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:100` |  |
| 7 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained f... | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:133` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:67` |  |
| 10 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:160` |  |
| 11 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:132` | Метод Закрыть() не принимает таймаут и вызывает Процессор.Закрыть() без таймаута. Таймаут доступен только косвенно через ЗакрытьАсинхронно().Получить(таймаут), что прерывает ожидание, но не саму операцию закрытия процессоров. |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:136` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:148` |  |
| 14 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:122` | СброситьБуфер() - процедура (void). ERROR-сигнал доступен только косвенно через СброситьБуферАсинхронно() (Обещание). Явного возврата ERROR/NO ERROR из синхронного API нет. |
| 15 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:122` | Синхронный СброситьБуфер() ничего не возвращает (NO ERROR/успех неотличим). Статус доступен только через СброситьБуферАсинхронно(). |
| 16 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:122` | Provider.СброситьБуфер() вызывает Процессор.СброситьБуфер() без параметра таймаута. Композитный процессор поддерживает таймаут внутри, но провайдер передаёт 0 (без ограничения). Прерывание возможно только через Обещание.Получить(таймаут). |
| 17 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:51` |  |
| 19 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the `LogRecord`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:132` |  |
| 20 | MUST | ✅ found | The trace context fields MUST be populated from the resolved `Context` (either the explicitly passed `Context` or the current `Context`) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 21 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:150` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes, TraceId, SpanId, TraceFlags, EventName. | `src/Логирование/Классы/ОтелЗаписьЛога.os:179` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | `LogRecord` attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:230` |  |
| 24 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the `LoggerProvider`, by allowing users to configure individual limits like in the Java example below. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50` |  |
| 25 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `LogRecordLimits`. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1` |  |
| 26 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:384` |  |
| 27 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per `LogRecord` (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:385` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18` |  |
| 29 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | SHOULD NOT | ✅ found | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` |  |
| 31 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` |  |
| 32 | SHOULD | ❌ not_found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | - | В документации процессоров/логгера нет рекомендации клонировать ЗаписьЛога для конкурентной обработки. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST NOT | ✅ found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:26` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:132` |  |
| 35 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:67` |  |
| 36 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:87` | Закрыть - Процедура (void), без возврата статуса. Асинхронная обёртка ЗакрытьАсинхронно возвращает Обещание на уровне провайдера, но у самого процессора статус успех/отказ/таймаут не возвращается.   |
| 37 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80` |  |
| 38 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:87` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 39 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be complet... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71` |  |
| 40 | SHOULD | ✅ found | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `Forc... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:148` |  |
| 41 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:18` |  |
| 42 | MUST | ✅ found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:129` |  |
| 43 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71` | СброситьБуфер - Процедура без возврата статуса. Провайдер предоставляет СброситьБуферАсинхронно → Обещание, но у самого процессора статус операции не возвращается. |
| 44 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProce... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:122` |  |
| 45 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71` |  |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 47 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 48 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:155` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:6` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:11` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:46` |  |
| 53 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:42-50` |  |
| 54 | SHOULD NOT | ✅ found | The default SDK's `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62` |  |
| 56 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62` | ОтелЭкспортерЛогов.СброситьБуфер() - Процедура (void), не возвращает статус успеха/ошибки/таймаута. На уровне Провайдера есть СброситьБуферАсинхронно() с Обещанием, но у самого экспортера возврата статуса нет. |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter expo... | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62` |  |
| 58 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62` | ОтелЭкспортерЛогов.СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по таймауту (синхронный экспортер, сам экспорт уже ограничен таймаутом в Экспортировать). |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:67` |  |
| 60 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34-36` |  |
| 61 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:67-69` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:282-289` |  |
| 63 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os` |  |
| 64 | MUST | ✅ found | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:69` |  |

### Metrics Api

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ⚠️ partial | Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:100` | Глобальный доступ к Meter осуществляется через ОтелГлобальный.ПолучитьМетр(), установка провайдера метрик - через билдер SDK (ОтелПостроительSdk.УстановитьПровайдерМетрик) и ОтелГлобальный.Установить(Сдк). Отдельного global MeterProvider getter/setter (как SetGlobalMeterProvider/GetGlobalMeterProvider) нет - доступ опосредован через глобальный SDK. |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `MeterProvider` MUST provide the following functions: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |
| 4 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:61` |  |
| 5 | MUST | ✅ found | Therefore, this API needs to be structured to accept a `schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:63` |  |
| 6 | MUST | ⚠️ partial | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` | Параметр АтрибутыОбласти принимает ОтелАтрибуты-контейнер (или Неопределено) - т.е. 'переменное число атрибутов, включая ноль' поддерживается через объект-контейнер, а не через варargs/массив. Семантически соответствует, но не через variadic-параметр. |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Note: `Meter` SHOULD NOT be responsible for the configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:260` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The `Meter` MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:51` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ➖ n_a | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | - | В OneScript единый числовой тип System.Decimal - различия integer/floating point на уровне языка отсутствуют, поэтому требование неприменимо к платформе. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:53` |  |
| 11 | MUST | ⚠️ partial | It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:621` | Строки в OneScript регистрозависимы по умолчанию (сравнение '=' case-sensitive), поэтому case-sensitivity обеспечивается платформой. Однако проверки на ASCII-only (отклонение/валидация не-ASCII символов) нет - единица измерения принимается как произвольная строка. |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:66` |  |
| 13 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11` |  |
| 14 | MUST | ✅ found | It MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11` |  |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 16 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 17 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:42` |  |
| 18 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:42` | Комментарии к методам СоздатьСчетчик/СоздатьГистограмму/СоздатьДатчик описывают параметр Имя, но не упоминают правила синтаксиса имён инструментов (instrument name syntax). |
| 19 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 20 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 21 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:13` |  |
| 22 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 23 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 24 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11` |  |
| 25 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 26 | SHOULD NOT | ⚠️ partial | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:796` | ПроверитьСовет() выполняет лёгкую валидацию типов advisory (Структура, Массив) с логированием предупреждений, тогда как спека говорит SHOULD NOT validate. |
| 27 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 28 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 29 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:272` |  |
| 30 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:272` | Комментарии к СоздатьНаблюдаемый* описывают параметр Имя, но не упоминают правила синтаксиса имён инструментов. |
| 31 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 32 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 33 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:12` |  |
| 34 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 35 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 36 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:10` |  |
| 37 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 38 | SHOULD NOT | ⚠️ partial | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:796` | ПроверитьСовет() выполняет лёгкую валидацию типов advisory с логированием предупреждений, что противоречит SHOULD NOT validate. |
| 39 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 40 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 41 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` |  |
| 42 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registrati... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:69` |  |
| 43 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:168` |  |
| 44 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелМетр.os:276` |  |
| 45 | SHOULD | ✅ found | Callback functions SHOULD be reentrant safe. | `src/Метрики/Классы/ОтелМетр.os:277` |  |
| 46 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT take an indefinite amount of time. | `src/Метрики/Классы/ОтелМетр.os:279` |  |
| 47 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | `src/Метрики/Классы/ОтелМетр.os:280` |  |
| 48 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 49 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелМетр.os:547` |  |
| 50 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:528` |  |
| 51 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be report... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:188` |  |
| 52 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be report... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:188` |  |
| 53 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:171` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is `Enabled` | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259` |  |
| 56 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259` |  |
| 57 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:260` |  |
| 58 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:248` | Документация метода Включен() описывает, что значение может изменяться, но не содержит явной рекомендации вызывать API при каждом измерении для получения актуального значения. |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:51` |  |

#### Counter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 61 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:13` |  |
| 64 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:13` |  |
| 65 | SHOULD NOT | ⚠️ partial | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:22` | Добавить() проверяет Значение < 0 и молча игнорирует отрицательные значения — это валидация на уровне API, тогда как спека говорит SHOULD NOT validate. |
| 66 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 67 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:291` |  |
| 69 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:188` |  |
| 70 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:188` |  |
| 71 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:174` |  |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Histogram` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:90` |  |

#### Histogram operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 74 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value to record. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 76 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:13` |  |
| 77 | SHOULD | ⚠️ partial | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелГистограмма.os:13` | Документирующий комментарий метода Записать описывает параметр как 'измеренное значение', но не упоминает явно что значение должно быть неотрицательным. |
| 78 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 79 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Gauge` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:241` |  |

#### Gauge operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 82 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value. The current absolute value. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 84 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:12` |  |
| 85 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 86 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:392` |  |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ✅ found | There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:202` |  |

#### UpDownCounter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:20` |  |
| 90 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:20` |  |
| 91 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:20` |  |
| 92 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:10` |  |
| 93 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:20` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:344` |  |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: | `src/Метрики/Классы/ОтелМетр.os:528` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелМетр.os:1` |  |
| 97 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелМетр.os:51` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:32` |  |
| 99 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:37` |  |
| 100 | MUST | ⚠️ partial | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:49` | Потокобезопасность документирована только для синхронных инструментов (ОтелБазовыйСинхронныйИнструмент:49-50). Базовый класс наблюдаемых инструментов (ОтелБазовыйНаблюдаемыйИнструмент) не содержит комментария о thread-safety на уровне класса. |

### Metrics Sdk

#### Metrics SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metrics-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:297` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:80` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:297` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration ( i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:16` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `Mete... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:223` |  |
| 7 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `Mete... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:270` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:144` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:70` |  |
| 10 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:179` |  |
| 11 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:179` | Синхронный метод Закрыть() не принимает таймаут. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, таймаут задаётся снаружи через Обещание.Получить(), но внутренняя операция Закрыть() не прерывается при превышении. |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:151` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:128` |  |
| 14 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:167` |  |
| 15 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERRO... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:167` | Асинхронный СброситьБуферАсинхронно() возвращает Обещание, которое может быть отклонено при исключении, но явного ERROR/NO ERROR статус-объекта нет. Синхронная СброситьБуфер() - процедура без возвращаемого статуса. |
| 16 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:167` | Синхронная СброситьБуфер() не принимает таймаут. Асинхронная СброситьБуферАсинхронно() возвращает Обещание, таймаут можно задать через Обещание.Получить(), но сама операция не прерывается при превышении. |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 18 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:191` |  |
| 19 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:191` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:34` |  |
| 21 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 22 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 23 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 24 | MUST NOT | ✅ found | Users can provide a `type`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 25 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 26 | MUST NOT | ✅ found | Users can provide a `meter_name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 27 | MUST NOT | ✅ found | Users can provide a `meter_version`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 28 | MUST NOT | ✅ found | Users can provide a `meter_schema_url`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 29 | MUST NOT | ➖ n_a | Users can provide these additional criteria the SDK accepts, but it is up to their discretion. Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | - | SDK не принимает дополнительные критерии сверх перечисленных в спецификации, поэтому требование к 'additional criteria' не применимо. |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 31 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:306` |  |
| 32 | SHOULD | ⚠️ partial | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | - | Нет явной проверки/предупреждения, что при заданном NewName селектор не должен сопоставляться более чем с одним инструментом (no fail-fast). |
| 33 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 34 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:283` |  |
| 35 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:309` |  |
| 36 | MUST NOT | ✅ found | Users can provide a `description`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 37 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:284` |  |
| 38 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелМетр.os:657` |  |
| 39 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелМетр.os:657` |  |
| 40 | MUST NOT | ✅ found | Users can provide `attribute_keys`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 41 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:650` |  |
| 42 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелМетр.os:650` |  |
| 43 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:10` |  |
| 44 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелМетр.os:661` |  |
| 45 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелМетр.os:661` |  |
| 46 | MUST NOT | ✅ found | Users can provide an `aggregation`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 47 | MUST | ✅ found | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:250` |  |
| 48 | MUST NOT | ✅ found | Users can provide an `exemplar_reservoir`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 49 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:323` |  |
| 50 | MUST NOT | ✅ found | Users can provide an `aggregation_cardinality_limit`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 51 | MUST | ✅ found | If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:253` |  |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Классы/ОтелМетр.os:635` |  |
| 53 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:654` |  |
| 54 | SHOULD | ❌ not_found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | - | View применяется, но нет диагностики 'conflicting metric identities' (когда несколько View дают одинаковый идентификатор потока). |
| 55 | SHOULD | ❌ not_found | If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warnin... | - | Нет проверки семантических ошибок конфигурации View (например, histogram-агрегация для асинхронного инструмента) и соответствующего warning. |
| 56 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:650` |  |
| 57 | SHOULD | ✅ found | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:817` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:15` |  |
| 59 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: Base2 Exponential Bucket Histogram | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:306` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ⚠️ partial | Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:51` | Sum собирается всегда без условного отключения для UpDownCounter/ObservableGauge. По умолчанию эти инструменты не используют гистограмму, но при явной настройке через View нет fallback. |
| 61 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118` |  |
| 62 | SHOULD NOT | ➖ n_a | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | - | OneScript Число = System.Decimal — +Inf, -Inf, NaN физически непредставимы на платформе, требование не применимо. |
| 63 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:218` |  |
| 64 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:306` |  |
| 65 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ⚠️ partial | Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collecti... | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:226` | Callback вызывается при сборе конкретным reader, но состояние инструмента общее для всех reader'ов — нет явной изоляции наблюдений по reader'у. |
| 67 | SHOULD | ⚠️ partial | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:81` | Есть ДобавитьВнешниеНаблюдения, разрешающая наблюдения вне зарегистрированного callback, что противоречит SHOULD-disregard (однако используется интеграциями как дополнительный механизм). |
| 68 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | Вызов ТекущееДействие.Выполнить в ВызватьCallbackИСобрать не ограничен таймаутом, зависшая callback блокирует сбор. |
| 69 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:209` |  |
| 70 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:168` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:192` |  |
| 72 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:98` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелМетр.os:645` |  |
| 74 | SHOULD | ✅ found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:253` |  |
| 75 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:401` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:405` |  |
| 77 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:112` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:170` |  |
| 79 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct a... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:110` |  |
| 80 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:111` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент не содержит логики ограничения кардинальности (нет ЛимитМощности, нет overflow, нет предпочтения первых наблюдений). Async-инструменты собирают все наблюдения без лимита. |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:57` |  |
| 83 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:727` |  |
| 84 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:727` | Предупреждение содержит сравнение старых и новых параметров и факт возврата ранее зарегистрированного инструмента, но не содержит конкретных рекомендаций (например, View-рецепта) по устранению конфликта. |
| 85 | SHOULD | ❌ not_found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | - | В ПроверитьКонфликтДескриптора нет логики, проверяющей, что конфликт описания разрешён через View: предупреждение выдаётся при любом различии Описание. |
| 86 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the war... | - | Текст предупреждения не содержит View-рецепта для переименования; лог выводит только описание конфликта. |
| 87 | SHOULD | ❌ not_found | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument regist... | - | Код возвращает ранее зарегистрированный инструмент (ОтелМетр.os:59), а не регистрирует второй Metric объект с другой единицей. Второй инструмент не создаётся и его данные не проходят отдельным потоком. |
| 88 | MUST | ✅ found | the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:59` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:56` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax. | - | В ОтелМетр.СоздатьСчетчик/СоздатьГистограмму/… имя нормализуется через НРег(), но не валидируется против синтаксиса имени (regex [A-Za-z][A-Za-z0-9_.\-/]{0,254}). Проверок нет ни в одном из методов создания инструмента. |
| 91 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Поскольку валидации имени нет, соответствующее предупреждение о неверном синтаксисе не эмитируется. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:53` |  |
| 93 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:621` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:52` |  |
| 95 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:621` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:796` |  |
| 97 | SHOULD | ⚠️ partial | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:796` | ПроверитьСовет эмитирует предупреждения и при некорректном типе Совет (не Структура) фактически игнорирует его (ПолучитьГраницыИзСовета/ПолучитьКлючиАтрибутовИзСовета возвращают Неопределено). Однако для невалидных вложенных полей (ГраницыГистограммы не Массив, КлючиАтрибутов не Массив) код только логирует, но всё равно возвращает исходное значение в дальнейшие вычисления - т.е. не «proceed as if not provided». |
| 98 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:707` |  |
| 99 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:683` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Классы/ОтелМетр.os:683` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 101 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:1` |  |
| 102 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:311` |  |
| 103 | MUST NOT | ✅ found | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:415` |  |
| 104 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Классы/ОтелФабрикаВыровненныхРезервуаровГистограммы.os:1` |  |
| 105 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74` |  |
| 107 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:299` |  |
| 108 | SHOULD | ✅ found | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:311` |  |
| 109 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114` |  |
| 110 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41` |  |
| 112 | MUST | ✅ found | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:429` |  |
| 113 | SHOULD | ✅ found | The "offer" method SHOULD accept measurements, including: The `value` of the measurement, the complete set of `Attributes` of the measurement, the Context of the measurement (Baggage and active Span), a `timestamp`. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41` |  |
| 114 | SHOULD | ✅ found | The "offer" method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:126` |  |
| 115 | MUST | ⚠️ partial | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additi... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41` | Параметр АтрибутыСерии передаётся в Предложить(), но в документирующем комментарии не подчёркнуто, что филтрованный набор атрибутов может расходиться с таймсерией. |
| 116 | MUST | ⚠️ partial | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additi... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:174` | Атрибуты таймсерии не передаются в резервуар при конструировании - они передаются пер-вызов в Предложить(АтрибутыСерии). Обходной путь, а не "at construction" как требует спека. |
| 117 | MUST | ✅ found | The "collect" method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:57` |  |
| 118 | SHOULD | ✅ found | In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:123` |  |
| 119 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:139` |  |
| 120 | SHOULD | ⚠️ partial | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:121` | СоздатьЭкземпляр создаёт новый Соответствие и новые объекты отфильтрованных атрибутов при каждом вызове Предложить - аллокации не оптимизированы. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: `SimpleFixedSizeExemplarReservoir`, `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1` |  |
| 122 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелМетр.os:137` |  |
| 123 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured ... | `src/Метрики/Классы/ОтелМетр.os:178` |  |
| 124 | SHOULD | ✅ found | All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:323` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 125 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements sho... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:100` |  |
| 126 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:164` |  |
| 127 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:174` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 128 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:194` |  |
| 129 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number o... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:76` |  |
| 130 | SHOULD | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number o... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:56` |  |
| 131 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:194` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 133 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph... | `src/Метрики/Классы/ОтелПредставление.os:83` |  |
| 134 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:432` |  |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | SHOULD | ⚠️ partial | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | СброситьБуфер/СобратьИЭкспортировать - процедуры (void), ошибки логируются, но каллеру не возвращается статус успеха/ошибки/таймаута. |
| 136 | SHOULD | ✅ found | `Collect` SHOULD invoke Produce on registered MetricProducers. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 137 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:112` |  |
| 138 | SHOULD | ⚠️ partial | SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | Reader's СброситьБуфер/СобратьИЭкспортировать не проверяет флаг Закрыт явно; подавление делегируется экспортёру (Экспортировать возвращает Ложь после Закрыть). Нет прямой сигнализации отказа из ридера. |
| 139 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:111` | Закрыть() - Процедура (void), не возвращает статус succ/fail/timeout; таймаут финального ожидания логируется, но не различим от успеха. |
| 140 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:117` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 141 | MUST | ✅ found | The reader MUST synchronize calls to `MetricExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:242` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | СброситьБуфер ридера собирает метрики и вызывает Экспортер.Экспортировать, но НЕ вызывает Экспортер.СброситьБуфер() (ForceFlush) после этого. |
| 143 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | СброситьБуфер - Процедура (void), без возврата статуса; ошибки логируются, но не различимы с таймаутом для вызывающего. |
| 144 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to mod... | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | Статус ERROR/NO ERROR не возвращается - метод void; ошибки только логируются. |
| 145 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | Явного параметра таймаута у СброситьБуфер нет; прерывание делегируется внутреннему Экспортер.Экспортировать (таймаут экспортёра), но собственного таймаута у ридера нет. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 146 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 147 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `Metr... | - | ОтелЭкспортерМетрик не проверяет совместимость агрегации/временности данных и не сообщает об ошибке при неподдерживаемой комбинации. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 148 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:13` |  |
| 149 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 150 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 151 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 152 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:34` |  |
| 153 | SHOULD | ⚠️ partial | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this me... | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58` | СброситьБуфер экспортёра - пустая реализация (no-op), потому что экспортёр синхронный и не буферизует данные. Формально "hint" выполняется тривиально, но без явной работы по отправке прежних метрик. |
| 154 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58` | СброситьБуфер - Процедура (void), не возвращает статус succ/fail/timeout. |
| 155 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports ... | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:55` |  |
| 156 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58` | СброситьБуфер - пустая процедура без параметра таймаута; прерывание по таймауту не реализовано явно, но операция тривиальна (завершается мгновенно). |
| 157 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64` | Закрыть() идемпотентен (Закрыт.Установить(Истина) можно вызывать повторно без побочных эффектов), но явной защиты/проверки повторного вызова (как в ридере через СравнитьИУстановить) нет. |
| 158 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ✅ found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:1` |  |
| 160 | SHOULD | ❌ not_found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | - | В интерфейсе ИнтерфейсПродюсерМетрик нет параметров/конфигурации AggregationTemporality; продюсеры не принимают этот параметр. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | MUST | ✅ found | A `MetricProducer` MUST support the following functions: | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 162 | MUST | ✅ found | A `MetricFilter` MUST support the following functions: | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### Defaults and configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#defaults-and-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 164 | MUST | ✅ found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | `src/Метрики/Классы/ОтелСчетчик.os:22` |  |
| 165 | MUST | ➖ n_a | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | - | OneScript использует System.Decimal (не IEEE 754): NaN, Infinity, отрицательный ноль невозможны, операции выбрасывают исключение. Требование про IEEE 754 неприменимо к платформе. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 166 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |
| 167 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 168 | MUST | ✅ found | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:308` |  |
| 169 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:98` |  |
| 170 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:210` |  |
| 171 | MUST | ✅ found | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64` |  |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:603` |  |
| 2 | MUST | ✅ found | Each configuration option MUST be overridable by a signal specific option. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:609` |  |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: scheme (http or https), host, port, path. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:116` |  |
| 4 | MUST | ✅ found | When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs as described below. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:661` |  |
| 5 | SHOULD | ⚠️ partial | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` | gRPC транспорт принимает адрес и передаёт его в oint/api/grpc клиент, но специальная обработка форм адреса (unix:, dns:, etc.) не реализована — URL разбирается как http/https. |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either http or https. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:665` |  |
| 7 | SHOULD | ❌ not_found | If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format for that implementation. | - | Преобразование URL http/https в альтернативную форму для gRPC-клиента не реализовано — адрес передаётся как есть. |
| 8 | MUST | ⚠️ partial | Options MUST be one of: grpc, http/protobuf, http/json. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:612` | Валидация значений выполняется (grpc, http/protobuf, http/json), однако http/protobuf фактически обрабатывается как http/json — ОтелHttpТранспорт всегда сериализует тело в JSON (ЗаписатьJSON), отдельной реализации http/protobuf нет. |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use http scheme unless they have good reasons to choose https scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:654` |  |
| 10 | SHOULD | ❌ not_found | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - | Obsolete-переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE не реализованы и, следовательно, требование о сохранении совместимости неприменимо к их наличию; однако в коде нет поддержки этих устаревших имён. |
| 11 | SHOULD | ❌ not_found | The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:606` | Значение по умолчанию для otel.exporter.otlp.protocol = http/json, а не http/protobuf как требует спецификация. |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:603` |  |
| 13 | MUST | ✅ found | For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:647` |  |
| 14 | MUST | ✅ found | The only exception is that if an URL contains no path part, the root path / MUST be used (see Example 2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:936` |  |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:928` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ⚠️ partial | SDKs SHOULD support both grpc and http/protobuf transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` | Реализованы grpc (ОтелGrpcТранспорт) и http/json (ОтелHttpТранспорт). Значение http/protobuf принимается, но транспорт http всегда сериализует тело в JSON (ЗаписатьJSON в ОтелHttpТранспорт), отдельной реализации http/protobuf нет. |
| 17 | MUST | ✅ found | SDKs SHOULD support both grpc and http/protobuf transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:64` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one, it SHOULD be http/protobuf. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:64` | SDK поддерживает более одного транспорта (grpc и http/json), поэтому условие «если поддерживается только один» формально не активно; однако реального http/protobuf нет, а http/json технически не соответствует названию. |
| 19 | SHOULD | ❌ not_found | If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default (e.g. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:606` | Значение по умолчанию otel.exporter.otlp.protocol = http/json (см. ПротоколHttpJson), а не http/protobuf, как требует спецификация. |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:740` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:128` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:185` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | Заголовок User-Agent не устанавливается ни в ОтелHttpТранспорт, ни в ОтелGrpcТранспорт — поиск по коду (grep по 'User-Agent'/'userAgent') не нашёл реализации. |
| 24 | SHOULD | ❌ not_found | The format of the header SHOULD follow RFC 7231. | - | Заголовок User-Agent не формируется, следовательно формат RFC 7231 не применяется. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string. | - | Конфигурационной опции для product identifier в User-Agent нет, так как сам User-Agent не реализован. |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |
| 2 | MUST | ✅ found | Each `Propagator` type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the `Context` first, such as `SpanContext`, `Baggage` or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:46` |  |

#### Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any p... | `src/Пропагация/Классы/ОтелW3CПропагатор.os:89` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any p... | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:71` |  |

#### Setter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#setter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |
| 9 | MUST | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The `Keys` function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59` |  |
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21` |  |
| 13 | MUST | ✅ found | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40` |  |
| 14 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:79` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |

#### Global Propagators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#global-propagators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:132` |  |
| 22 | SHOULD | ⚠️ partial | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | `src/Ядро/Модули/ОтелГлобальный.os:132` | В SDK нет pre-configured пропагаторов: если пользователь не задал, ПолучитьПропагаторы возвращает ОтелНоопПропагатор вместо композита W3C Trace Context + W3C Baggage. Классы W3C-пропагаторов существуют (ОтелW3CПропагатор, ОтелW3CBaggageПропагатор), но не используются по умолчанию. |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | This method MUST exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | This method MUST exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Propagators Distribution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#propagators-distribution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` |  |
| 27 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/ОтелB3Пропагатор.os:1` |  |
| 28 | MUST NOT | ✅ found | It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | `src/Пропагация/Классы/` |  |
| 29 | MUST NOT | ✅ found | Additional `Propagator`s implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | `src/Пропагация/Классы/` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ⚠️ partial | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` | Парсинг и валидация traceparent/tracestate реализованы (версия ff отклоняется, проверка длин id, all-zeros отклоняются), но комментарий заявляет соответствие W3C Trace Context Level 1. Level 2 добавляет дополнительные требования (random trace flag), которые не проверяются. |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty, in which case the `tracestate` header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST | ✅ found | MUST attempt to extract B3 encoded using single and multi-header formats. The single-header variant takes precedence over the multi-header version. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:72` |  |
| 34 | MUST | ✅ found | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:158` |  |
| 35 | MUST | ✅ found | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:159` |  |
| 36 | MUST NOT | ✅ found | MUST NOT reuse `X-B3-SpanId` as the id for the server-side span. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:213` |  |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | MUST default to injecting B3 using the single-header format | `src/Пропагация/Классы/ОтелB3Пропагатор.os:240` |  |
| 38 | MUST | ✅ found | MUST provide configuration to change the default injection format to B3 multi-header | `src/Пропагация/Классы/ОтелB3Пропагатор.os:233` |  |
| 39 | MUST NOT | ✅ found | MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same id for both sides of a request. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:113` |  |

#### Fields

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#fields)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:86` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:238` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:91` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Классы/ОтелКонфигурация.os:1` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:867` |  |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:853` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:853` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:851` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | В функциях парсинга Boolean (Отключён в Автоконфигурации и Insecure в настройках TLS) отсутствует логирование предупреждения при получении невалидного значения - функции просто возвращают false без вывода warning. |
| 9 | SHOULD | ✅ found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:852` |  |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | - |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:886` |  |
| 12 | MUST | ✅ found | For new implementations, these should be treated as MUST requirements. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:886` |  |
| 13 | SHOULD | ✅ found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat ... | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:886` |  |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ✅ found | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:238` |  |
| 15 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:293` | Предупреждение и безопасное игнорирование реализовано для otel.traces.sampler (строка 293) и otel.propagators (строка 529), но для otel.traces.exporter / otel.logs.exporter / otel.metrics.exporter неизвестное значение не логируется - оно молча трактуется как otlp (строки 238, 363, 431). |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | Values MUST be deduplicated in order to register a `Propagator` only once. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:517` |  |
| 17 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:890` |  |
| 18 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:892` |  |
| 19 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:271` |  |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Трассировка/Классы/ОтелСпан.os:285` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:238` |  |
| 22 | SHOULD | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:431` |  |
| 23 | SHOULD | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:363` |  |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96` |  |

## Требования Development-статуса

Эти требования находятся в секциях со статусом Development. Их реализация не обязательна для соответствия стабильной спецификации.

### Resource Sdk

#### Resource detector name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Declarative configuration и именование детекторов не реализованы в SDK. Детекторы встроены и вызываются напрямую (host, process, cpu), без регистра имён для ссылок из декларативной конфигурации. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures they conform to declarative configuration property name requirements. | - | Фича именования детекторов не реализована. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Фича именования детекторов не реализована. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Фича именования детекторов не реализована. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Фича именования детекторов и реестра не реализована. |
| 6 | SHOULD | ➖ n_a | In order to limit collisions, resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Фича именования детекторов не реализована. |

### Trace Api

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:31` | Комментарий перед Включен() описывает назначение метода (позволяет пропустить создание спана), но не содержит явного указания вызывать API перед каждым созданием спана для получения актуального значения. |

### Trace Sdk

#### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API). | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` |  |
| 2 | MUST | ✅ found | The `TracerProvider` MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76` |  |
| 4 | MUST | ✅ found | Status: Development - The `TracerProvider` MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a `Tracer` whose behavior conforms to that `TracerConfig`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:84` |  |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `tracer_scope`: The `InstrumentationScope` of the `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:312` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `TracerConfig`, or some signal indicating that the default TracerConfig should be used. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:307` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Status: Development - `Tracer` MUST behave according to the TracerConfig computed during Tracer creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | MUST | ✅ found | If the `TracerProvider` supports updating the TracerConfigurator, then upon update the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:165` |  |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Tracer`s are enabled by default). | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ✅ found | If a `Tracer` is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:57` |  |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Трассировка/Классы/ОтелТрассировщик.os:194` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | `Enabled` MUST return `false` when either: there are no registered `SpanProcessors`, `Tracer` is disabled (`TracerConfig.enabled` is `false`). | `src/Трассировка/Классы/ОтелТрассировщик.os:38` | Функция Включен() возвращает Конфигурация.Включен() когда конфигурация задана, но при этом НЕ проверяет дополнительно наличие процессоров (ЕстьПроцессоры). Если TracerConfig задан и включён, но процессоров нет - вернёт Истина, что нарушает MUST-требование вернуть Ложь при отсутствии процессоров. Проверка ЕстьПроцессоры() выполняется только в ветке, где Конфигурация = Неопределено. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |

#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:240` |  |
| 2 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 3 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 4 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:277` |  |
| 6 | MUST | ✅ found | To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:290` |  |
| 7 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:292` |  |
| 8 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context, meaning when it is used not as a root sampler, the SDK SHOULD emit a warning such as: | - | В коде не найдено логирования предупреждения при использовании TraceIdRatioBased как child sampler (non-empty parent context) - СэмплироватьПоДоле не проверяет наличие родителя и не эмитит warning. |

#### ProbabilitySampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#probabilitysampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | - | ProbabilitySampler не реализован в SDK - нет класса/стратегии, использующей rejection threshold на базе W3C Trace Context Level 2 randomness (56 бит); реализован только TraceIdRatioBased. |
| 2 | SHOULD | ❌ not_found | When (R >= T), the OpenTelemetry TraceState SHOULD be modified to include the key-value `th:T` for rejection threshold value (T), as specified for the OpenTelemetry TraceState `th` sub-key. | - | ProbabilitySampler не реализован - нет кода, модифицирующего OpenTelemetry TraceState (ot/th sub-key) по результату вероятностного сэмплирования. |
| 3 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement... | - | ProbabilitySampler не реализован, соответственно отсутствует и логирование compatibility warning о незаданном Trace random flag. |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | - | AlwaysRecord декоратор не реализован - нет стратегии/класса, преобразующего DROP из обёрнутого семплера в RECORD_ONLY с сохранением RECORD_AND_SAMPLE. |

#### CompositeSampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#compositesampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST NOT | ❌ not_found | Note: ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | CompositeSampler / ComposableSampler / GetSamplingIntent не реализованы - в SDK нет composable-цепочки семплеров, поэтому требование read-only параметров не применимо к существующему коду. |
| 2 | SHOULD | ❌ not_found | For the zero case a `ComposableAlwaysOff` instance SHOULD be returned instead. | - | ComposableProbability и ComposableAlwaysOff не реализованы - нет fallback на ComposableAlwaysOff при ratio=0. |
| 3 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the `ot` sub-key of TraceState). | - | ComposableSampler не реализован - нет кода, оперирующего с trace_state_provider или ограничением на модификацию ot sub-key в composable-цепочке. |
| 4 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) and that the explicit randomness values MUST not be modified. | - | CompositeSampler не реализован - нет логики обновления threshold исходящего TraceState по результату GetSamplingIntent. |
| 5 | MUST | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) and that the explicit randomness values MUST not be modified. | - | CompositeSampler не реализован - отсутствует сам механизм, в котором можно было бы гарантировать сохранение explicit randomness значений. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace `random` flag will be set in the associated Trace contexts. | - | Отсутствует маркер-интерфейс или иное средство, через которое IdGenerator мог бы заявить о соответствии W3C Trace Context Level 2 randomness; Trace random flag в TraceFlags не поддерживается. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the `OnEnding` method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:461-467` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is called. | `src/Трассировка/Классы/ОтелСпан.os:467-469` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:466-468` |  |
| 4 | MUST | ⚠️ partial | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `OnEnding` of the first `SpanProcessor`. | `src/Трассировка/Классы/ОтелСпан.os:459-474` | Нет явной блокировки модификаций от других потоков перед вызовом ПередЗавершением. Флаг Завершен устанавливается только после ПередЗавершением, а модифицирующие методы (SetAttribute и др.) не синхронизируются с Завершить() через блокировку - другой поток может изменить спан параллельно. |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | В Logs API отсутствует отдельный эргономичный API для эмиссии событий: единственный способ эмитировать запись - СоздатьЗаписьЛога() + Записать(), ИмяСобытия устанавливается как поле записи вручную, нет удобного метода вида EmitEvent(name, attributes). |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Эргономичный API не реализован, поэтому оценить его идиоматичность невозможно. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:56` |  |
| 2 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:56` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 4 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:61` |  |
| 5 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:63` |  |
| 6 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:62` |  |
| 7 | MUST | ✅ found | Status: Development - The `LoggerProvider` MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a `Logger` whose behavior conforms to that `LoggerConfig`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:78` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: `logger_scope`: The `InstrumentationScope` of the `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:80` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `LoggerConfig`, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:233` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Status: Development - `Logger` MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:60` |  |
| 2 | MUST | ✅ found | If the `LoggerProvider` supports updating the LoggerConfigurator, then upon update the `Logger` MUST be updated to behave according to the new `LoggerConfig`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:171` |  |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Logger`s are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 2 | MUST | ✅ found | If a `Logger` is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:178` |  |
| 3 | MUST | ✅ found | If not explicitly set, the `minimum_severity` parameter MUST default to `0`. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST be dropped by the `Logger`. | `src/Логирование/Классы/ОтелЛоггер.os:182` |  |
| 5 | MUST | ✅ found | If not explicitly set, the `trace_based` parameter MUST default to `false`. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 6 | MUST | ✅ found | If `trace_based` is `true`, log records associated with unsampled traces MUST be dropped by the `Logger`. | `src/Логирование/Классы/ОтелЛоггер.os:186` |  |
| 7 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:171` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:120` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the `LogRecord` with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:213` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:226` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:226` |  |
| 5 | MUST | ✅ found | Status: Development Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case `Enabled` was not called prior to emitting the record): | `src/Логирование/Классы/ОтелЛоггер.os:112` |  |
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:182` |  |
| 7 | MUST | ✅ found | Trace-based: If `trace_based` is `true`, and if the log record has a `SpanId` and the `TraceFlags` SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:186` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Enabled` MUST return `false` when either: there are no registered `LogRecordProcessors`; Logger is disabled; severity is less than minimum_severity; trace_based and unsampled; all processors return false. | `src/Логирование/Классы/ОтелЛоггер.os:49` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Логирование/Классы/ОтелЛоггер.os:78` |  |

### Metrics Api

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:796` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |
| 2 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:75` |  |
| 4 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ori... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:64` |  |
| 5 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ori... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:66` |  |
| 6 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ori... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:65` |  |
| 7 | MUST | ✅ found | Status: Development - The `MeterProvider` MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a `Meter` whose behavior conforms to that `MeterConfig`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:260` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `meter_scope`: The `InstrumentationScope` of the `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:264` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `MeterConfig`, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:264` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:174` |  |
| 2 | MUST | ✅ found | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:349` |  |
| 3 | MUST | ✅ found | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:321` |  |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:321` | Start timestamp фиксируется в момент создания инструмента, а не в момент первого измерения серии. Для большинства случаев близко по значению, но формально отличается от спеки. |
| 5 | SHOULD | ❌ not_found | For asynchronous instrument, the start timestamp SHOULD be: | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:192` | Для async-инструментов startTimeUnixNano = ВремяСейчас на каждый collect, что не соответствует требованию (creation time или предыдущий collection interval). |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:14` |  |
| 2 | MUST | ✅ found | `Meter` MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:260` |  |
| 3 | MUST | ✅ found | If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be updated to behave according to the new `MeterConfig`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:223` |  |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Meter`s are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ⚠️ partial | If a `Meter` is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88` | Синхронный Записать проверяет только локальный флаг 'Включен', не 'МетрВключен'. При выключенном Meter (МетрВключен=Ложь) синхронные измерения всё равно будут записаны. Асинхронные инструменты не проверяют ни один из флагов. Функция Включен(Атрибуты) возвращает комбинированное значение, но Записать его не использует. |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:436` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The synchronous instrument `Enabled` MUST return `false` when either: The MeterConfig of the `Meter` used to create the instrument has parameter `enabled=false`. All resolved v... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259` | Включен() учитывает МетрВключен (MeterConfig.enabled=false), но не возвращает false когда все resolved views настроены с Drop Aggregation — такой логики нет ни в Включен(), ни в ПрименитьПредставлениеКИнструменту. Drop-агрегатор молча отбрасывает измерения, но Enabled продолжает возвращать true. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: the `exporter` to use, the default output `aggregation`, the output `tem... | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:398` |  |
| 2 | SHOULD | ⚠️ partial | The default output `aggregation` (optional), a function of instrument kind. This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:419` | Селектор агрегации инициализируется из статических дефолтов и параметра НоваяАгрегацияГистограмм, а не запрашивается у экспортера как функции от вида инструмента. |
| 3 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:419` |  |
| 4 | SHOULD | ✅ found | The output `temporality` (optional), a function of instrument kind. This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:265` |  |
| 5 | SHOULD | ⚠️ partial | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:262` | Временность делегируется экспортеру через Экспортер.ПолучитьВременнуюАгрегацию; явного fallback на Cumulative в читателе нет - зависит от экспортера. |
| 6 | SHOULD | ✅ found | The default aggregation cardinality limit (optional) to use, a function of instrument kind. If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:401` |  |
| 7 | SHOULD | ✅ found | A `MetricReader` SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the `Produce` operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366` |  |
| 8 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:398` |  |
| 9 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250` |  |
| 10 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether ... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:163` |  |
| 11 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collect... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:170` |  |
| 12 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the p... | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:228` |  |
| 13 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting times... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:170` |  |
| 14 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp (e.g... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:174` |  |
| 15 | MUST | ✅ found | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйАгрегатор.os:48` |  |
| 16 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instan... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:317` |  |
| 17 | SHOULD NOT | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instan... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:128` |  |
| 18 | MUST NOT | ✅ found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:197` |  |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` |  |
| 2 | SHOULD | ⚠️ partial | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` | Фильтр принимается в интерфейсе, но применение зависит от реализации продюсера. Никакой внутренней реализации продюсера в SDK нет - только интерфейс, поэтому ранняя фильтрация не гарантирована. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | - | Функция Произвести(ФильтрМетрик) не принимает параметр resource. |
| 4 | SHOULD | ⚠️ partial | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` | Функция возвращает только Массив данных, статус succ/fail/timeout отдельно не возвращается; ошибки в вызывающем коде обрабатываются через Попытка/Исключение. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | - | Интерфейс продюсера не требует и не документирует привязку InstrumentationScope, идентифицирующего сам MetricProducer. Данные продюсера добавляются в общий массив без гарантии единой области. |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Сводка условных секций

| Раздел | Секция | Scope | Stability | Keywords | Ссылка |
|---|---|---|---|---|---|
| Resource Sdk | Resource detector name | conditional:Resource Detector Naming (conditional) | Development | 6 | [spec](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет opaque-объектов | Ключи контекста - строки | Строковые константы как ключи |
| Нет thread-local | ФоновыеЗадания вместо goroutines | Передача контекста через параметры |
| Число = System.Decimal (не IEEE 754) | NaN, Infinity, отрицательный ноль невозможны | Операции, порождающие NaN/Inf, выбрасывают исключение - требования к обработке NaN/Inf неприменимы |
| Нет varargs (переменного числа параметров) | Спека требует "variable number of attributes" (metrics) и "zero or more callbacks" | Используется контейнерный объект: `ОтелАтрибуты` для атрибутов, один полиморфный параметр `Callback = Неопределено \| Действие \| Массив` для callback-ов. Семантически эквивалентно. |
| Модель распространения opm-пакета | Спека OTel описывает пропагаторы как отдельные extension-packages (Java/JS) | Пропагаторы (W3C TraceContext, W3C Baggage, B3, Jaeger и др.) поставляются в составе основного opm-пакета `opentelemetry`. Функциональность полностью соответствует спеке; отличие только в модели распространения. |

## Методология

### Процесс анализа

1. **Извлечение требований** (`extract_requirements.py`): загрузка 12 страниц спецификации, разбиение на секции, подсчёт MUST/SHOULD keywords
2. **Генерация промптов** (`generate_prompts.py`): группировка секций по доменам, генерация промптов с JSON-схемой вывода для агентов
3. **Верификация** (general-purpose агенты): каждый агент анализирует 5-8 секций, записывает результат в JSON
4. **Сборка отчёта** (`assemble_report.py`): детерминированная сборка markdown из JSON-результатов

### Статусы

| Статус | Значение |
|---|---|
| ✅ found | Требование полностью реализовано с корректной семантикой |
| ⚠️ partial | Код существует, но не полностью соответствует спецификации |
| ❌ not_found | Реализация отсутствует |
| ➖ n_a | Неприменимо из-за ограничений платформы |

### Статистика извлечения

| Метрика | Значение |
|---|---|
| Страниц спецификации | 12 |
| Всего секций | 242 |
| Stable секций | 213 |
| Development секций | 29 |
| Conditional секций | 1 |
| Всего keywords | 824 |
| Stable universal keywords | 701 |

