# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             753    771 +   18 ✅
  partial            18     13    -5
  not_found           6      1    -5
  n_a                92     83    -9
  Всего             869    868    -1

  🔴 ПОНИЖЕНИЕ СТАТУСА (8) - требует перепроверки:

     [Logs Sdk / Enabled]
       found → partial
       Текст: Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller.
       Расположение: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:19-42, src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101, src/Логирование/Классы/ОтелЛоггер.os:72-90 → src/Логирование/Классы/ОтелЛоггер.os:57-84; src/Логирование/Классы/ОтелЛоггер.os:147-161; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101
       Пояснение: Внешний вызывающий защищён: ОтелЛоггер.Включен и ОтелКомпозитныйПроцессорЛогов.Включен принимают параметры как Знач, контекст передаётся как Фиксирова
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:451-470; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:192-202 → src/Метрики/Классы/ОтелПровайдерМетрик.os:176-178,229-234,354-365; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399-417 (БлокировкаСбора.Захватить(срок)), 419-453 (сбор без срока), 468-487 (экспорт в пределах срока); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:68-70; src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:142-143
       Пояснение: СброситьБуфер(ТаймаутМс) / ПринудительноВыгрузитьСРезультатом(ТаймаутМс) принимают таймаут, передают читателям оставшееся время, ограничивают сроком о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Расположение: src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:108-146 (ВызватьСТаймаутом) → src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165 (ВызватьСТаймаутом: ФоновыеЗадания.Выполнить + ОжидатьЗавершения(ТаймаутМс)), 182-192 (ЗаданиеВыполняется); src/Метрики/Классы/ОтелМетр.os:406-416,1035 (таймаут callback-ов, по умолчанию 30000 мс)
       Пояснение: Таймаут реализован как soft-timeout: ОтелИсполнительОбратныхВызовов.ВызватьСТаймаутом запускает callback через ФоновыеЗадания.Выполнить и ждет Задание
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: The implementation MUST complete the execution of all callbacks for a given instrument before starti
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:389-409 (ВызватьCallbackи - синхронный цикл); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:33-35,386-398 (БлокировкаСбора сериализует сборы) → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399-417 (БлокировкаСбора сериализует сборы); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:159-169 (БлокировкаСбора); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:394-414 (ВызватьCallbackи - синхронный цикл); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165
       Пояснение: В штатном режиме выполняется: сборы одного читателя сериализованы (БлокировкаСбора в ОтелПериодическийЧитательМетрик и ОтелПрометеусЧитательМетрик), c
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / User Agent]
       found → partial
       Текст: OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the export
       Расположение: src/Ядро/Модули/ОтелУтилиты.os:508-519 (UserAgentЭкспортераOtlp -> "OTel-OTLP-Exporter-OneScript/<версия>"); src/Экспорт/Классы/ОтелHttpТранспорт.os:368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:300 → src/Ядро/Модули/ОтелУтилиты.os:487-498 (UserAgentЭкспортераOtlp: OTel-OTLP-Exporter-OneScript/<версия>); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302
       Пояснение: HTTP-транспорт отправляет заголовок User-Agent: OTel-OTLP-Exporter-OneScript/<версия> (экспортер, язык и версия; подтверждено перехватом запроса). gRP
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / User Agent]
       found → partial
       Текст: The resulting User-Agent SHOULD include the exporter’s default User-Agent string.
       Расположение: src/Ядро/Модули/ОтелУтилиты.os:508-519 (ИдентификаторПродукта + " " + СтандартныйUserAgent); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302 (СформироватьМетаданные) → src/Ядро/Модули/ОтелУтилиты.os:487-498 (ИдентификаторПродукта + пробел + СтандартныйUserAgent); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302
       Пояснение: Для HTTP итоговый заголовок содержит стандартную строку после идентификатора продукта (перехвачено: MyDistribution/1.2.3 OTel-OTLP-Exporter-OneScript/
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Link]
       found → partial
       Текст: The API documentation MUST state that adding links at span creation is preferred to calling `AddLink
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:91-93 → src/Трассировка/Классы/ОтелПостроительСпана.os:85-87; src/Трассировка/Классы/ОтелСпан.os:420-429
       Пояснение: Предпочтение задокументировано лишь частично: комментарий ОтелПостроительСпана.ДобавитьЛинк (стр. 85-87) говорит, что линки предпочтительно задавать п
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceIdRatioBased]
       found → partial
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:126 (те же 6 знаков после запятой дают разрешение 0.000001 - достаточно для различения сэмплеров с разными долями) → src/Трассировка/Модули/ОтелСэмплер.os:126
       Пояснение: Доля выводится с фиксированной точностью 6 знаков после запятой: Формат(Доля, "ЧДЦ=6; ЧРД=.; ЧН=0; ЧГ="). При этом сама доля принимается и применяется
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (25) - требует перепроверки:

     [Metrics Sdk / Exemplar]
       partial → found
       Текст: If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling.
       Код: src/Метрики/Классы/ОтелХранилищеМетрики.os:54-61,259-269,450-471; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:357-382
       Было: Оверхед на горячем пути (per-measurement) действительно устраняется: ЗахватитьЭкземпляр = ЕстьРезерв
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: This function SHOULD be obtained from the `exporter`.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302-314 (АгрегацияПоУмолчанию: без агрегации, заданной читателю, вызывается Экспортер.АгрегацияПоУмолчанию(ВидИнструмента)), 759-765 (ЭкспортерЗадаетАгрегацию - наличие метода у экспортера); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:144-159 (АгрегацияПоУмолчанию OTLP-экспортера); src/Метрики/Модули/ОтелПотокиМетрик.os:412-440 (поток берет агрегацию читателя по виду инструмента); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1589,1602
       Было: Речь о default aggregation: селектор агрегации по умолчанию по виду инструмента задаётся самим читат
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → found
       Текст: If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as 
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:18-26; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:354-363,656,706-711; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:405,435-440
       Было: Функция Произвести() (ИнтерфейсПродюсерМетрик.os:33) не содержит параметра ресурса, хотя возвращаемы
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       partial → found
       Текст: If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:15-16; src/Метрики/Классы/ОтелДанныеМетрики.os:43-50,208-218; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:449-461
       Было: ОтелДанныеМетрики принимает ОбластьИнструментирования вторым обязательным параметром конструктора (с
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       n_a → found
       Текст: However, if they are already implemented, they SHOULD continue to be supported as they were part of 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1365-1370 (поддерживаются актуальные OTEL_EXPORTER_OTLP_[<SIGNAL>_]INSECURE; устаревшие OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE в истории src/ никогда не реализовывались, поэтому сохранять нечего)
       Было: Требование условное ("if they are already implemented"): устаревшие переменные OTEL_EXPORTER_OTLP_SP
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exemplar Conversion]
       n_a → found
       Текст: When an exemplar is converted per the metric-type-specific sections above, the OpenTelemetry Exempla
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:743,776,829-833,909-935; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:581-592,692-694,721-731
       Было: Условное требование (если протокол поддерживает exemplars). Читатель выдает только обязательный text
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exemplar Conversion]
       n_a → found
       Текст: If present, the OpenTelemetry Exemplar’s Trace ID and Span ID MUST be added as Exemplar labels using
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:912-920,924-926
       Было: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только об
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exemplar Conversion]
       n_a → found
       Текст: These labels MUST take precedence over labels from `filtered_attributes` in cases where there is a k
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:911,918,924-926
       Было: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только об
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exemplar Conversion]
       n_a → found
       Текст: Timestamps MUST be added as timestamps on the Prometheus exemplar.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:930-933,976-978; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:725-728
       Было: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только об
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Exemplar Conversion]
       n_a → found
       Текст: `filtered_attributes` MUST be added as labels on the Prometheus exemplar, unless they would exceed t
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:910-911,921-923,945-974
       Было: Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только об
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Histograms]
       partial → found
       Текст: OpenTelemetry Histograms with Delta aggregation temporality MAY be aggregated into a Cumulative aggr
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:330-332,596-599,669-681
       Было: Для метрик SDK временная агрегация читателя всегда кумулятивная (ВременнаяАгрегацияДляВида, стр. 338
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Histograms as Prometheus Histograms]
       not_found → found
       Текст: If set, `StartTimeUnixNano` SHOULD be transformed into Prometheus `StartTime`, following the appropr
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:780-781,816-821; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:595-599,705-711
       Было: startTimeUnixNano точки гистограммы не используется: ДобавитьСэмплыГистограммы (ОтелПрометеусЧитател
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Histograms as Prometheus Histograms]
       n_a → found
       Текст: If the Prometheus protocol only supports a single exemplar per-bucket, the latest exemplar that fall
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:768-776,858-887
       Было: Условное требование для протокола с одним exemplar на бакет (OpenMetrics). Читатель выдает только об
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Metric Attributes]
       partial → found
       Текст: String Attribute values are converted directly to Metric Attributes, and non-string Attribute values
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1652-1669,1680-1766
       Было: Строковые значения переносятся как есть, число, булево и массив - в JSON-представление (42 -> '42', 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Metric Attributes]
       partial → found
       Текст: In such cases, the values MUST be concatenated together, separated by `;`, and ordered by the lexico
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1376-1381,1537-1548,1559-1601,1609-1639
       Было: Значения атрибутов, чьи ключи дали одно имя лейбла, склеиваются через ';' в порядке исходных ключей 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Metric Metadata]
       partial → found
       Текст: If dropping a comment or metric points, the exporter SHOULD warn the user through error logging.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:608-617,640-653,677-679,1043-1064,1120-1121,1198-1199
       Было: Во всех штатных путях отбрасывания пишется предупреждение (Лог.Предупреждение): конфликт TYPE - метр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Metric Metadata]
       not_found → found
       Текст: The resulting unit SHOULD be added to the metric as UNIT metadata.
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:699,713; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:553-556
       Было: UNIT-метаданные не выводятся. Семейство, которое строит СемействоМетрики (ОтелПрометеусЧитательМетри
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Sums]
       partial → found
       Текст: If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of 
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:505-506,515,1281-1285
       Было: Имя без суффикса _total получает его, а имя с одним суффиксом _total остается без изменений (ИменаМе
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Sums]
       not_found → found
       Текст: Monotonic Sum metric points with `StartTimeUnixNano` SHOULD transform `StartTimeUnixNano` into Prome
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:741-744,816-821; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:595-599,705-711
       Было: startTimeUnixNano точек читателем не используется: ОтелПрометеусЧитательМетрик.os не обращается к эт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Sums]
       n_a → found
       Текст: If Sum is converted to a Prometheus Counter, then `Exemplars` MUST be converted as described in the 
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:741-744,829-833,909-935; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:589-592,692-694,721-731
       Было: Условное требование: exemplars конвертируются только для протокола, который их поддерживает (Exempla
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Compatibility / Sums]
       n_a → found
       Текст: If the Prometheus protocol only supports a single exemplar on the Counter sample, the latest exempla
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:743,843-845,858-874
       Было: Условное требование для протокола с одним exemplar на сэмпл счетчика (OpenMetrics). Читатель выдает 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attrib
       Код: src/Ядро/Модули/ОтелУтилиты.os:541-544; src/Ядро/Классы/ОтелРесурс.os:143-158
       Было: АдресСхемыСемантическихСоглашений присваивается ресурсу безусловно в начале Обнаружить() во всех трё
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       partial → found
       Текст: This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`.
       Код: src/Трассировка/Классы/ОтелПостроительСпана.os:37-41 (УстановитьРодителя(Context)); src/Трассировка/Классы/ОтелТрассировщик.os:121-126,158-166; src/Ядро/Модули/ОтелКонтекст.os:139-144
       Было: ОтелПостроительСпана.УстановитьРодителя() (ОтелПостроительСпана.os:37-47) корректно принимает только
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had al
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217 (экспорт буфера до опустошения до возврата), 231-252 (ожидание экспорта, начатого фоновым заданием, через БлокировкаЭкспорта); src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:79-84 -> src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120 (дожидается экспорта в другом потоке)
       Было: Пакетный процессор корректно ждёт: ЭкспортироватьПакет безусловно захватывает БлокировкаЭкспорта пер
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:150-157; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,159-177,192-202; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:96-104
       Было: TracerProvider.Закрыть(ТаймаутМс) принимает таймаут и корректно урезает остаток времени для каждого 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  📋 Новые секции (15):
     + [Metrics Api] Add (13 req)
     + [Metrics Api] Asynchronous Instrument API (27 req)
     + [Metrics Api] Record (13 req)
     + [Metrics Api] Synchronous Instrument API (12 req)
     + [Metrics Sdk] Explicit Bucket Histogram Aggregation (1 req)
     + [Metrics Sdk] Export(batch) (4 req)
     + [Metrics Sdk] Handle all normal values (1 req)
     + [Metrics Sdk] Maintain the ideal scale (1 req)
     + [Metrics Sdk] Support a minimum and maximum scale (1 req)
     + [Metrics Sdk] Use the maximum scale for single measurements (1 req)
     + [Propagators] Get (2 req)
     + [Propagators] GetAll (4 req)
     + [Propagators] Keys (1 req)
     + [Propagators] Set (2 req)
     + [Trace Sdk] Requirements for `TraceIdRatioBased` sampler algorithm (3 req)

  📋 Исчезнувшие секции (7):
     - [Metrics Api] Counter operations (8 req)
     - [Metrics Api] Gauge operations (6 req)
     - [Metrics Api] Histogram operations (7 req)
     - [Metrics Api] Synchronous and Asynchronous instruments (39 req)
     - [Metrics Api] UpDownCounter operations (5 req)
     - [Propagators] Getter argument (7 req)
     - [Propagators] Setter argument (2 req)

  ➕ НОВЫЕ ТРЕБОВАНИЯ (11) - агент нашёл дополнительные:

     [Logs Sdk] MUST NOT found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST found: `Enabled` MUST return `false` when either:
     [Metrics Sdk] SHOULD found: This is a hint to ensure that the export of any `Metrics` the exporter has recei
     [Metrics Sdk] SHOULD found: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, f
     [Metrics Sdk] SHOULD n_a: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, su
     [Metrics Sdk] SHOULD found: `ForceFlush` SHOULD complete or abort within some timeout.
     [Metrics Sdk] MUST found: `Produce` MUST return a batch of Metric Points, filtered by the optional `metric
     [Metrics Sdk] SHOULD found: Shutdown SHOULD be called only once for each `MetricExporter` instance.
     [Metrics Sdk] SHOULD NOT found: `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data 
     [Resource Sdk] MUST found: If either resource contains `Entities` then merge behavior with Entities MUST be
     [Trace Sdk] MUST found: `Enabled` MUST return `false` when either:

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (24) - были раньше, теперь нет:

     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST found: `Enabled` MUST return `false` when either: there are no registered `LogRecordPro
     [Metrics Sdk] SHOULD found: SDKs SHOULD use the default value when boundaries are not explicitly provided, u
     [Metrics Sdk] SHOULD NOT n_a: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and 
     [Metrics Sdk] MUST found: The implementation MUST maintain reasonable minimum and maximum scale parameters
     [Metrics Sdk] SHOULD found: When the histogram contains not more than one value in either of the positive or
     [Metrics Sdk] SHOULD found: Implementations SHOULD adjust the histogram scale as necessary to maintain the b
     [Metrics Sdk] MUST found: The SDK MUST provide a way for the exporter to get the Meter information (e.g. n
     [Metrics Sdk] MUST NOT found: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit aft
     [Metrics Sdk] MUST found: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit aft
     [Metrics Sdk] SHOULD NOT found: The default SDK SHOULD NOT implement retry logic, as the required logic is likel
     [Metrics Sdk] SHOULD found: This is a hint to ensure that the export of any `Metrics` the exporter has recei
     [Metrics Sdk] SHOULD found: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, f
     [Metrics Sdk] SHOULD n_a: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, su
     [Metrics Sdk] SHOULD found: `ForceFlush` SHOULD complete or abort within some timeout.
     [Metrics Sdk] SHOULD found: Shutdown SHOULD be called only once for each `MetricExporter` instance.
     [Metrics Sdk] SHOULD NOT found: `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data 
     [Metrics Sdk] MUST found: `Produce` MUST return a batch of Metric Points.
     [Resource Sdk] MUST found: [...] otherwise merge behavior without Entities MUST be used.
     [Trace Sdk] MUST not_found: `Enabled` MUST return `false` when [...] there are no registered `SpanProcessors
     ... и ещё 4

  Итого изменений: 68
    Понижений: 8, Повышений: 25, Боковых: 0
    Новых req: 11, Пропущенных req: 24
    Новых секций: 15, Исчезнувших секций: 7

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
