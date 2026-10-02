# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             683    822 +  139 ✅
  partial           173     30  -143
  not_found          99     79   -20
  n_a                92    116 +   24
  Всего            1047   1047 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (38) - требует перепроверки:

     [Context / Optional Global operations]
       found → n_a
       Текст: These operations SHOULD only be used to implement automatic scope switching and define higher level 
       Расположение: src/Ядро/Модули/ОтелКонтекст.os:216 → -
       Пояснение: Требование - рекомендация по использованию (caller guidance) для авторов SDK-компонентов и instrumentation libraries о том, в каких случаях следует ис
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD NOT take an indefinite amount of time.
       Расположение: src/Метрики/Классы/ОтелМетр.os:295 → src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:88-146 (ВызватьСТаймаутом); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:349-364 (ТаймаутCallbackМс, по умолчанию 30000мс у инструментов метра)
       Пояснение: Реализован только soft-timeout: SDK перестает ждать callback и отбрасывает результат по истечении таймаута, но платформа OneScript не позволяет прерва
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar]
       found → partial
       Текст: If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:440-442; src/Метрики/Модули/ОтелФильтрЭкземпляров.os:49-51 → src/Метрики/Классы/ОтелХранилищеМетрики.os:54-61,321-328,440-445
       Пояснение: Оверхед на горячем пути (per-measurement) действительно устраняется: ЗахватитьЭкземпляр = ЕстьРезервуар() И ОтелФильтрЭкземпляров.ДолженЗахватить(...)
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:183-187,202-203 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:180-198
       Пояснение: Аналогично Shutdown: ПринудительноВыгрузитьСРезультатом задействует Обещание.Получить(timeout) внутри СбросБуфер/СобратьИЭкспортировать и Экспортер.Эк
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       partial → n_a
       Текст: If a setting selected for the stream would produce semantic errors, the implementation SHOULD emit a
       Расположение: src/Метрики/Классы/ОтелМетр.os:1364-1372,1527-1579 → -
       Пояснение: Требование из ветки "(Development) If view_matching_mode is composable" раздела Measurement processing (статус Mixed): группы View есть только в режим
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       partial → n_a
       Текст: If both the matching Views and Instrument advisory parameters specify the same aspect of the Stream 
       Расположение: src/Метрики/Классы/ОтелМетр.os:899-912,980-992,1364-1372 → -
       Пояснение: Требование из ветки "(Development) If view_matching_mode is composable" раздела Measurement processing (статус Mixed): приоритет объединенных View гру
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → n_a
       Текст: However, if they are already implemented, they SHOULD continue to be supported as they were part of 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1250 → -
       Пояснение: Требование условное ("if they are already implemented"): устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Exemplar Conversion]
       found → n_a
       Текст: When an exemplar is converted per the metric-type-specific sections above, the OpenTelemetry Exempla
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:63-78,589-630 → -
       Пояснение: Условное требование (если протокол поддерживает exemplars). Читатель выдает только обязательный text format 0.0.4, в нем exemplars нет, и они отбрасыв
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Exemplar Conversion]
       found → n_a
       Текст: If present, the OpenTelemetry Exemplar’s Trace ID and Span ID MUST be added as Exemplar labels using
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:63-78,589-630,684-729 → -
       Пояснение: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываю
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Exemplar Conversion]
       found → n_a
       Текст: These labels MUST take precedence over labels from `filtered_attributes` in cases where there is a k
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:63-78,589-630,684-729 → -
       Пояснение: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываю
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Exemplar Conversion]
       found → n_a
       Текст: Timestamps MUST be added as timestamps on the Prometheus exemplar.
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:63-78,589-630,684-729 → -
       Пояснение: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываю
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Exemplar Conversion]
       found → n_a
       Текст: `filtered_attributes` MUST be added as labels on the Prometheus exemplar, unless they would exceed t
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:63-78,589-630,684-729 → -
       Пояснение: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываю
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Exponential Histograms]
       not_found → n_a
       Текст: The Native Histogram `Sum` MUST be set to the Stale NaN value.
       Пояснение: Ограничение платформы OneScript: Число = System.Decimal, NaN невозможен (Число('NaN') выбрасывает исключение), поэтому специальное значение Stale NaN 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Histograms]
       found → partial
       Текст: OpenTelemetry Histograms with Delta aggregation temporality MAY be aggregated into a Cumulative aggr
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:90-92; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:168-183 → src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:338-340,395-406,609-640; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175
       Пояснение: Для метрик SDK временная агрегация читателя всегда кумулятивная (ВременнаяАгрегацияДляВида, стр. 338-340; ОтелПотокиМетрик.ВременнаяАгрегацияЧитателя,
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Histograms as Prometheus Histograms]
       found → n_a
       Текст: If the Prometheus protocol only supports a single exemplar per-bucket, the latest exemplar that fall
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:622-630,684-729 → -
       Пояснение: Условное требование для протокола с одним exemplar на бакет (OpenMetrics). Читатель выдает только обязательный text format 0.0.4 без exemplars, другие
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Histograms as Prometheus NHCB]
       not_found → n_a
       Текст: The Native Histogram `Sum` MUST be set to the Stale NaN value.
       Пояснение: Ограничение платформы OneScript: Число = System.Decimal, NaN невозможен (Число('NaN') выбрасывает исключение, ОписаниеТипов('Число').ПривестиЗначение(
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Resource Attributes]
       found → not_found
       Текст: There MUST be at most one `target` info metric exported for each unique combination of `job` and `in
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:99-150 → -
       Пояснение: Метрики target не выводятся вообще (их ноль), поэтому не более одной на job/instance формально не нарушено, но механизма (job/instance, контроля уника
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Sums]
       found → partial
       Текст: If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of 
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:490-494,592 → src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-478,1060-1072
       Пояснение: Имя без суффикса _total получает его, а имя с одним суффиксом _total остается без изменений (ИменаМетрики, стр. 467-478; БазовоеИмя, стр. 1060-1072). 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Sums]
       found → n_a
       Текст: If Sum is converted to a Prometheus Counter, then `Exemplars` MUST be converted as described in the 
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:589-607 → -
       Пояснение: Условное требование: exemplars конвертируются только для протокола, который их поддерживает (Exemplar Conversion). Читатель выдает только обязательный
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Compatibility / Sums]
       found → n_a
       Текст: If the Prometheus protocol only supports a single exemplar on the Counter sample, the latest exempla
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:589-607 → -
       Пояснение: Условное требование для протокола с одним exemplar на сэмпл счетчика (OpenMetrics). Читатель выдает только обязательный text format 0.0.4 без exemplar
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Exporter / Interaction with Translation Strategy]
       partial → not_found
       Текст: Then, the Prometheus Exporter MUST apply content negotiation, which may include a second translation
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:485-500,838-856 → -
       Пояснение: Согласование содержимого читателем не применяется (см. Content Negotiation): нет ни разбора Accept, ни второго перевода имен по запрошенной escaping-с
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Exporter / Resource Attributes as Metric Labels]
       not_found → n_a
       Текст: Copied Resource attributes MUST NOT be excluded from the `target_info` metric.
       Пояснение: Требование относится к содержимому метрики target_info, а ее описывает раздел Target Info со статусом Development: target_info не формируется (удалена
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Exporter / Translation Strategy]
       found → not_found
       Текст: If the Prometheus exporter supports such configuration it MUST be named to something that resembles 
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:26-28,190-198,866-874 → -
       Пояснение: Настройки стратегии перевода имен нет: ни translation_strategy, ни эквивалента в читателе не существует (grep translation_strategy, UnderscoreEscaping
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Prometheus Exporter / Translation Strategy]
       found → partial
       Текст: If the Prometheus exporter supports such configuration it MUST be named to something that resembles 
       Расположение: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:774-794,485-500,589-596 → src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-500,1060-1072,1496-1527,1533-1537
       Пояснение: Реализована только стратегия по умолчанию UnderscoreEscapingWithSuffixes, и только как единственное жестко заданное поведение: НормализоватьИмя заменя
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attrib
       Расположение: src/Ядро/Классы/ОтелРесурс.os:139 → src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:19-21
       Пояснение: АдресСхемыСемантическихСоглашений присваивается ресурсу безусловно в начале Обнаружить() во всех трёх генерик-детекторах (host/process/cpu), до Попытк
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Merge]
       not_found → n_a
       Текст: If either resource contains `Entities` then merge behavior with Entities MUST be used, otherwise mer
       Пояснение: Первое MUST относится к слиянию с сущностями (Merge behavior with Entities, Development), а сущности ресурса появились в Create как Development с 1.60
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Resource detectors SHOULD have a unique name for reference in configuration.
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: grep по src/Ядро и src/Конфигурация подтверждает, что у детекторов (ОтелДетекторРесурсаХос
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures t
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: у детекторов ресурса нет строковых имён вообще (нет полей/методов имени, нет формата snake
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Resource detector names SHOULD reflect the root namespace of attributes they populate.
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: детекторы (ОтелДетекторРесурсаХоста/Процесса/Процессора) идентифицируются только русскоязы
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name whic
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: понятие 'имя детектора' в коде отсутствует (см. предыдущие пункты), поэтому и правило выбо
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: An SDK which identifies multiple resource detectors with the same name SHOULD report an error.
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: т.к. у детекторов нет имени и нет реестра детекторов по имени, коллизии имён структурно не
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: In order to limit collisions, resource detectors SHOULD document their name in a manner which is eas
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: у детекторов нет публикуемого 'имени' (для конфигурации), которое требовалось бы документи
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Populates `service.name` from the OTEL_SERVICE_NAME environment variable and SHOULD fall back to lan
       Пояснение: Conditional-фича 'Resource Detector Naming' не реализована: в SDK нет отдельного детектора, зарегистрированного под зарезервированным именем 'service'
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Retrieve unassociated attributes]
       partial → not_found
       Текст: The SDK SHOULD provide a way to retrieve attributes which are NOT associated with an entity in the r
       Расположение: src/Ядро/Классы/ОтелРесурс.os:19 → -
       Пояснение: Сущности ресурса (Entities, Development) не поддерживаются, поэтому нет и способа получить атрибуты, не связанные с сущностями: ОтелРесурс хранит толь
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / IsRecording]
       found → n_a
       Текст: This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when
       Расположение: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:68 → -
       Пояснение: Требование является рекомендацией по использованию флага IsRecording для инструментирующего кода/вызывающих (caller guidance) - оно советует авторам и
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise gener
       Расположение: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:264-269 → -
       Пояснение: Требование адресовано внешним downstream Analysis tools (бэкендам/системам анализа телеметрии), а не Trace API/SDK - аналогично категории Instrumentat
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / CompositeSampler]
       partial → not_found
       Текст: The explicit randomness values MUST not be modified.
       Расположение: src/Трассировка/Классы/ОтелСостояниеТрассировки.os:201 → -
       Пояснение: Требование сформулировано в контексте trace_state_provider внутри ComposableSampler, которого нет в коде. Общая защита 'rv' в ОтелСостояниеТрассировки
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:146-168 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114,330-339; oscript_modules/async/src/internal/Классы/Обещание.os:23-35
       Пояснение: TracerProvider.Закрыть(ТаймаутМс) принимает таймаут и корректно урезает остаток времени для каждого процессора (ОтелРезультатыЗакрытия.ОставшеесяВремя
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (164) - требует перепроверки:

     [Baggage Api / Propagation]
       partial → found
       Текст: The API layer or an extension package MUST include the following `Propagator`s:
       Код: src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:31 (Внедрить/inject), :97 (Извлечь/extract) - TextMapPropagator реализующий W3C Baggage Specification, включён в основной пакет (lib.config:144)
       Было: TextMapPropagator ОтелW3CBaggageПропагатор (Внедрить/Извлечь/Поля, заголовок baggage, key=value;prop
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Declarative configuration]
       partial → found
       Текст: When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the conf
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:104-126; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:73,784; src/Ядро/Классы/ОтелРесурс.os:102-106,138-140; src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:246
       Было: Инициализировать() без МенеджерПараметров при заданной OTEL_CONFIG_FILE (фолбэк OTEL_EXPERIMENTAL_CO
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Environment Variable Specification]
       partial → found
       Текст: If they do, they SHOULD use the names and value parsing behavior specified in this document.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-74,149-155,952-964,1074-1080,1094-1112,1205-1214,1249-1265
       Было: Имена соответствуют спецификации: стандартные OTEL_* читаются через ПровайдерПараметровENV из config
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Environment Variable Specification]
       partial → found
       Текст: They SHOULD also follow the common configuration specification.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130,1163-1172,1186-1193; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:272; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:524-532
       Было: Common-спецификация соблюдена частично. Выполнено: нераспарсиваемые и отрицательные числовые значени
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       partial → found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:981-985,1109-1110,1231-1233
       Было: Некорректный аргумент логируется и заменяется умолчанием: нечисловой и отрицательный - БезопасноеЧис
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Numeric]
       partial → found
       Текст: The following paragraph was added after stabilization and the requirements are thus qualified as “SH
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130
       Было: Мета-требование: квалифицирует как SHOULD следующий абзац о числовых значениях (warning + graceful i
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Numeric]
       partial → found
       Текст: For new implementations, these should be treated as MUST requirements.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130,1163-1172
       Было: Реализация новая, поэтому требование о числовых значениях действует как MUST; выполнено не полностью
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Numeric]
       partial → found
       Текст: For variables accepting a numeric value, if the user provides a value the implementation cannot pars
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130,978-987
       Было: БезопасноеЧисло (стр. 1045-1062) применяется ко всем числовым переменным автоконфигурации (таймауты 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Parsing empty value]
       partial → found
       Текст: The SDK MUST interpret an empty value of an environment variable the same way as when the variable i
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:894-898,920-926,953-955,1052-1054,1074-1080,1094-1097,1279-1287; src/Ядро/Классы/ОтелРесурс.os:143-158; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-119; src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:246-259
       Было: Почти все переменные трактуют пустое значение как незаданное: ПараметрИлиУмолчание (стр. 1026-1032),
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Enabled]
       partial → found
       Текст: The API documentation SHOULD state that calling `Enabled` is optional and is not required before emi
       Код: src/Логирование/Классы/ОтелЛоггер.os:29-33
       Было: Документирующий комментарий Включен() (ОтелЛоггер.os:28-45) и docs/api/Логирование/ОтелЛоггер.md опи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / LoggerProvider]
       partial → found
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`.
       Код: src/Ядро/Модули/ОтелГлобальный.os:147,157
       Было: Глобальный реестр ОтелГлобальный хранит только SDK целиком: регистрация через ОтелГлобальный.Установ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Concurrency requirements]
       partial → found
       Текст: LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:60-108,138-140,152-160,334-336
       Было: ForceFlush и Shutdown безопасны: Закрыть() использует CAS на АтомарноеБулево (стр. 141; покрыто тест
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Concurrency requirements]
       partial → found
       Текст: Logger - all methods MUST be safe to be called concurrently.
       Код: src/Логирование/Классы/ОтелЛоггер.os:7,60-141,324
       Было: Записать()/Включен() не мутируют разделяемое состояние логгера (запись принадлежит вызывающему, scop
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Enabled]
       partial → found
       Текст: Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller.
       Код: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:19-42, src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101, src/Логирование/Классы/ОтелЛоггер.os:72-90
       Было: ОтелЛоггер.Включен передаёт процессорам защищённую копию InstrumentationScope (ЗащищеннаяКопияОбласт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       partial → found
       Текст: all `LogRecord` Attributes MUST be copied to the span event as span event attributes.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:76,82, src/Логирование/Классы/ОтелЗаписьЛога.os:101-107
       Было: Все атрибуты записи попадают в span event, но не копируются: мост передаёт в Спан.ДобавитьСобытие са
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcess
       Код: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:91-97, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217
       Было: Записи, находящиеся в буфере, экспортируются синхронно до возврата (СброситьБуфер → ЭкспортироватьВс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-210
       Было: Основной путь соблюдает таймаут: ЭкспортироватьВсеПакеты проверяет истечение ТаймаутМс перед каждым 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:44-54, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81
       Было: СброситьБуфер возвращает ОтелРезультатЭкспорта (Успех/Ошибка/Таймаут), ПринудительноВыгрузитьСРезуль
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / LogRecord Limits]
       partial → found
       Текст: `LogRecord` attributes MUST adhere to the common rules of attribute limits.
       Код: src/Логирование/Классы/ОтелЗаписьЛога.os:249-251; src/Ядро/Модули/ОтелУтилиты.os:406
       Было: Реализованы лимит количества атрибутов (новый ключ сверх МаксАтрибутов, по умолчанию 128, отбрасывае
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / OnEmit]
       partial → found
       Текст: This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD 
       Код: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:5-8, src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:39-56, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:41-69
       Было: Исключения наружу не пробрасываются: ОтелКомпозитныйПроцессорЛогов.ПриПоявлении оборачивает вызов ка
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:56-67, src/Ядро/Модули/ОтелРезультатыЗакрытия.os:1-37
       Было: Закрыть возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут) в пакетном (ОтелБазовыйПакетныйПроце
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: `Shutdown` MUST include the effects of `ForceFlush`.
       Код: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:109-117, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114
       Было: Пакетный процессор требование выполняет: ОтелБазовыйПакетныйПроцессор.Закрыть() дожидается фонового 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159,196-199; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,215-236
       Было: Закрыть() возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут), ЗакрытьАсинхронно() - Обещание, о
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,159-177,192-202
       Было: Закрыть(ТаймаутМс = 30000) принимает таймаут, но проверяет его только между процессорами (стр. 149-1
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-54,69-76
       Было: Закрыть() вызывает Процессор.Закрыть() для каждого процессора из снимка (стр. 148-155), но не гарант
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Asynchronous Counter creation]
       partial → found
       Текст: The API MUST treat observations from a single callback as logically taking place at a single instant
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:396-401 (одиночный callback); src/Метрики/Классы/ОтелМетр.os:778-784 (мульти-callback)
       Было: Для callback-ов отдельного инструмента (переданных в СоздатьНаблюдаемыйСчетчик или через ДобавитьCal
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Asynchronous Counter creation]
       partial → found
       Текст: The API MUST treat observations from a single callback as logically taking place at a single instant
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:396-401 (одиночный callback); src/Метрики/Классы/ОтелМетр.os:778-784 (мульти-callback)
       Было: Идентичные startTimeUnixNano/timeUnixNano (ОтелБазовыйНаблюдаемыйИнструмент.os:450-451) гарантируютс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Concurrency requirements]
       partial → found
       Текст: Instrument - all methods MUST be documented that implementations need to be safe for concurrent use 
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:33-34; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:43-46
       Было: Документация потокобезопасности есть только у синхронных инструментов: ОтелБазовыйСинхронныйИнструме
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument advisory parameters]
       partial → found
       Текст: OpenTelemetry SDKs MUST handle `advisory` parameters as described here.
       Код: src/Метрики/Классы/ОтелМетр.os:1551-1597 (ПроверитьСовет); src/Метрики/Модули/ОтелПотокиМетрик.os:376,401 (ExplicitBucketBoundaries/ГраницыГистограммы и Attributes/КлючиАтрибутов применяются при разрешении потоков)
       Было: Advisory-параметры полноценно обрабатываются только для синхронных инструментов: ПроверитьСовет (Оте
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / MeterProvider]
       partial → found
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`.
       Код: src/Ядро/Модули/ОтелГлобальный.os:175-177,185-194
       Было: Глобальный реестр ОтелГлобальный хранит только SDK целиком: регистрация через ОтелГлобальный.Установ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API MUST support creation of asynchronous instruments by passing zero or more `callback` functio
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:511-522 (callback-и из конструктора добавляются в Действия навсегда)
       Было: Callback-и, переданные в СоздатьНаблюдаемыйСчетчик/СоздатьНаблюдаемыйРеверсивныйСчетчик/СоздатьНаблю
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Where the API supports registration of `callback` functions after asynchronous instrumentation creat
       Код: src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14-20 (Закрыть); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:151-163 (УдалитьCallback)
       Было: Отмена регистрации возможна только для callback-ов отдельного инструмента: ОтелБазовыйНаблюдаемыйИнс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions MUST be documented as follows for the end user:
       Код: src/Метрики/Классы/ОтелМетр.os:157-170; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:109-118 (doc-комментарии перечисляют reentrant/no-indefinite-time/no-duplicates)
       Было: Рекомендации для callback-ов задокументированы в комментариях СоздатьНаблюдаемыйСчетчик/СоздатьНаблю
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same
       Код: src/Метрики/Классы/ОтелМетр.os:161-164 (задокументировано в doc-комментарии); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:299-322 (ДобавитьНаблюдение агрегирует наблюдения с одинаковыми атрибутами в одну серию, не нарушая сбор)
       Было: Рекомендация задокументирована в суженном виде: в описаниях СоздатьНаблюдаемыйСчетчик/СоздатьНаблюда
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of 
       Код: src/Метрики/Классы/ОтелМетр.os:529-557 (ЗарегистрироватьОбратныйВызов: проверка ПринадлежитМетру и ЭтоАсинхронныйИнструмент для каждого инструмента набора при регистрации)
       Было: Мульти-callback ассоциируется при регистрации с объявленным набором инструментов (ОтелМетр.Зарегистр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API MUST treat observations from a single Callback as logically taking place at a single instant
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:389-409 (одно ВремяНаблюдения на все записи одного вызова callback-а)
       Было: Для callback-ов одного инструмента (переданных при создании или через ДобавитьCallback) наблюдения о
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API MUST treat observations from a single Callback as logically taking place at a single instant
       Код: src/Метрики/Классы/ОтелМетр.os:771-791 (ВыполнитьОднуРегистрацию - одно ВремяНаблюдения на все инструменты одного мульти-callback)
       Было: Идентичные timestamps гарантируются только в пределах одного инструмента. Наблюдения мульти-инструме
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Aggregation]
       partial → found
       Текст: The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Mo
       Код: src/Метрики/Модули/ОтелАгрегация.os:15-65,215-240 (Drop/Default/Sum/LastValue/ExplicitBucketHistogram, СоздатьАгрегаторПотока)
       Было: Все агрегации есть (ОтелАгрегация: ПоУмолчанию/Сумма/ПоследнееЗначение/Отбросить/ГистограммаСЯвнымиГ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Aggregation]
       partial → found
       Текст: The SDK SHOULD provide the following `Aggregation`:
       Код: src/Метрики/Модули/ОтелАгрегация.os:76-81,232-237; src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os
       Было: ОтелАгрегаторЭкспоненциальнойГистограммы и ОтелАгрегация.ГистограммаЭкспоненциальная есть и работают
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Collect]
       partial → found
       Текст: `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:386-398; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:93-115,357-385
       Было: Отдельной операции Collect нет: у ОтелПериодическийЧитательМетрик сбор выполняет приватная СобратьИЭ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:76-128,179-181,191-222
       Было: Синхронизация есть, но неполная. Создание Meter защищено СинхронизированнаяКарта + double-checked lo
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: ExemplarReservoir - all methods MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-134; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50-116
       Было: Синхронизация частичная. ОтелРезервуарЭкземпляров: Предложить защищён (СинхронизированнаяКарта + Ато
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105-111,142-168,180-198,386-398
       Было: Синхронизация частичная. Списки метров и продюсеров копируются под БлокировкаРесурса (ОтелПериодичес
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also app
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:269-360 (ЗарегистрироватьПредставление, УстановитьАгрегациюГистограммПоУмолчанию, УстановитьТаймаутОбратныхВызововМс, ОбновитьКонфигуратор - все проходят по Метрики.Значения() и обновляют уже выданные Meter)
       Было: Обновления Views (ЗарегистрироватьПредставление, стр. 273-278; массив Представления передается метра
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also app
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:102-118 (новые метры получают текущую конфигурацию при создании), :269-360 (уже выданные метры обновляются на месте) - поведение не зависит от момента получения Meter
       Было: Для Views и для конфигуратора, возвращающего явную ОтелКонфигурацияМетра, момент получения метра зна
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardi
       Код: src/Метрики/Классы/ОтелПредставление.os:92-93,112-113,170-180; src/Метрики/Модули/ОтелПотокиМетрик.os:338-340,366-382
       Было: Для синхронных инструментов ЛимитМощностиАгрегации() совпавшего View переопределяет лимит читателя (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:257-280; src/Метрики/Модули/ОтелПотокиМетрик.os:378-380,455-468
       Было: Лимит читателя (ОтелПериодическийЧитательМетрик.ЛимитМощности(), параметр конструктора НовыйЛимитМощ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Custom ExemplarReservoir]
       partial → found
       Текст: This extension MUST be configurable on a metric View, although individual reservoirs MUST still be i
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:316-328,440-445
       Было: Per-timeseries инстанцирование гарантируется, только если во View передана фабрика (объект с методом
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Defaults and configuration]
       partial → found
       Текст: The SDK MUST provide configuration according to the SDK environment variables specification.
       Код: src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129
       Было: Конфигурация метрик через переменные окружения реализована, но не полностью. Поддерживаются (ОтелАвт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: This means that the Meter MUST return a functional instrument that can be expected to export data ev
       Код: src/Метрики/Классы/ОтелМетр.os:1136-1147,1230-1266
       Было: Для синхронных инструментов выполняется: при конфликте вида или единицы (ЕстьНесовместимыйКонфликт, 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: The emitted warning SHOULD include information for the user on how to resolve the conflict, if possi
       Код: src/Метрики/Классы/ОтелМетр.os:1683-1726 (ПостроитьРецептРазрешенияКонфликта)
       Было: Рецепт добавляется к предупреждению (ПостроитьРецептРазрешенияКонфликта, стр. 1491-1507): при конфли
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: To accommodate the recommendations from the data model, the SDK MUST aggregate data from identical I
       Код: src/Метрики/Классы/ОтелМетр.os:1136-1147 (НайтиЗарегистрированныйИнструмент)
       Было: Для синхронных инструментов идентичные регистрации (имя без учёта регистра, вид, единица, описание) 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar defaults]
       partial → found
       Текст: Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExem
       Код: src/Метрики/Модули/ОтелАгрегация.os:259-261
       Было: AlignedHistogramBucketExemplarReservoir назначается только в ОтелМетр.СоздатьГистограмму — при View 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar defaults]
       partial → found
       Текст: Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reser
       Код: src/Метрики/Модули/ОтелАгрегация.os:255,262-263
       Было: Размер min(20, МаксБакетов) задаётся только в ОтелМетр.СоздатьЭкспоненциальнуюГистограмму (стр. 198-
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarFilter]
       partial → found
       Текст: The filter configuration SHOULD follow the environment variable specification.
       Код: src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:892-900; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:673-687; src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:347
       Было: OTEL_METRICS_EXEMPLAR_FILTER (always_on/always_off/trace_based, без учёта регистра; неизвестное знач
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by ag
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:316-328,440-445; src/Метрики/Модули/ОтелАгрегация.os:254-266
       Было: Для синхронных инструментов с фабрикой резервуар создаётся на каждую серию (ключ атрибутов после фил
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggreg
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:226-249; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:246-269
       Было: Для обычных серий filteredAttributes = атрибуты измерения минус ключи атрибутов серии после фильтра 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `Force
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:375-386
       Было: ОтелПровайдерМетрик.СброситьБуфер обходит всех читателей, но собственный ForceFlush читателя (Сброси
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:451-470; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:192-202
       Было: СброситьБуфер/ПринудительноВыгрузитьСРезультатом принимают ТаймаутМс, но он передаётся только послед
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each b
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:180-198,787-803
       Было: ПринудительноВыгрузитьСРезультатом собирает метрики и передаёт их одним вызовом Экспортировать (разб
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: If any `Export(batch)` call fails or times out, or if the configured exporter’s `ForceFlush()` fails
       Код: src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-236
       Было: Сбой или таймаут Экспортировать даёт Ошибка («Сбой выгрузки буфера»), ошибочный ОтелРезультатЗакрыти
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpD
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:64-68 (Записать); src/Метрики/Модули/ОтелАгрегация.os:216-218 (СобиратьSum = НЕ ЗаписываетОтрицательные(Вид))
       Было: Для explicit-гистограммы через View на UpDownCounter sum не собирается (СобиратьSum = Ложь для немон
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument advisory parameters]
       partial → found
       Текст: When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters.
       Код: src/Метрики/Классы/ОтелМетр.os:1551-1597 (ПроверитьСовет)
       Было: ПроверитьСовет (стр. 1330-1362, вызывается во всех СоздатьXxx с Совет) проверяет только форму: Совет
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument advisory parameters]
       partial → found
       Текст: If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed
       Код: src/Метрики/Классы/ОтелМетр.os:1566-1594 (Лог.Предупреждение + сброс поля в Неопределено внутри ПроверитьСовет)
       Было: Для ошибок формы, которые обнаруживает ПроверитьСовет, поведение соответствует спеке: Лог.Предупрежд
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument advisory parameters]
       partial → found
       Текст: If both a View and advisory parameters specify the same aspect of the Stream configuration, the sett
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:366-402 (ЗавершитьПоток, ГраницыПотока - границы View приоритетнее advisory),252-253,375-376 (ключи атрибутов View приоритетнее advisory)
       Было: Приоритет View реализован для границ гистограммы (ОпределитьГраницыГистограммы стр. 980-992: View.Гр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument enabled]
       partial → found
       Текст: The synchronous instrument `Enabled` MUST return `false` when either:
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253 (Включен),322-333 (ВсеПотокиОтбрасывают, drop-агрегация)
       Было: Включен() = МетрВключен.Получить() И Включен.Получить() (стр. 273-276): возвращает Ложь при MeterCon
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument selection criteria]
       partial → found
       Текст: The SDK MUST accept the following criteria:
       Код: src/Метрики/Классы/ОтелСелекторИнструментов.os:164-174
       Было: ОтелСелекторИнструментов принимает все шесть критериев (name с «*», type, unit, meter_name, meter_ve
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48-71
       Было: ОтелЭкспортерМетрик.Экспортировать ограничивает ожидание отправки (Обещание.Получить) таймаутом - по
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48-71
       Было: Верхний предел у экспортера есть (ТаймаутМс, по умолчанию 10000; при превышении - Ложь), но он дейст
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrum
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:111-125,218-232 (СоздатьХранилища, ПотокиЧитателя)
       Было: Применяется только первый совпавший View (НайтиПредставление в метре и ПрименитьПредставление в чита
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: Instrument advisory parameters, if any, MUST be honored.
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:356-382,394-402 (ЗавершитьПоток, ГраницыПотока - ЗначениеСовета)
       Было: Для синхронных инструментов advisory ГраницыГистограммы (ОпределитьГраницыГистограммы) и КлючиАтрибу
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Код: src/Метрики/Классы/ОтелМетр.os:848-891 (ЗарегистрироватьИменаПотоков, ПредупредитьОКонфликтеПотоков)
       Было: View применяется, но предупреждение выдаётся только для View с НовоеИмя и селектором без точного име
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: If applying the View would produce semantic errors (for example, configuring an asynchronous instrum
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:288-314,246-256 (ПрименитьАгрегацию, ПотокПредставления)
       Было: Предупреждение и отказ от View-агрегации есть только для гистограммной агрегации у async-инструменто
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: If both the View and Instrument advisory parameters specify the same aspect of the Stream configurat
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:366-382,394-402 (ЗавершитьПоток, ГраницыПотока - advisory применяется только как fallback)
       Было: Границы гистограммы из View приоритетнее advisory ГраницыГистограммы (ОпределитьГраницыГистограммы),
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter]
       partial → found
       Текст: Status: Development - `Meter` MUST behave according to the MeterConfig computed during Meter creatio
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:105-117,407-416
       Было: MeterConfig вычисляется при создании метра (ПрименитьКонфигурацию -> Метрика.УстановитьМетрВключен, 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter]
       partial → found
       Текст: If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:350-360,418-424
       Было: ОбновитьКонфигуратор() сохраняет новый конфигуратор и применяет его ко всем созданным метрам (Примен
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: Status: Development - The `MeterProvider` MUST compute the relevant MeterConfig using the configured
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:407-416 (ПрименитьКонфигурацию), :116 (вызов при создании метра в ПолучитьМетр); src/Метрики/Классы/ОтелМетр.os:372-374,441-443 (Включен() влияет на поведение метра - СобратьДляЧитателя)
       Было: MeterConfig вычисляется при создании метра: ПрименитьКонфигурацию (стр. 110, 342-350) вызывает Конфи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MeterConfig]
       partial → found
       Текст: If a `Meter` is disabled, it MUST behave equivalently to No-op Meter.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:456-460; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76-93,250-253; src/Метрики/Классы/ОтелМетр.os:439-443
       Было: Частично: ОтелПериодическийЧитательМетрик не собирает отключённый метр (стр. 405-408), Включен() син
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricExporter]
       partial → found
       Текст: `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they 
       Код: src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1-47; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:243-249
       Было: ИнтерфейсЭкспортерМетрик (Экспортировать, СброситьБуфер, Закрыть) реализуется ОтелЭкспортерМетрик че
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricExporter]
       partial → found
       Текст: Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsuppo
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:163-214
       Было: ОтелЭкспортерМетрик.ВалидироватьСовместимостьДанных сообщает (предупреждение + Ложь) о неподдерживае
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided:
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:749-771
       Было: Конструктор ОтелПериодическийЧитательМетрик(Экспортер, ИнтервалЭкспортаМс, НовыйЛимитМощности, Новая
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the con
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:92-111; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:62-84
       Было: Для синхронных инструментов Delta/Cumulative реализованы сбросом или сохранением аккумуляторов (Очис
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only recei
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:350-378
       Было: Delta-аккумуляторы сбрасываются не в момент сбора, а в ВыполнитьЭкспорт и только при успешном экспор
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: For instruments with Cumulative aggregation temporality, successive data points received by successi
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:356-368; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:279-281
       Было: Для синхронных инструментов при Cumulative ВремяСтарта сохраняется и повторяется. Для асинхронных (O
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: For instruments with Delta aggregation temporality, successive data points received by successive ca
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:356-358; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:235-238,279-281
       Было: Для асинхронных инструментов startTimeUnixNano = timeUnixNano = время текущего сбора (ПреобразоватьЗ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`,
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:71-149
       Было: Состояние асинхронных инструментов изолировано per-reader (КумулятивноеСостояниеАсинх), но состояние
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and Mete
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:179-222
       Было: Провайдер делегирует ForceFlush/Shutdown читателям, но формального интерфейса читателя нет, и ОтелПр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:254-275 (СобратьДляЧитателя); src/Метрики/Классы/ОтелМетр.os:439-470 (СобратьДляЧитателя)
       Было: Callback-и вызываются в момент сбора конкретным читателем (Метр.ВызватьМультиОбратныеВызовы + Инстру
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Код: src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:108-146 (ВызватьСТаймаутом)
       Было: Таймаут есть (ТаймаутCallbackМс → ФоновыеЗадания.Выполнить + ОжидатьЗавершения), но по умолчанию 0 (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: The implementation MUST complete the execution of all callbacks for a given instrument before starti
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:389-409 (ВызватьCallbackи - синхронный цикл); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:33-35,386-398 (БлокировкаСбора сериализует сборы)
       Было: Внутри одного раунда callback-и выполняются синхронно и завершаются до возврата Собрать() (при Тайма
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Overflow attribute]
       partial → found
       Текст: The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct,
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:305-319
       Было: В последовательном случае гарантия обеспечена: переполнение наступает только для нового набора при А
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Periodic exporting MetricReader]
       not_found → found
       Текст: When `maxExportBatchSize` is configured, the reader MUST ensure no batch provided to `Export` exceed
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:543-574
       Было: Параметра maxExportBatchSize нет ни в ОтелПериодическийЧитательМетрик (конструктор: Экспортер, Интер
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Periodic exporting MetricReader]
       not_found → found
       Текст: The initial batch of metric data MUST be split into as many “full” batches of size `maxExportBatchSi
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:543-574,586-600
       Было: Разбиение собранных данных на «полные» пакеты размера maxExportBatchSize (в том числе с разделением 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Periodic exporting MetricReader]
       partial → found
       Текст: The reader MUST ensure all batches produced from a single `Collect()` are provided to `Export` seria
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:386-398,451-470
       Было: Разбиения на пакеты нет, поэтому каждый сбор даёт ровно один вызов Экспортировать, и вызовы сериализ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: SDKs SHOULD return a valid no-op Meter for these calls, if possible.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:88-90,456-460 (НоопМетр - после Закрыть возвращается выключенный Meter)
       Было: После Закрыть() ПолучитьМетр (стр. 84-88) возвращает новый ОтелМетр, не зарегистрированный у читател
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40 (Успешно/ИстекТаймаут/Описание); src/Метрики/Классы/ОтелПровайдерМетрик.os:221 (Закрыть возвращает ОтелРезультатЗакрытия)
       Было: Закрыть(ТаймаутМс) возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут), ЗакрытьАсинхронно() - Об
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and Me
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:207-220 (цикл по ЧитателиМетрик, вызов Закрыть у каждого); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:164-166 (читатель вызывает Закрыть у своего Экспортер)
       Было: Закрыть() вызывает Закрыть() у каждого зарегистрированного читателя (стр. 196-207), а ОтелПериодичес
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: SDKs SHOULD return some failure for these calls, if possible.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105-109,123-127; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:358-361
       Было: ОтелПериодическийЧитательМетрик после Закрыть возвращает Ошибка из СброситьБуфер/СброситьБуферБезОчи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:142-168; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-31
       Было: ОтелПериодическийЧитательМетрик.Закрыть возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут), но 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval’s timestamp,
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:139-153,330-332,552
       Было: Синхронные инструменты соответствуют: ВремяСтарта = время создания инструмента (стр. 344), при delta
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:330-332,350-378,392-408
       Было: Синхронные инструменты передают одно ВремяСтарта во все точки сбора (стр. 373-375). У асинхронных ин
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:139-153
       Было: Синхронные инструменты при cumulative не сбрасывают ВремяСтарта (ОчиститьТочкиДанных, стр. 177-182) 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       not_found → found
       Текст: For asynchronous instrument, the start timestamp SHOULD be: * The creation time of the instrument, i
       Код: src/Метрики/Классы/ОтелХранилищеНаблюдений.os:279-297,438-455
       Было: Асинхронные инструменты не хранят ни время своего создания, ни время предыдущего сбора: ОтелБазовыйН
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other
       Код: src/Метрики/Классы/ОтелОбработчикАтрибутов.os:22-56
       Было: Отбрасывание атрибутов вне allow-list реализовано только для синхронных инструментов (Записать → Фил
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter confi
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:375-377 (ЗначениеСовета(Дескриптор, "КлючиАтрибутов"))
       Было: Для синхронных инструментов при отсутствии allow-list во View используются КлючиАтрибутов из Совет (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all oth
       Код: src/Метрики/Классы/ОтелОбработчикАтрибутов.os:51-56 (КлючСохраняется)
       Было: Исключение работает только для синхронных инструментов без advisory КлючиАтрибутов и без allow-list 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all oth
       Код: src/Метрики/Классы/ОтелОбработчикАтрибутов.os:51-56 (КлючСохраняется)
       Было: При одном exclude-list прочие атрибуты сохраняются (ИсключитьАтрибутыПоКлючам). Но если у инструмент
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: SDK documentation SHOULD inform users that attributes excluded from a metric stream by View configur
       Код: src/Метрики/Классы/ОтелПредставление.os:142-145 (комментарий-документация класса View)
       Было: Ни в документации (docs/product/050-metrics.md, раздел «Представления (Views)»; docs/api/Метрики/Оте
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggreg
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:367-370,415-443 (АгрегацияЧитателя); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302-318 (АгрегацияПоУмолчанию)
       Было: Агрегация по умолчанию захардкожена в ОтелМетр по виду инструмента (Sum/LastValue/гистограмма); от M
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST appl
       Код: src/Метрики/Модули/ОтелПотокиМетрик.os:378-380,455-468 (ЛимитМощностиЧитателя)
       Было: Лимит берётся из ЛимитМощности() только первого зарегистрированного читателя (ПрименитьНастройкиЧита
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Synchronous instrument cardinality limits]
       partial → found
       Текст: Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in ex
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,305-319
       Было: Маршрутизация в Записать() корректна: измерение пишется ровно в один аккумулятор - своего набора атр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Synchronous instrument cardinality limits]
       partial → found
       Текст: Measurements MUST NOT be double-counted or dropped during an overflow.
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,305-319
       Было: Логика переполнения сама по себе не теряет и не дублирует измерения (одна запись в свой или overflow
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: Each configuration option MUST be overridable by a signal specific option.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:666-751 (СоздатьТранспортДляСигнала), 1267-1287 (ПараметрСигналаИлиОбщий), 1127-1130 (ЧислоСОткатом)
       Было: Per-signal переопределение реализовано для всех env-опций: ПараметрСигналаИлиОбщий (protocol, header
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Retry]
       partial → found
       Текст: Transient errors MUST be handled with a retry strategy.
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:204-232 (коды 429/502/503/504 бросают исключение, перехватываемое стратегией повтора), 350-354; src/Экспорт/Классы/ОтелGrpcТранспорт.os:191-209 (ОшибкаПовторяемая), 256-259
       Было: HTTP соответствует: коды 429/502/503/504 (ОтелHttpТранспорт.os:168-172) и сетевые исключения Коннект
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       partial → found
       Текст: OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the export
       Код: src/Ядро/Модули/ОтелУтилиты.os:508-519 (UserAgentЭкспортераOtlp -> "OTel-OTLP-Exporter-OneScript/<версия>"); src/Экспорт/Классы/ОтелHttpТранспорт.os:368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:300
       Было: HTTP и gRPC транспорты отправляют User-Agent «OTel-OTLP-Exporter-OneScript/<версия>» (экспортер и яз
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       partial → found
       Текст: The resulting User-Agent SHOULD include the exporter’s default User-Agent string.
       Код: src/Ядро/Модули/ОтелУтилиты.os:508-519 (ИдентификаторПродукта + " " + СтандартныйUserAgent); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302 (СформироватьМетаданные)
       Было: Отдельной опции product identifier нет. Изменить User-Agent можно только через общие заголовки (OTEL
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Differences between Prometheus formats]
       not_found → found
       Текст: If the specification below requires producing a Prometheus Info-typed metric, a Prometheus Gauge wit
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-500,512-531,542-550,717-718
       Было: Замены Info-метрики gauge-метрикой с суффиксом `_info` нет. ОтелПрометеусЧитательМетрик выдаёт тольк
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exponential Histograms]
       partial → found
       Текст: If `Scale` is < -4, the data point MUST be dropped.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:609-611,651-658
       Было: Метрики типа exponentialHistogram отбрасываются целиком независимо от Scale (стр. 318-323), поэтому 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exponential Histograms]
       partial → found
       Текст: Any data point unable to be rescaled to an acceptable range MUST be dropped.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:609-611,651-658
       Было: Для метрик типа exponentialHistogram требование выполняется за счет отбрасывания всех точек (стр. 31
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Gauges]
       partial → found
       Текст: An OpenTelemetry Gauge MUST be converted following a hint present in metric.metadata:
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:512-531; src/Метрики/Классы/ОтелДанныеМетрики.os:133-150
       Было: OpenTelemetry Gauge всегда выводится как Prometheus gauge (ОпределитьТипPrometheus стр. 574-587, Доб
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Gauges]
       not_found → found
       Текст: If the `prometheus.type` key has value equal to `unkown`, the datapoint MUST be transformed to a Pro
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:523-525,542-544
       Было: Обработки prometheus.type=unknown нет: metric.metadata в модели данных SDK отсутствует (у ОтелДанные
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Gauges]
       not_found → found
       Текст: If the `prometheus.type` key has value equal to `info`, the datapoint SHOULD be transformed to a Pro
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-474,526-527,545-546,717-718
       Было: Обработки prometheus.type=info нет: metric.metadata в модели данных SDK отсутствует, подсказка не чи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Histograms]
       partial → found
       Текст: An OpenTelemetry Histogram with a cumulative aggregation temporality MUST be converted to a Promethe
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:301-304,338-340,512-516,733-750; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175
       Было: Гистограмма конвертируется в семейство histogram (_bucket с le и накопленным счетом, +Inf, _sum, _co
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Histograms as Prometheus Histograms]
       partial → found
       Текст: When converting to a Prometheus Histogram, an OpenTelemetry Histogram MUST be converted following th
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:733-750; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:199-264
       Было: Правила конвертации одной точки реализованы: count -> _count и sum -> _sum (ДобавитьСуммуИСчет стр. 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Instrumentation Scope]
       partial → found
       Текст: Prometheus exporters MUST by default add the scope name as the `otel_scope_name` label, the scope ve
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1154-1165,1265-1288,1320-1349
       Было: Лейблы otel_scope_name, otel_scope_version, otel_scope_schema_url и otel_scope_<атрибут> добавляются
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Metric Attributes]
       partial → found
       Текст: Discouraged characters SHOULD be replaced with the `_` character.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1496-1514,1525-1527,1545
       Было: Имена лейблов нормализуются функцией НормализоватьИмя (стр. 752, 838-856): символы вне [a-zA-Z0-9_:]
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Metric Attributes]
       not_found → partial
       Текст: In such cases, the values MUST be concatenated together, separated by `;`, and ordered by the lexico
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1154-1165,1320-1349,1357-1363,1374-1387
       Было: Склейки значений через ; нет: в ЛейблыИзАтрибутовOtlp (src/Метрики/Классы/ОтелПрометеусЧитательМетри
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Resource Attributes]
       not_found → partial
       Текст: To convert OTLP resource attributes to Prometheus labels, string Attribute values are converted dire
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1176-1194,1320-1349,1398-1433
       Было: Атрибуты ресурса в лейблы Prometheus не конвертируются вовсе: нет ни target_info, ни опции копирован
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Summaries]
       not_found → found
       Текст: An OpenTelemetry Summary MUST be converted to a Prometheus Summary as follows:
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:517-519,651-669,763-772
       Было: Конвертации OTel Summary нет: в SDK нет типа Summary (ОтелТипМетрики: sum, gauge, histogram, exponen
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Summaries]
       not_found → found
       Текст: The `quantile` label value MUST be the stringified floating point value of each quantile (between 0.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:763-772,782-796; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:275-329
       Было: Лейбл quantile не формируется: конвертации OTel Summary в Prometheus Summary нет (см. предыдущее тре
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Exporter / Client Libraries]
       partial → found
       Текст: If a Prometheus client library is used, the OpenTelemetry Prometheus Exporter SHOULD be modeled as a
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:141-169,207-209; oscript_modules/prometheus/src/Классы/CollectorRegistry.os:3-7,22,50-65
       Было: Клиентская библиотека используется (неофициальная prometheus); её модель коллектора - объект с метод
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Exporter / Default Aggregation]
       not_found → found
       Текст: A Prometheus Exporter SHOULD support a configuration option to set the MetricReader default `aggrega
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:301-328; src/Метрики/Модули/ОтелПотокиМетрик.os:415-443
       Было: У ОтелПрометеусЧитательМетрик нет опции для задания агрегации по умолчанию в зависимости от вида инс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Exporter / Resource Attributes as Metric Labels]
       not_found → found
       Текст: The configuration SHOULD allow the user to select resource attributes to include or exclude.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:221-227,1176-1252
       Было: Опциональная (MAY) настройка добавления атрибутов ресурса в лейблы метрик (resource_constant_labels)
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Exporter / Version and Format]
       partial → found
       Текст: Regardless of whether a Prometheus client library is used, the Prometheus Exporter MUST support vers
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:95-110; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:6-8,342-399
       Было: Text format 0.0.4 поддерживается: СобратьВТексте() (стр. 63-69) сериализует семейства через Promethe
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Global Propagators]
       not_found → found
       Текст: The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise.
       Код: src/Ядро/Модули/ОтелГлобальный.os:215-227 (ПолучитьПропагаторы), 272-287 (ПолучитьИлиСоздатьПропагаторыПоУмолчанию возвращает Новый ОтелНоопПропагатор())
       Было: По умолчанию API использует не no-op, а предконфигурированный composite W3C Trace Context + W3C Bagg
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / TextMap Propagator]
       partial → found
       Текст: In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters tha
       Код: src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:57-103 (КлючВалиден - RFC 9110 tchar; ЗначениеВалидно - VCHAR/SP/HTAB)
       Было: Проверка US-ASCII по RFC 9110 реализована только в сеттере по умолчанию: ОтелСеттерТекстовойКарты.Ус
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / W3C Trace Context Requirements]
       partial → found
       Текст: A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP heade
       Код: src/Пропагация/Классы/ОтелW3CПропагатор.os:99-167; src/Трассировка/Классы/ОтелСостояниеТрассировки.os:333-411
       Было: traceparent разбирается и валидируется полностью по Level 2 (ОтелW3CПропагатор.Извлечь, стр. 99-173)
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Create]
       partial → found
       Текст: The interface MUST provide a way to create a new resource.
       Код: src/Ядро/Классы/ОтелРесурс.os:102-107; src/Ядро/Классы/ОтелПостроительРесурса.os:77-83
       Было: Способы создания ресурса есть, но нет операции Create с параметрами (Attributes, schema_url): констр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / SDK-provided resource attributes]
       partial → found
       Текст: The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes
       Код: src/Ядро/Классы/ОтелРесурс.os:110-114 (ЗаполнитьАтрибутыПоУмолчанию); src/Ядро/Модули/ОтелУтилиты.os:476-495,531-549 (ВерсияSDK, ВерсияПакета: packagedef, в установленном пакете - opm-metadata.xml)
       Было: Ресурс по умолчанию (Новый ОтелРесурс() -> ЗаполнитьАтрибутыПоУмолчанию(), ОтелРесурс.os:108-112) со
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       partial → found
       Текст: If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.
       Код: src/Трассировка/Классы/ОтелНезаписывающийСпан.os:275-284
       Было: Для неявного текущего контекста без спана (ОтелТрассировщик.НачатьСпан) и для корневого спана (Начат
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Concurrency requirements]
       partial → found
       Текст: Span - all methods MUST be documented that implementations need to be safe for concurrent use by def
       Код: src/Трассировка/Классы/ОтелСпан.os:5-6; :38-44,528-550 (Блокировка, АтомарноеБулево)
       Было: Doc-комментарий класса (ОтелСпан.os:5-6) заявляет, что все публичные методы Span безопасны для парал
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Concurrency requirements]
       partial → found
       Текст: Event - Events are immutable and MUST be safe for concurrent use by default.
       Код: src/Трассировка/Классы/ОтелСобытиеСпана.os:3
       Было: ОтелСобытиеСпана не имеет экспортных сеттеров (поверхностная иммутабельность, комментарий ОтелСобыти
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Concurrency requirements]
       partial → found
       Текст: Link - Links are immutable and SHOULD be safe for concurrent use by default.
       Код: src/Трассировка/Классы/ОтелЛинк.os:1-13
       Было: ОтелЛинк имеет только геттеры, но атрибуты хранит по ссылке на изменяемый ОтелАтрибуты вызывающего: 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       partial → found
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Код: src/Трассировка/Классы/ОтелСпан.os:528-550
       Было: Сам ОтелСпан.Завершить() не выполняет I/O: фиксирует время окончания, проходит lock-free CAS-guard и
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       partial → found
       Текст: Any locking used needs be minimized and SHOULD be removed entirely if possible.
       Код: src/Трассировка/Классы/ОтелСпан.os:543-546
       Было: В самом ОтелСпан.Завершить() блокировки заменены lock-free CAS (АтомарноеБулево.СравнитьИУстановить)
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       partial → found
       Текст: The semantic parent of the Span MUST be determined according to the rules described in Determining t
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:167-187 (НачатьСпанВКонтексте: Родитель = ОтелКонтекст.СпанИзКонтекста(Контекст))
       Было: По правилам Determining the Parent Span from a Context: если в Context есть Span, он становится роди
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / TracerProvider]
       partial → found
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`.
       Код: src/Ядро/Модули/ОтелГлобальный.os:119-137
       Было: Глобальный реестр ОтелГлобальный хранит только SDK целиком: регистрация через ОтелГлобальный.Установ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       n_a → partial
       Текст: If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possib
       Код: src/Трассировка/Классы/ОтелНезаписывающийСпан.os:260-267
       Было: OneScript не поддерживает internal/package-private модификаторы (в т.ч. видимость классов) и приватн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Batching processor]
       partial → found
       Текст: The processor SHOULD export a batch when any of the following happens AND the previous export call h
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69 (автозапуск фонового экспорта при первом элементе, стр. 66-68), 168-174 (переинтервал после завершения предыдущего экспорта), 351-368 (триггер по интервалу и по полному пакету), 79-81 (триггер ForceFlush)
       Было: Триггеры реализованы: периодический экспорт (ПериодическийЭкспорт, стр. 162-170: Приостановить(Интер
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Concurrency requirements]
       partial → found
       Текст: Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrentl
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-115 (ПолучитьТрассировщик, double-checked locking через БлокировкаТрассировщиков),145-147 (СброситьБуфер),158-165 (Закрыть, АтомарноеБулево.СравнитьИУстановить)
       Было: ForceFlush и Shutdown безопасны: Закрыть() использует CAS на АтомарноеБулево (стр. 147), СброситьБуф
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Concurrency requirements]
       partial → found
       Текст: Span processor - all methods MUST be safe to be called concurrently.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:55-74,102-110; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69,95-114,231-252,297-328; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:77-97
       Было: Синхронизация есть во всех процессорах: ОтелПростойПроцессорСпанов (Export под БлокировкаЭкспорта, C
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over f
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-252 (таймаут проверяется перед каждым пакетом, остаток передаётся и в захват БлокировкаЭкспорта, и в вызов Export); src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:108-127 (остаток общего таймаута делится между процессорами в цепочке)
       Было: ЭкспортироватьВсеПакеты проверяет истечение таймаута перед каждым пакетом и возвращает Таймаут (стр.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85-90; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217; src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-38
       Было: СброситьБуфер возвращает ОтелРезультатЭкспорта (Успех/Ошибка/Таймаут; Успешно()/ИстекТаймаут()/Стату
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       partial → found
       Текст: If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine wh
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:373-384 (ФлагRandomДляНовыхИд - запрашивает у пользовательского ГенераторИд необязательный метод ФлагRandomДляНовыхИд() через Попытка/Исключение); src/Ядро/Модули/ОтелУтилиты.os:93-103 (тот же паттерн для генератора по умолчанию, явно комментирует 'Trace SDK §93 (SHOULD)')
       Было: Механизм есть: генератор, заданный через ОтелПостроительПровайдераТрассировки.УстановитьГенераторИд(
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       partial → found
       Текст: Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all genera
       Код: src/Ядро/Модули/ОтелУтилиты.os:93-103; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:373-380; src/Трассировка/Классы/ОтелТрассировщик.os:283-289
       Было: Механизм самоидентификации реализован через необязательный метод пользовательского генератора ФлагRa
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ProbabilitySampler]
       partial → found
       Текст: The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`.
       Код: src/Трассировка/Модули/ОтелСэмплер.os:253-283 (ВычислитьРешение, ветка ПоДолеТрассировок),370-394 (СэмплироватьПоДоле - сигнатура не принимает РодительСэмплирован/ЕстьРодитель, в отличие от НаОсновеРодителя)
       Было: Отдельного ProbabilitySampler нет: grep Probability по src/ находит только комментарии, в ОтелАвтоко
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / SDK Span creation]
       partial → found
       Текст: When asked to create a Span, the SDK MUST act as if doing the following in order:
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:213-249 (НачатьСпанSdk: TraceId разрешается из валидного родителя или генерируется ДО вызова сэмплера; НовыйИдСпана генерируется независимо от решения сэмплера - до факта вызова ПрошелСэмплирование и без использования его результата; ПрошелСэмплирование вызывает ОтелСэмплер.ДолженСэмплировать; итоговый спан создается по решению - ОтелСпан для RECORD_ONLY/RECORD_AND_SAMPLE, ОтелНезаписывающийСпан для DROP)
       Было: Основной алгоритм в ОтелТрассировщик.НачатьСпанSdk (стр. 190-226) соответствует спеке: TraceId берёт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165,198-201; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,215-236; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40
       Было: Закрыть(ТаймаутМс) возвращает ОтелРезультатЗакрытия (Успешно()/ИстекТаймаут()/Описание()), ЗакрытьАс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165,397-399; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,192-202
       Было: Закрыть() вызывает Процессор.Закрыть() для каждого процессора из снимка (стр. 154-165), но вызов для
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:102-109 (returns ОтелРезультатЗакрытия via ЗакрытьЭкспортерПослеЭкспорта); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114 (aggregates real export/close outcomes via РезультатФинальногоЭкспорта + ВызватьВПределахСрока)
       Было: Закрыть возвращает ОтелРезультатЗакрытия (Успешно()/ИстекТаймаут()/Описание()); пакетный процессор р
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` MUST include the effects of `ForceFlush`.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:109 -> src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121,89-95 (СброситьБуфер, затем Закрыть); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:105 вызывает тот же ЭкспортироватьВсеПакеты, что и СброситьБуфер на строке 80, перед Экспортер.Закрыть на строке 111
       Было: Для пакетного процессора выполнено: ОтелБазовыйПакетныйПроцессор.Закрыть (стр. 96-97) останавливает 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Span Limits]
       partial → found
       Текст: Span attributes MUST adhere to the common rules of attribute limits.
       Код: src/Трассировка/Классы/ОтелСпан.os:330-345
       Было: Лимит количества атрибутов (новый ключ сверх МаксАтрибутов отбрасывается с увеличением ОтброшенныхАт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceIdRatioBased]
       partial → found
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Код: src/Трассировка/Модули/ОтелСэмплер.os:126 (те же 6 знаков после запятой дают разрешение 0.000001 - достаточно для различения сэмплеров с разными долями)
       Было: Точность жёстко фиксирована форматом «ЧДЦ=6; ЧРД=.; ЧН=0; ЧГ=» (всегда 6 знаков после точки): доли, 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceIdRatioBased]
       partial → found
       Текст: To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the s
       Код: src/Трассировка/Модули/ОтелСэмплер.os:388-393 (ОтелУтилиты.ИзШестнадцатеричнойСтроки(Прав(ИдТрассировки, ДлинаЗначенияСлучайности)) - детерминированное значение из правых 56 бит TraceId, тот же подход, что и в эталонных SDK, использующих часть байт TraceId как хэш-значение),449-455 (РешениеПоСлучайности - пороговое сравнение)
       Было: Детерминированная функция TraceId (правые 7 байт = 56 бит как значение случайности R, решение R >= (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (7) - агент нашёл дополнительные:

     [Env Vars] SHOULD NOT found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD NOT found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD NOT found: It SHOULD NOT be supported by new implementations.
     [Logs Api] MUST NOT found: For each optional parameter, the API MUST be structured to accept it, but MUST N
     [Logs Sdk] MUST found: `Enabled` MUST return `false` when either: there are no registered `LogRecordPro
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including: the value, the complet
     [Trace Api] MUST found: The `Tracer` MUST provide functions to: * Create a new `Span` (see the section o

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (7) - были раньше, теперь нет:

     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Logs Api] MUST found: For each required parameter, the API MUST be structured to obligate a user to pr
     [Logs Sdk] MUST found: `Enabled` MUST return `false` when either:
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including:
     [Trace Api] MUST found: The `Tracer` MUST provide functions to:

  Итого изменений: 216
    Понижений: 38, Повышений: 164, Боковых: 0
    Новых req: 7, Пропущенных req: 7
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
