# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             768    648  -120 ⚠️  РЕГРЕССИЯ
  partial            12    138 +  126
  not_found          14     38 +   24 ⚠️  РЕГРЕССИЯ
  n_a                46     52 +    6
  Всего             840    876 +   36

  🔴 ПОНИЖЕНИЕ СТАТУСА (126) - требует перепроверки:

     [Env Vars / Declarative configuration]
       found → partial
       Текст: When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the conf
       Пояснение: Инициализировать() (без явного МенеджерПараметров) при заданной OTEL_CONFIG_FILE (фолбэк OTEL_EXPERIMENTAL_CONFIG_FILE) строит SDK только из файла: От
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Enum]
       found → partial
       Текст: Enum values SHOULD be interpreted in a case-insensitive manner.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:550 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:305
       Пояснение: Большинство enum-переменных нормализуются через НРег: OTEL_TRACES_SAMPLER (стр. 305), OTEL_PROPAGATORS (стр. 550), OTEL_TRACES/METRICS/LOGS_EXPORTER (
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Enum]
       found → partial
       Текст: For sources accepting an enum value, if the user provides a value the implementation does not recogn
       Пояснение: Предупреждение + graceful fallback реализованы для OTEL_TRACES_SAMPLER (стр. 345-350 -> parentbased_always_on), OTEL_PROPAGATORS (стр. 1198, неизвестн
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Environment Variable Specification]
       found → partial
       Текст: If they do, they SHOULD use the names and value parsing behavior specified in this document.
       Пояснение: Стандартные имена OTEL_* используются (ПровайдерПараметровENV из configor: OTEL_FOO_BAR -> otel.foo.bar, перечень в шапке ОтелАвтоконфигурация.os:6-74
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Environment Variable Specification]
       found → partial
       Текст: They SHOULD also follow the common configuration specification.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:148 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:961
       Пояснение: Common-спецификация соблюдена частично. Выполнено: нераспарсиваемые и отрицательные числовые значения (Integer/Duration/Timeout) дают предупреждение и
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → partial
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:960 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:968
       Пояснение: Логируются: нечисловой аргумент traceidratio/parentbased_traceidratio (БезопасноеЧисло, стр. 968), отрицательный (стр. 972-975) и аргумент для сэмплер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Numeric]
       found → partial
       Текст: The following paragraph was added after stabilization and the requirements are thus qualified as "SH
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:960 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:961
       Пояснение: Мета-требование: квалифицирует как SHOULD следующий абзац о числовых значениях (warning + graceful ignore), поэтому оценивается по реализации этого аб
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Numeric]
       found → partial
       Текст: For new implementations, these should be treated as MUST requirements.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:960 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:961
       Пояснение: Реализация новая, поэтому требование о числовых значениях должно выполняться как MUST; выполнено не полностью: БезопасноеЧисло (стр. 961-977) логирует
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Numeric]
       found → partial
       Текст: For variables accepting a numeric value, if the user provides a value the implementation cannot pars
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:966 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:968
       Пояснение: БезопасноеЧисло (стр. 961-977) для всех числовых переменных, читаемых автоконфигурацией (таймауты OTLP, BSP/BLRP, интервал экспорта метрик, лимиты, OT
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Parsing empty value]
       found → partial
       Текст: The SDK MUST interpret an empty value of an environment variable the same way as when the variable i
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:961 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:942
       Пояснение: Большинство переменных обрабатываются корректно: ПараметрИлиУмолчание (стр. 942-948), БезопасноеЧисло (стр. 962), Отключен (стр. 925), ПараметрСигнала
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Api / LoggerProvider]
       found → partial
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`.
       Расположение: src/Ядро/Модули/ОтелГлобальный.os:95 → src/Ядро/Модули/ОтелГлобальный.os:36
       Пояснение: Глобальный реестр ОтелГлобальный хранит только SDK целиком: регистрация через ОтелГлобальный.Установить(Сдк) / ОтелПостроительSdk.ПостроитьИЗарегистри
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:178 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:180
       Пояснение: Основной путь соблюдает таймаут: ЭкспортироватьВсеПакеты проверяет истечение ТаймаутМс перед каждым пакетом (стр. 180), передаёт остаток в Экспортер.Э
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → n_a
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:185 → -
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / LogRecord Limits]
       found → partial
       Текст: LogRecord attributes MUST adhere to the common rules of attribute limits.
       Пояснение: Лимит количества атрибутов (новый ключ сверх МаксАтрибутов, default 128, отбрасывается с инкрементом ОтброшенныхАтрибутов; перезапись существующего кл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Logger Creation]
       found → partial
       Текст: The input provided by the user MUST be used to create an `InstrumentationScope` instance which is st
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:76 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:76-96
       Пояснение: InstrumentationScope строится из всех входных параметров (Новый ОтелОбластьИнструментирования(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресС
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / OnEmit]
       found → partial
       Текст: This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD 
       Расположение: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:18 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:63
       Пояснение: Исключения наружу не пробрасываются: ОтелКомпозитныйПроцессорЛогов.ПриПоявлении (стр. 20-24), ОтелПростойПроцессорЛогов.ПриПоявлении (стр. 42-48), Оте
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       found → partial
       Текст: `Shutdown` MUST include the effects of `ForceFlush`.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:94 → src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:103
       Пояснение: Пакетный процессор требование выполняет: ОтелБазовыйПакетныйПроцессор.Закрыть() вызывает ЭкспортироватьВсеПакеты(ТаймаутМс) (стр. 96) — ту же логику, 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:159 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:155-172
       Пояснение: Закрыть() вызывает Процессор.Закрыть() для каждого процессора из снимка (стр. 157-166), но не гарантирует вызов для всех: при исчерпании таймаута цикл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Asynchronous Counter creation]
       found → n_a
       Текст: There MUST NOT be any API for creating an Asynchronous Counter other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:343 → src/Метрики/Классы/ОтелМетр.os:345
       Пояснение: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Кроме публичного констру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Asynchronous Gauge creation]
       found → n_a
       Текст: There MUST NOT be any API for creating an Asynchronous Gauge other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:486 → src/Метрики/Классы/ОтелМетр.os:488
       Пояснение: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Кроме публичного констру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Asynchronous UpDownCounter creation]
       found → n_a
       Текст: There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:414 → src/Метрики/Классы/ОтелМетр.os:416
       Пояснение: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Кроме публичного констру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Concurrency requirements]
       found → partial
       Текст: Instrument - all methods MUST be documented that implementations need to be safe for concurrent use 
       Пояснение: Документация потокобезопасности есть только для синхронных инструментов: ОтелБазовыйСинхронныйИнструмент.os:49-50 («Instrument - потокобезопасный объе
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Gauge creation]
       found → n_a
       Текст: There MUST NOT be any API for creating a `Gauge` other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:277 → src/Метрики/Классы/ОтелМетр.os:279
       Пояснение: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Кроме публичного констру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Histogram creation]
       found → n_a
       Текст: There MUST NOT be any API for creating a `Histogram` other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:103 → src/Метрики/Классы/ОтелМетр.os:105
       Пояснение: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Кроме публичного констру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument advisory parameters]
       found → partial
       Текст: OpenTelemetry SDKs MUST handle `advisory` parameters as described here.
       Расположение: src/Метрики/Классы/ОтелМетр.os:1219 → src/Метрики/Классы/ОтелМетр.os:933
       Пояснение: Advisory-параметры полноценно обрабатываются только для синхронных инструментов: ПроверитьСовет() (ОтелМетр.os:1222) валидирует Совет и отбрасывает не
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / MeterProvider]
       found → partial
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default MeterProvider.
       Пояснение: Глобальный реестр ОтелГлобальный хранит только SDK целиком: регистрация через ОтелГлобальный.Установить(Сдк) / ОтелПостроительSdk.ПостроитьИЗарегистри
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Where the API supports registration of `callback` functions after asynchronous instrumentation creat
       Расположение: src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:128
       Пояснение: Отмена регистрации возможна только для callback-ов отдельного инструмента: ОтелБазовыйНаблюдаемыйИнструмент.УдалитьCallback(Callback) или вручную созд
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:398 → src/Метрики/Классы/ОтелМетр.os:329
       Пояснение: Рекомендация задокументирована в описаниях СоздатьНаблюдаемыйСчетчик/СоздатьНаблюдаемыйРеверсивныйСчетчик/СоздатьНаблюдаемыйДатчик в суженном виде: «Н
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API MUST treat observations from a single Callback as logically taking place at a single instant
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:419 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:420
       Пояснение: Для callback-ов одного инструмента (переданных при создании или через ДобавитьCallback) наблюдения одного вызова трактуются как единый момент: Преобра
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API MUST treat observations from a single Callback as logically taking place at a single instant
       Пояснение: Идентичные timestamps гарантируются только в пределах одного инструмента: ВремяСейчас вычисляется в ПреобразоватьЗаписиВТочки на каждый вызов. Наблюде
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / UpDownCounter creation]
       found → n_a
       Текст: There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:231 → src/Метрики/Классы/ОтелМетр.os:233
       Пояснение: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Кроме публичного констру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Aggregation]
       found → partial
       Текст: The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Mo
       Расположение: src/Метрики/Модули/ОтелАгрегация.os:1 → src/Метрики/Модули/ОтелАгрегация.os:103
       Пояснение: Все агрегации есть (ОтелАгрегация: ПоУмолчанию/Сумма/ПоследнееЗначение/Отбросить/ГистограммаСЯвнымиГраницами + ОтелАгрегатор*), но при выборе через Vi
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Aggregation]
       found → partial
       Текст: The SDK SHOULD provide the following `Aggregation`:
       Расположение: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:1 → src/Метрики/Модули/ОтелАгрегация.os:76
       Пояснение: ОтелАгрегаторЭкспоненциальнойГистограммы и ОтелАгрегация.ГистограммаЭкспоненциальная есть и корректно работают через агрегацию гистограмм по умолчанию
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Collect]
       found → partial
       Текст: `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: Отдельного публичного Collect нет: у периодического читателя сбор выполняет приватный СобратьИЭкспортировать, доступный через СброситьБуфер/СброситьБу
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → partial
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:94 → src/Метрики/Классы/ОтелПровайдерМетрик.os:94-121,185-192
       Пояснение: Синхронизация есть, но неполная. Создание Meter защищено СинхронизированнаяКарта + double-checked locking под БлокировкаМетрик (ОтелПровайдерМетрик.os
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → partial
       Текст: ExemplarReservoir - all methods MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:72 → src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:48-112
       Пояснение: Синхронизация частичная. ОтелРезервуарЭкземпляров: Предложить защищён (СинхронизированнаяКарта + АтомарноеЧисло + БлокировкаРесурса, стр. 59-98), но С
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → partial
       Текст: MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:289 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:288-363
       Пояснение: Синхронизация частичная. Списки метров и продюсеров копируются под БлокировкаРесурса (ОтелПериодическийЧитательМетрик.os:289-300, 675-685), вызов Эксп
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also app
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:305 → src/Метрики/Классы/ОтелПровайдерМетрик.os:108,273-278,295-297,305-308,332-356; src/Метрики/Классы/ОтелМетр.os:555-556
       Пояснение: Обновления через ЗарегистрироватьПредставление (массив Представления передаётся метрам по ссылке: стр. 108, 273-278; ОтелМетр.os:556) и ОбновитьКонфиг
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also app
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:352 → src/Метрики/Классы/ОтелПровайдерМетрик.os:305-308,342-350; src/Метрики/Классы/ОтелМетр.os:555-556
       Пояснение: Для Views и конфигуратора, возвращающего явную ОтелКонфигурацияМетра, момент получения метра значения не имеет (метры ссылаются на массив Представлени
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardi
       Расположение: src/Метрики/Классы/ОтелМетр.os:947 → src/Метрики/Классы/ОтелМетр.os:950
       Пояснение: Для синхронных инструментов ЛимитМощностиАгрегации() из View переопределяет лимит читателя (ПрименитьПредставлениеКИнструменту, стр. 950-951). Для аси
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Пояснение: Лимит читателя (ОтелПериодическийЧитательМетрик.ЛимитМощности(), параметр конструктора НовыйЛимитМощности) передаётся метру при создании и далее всем 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Defaults and configuration]
       found → partial
       Текст: The SDK MUST provide configuration according to the SDK environment variables specification.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:16 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479-528; src/Метрики/Классы/ОтелПровайдерМетрик.os:332-340; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-133
       Пояснение: Конфигурация метрик через переменные окружения реализована (ОтелАвтоконфигурация.СоздатьПровайдерМетрик: OTEL_METRICS_EXPORTER - otlp/none, прочие зна
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       found → partial
       Текст: This means that the Meter MUST return a functional instrument that can be expected to export data ev
       Расположение: src/Метрики/Классы/ОтелМетр.os:67 → src/Метрики/Классы/ОтелМетр.os:91
       Пояснение: Если конфликтуют только описание, advisory или регистр имени, возвращается ранее созданный рабочий инструмент (строки 65-72). При конфликте вида или е
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       found → partial
       Текст: The emitted warning SHOULD include information for the user on how to resolve the conflict, if possi
       Расположение: src/Метрики/Классы/ОтелМетр.os:1112 → src/Метрики/Классы/ОтелМетр.os:1358
       Пояснение: Рецепт добавляется к предупреждению (ПостроитьРецептРазрешенияКонфликта, вызов в строке 1115): при конфликте вида или единицы предлагается переименова
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       found → partial
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Расположение: src/Метрики/Классы/ОтелМетр.os:68 → src/Метрики/Классы/ОтелМетр.os:1140
       Пояснение: При конфликте единиц или вида (ЕстьНесовместимыйКонфликт) создаётся второй инструмент, он добавляется в Инструменты, в лог пишется предупреждение (стр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       found → partial
       Текст: Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExem
       Расположение: src/Метрики/Классы/ОтелМетр.os:137 → src/Метрики/Классы/ОтелМетр.os:159
       Пояснение: Выровненный резервуар назначается только инструментам Histogram (ОтелМетр.СоздатьГистограмму, стр. 139-140 и 159-160). Если View задаёт explicit_bucke
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       found → partial
       Текст: Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reser
       Расположение: src/Метрики/Классы/ОтелМетр.os:204 → src/Метрики/Классы/ОтелМетр.os:207
       Пояснение: Размер min(20, МаксБакетов) задаётся только в ОтелМетр.СоздатьЭкспоненциальнуюГистограмму (в т.ч. при default-агрегации base2 из СоздатьГистограмму). 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarFilter]
       found → partial
       Текст: The filter configuration SHOULD follow the environment variable specification.
       Пояснение: OTEL_METRICS_EXEMPLAR_FILTER (always_on/always_off/trace_based, без учёта регистра; неизвестное значение → предупреждение) читается только в конструкт
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarFilter]
       found → partial
       Текст: An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased.
       Расположение: src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14 → src/Метрики/Модули/ОтелФильтрЭкземпляров.os:60
       Пояснение: AlwaysOn (ВсегдаВключен) и AlwaysOff (ВсегдаВыключен) реализованы корректно. TraceBased (ПоТрассировке) в ДолженЗахватить() проверяет лишь КонтекстСпа
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by ag
       Расположение: src/Метрики/Классы/ОтелФабрикаПростыхРезервуаров.os:21 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:457
       Пояснение: Для синхронных инструментов резервуар создаётся на каждую серию через ФабрикаРезервуаров.СоздатьРезервуар() (карта РезервуарыПоКлючу). Но: (1) асинхро
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggreg
       Пояснение: Для обычных серий filteredAttributes = атрибуты измерения минус атрибуты серии (фильтр View) — корректно. Однако при переполнении лимита кардинальност
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `Force
       Пояснение: СброситьБуфер обходит всех читателей, но собственный ForceFlush читателя (СброситьБуфер(ТаймаутМс)) вызывается только у последнего; остальным вызывает
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Пояснение: ПринудительноВыгрузитьСРезультатом/СброситьБуфер принимают ТаймаутМс, но он передаётся только последнему читателю (ограничивает лишь его экспорт через
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each b
       Пояснение: ПринудительноВыгрузитьСРезультатом собирает метрики (СброситьБуфер -> СобратьИЭкспортировать), передаёт их одним вызовом Экспортировать (разбиение не 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with in
       Расположение: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:15 → src/Метрики/Модули/ОтелАгрегация.os:129
       Пояснение: Для explicit-гистограммы через View на UpDownCounter sum не собирается (СобиратьSum=Ложь при немонотонной сумме), а async-инструментам гистограммная а
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameters]
       found → partial
       Текст: If both a View and advisory parameters specify the same aspect of the Stream configuration, the sett
       Расположение: src/Метрики/Классы/ОтелМетр.os:1033 → src/Метрики/Классы/ОтелМетр.os:956
       Пояснение: Приоритет View реализован для агрегации и границ гистограммы (View-агрегация в СоздатьГистограмму; ОпределитьГраницыГистограммы, строка 1036, берёт гр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument selection criteria]
       found → partial
       Текст: The SDK MUST accept the following criteria:
       Пояснение: Конструктор ОтелСелекторИнструментов принимает все 6 критериев, но при применении Views Совпадает вызывается только с (имя, вид, имя метра) (ОтелМетр.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → n_a
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:111 → -
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter]
       found → partial
       Текст: Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instr
       Расположение: src/Метрики/Классы/ОтелМетр.os:828 → src/Метрики/Классы/ОтелМетр.os:830
       Пояснение: Каждый ОтелМетр имеет собственные ИнструментыПоИмени и ДескрипторыИнструментов (стр. 830-831), поэтому метры с разными именем или версией - независимы
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter]
       found → partial
       Текст: Status: Development - `Meter` MUST behave according to the MeterConfig computed during Meter creatio
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:342 → src/Метрики/Классы/ОтелПровайдерМетрик.os:110
       Пояснение: MeterConfig вычисляется при создании метра (ПрименитьКонфигурацию -> Метрика.УстановитьМетрВключен, стр. 110, 342-350), но при enabled=false метр ведё
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter]
       found → partial
       Текст: If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be
       Пояснение: ОбновитьКонфигуратор() сохраняет новый конфигуратор и применяет его ко всем созданным метрам (ПрименитьКонфигурацииКоВсемМетрам, стр. 352-356); флаг М
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: The `MeterProvider` MUST implement the Get a Meter API.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:74 → src/Метрики/Классы/ОтелПровайдерМетрик.os:59-61,74-122,332-340
       Пояснение: ПолучитьМетр(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы) (все параметры, кроме имени, опциональны) и ПостроительМетра() реализуют Ge
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: The input provided by the user MUST be used to create an `InstrumentationScope` instance which is st
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:89 → src/Метрики/Классы/ОтелПровайдерМетрик.os:89-111; src/Ядро/Классы/ОтелОбластьИнструментирования.os:59-63
       Пояснение: InstrumentationScope создаётся из всех входных параметров (Новый ОтелОбластьИнструментирования(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, Адрес
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:79 → src/Метрики/Классы/ОтелПровайдерМетрик.os:79-90,104-111; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:292-293
       Пояснение: ПолучитьМетр для Неопределено или пустого имени не бросает исключение и не возвращает Неопределено: логирует предупреждение и создаёт обычный ОтелМетр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: Status: Development - The `MeterProvider` MUST compute the relevant MeterConfig using the configured
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:342 → src/Метрики/Классы/ОтелПровайдерМетрик.os:110,116-118,342-350; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92-95,273-276; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:103-132
       Пояснение: MeterConfig вычисляется: при создании метра ПрименитьКонфигурацию (стр. 110, 342-350) вызывает Конфигуратор.Выполнить(ОбластьИнструментирования) и пер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricExporter]
       found → partial
       Текст: `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they 
       Расположение: src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1 → src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:14
       Пояснение: ИнтерфейсЭкспортерМетрик (Экспортировать, СброситьБуфер, Закрыть) реализуется ОтелЭкспортерМетрик через &Реализует, но читатель дополнительно вызывает
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided:
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:627 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:735
       Пояснение: Конструктор ОтелПериодическийЧитательМетрик принимает экспортер, интервал, лимит мощности (одно число, а не функция вида инструмента) и агрегацию гист
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The output `temporality` (optional), a function of instrument kind. This function SHOULD be obtained
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:368 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:739
       Пояснение: Агрегация по умолчанию хранится в самом читателе (параметр НоваяАгрегацияГистограмм, СелекторАгрегации, УстановитьАгрегациюПоУмолчанию) и не запрашива
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the con
       Пояснение: Для синхронных инструментов Delta/Cumulative реализованы через ОчиститьТочкиДанных(Временность); для асинхронных Sum и явных гистограмм абсолютные зна
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only recei
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:177 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:348
       Пояснение: Аккумуляторы сбрасываются в ОчиститьТочкиДанных только после успешного экспорта (ВыполнитьЭкспорт: «Если Результат И ОчищатьДанные»), а не в момент сб
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: For instruments with Cumulative aggregation temporality, successive data points received by successi
       Пояснение: Для синхронных инструментов при Cumulative ВремяСтарта сохраняется (ОчиститьТочкиДанных) и стартовая метка повторяется; для асинхронных инструментов П
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: For instruments with Delta aggregation temporality, successive data points received by successive ca
       Пояснение: Для синхронных инструментов при Delta ВремяСтарта переносится на текущее время в ОчиститьТочкиДанных, но только после успешного экспорта (при ошибке э
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-eff
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:163 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:36
       Пояснение: Состояние асинхронных инструментов изолировано per-reader (КумулятивноеСостояниеАсинх), но состояние синхронных инструментов (Аккумуляторы, ВремяСтарт
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:420 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:308
       Пояснение: Callback-и вызываются в момент сбора конкретным ридером (Метр.ВызватьМультиОбратныеВызовы + Инструмент.Собрать), наблюдения одиночных callback-ов возв
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:238 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:375
       Пояснение: Таймаут есть (ТаймаутCallbackМс → ФоновыеЗадания.Выполнить + ОжидатьЗавершения), но по умолчанию 0 (без таймаута, inline) и задаётся только вручную дл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: The implementation MUST complete the execution of all callbacks for a given instrument before starti
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:238 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:341
       Пояснение: Внутри раунда callback-и выполняются синхронно и завершаются до возврата Собрать(); но раунды сбора не взаимоисключаются: СобратьИЭкспортировать держи
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Overflow attribute]
       found → partial
       Текст: The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality 
       Пояснение: Синхронные инструменты: при Аккумуляторы.Количество() >= ЛимитМощности (стр. 117) создаётся единый overflow-аккумулятор с атрибутом otel.metric.overfl
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Periodic exporting MetricReader]
       found → partial
       Текст: The reader MUST ensure all metric data points from a single `Collect()` are provided to `Export` bef
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:288 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:340
       Пояснение: Разбиения на пакеты нет, поэтому каждый Collect даёт ровно один пакет, а вызовы Экспортировать сериализованы Блокировкой; однако сбор в СобратьИЭкспор
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: SDKs SHOULD return a valid no-op Meter for these calls, if possible.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:84 → src/Метрики/Классы/ОтелПровайдерМетрик.os:84-88
       Пояснение: После Закрыть() ПолучитьМетр (стр. 84-88) возвращает новый ОтелМетр — валидный объект без исключения, не зарегистрированный у читателей и не кешируемы
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and Me
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:196 → src/Метрики/Классы/ОтелПровайдерМетрик.os:188-213; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:154-160; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:169-177
       Пояснение: Закрыть() вызывает Закрыть() у каждого зарегистрированного читателя (стр. 196-207), а ОтелПериодическийЧитательМетрик.Закрыть закрывает свой экспортер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: SDKs SHOULD return some failure for these calls, if possible.
       Пояснение: ОтелПериодическийЧитательМетрик после Закрыть возвращает Ошибка из СброситьБуфер/СброситьБуферБезОчистки/ПринудительноВыгрузитьСРезультатом, но ОтелПр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: ОтелПериодическийЧитательМетрик.Закрыть возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут), но ОтелПрометеусЧитательМетрик.Закрыть - процедура бе
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:138 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:142
       Пояснение: Закрыть(ТаймаутМс = 30000) ограничивает дедлайном только ожидание фонового задания (Обещание.Получить); финальные СобратьИЭкспортировать и Экспортер.З
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / SimpleFixedSizeExemplarReservoir]
       found → partial
       Текст: This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the r
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:74 → src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:79
       Пояснение: Реализован Algorithm R по числу увиденных измерений, но с ошибкой на единицу: АтомарноеЧисло.ПолучитьИДобавить(1) возвращает предыдущее значение (0-ba
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp,
       Расположение: src/Метрики/Классы/ОтелБазовыйАгрегатор.os:50 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:181
       Пояснение: Синхронные инструменты соответствуют: ВремяСтарта = время создания инструмента (стр. 344), при delta-сбросе ОчиститьТочкиДанных() переустанавливает ег
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:418 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:374
       Пояснение: Синхронные инструменты передают одно ВремяСтарта во все точки (стр. 374). У асинхронных инструментов startTimeUnixNano = ВремяСейчас вычисляется занов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other
       Расположение: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:203 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:382
       Пояснение: Отбрасывание атрибутов вне allow-list реализовано только для синхронных инструментов; у асинхронных инструментов View allow-list игнорируется и все ат
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter confi
       Расположение: src/Метрики/Классы/ОтелМетр.os:952-960 → src/Метрики/Классы/ОтелМетр.os:959
       Пояснение: Для синхронных инструментов при отсутствии ключей во View используются КлючиАтрибутов из Совет; для асинхронных инструментов advisory-атрибуты не прим
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all oth
       Расположение: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:207 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:110
       Пояснение: Исключение работает только для синхронных инструментов (ИсключитьАтрибутыПоКлючам); к асинхронным инструментам exclude-list не применяется. Кроме того
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all oth
       Расположение: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:207 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:393
       Пояснение: При одном exclude-list прочие атрибуты сохраняются; но если у инструмента задан advisory КлючиАтрибутов, вместо exclude-list View применяется allow-li
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggreg
       Расположение: src/Метрики/Классы/ОтелМетр.os:396 → src/Метрики/Классы/ОтелПровайдерМетрик.os:332
       Пояснение: Агрегация по умолчанию захардкожена в ОтелМетр по виду инструмента (Sum/LastValue/гистограмма); от MetricReader берётся только вариант агрегации гисто
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST appl
       Расположение: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:68 → src/Метрики/Классы/ОтелПровайдерМетрик.os:335
       Пояснение: Лимит берётся из ЛимитМощности() только первого зарегистрированного читателя и применяется ко всем инструментам метра (хранилище агрегатов общее для в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Synchronous instrument cardinality limits]
       found → partial
       Текст: Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in ex
       Пояснение: Маршрутизация в Записать() корректна: измерение пишется ровно в один аккумулятор - своего набора атрибутов или overflow (стр. 115-131). Но при delta-в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Synchronous instrument cardinality limits]
       found → partial
       Текст: Measurements MUST NOT be double-counted or dropped during an overflow.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:115 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179
       Пояснение: Логика переполнения сама по себе не теряет и не дублирует измерения (одна запись в свой или overflow-аккумулятор). Однако при delta-временности снимок
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: The following configuration options MUST be available to configure the OTLP exporter.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:217 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:673
       Пояснение: Доступны (env общие + per-signal и параметры конструкторов транспортов): Endpoint, Headers, Compression, Timeout (по умолчанию 10000 мс), Protocol, In
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: Each configuration option MUST be overridable by a signal specific option.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1063 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1064
       Пояснение: Per-signal переопределение реализовано для всех env-опций: ПараметрСигналаИлиОбщий (protocol, headers, compression, timeout, certificate, client.key, 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Retry]
       found → partial
       Текст: Transient errors MUST be handled with a retry strategy.
       Расположение: src/Экспорт/Классы/ОтелHttpТранспорт.os:232 → src/Экспорт/Классы/ОтелGrpcТранспорт.os:289
       Пояснение: HTTP соответствует: коды 429/502/503/504 (ОтелHttpТранспорт.os:168-172) и сетевые исключения КоннекторHTTP.Post повторяются через СтратегияПовтора (re
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Extract]
       found → partial
       Текст: If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST 
       Расположение: src/Пропагация/Классы/ОтелW3CПропагатор.os:110 → src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:125
       Пояснение: ОтелW3CПропагатор.Извлечь при любой ошибке разбора traceparent (строки 103-149) возвращает входной Контекст без изменений — корректно; ОтелКомпозитный
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Global Propagators]
       found → not_found
       Текст: The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise.
       Расположение: src/Ядро/Модули/ОтелГлобальный.os:188 → -
       Пояснение: По умолчанию API использует не no-op, а pre-configured composite W3C Trace Context + W3C Baggage: ОтелГлобальный.ПолучитьПропагаторы() (ОтелГлобальный
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / W3C Trace Context Requirements]
       found → partial
       Текст: A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP heade
       Пояснение: Извлечь() разбирает и валидирует traceparent (длины trace-id/parent-id/trace-flags, hex-символы, нулевые ID, запрет версии ff, ровно 4 части для верси
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Create]
       found → partial
       Текст: The interface MUST provide a way to create a new resource, from `Attributes`.
       Расположение: src/Ядро/Классы/ОтелПостроительРесурса.os:77 → src/Ядро/Классы/ОтелРесурс.os:100
       Пояснение: Способы создания ресурса есть (конструктор Новый ОтелРесурс(БезУмолчаний, АдресСхемы) и построитель ОтелПостроительРесурса.Построить(), ОтелПостроител
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Specifying resource information via an environment variable]
       found → partial
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Пояснение: Механизм отбрасывания есть: РазобратьСтрокуАтрибутовРесурса обёрнута в Попытка/Исключение и при исключении возвращает Неопределено, так что значение п
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Specifying resource information via an environment variable]
       found → partial
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Пояснение: Лог.Ошибка вызывается только в ветке Исключение (ОтелРесурс.os:182-185), которая для некорректного ввода фактически недостижима: некорректные %-послед
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       found → partial
       Текст: If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.
       Расположение: src/Трассировка/Модули/ОтелСпаны.os:54-59; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:280-281 → src/Трассировка/Классы/ОтелТрассировщик.os:83-87,153-155; src/Трассировка/Модули/ОтелСпаны.os:54-59; src/Трассировка/Классы/ОтелПостроительСпана.os:33-43,127-135
       Пояснение: Для неявного текущего контекста без спана (ОтелТрассировщик.НачатьСпан) и для корневого спана (НачатьКорневойСпан / ПостроительСпана.БезРодителя) в AP
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → partial
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Пояснение: Сам ОтелСпан.Завершить() не выполняет I/O: фиксирует время окончания, проходит CAS-guard и вызывает ПередЗавершением/ПриЗавершении процессора. Однако 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → partial
       Текст: Any locking used needs be minimized and SHOULD be removed entirely if possible.
       Пояснение: В самом ОтелСпан.Завершить() блокировки заменены lock-free CAS (АтомарноеБулево.СравнитьИУстановить), ОтелКомпозитныйПроцессорСпанов блокировок не бер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → partial
       Текст: This API MUST NOT accept a Span or SpanContext as parent, only a full Context.
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:33 → src/Трассировка/Классы/ОтелТрассировщик.os:190
       Пояснение: ОтелПостроительСпана.УстановитьРодителя() принимает только Context (Соответствие/ФиксированноеСоответствие) и отклоняет другие типы исключением. Однак
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → partial
       Текст: The semantic parent of the Span MUST be determined according to the rules described in Determining t
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:127 → src/Трассировка/Классы/ОтелПостроительСпана.os:134
       Пояснение: По правилам Determining the Parent Span from a Context: если в Context есть Span, он становится родителем, иначе создаётся корневой спан. Явный Contex
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → n_a
       Текст: Start timestamp, default to current time. This argument SHOULD only be set when span creation time h
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:103 → src/Трассировка/Классы/ОтелПостроительСпана.os:106
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Рекоменд
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → n_a
       Текст: If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:103 → src/Трассировка/Классы/ОтелПостроительСпана.os:106
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Требован
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → n_a
       Текст: Any span that is created MUST also be ended.
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Специфик
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / TracerProvider]
       found → partial
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`.
       Пояснение: Глобальный реестр ОтелГлобальный хранит только SDK целиком: регистрация через ОтелГлобальный.Установить(Сдк) / ОтелПостроительSdk.ПостроитьИЗарегистри
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Batching processor]
       found → partial
       Текст: The processor SHOULD export a batch when any of the following happens AND the previous export call h
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:159 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:161
       Пояснение: Триггеры реализованы: периодический экспорт (ПериодическийЭкспорт: Приостановить(ИнтервалЭкспортаМс) после завершения предыдущего экспорта), при запол
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Concurrency requirements]
       found → partial
       Текст: Span processor - all methods MUST be safe to be called concurrently.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:328 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:89
       Пояснение: Синхронизация есть, но неполная. ОтелПростойПроцессорСпанов корректен (CAS Закрыт.СравнитьИУстановить в Закрыть, Export под БлокировкаЭкспорта); в Оте
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over f
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:178 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:180
       Пояснение: ЭкспортироватьВсеПакеты проверяет истечение таймаута перед каждым пакетом (стр. 180-182), передаёт экспортеру оставшееся время (стр. 195-196, 220-221)
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / GetDescription]
       found → n_a
       Текст: Callers SHOULD NOT cache the returned value.
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:118 → -
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Сам SDK 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / IdGenerator randomness]
       found → partial
       Текст: If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine wh
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:386 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:390
       Пояснение: Механизм есть: пользовательский ГенераторИд (ОтелПостроительПровайдераТрассировки.УстановитьГенераторИд) может реализовать необязательную ФлагRandomДл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / IdGenerator randomness]
       found → partial
       Текст: Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all genera
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:386 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:390
       Пояснение: Механизм самоидентификации реализован через опциональный метод пользовательского генератора ФлагRandomДляНовыхИд() (duck typing): ОтелПровайдерТрассир
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Presumption of TraceID randomness]
       found → partial
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Пояснение: Приоритет rv реализован: СэмплироватьПоДоле() при наличии валидного rv в ot-подключе использует его (:377-379, РешениеПоRv), иначе опирается на случай
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / SDK Span creation]
       found → partial
       Текст: When asked to create a Span, the SDK MUST act as if doing the following in order:
       Пояснение: Порядок в целом соблюдён: TraceId берётся у родителя или генерируется до вызова сэмплера, SpanId генерируется до сэмплирования независимо от решения (
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors.
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:171 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:161-182
       Пояснение: Закрыть() вызывает Процессор.Закрыть() для каждого процессора из снимка (стр. 165-176), но не гарантирует вызов для всех: при исчерпании таймаута цикл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown()]
       found → partial
       Текст: `Shutdown` MUST include the effects of `ForceFlush`.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:94 → src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:100
       Пояснение: Для пакетного процессора выполнено: ОтелБазовыйПакетныйПроцессор.Закрыть (стр. 95-96) останавливает фоновый экспорт и вызывает ЭкспортироватьВсеПакеты
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Span Limits]
       found → partial
       Текст: Span attributes MUST adhere to the common rules of attribute limits.
       Расположение: src/Трассировка/Классы/ОтелЛимитыСпана.os:1 → src/Трассировка/Классы/ОтелСпан.os:314
       Пояснение: Лимит количества атрибутов (новый ключ сверх МаксАтрибутов отбрасывается со счетчиком ОтброшенныхАтрибутов, перезапись существующего ключа разрешена) 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceIdRatioBased]
       found → partial
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Пояснение: Точность жёстко фиксирована форматом «ЧДЦ=6; ЧРД=.; ЧН=0; ЧГ=» (всегда 6 знаков после точки), поэтому доли, различающиеся после 6-го знака (например 0
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceIdRatioBased]
       found → partial
       Текст: implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision.
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:386 → src/Трассировка/Модули/ОтелСэмплер.os:388
       Пояснение: Детерминированная функция TraceId (младшие 64 бита, стр. 386-393) используется только как fallback: если в родительском tracestate есть ot=rv:<14 hex>
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Tracer Creation]
       found → partial
       Текст: The input provided by the user MUST be used to create an `InstrumentationScope` instance which is st
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:85 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:85-101
       Пояснение: InstrumentationScope строится из всех входных параметров (Новый ОтелОбластьИнструментирования(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресС
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (8) - требует перепроверки:

     [Logs Api / Emit a LogRecord]
       n_a → found
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Код: src/Ядро/Модули/ОтелКонтекст.os:58
       Было: Реализация поддерживает implicit Context (ОтелКонтекст.Текущий() при Контекст=Неопределено в ОтелЛог
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       n_a → partial
       Текст: The resulting User-Agent SHOULD include the exporter's default User-Agent string.
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:289
       Было: Условное требование: применимо только если экспортер реализует MAY-фичу — конфигурационную опцию для
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       n_a → found
       Текст: However, all API implementations of such methods MUST internally call the `End` method and be docume
       Код: src/Трассировка/Классы/ОтелСпан.os:520
       Было: В OneScript нет языковых конструкций вроде Python with-statement, требующих альтернативных End-метод
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: The status code SHOULD remain unset, except for the following circumstances:
       Код: src/Трассировка/Классы/ОтелСпан.os:749
       Было: Требование адресовано instrumentation-библиотекам/вызывающему коду (политика, когда ставить статус);
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise gener
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:257
       Было: Требование адресовано инструментам анализа (analysis tools), а не SDK; данный пакет реализует только
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       n_a → found
       Текст: This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.
       Код: src/Трассировка/Модули/ОтелСпаны.os:36-59
       Было: OneScript не поддерживает запрет наследования/sealed-классы; контроль 'не должно быть переопределяем
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ProbabilitySampler]
       not_found → partial
       Текст: The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`.
       Код: src/Трассировка/Модули/ОтелСэмплер.os:368
       Было: ProbabilitySampler (W3C TC L2 Consistent Probability на 56 битах rv) как самостоятельный встроенный 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceIdRatioBased]
       partial → found
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Код: src/Трассировка/Модули/ОтелСэмплер.os:125
       Было: Точность жёстко задана как ЧДЦ=6 (6 знаков после запятой) в Формат(); это не вытекает из «language s
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  📋 Новые секции (11):
     + [Logs Sdk] Self-observability (1 req)
     + [Metrics Api] Bind (5 req)
     + [Metrics Sdk] Instrument bind (7 req)
     + [Metrics Sdk] Self-observability (1 req)
     + [Metrics Sdk] View matching mode (4 req)
     + [Resource Sdk] Merge behavior with entities (2 req)
     + [Resource Sdk] Merge behavior without Entities (2 req)
     + [Resource Sdk] Retrieve attributes (1 req)
     + [Resource Sdk] Retrieve entities (1 req)
     + [Resource Sdk] Retrieve unassociated attributes (1 req)
     + [Trace Sdk] Self-observability (1 req)

  ➕ НОВЫЕ ТРЕБОВАНИЯ (42) - агент нашёл дополнительные:

     [Logs Api] MUST found: The API MUST accept the following parameters:
     [Logs Api] SHOULD partial: The API documentation SHOULD state that calling `Enabled` is optional and is not
     [Logs Api] SHOULD found: The documentation SHOULD also state that the returned value is not static and ca
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST found: Enabled: If the `Logger` is not enabled (i.e. `LoggerConfig.enabled` is `false`)
     [Logs Sdk] MUST found: `Enabled` MUST return `false` when either:
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: SDKs SHOULD ignore these calls gracefully, if possible.
     [Metrics Sdk] MUST partial: This extension MUST be configurable on a metric View, although individual reserv
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including:
     [Metrics Sdk] MUST found: This MUST be clearly documented in the API and the reservoir MUST be given the `
     [Metrics Sdk] SHOULD partial: If any `Export(batch)` call fails or times out, or if the configured exporter’s 
     [Metrics Sdk] SHOULD found: If all calls succeed, `ForceFlush` SHOULD return some NO ERROR status.
     [Metrics Sdk] MUST found: The implementation MUST maintain reasonable minimum and maximum scale parameters
     [Metrics Sdk] SHOULD partial: The SDK SHOULD use the following logic to determine how to process Measurements 
     [Metrics Sdk] MUST partial: Instrument advisory parameters, if any, MUST be honored.
     [Metrics Sdk] SHOULD partial: If applying the View results in conflicting metric identities the implementation
     [Metrics Sdk] SHOULD partial: If applying the View would produce semantic errors (for example, configuring an 
     [Metrics Sdk] MUST partial: If both the View and Instrument advisory parameters specify the same aspect of t
     ... и ещё 22

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (32) - были раньше, теперь нет:

     [Logs Api] MUST found: The API MUST accept the following parameters: Timestamp (optional), Observed Tim
     [Logs Api] SHOULD found: The API SHOULD be documented that instrumentation authors needs to call this API
     [Logs Sdk] MUST NOT found: ... (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerPro
     [Logs Sdk] MUST found: Enabled MUST return false when either: there are no registered LogRecordProcesso
     [Logs Sdk] SHOULD found: ... its `name` SHOULD keep the original invalid value, ...
     [Logs Sdk] SHOULD found: ... and a message reporting that the specified value is invalid SHOULD be logged
     [Logs Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View,
     [Metrics Sdk] SHOULD found: The "offer" method SHOULD accept measurements, including: The `value` of the mea
     [Metrics Sdk] MUST found: The "offer" method MAY accept a filtered subset of `Attributes` which diverge fr
     [Metrics Sdk] SHOULD found: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and
     [Metrics Sdk] MUST found: Implementations are REQUIRED to accept the entire normal range of IEEE floating 
     [Metrics Sdk] MUST found: If a `View` is registered to a `MeterProvider` and an Instrument is registered t
     [Metrics Sdk] MUST found: If a `View` matches an Instrument, MUST support the `attribute_keys` field as an
     [Metrics Sdk] SHOULD found: The `View`s applying to an Instrument SHOULD be applied in the order they were r
     [Metrics Sdk] SHOULD found: The `View` SHOULD NOT be used to filter attributes in case where its `attribute_
     [Metrics Sdk] SHOULD found: The Instrument `unit` SHOULD be used if it is not overridden by a `View`.
     [Metrics Sdk] SHOULD found: The Instrument `description` SHOULD be used if it is not overridden by a `View`.
     [Metrics Sdk] SHOULD partial: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD found: For asynchronous instrument, the start timestamp SHOULD be:
     ... и ещё 12

  Итого изменений: 208
    Понижений: 126, Повышений: 8, Боковых: 0
    Новых req: 42, Пропущенных req: 32
    Новых секций: 11, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
