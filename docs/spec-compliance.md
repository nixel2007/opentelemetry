# Анализ соответствия спецификации OpenTelemetry v1.61.0

> **Версия спецификации**: [v1.61.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-09-28
> **Состояние кода**: статусы и ссылки на строки соответствуют коммиту `60a203e`; исправления после него в отчете не отражены
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Stable + universal keywords | 833 |
| Conditional keywords | 36 |
| Найдено требований (Stable universal) | 777 |
| ✅ Реализовано (found) | 753 (96.9%) |
| ⚠️ Частично (partial) | 18 (2.3%) |
| ❌ Не реализовано (not_found) | 6 (0.8%) |
| ➖ Неприменимо (n_a) | 56 |
| **MUST/MUST NOT found** | 466/474 (98.3%) |
| **SHOULD/SHOULD NOT found** | 287/303 (94.7%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 0 | 0 | 1 | 14 | 100.0% |
| Baggage Api | 17 | 0 | 0 | 0 | 17 | 100.0% |
| Resource Sdk | 20 | 1 | 0 | 0 | 21 | 95.2% |
| Trace Api | 108 | 2 | 0 | 16 | 110 | 98.2% |
| Trace Sdk | 83 | 2 | 1 | 4 | 86 | 96.5% |
| Logs Api | 22 | 0 | 0 | 0 | 22 | 100.0% |
| Logs Sdk | 73 | 0 | 0 | 3 | 73 | 100.0% |
| Metrics Api | 92 | 1 | 0 | 8 | 93 | 98.9% |
| Metrics Sdk | 198 | 6 | 1 | 4 | 205 | 96.6% |
| Otlp Exporter | 23 | 1 | 0 | 1 | 24 | 95.8% |
| Propagators | 29 | 0 | 0 | 11 | 29 | 100.0% |
| Env Vars | 24 | 0 | 0 | 0 | 24 | 100.0% |
| Prometheus Compatibility | 38 | 5 | 3 | 8 | 46 | 82.6% |
| Prometheus Exporter | 12 | 0 | 1 | 0 | 13 | 92.3% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`.  
  ОтелПостроительСпана.УстановитьРодителя() (ОтелПостроительСпана.os:37-47) корректно принимает только Context (Соответствие/ФиксированноеСоответствие) и выбрасывает исключение при попытке передать иной тип. Но публичный метод ОтелТрассировщик.НачатьДочернийСпан(ИмяСпана, РодительскийКонтекст, ...) (ОтелТрассировщик.os:113-128) принимает параметр РодительскийКонтекст именно как ОтелСпан или ОтелКонтекстСпана напрямую (проверка ТипЗнч на 'ОтелКонтекстСпана', иначе вызывается .КонтекстСпана() как у Span), а не как полный Context - это отдельный публичный путь создания дочернего спана, нарушающий требование.

- ⚠️ **[Metrics Sdk]** [MUST NOT] If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling.  
  Оверхед на горячем пути (per-measurement) действительно устраняется: ЗахватитьЭкземпляр = ЕстьРезервуар() И ОтелФильтрЭкземпляров.ДолженЗахватить(...) вычисляется до блокировки, и при ФильтрЭкземпляров=ВсегдаВыключен() ДолженЗахватить сразу возвращает Ложь (ОтелФильтрЭкземпляров.os:69-71), так что ПредложитьЭкземпляр (аллокация структуры экземпляра, вычисление filteredAttributes, RNG) не вызывается. Но per-series оверхед не устранён: ФабрикаРезервуаров по умолчанию не становится Неопределено при выключенном фильтре, поэтому НоваяСерия (ОтелХранилищеМетрики.os:321-328) всё равно создаёт полноценный объект ОтелРезервуарЭкземпляров (с СинхронизированнаяКарта x2, ГенераторСлучайныхЧисел, БлокировкаРесурса) для каждой новой серии атрибутов, даже если ни один exemplar никогда не будет захвачен. Единственный способ полностью убрать этот оверхед - явно задать ОтелФабрикаNoopРезервуаров на View, что не происходит автоматически при ФильтрЭкземпляров=ВсегдаВыключен().

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter.  
  Большинство опций (Endpoint, Insecure, Headers, Compression, Timeout, Protocol, Max Request/Response Size, Certificate File для gRPC) полностью настраиваемы и применяются. Но Client key file и Client certificate file (mTLS) принимаются как поля ОтелНастройкиTls, однако не применяются ни в ОтелHttpТранспорт (библиотека 1connector не поддерживает клиентский сертификат - предупреждение в ПриСозданииОбъекта, строки 379-383), ни в ОтелGrpcТранспорт (OPI_GRPC/tonic не поддерживает mTLS - предупреждение в ПроверитьНастройкиTls, строки 542-552); Certificate File (root CA) также не применяется в HTTP-транспорте (только в gRPC). Часть заявленных опций конфигурации принимается, но не оказывает эффекта.

- ⚠️ **[Prometheus Compatibility]** [MUST] If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged.  
  Имя без суффикса _total получает его, а имя с одним суффиксом _total остается без изменений (ИменаМетрики, стр. 467-478; БазовоеИмя, стр. 1060-1072). Но имя, оканчивающееся на _total дважды, теряет один суффикс: БазовоеИмя отрезает _total у счетчика (стр. 1063-1066), ИменаМетрики отрезает его повторно (БезСуффикса, стр. 475) и добавляет один _total. Проверено запуском: счетчик requests_total_total выдается как requests_total (# TYPE requests_total counter), хотя имя уже оканчивается на _total и по спецификации должно остаться без изменений.

- ⚠️ **[Prometheus Compatibility]** [MUST] OpenTelemetry Histograms with Delta aggregation temporality MAY be aggregated into a Cumulative aggregation temporality and follow the logic below, or MUST be dropped.  
  Для метрик SDK временная агрегация читателя всегда кумулятивная (ВременнаяАгрегацияДляВида, стр. 338-340; ОтелПотокиМетрик.ВременнаяАгрегацияЧитателя, ОтелПотокиМетрик.os:162-175): SDK агрегирует гистограммы в кумулятивную сам, дельта-гистограммы инструментов в выдачу не попадают. Но метрики внешних продюсеров (ДобавитьПродюсер) читатель по временной агрегации не проверяет: ФильтрДляПродюсера (стр. 395-406) лишь передает предпочтение кумулятивной агрегации (фильтр с уже заданным предпочтением, в том числе дельта, передается как есть), а КонвертироватьИДобавить (стр. 609-640) не смотрит на ОтелДанныеМетрики.ВременнаяАгрегация(). Проверено запуском: гистограмма продюсера с временной агрегацией Дельта выводится как обычная кумулятивная Prometheus histogram - ее не агрегируют в кумулятивную и не отбрасывают (то же для дельта-суммы).

- ⚠️ **[Prometheus Compatibility]** [MUST] String Attribute values are converted directly to Metric Attributes, and non-string Attribute values MUST be converted to string attributes following the attribute specification.  
  Строковые значения переносятся как есть, число, булево и массив - в JSON-представление (42 -> '42', true -> 'true', 2.5 -> '2.5', [1,2] и массив строк - в JSON-массив), как требует раздел AnyValue representation for non-OTLP protocols. Но ЗначениеВJSON (ОтелПрометеусЧитательМетрик.os:1409-1433) не знает kvlistValue (Соответствие/Структура), bytesValue (ДвоичныеДанные) и пустое значение: они дают 'null' вместо JSON-объекта, base64-строки и пустой строки (проверено запуском: map='null', bytes='null', empty='null'; так же вложенные в массив map/bytes). Спецификация (v1.61) допускает такие значения атрибутов. NaN/Infinity невозможны (Число = Decimal).

- ⚠️ **[Prometheus Compatibility]** [MUST] In such cases, the values MUST be concatenated together, separated by `;`, and ordered by the lexicographical order of the original keys.  
  Значения атрибутов, чьи ключи дали одно имя лейбла, склеиваются через ';' в порядке исходных ключей (ЛейблыИзАтрибутовOtlp, стр. 1320-1349, ВставитьПоПорядкуКлюча, стр. 1357-1363; проверено запуском: a.b, a:b и a_b дали a_b='first;third;second'). Но коллизии с лейблами, которые добавляет сама спецификация (в тексте пример - otel_scope_name), не склеиваются: ЛейблыТочки (стр. 1154-1165) перезаписывает атрибут точки лейблом области (otel.scope.name='user' потерян, остался otel_scope_name='lib'), а атрибут точки с тем же именем, что и скопированный атрибут ресурса, вытесняет ресурсный (service.name='point-attr' без 'checkout').

- ❌ **[Trace Sdk]** [MUST] `Enabled` MUST return `false` when [...] there are no registered `SpanProcessors`.  
  Включен() трассировщика не проверяет зарегистрированные процессоры: делегирует в Провайдер.Включен() (ОтелПровайдерТрассировки.os:299-301), который возвращает признак SDK-режима, по умолчанию Истина независимо от числа процессоров (ОтелПровайдерТрассировки.os:520). У Logger такая проверка есть: «Если НЕ Провайдер.Процессор().ЕстьПроцессоры() Тогда Возврат Ложь» (ОтелЛоггер.os:82).

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will popula...  
  АдресСхемыСемантическихСоглашений присваивается ресурсу безусловно в начале Обнаружить() во всех трёх генерик-детекторах (host/process/cpu), до Попытки заполнения атрибутов. Если Попытка завершается исключением и ни один атрибут не установлен (детектор фактически не узнал ни одного известного атрибута), итоговый ресурс всё равно получает non-empty Schema URL вместо пустой строки, как требует SHOULD. Отдельного детектора-обёртки над OTEL_RESOURCE_ATTRIBUTES (пример из самой спеки - 'детектор, который читает атрибуты из окружения, не будет знать, какую Schema URL использовать') с явной пустой схемой тоже нет: эти атрибуты применяются напрямую в ОтелРесурс.ПрименитьАтрибутыИзОкружения (строки 326-341) без какой-либо работы со Schema URL.

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type).  
  Требуемая функция-обертка есть (ОтелСпаны.Обернуть/Невалидный возвращают объект с интерфейсом Span), и комментарии в коде прямо не рекомендуют прямое создание класса. Но сам тип ОтелНезаписывающийСпан зарегистрирован в lib.config как обычный публичный класс (см. lib.config:38) наравне с ОтелСпан и может быть создан напрямую (Новый ОтелНезаписывающийСпан(...)) из любого вызывающего кода. OneScript не поддерживает package-private/internal классы - только общий реестр классов в lib.config, поэтому техническое сокрытие типа не достигнуто, только рекомендация через документацию.

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  TracerProvider.Закрыть(ТаймаутМс) принимает таймаут и корректно урезает остаток времени для каждого процессора (ОтелРезультатыЗакрытия.ОставшеесяВремя), но для ОтелПакетныйПроцессорСпанов Закрыть сначала останавливает фоновое задание периодического экспорта через ОстановитьФоновыйЭкспорт → Обещание.Получить(ТаймаутМс) → Задание.ОжидатьЗавершения(Таймаут) (oscript_modules async). OneScript ФоновоеЗадание не поддерживает принудительную отмену (нет Прервать()/ОтменитьЗадание(), см. github.com/EvilBeaver/OneScript/issues/1672): по истечении таймаута вызывающий поток просто перестаёт ждать (исключение перехватывается, Лог.Отладка), а само фоновое задание продолжает работу. Это soft-timeout: Shutdown гарантированно возвращает управление в пределах бюджета времени, но не гарантирует физическую остановку фоновой активности.

- ⚠️ **[Trace Sdk]** [SHOULD] This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, pre...  
  Пакетный процессор корректно ждёт: ЭкспортироватьПакет безусловно захватывает БлокировкаЭкспорта перед каждой попыткой извлечения (стр. 231-234), поэтому конкурентный фоновый экспорт, уже начатый до вызова ForceFlush, дожидается своего завершения прежде, чем ForceFlush продолжит и вернёт управление. Но ОтелПростойПроцессорСпанов.СброситьБуфер (стр. 85-90) вызывает Экспортер.СброситьБуфер() напрямую, не захватывая БлокировкаЭкспорта, которую ПриЗавершении использует вокруг Экспортер.Экспортировать (стр. 62-73): если ПриЗавершении в другом потоке в этот момент ещё выполняет Export, конкурентный ForceFlush не дожидается его завершения перед возвратом. На практике для встроенного ОтелЭкспортерСпанов не проявляется, так как сам Export ограничен собственным таймаутом.

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Реализован только soft-timeout: SDK перестает ждать callback и отбрасывает результат по истечении таймаута, но платформа OneScript не позволяет прервать ФоновоеЗадание (нет Прервать()/ОтменитьЗадание(), см. https://github.com/EvilBeaver/OneScript/issues/1672) - зависший callback продолжает выполняться в фоне до собственного завершения.

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Закрыть принимает ТаймаутМс и распределяет оставшееся время между читателями. Читатель ждёт фоновое задание периодического сбора через Обещание.Получить(timeout) - это soft-timeout: при истечении ожидание прекращается и результат отбрасывается, но само ФоновоеЗадание не может быть принудительно прервано (OneScript не поддерживает Прервать()/ОтменитьЗадание(), см. EvilBeaver/OneScript#1672) и продолжает выполняться в фоне. Вызывающий получает управление вовремя, но полное завершение операции внутри таймаута не гарантировано.

- ⚠️ **[Metrics Sdk]** [SHOULD] This function SHOULD be obtained from the `exporter`.  
  Речь о default aggregation: селектор агрегации по умолчанию по виду инструмента задаётся самим читателем (ИнициализироватьСелекторАгрегации/УстановитьАгрегациюПоУмолчанию), а не запрашивается у экспортера. ИнтерфейсЭкспортерМетрик (src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os) не содержит метода получения агрегации по умолчанию - только temporality (ПолучитьВременнуюАгрегацию) действительно берётся из экспортера.

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  OneScript ФоновоеЗадание не поддерживает жёсткую отмену (только ОжидатьЗавершения(timeout), нет Прервать()/ОтменитьЗадание() - см. issue EvilBeaver/OneScript#1672). Закрыть() реализует soft-timeout: Обещание.Получить(ОставшееcяВремя) перестаёт ждать по истечении срока (перехватывается исключение, пишется debug-лог) и переходит к следующему шагу с оставшимся бюджетом времени, но само фоновое задание периодического сбора/экспорта не прерывается принудительно и может доработать в фоне. Вызывающий получает результат в срок, но операция не 'abort', а лишь перестаёт ожидаться.

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Аналогично Shutdown: ПринудительноВыгрузитьСРезультатом задействует Обещание.Получить(timeout) внутри СбросБуфер/СобратьИЭкспортировать и Экспортер.Экспортировать без возможности жёстко отменить фоновое задание (ограничение платформы OneScript - ФоновоеЗадание не имеет Прервать()/ОтменитьЗадание()). Реализован soft-timeout: вызывающий получает результат в срок, но сама операция экспорта может доработать в фоне, а не быть прервана.

- ⚠️ **[Metrics Sdk]** [SHOULD] If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`.  
  ОтелДанныеМетрики принимает ОбластьИнструментирования вторым обязательным параметром конструктора (стр. 208), поэтому продюсер может передать InstrumentationScope. Но ни контракт ИнтерфейсПродюсерМетрик, ни читатель не требуют и не обеспечивают, чтобы это была единая область, идентифицирующая сам MetricProducer: СобратьДанныеПродюсеров добавляет данные продюсера как есть, без проверки или подстановки области, а собственной реализации продюсера с такой областью в SDK нет.

- ⚠️ **[Prometheus Compatibility]** [SHOULD] If dropping a comment or metric points, the exporter SHOULD warn the user through error logging.  
  Во всех штатных путях отбрасывания пишется предупреждение (Лог.Предупреждение): конфликт TYPE - метрика отброшена целиком (стр. 618-620, 979-980), сэмплы с уже выведенными именем и лейблами - точки отброшены (стр. 624-631), отличающийся HELP - описание отброшено (стр. 837-843). Но есть путь без предупреждения: семейство info-метрики в text format называется база + _info, а датчик или stateset с таким именем имеет другую базу. ЕстьКонфликтТипа (стр. 965-982) находит семейство по имени в text format, видит тот же тип gauge и то же имя и конфликта не отмечает, а СемействоМетрики (стр. 683-697) ищет только по базовому имени и создает второе семейство с тем же именем. СобратьСемейства возвращает два семейства с одним именем, PrometheusTextFormat.Сериализовать (oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:351-355) оставляет последнее, серии первого теряются без предупреждения. Проверено запуском: info-метрика x (метка k=info-series) и датчик x_info (метка k=gauge-series) дали только x_info{k=gauge-series}, в логе ничего.

- ❌ **[Metrics Sdk]** [SHOULD] If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter.  
  Функция Произвести() (ИнтерфейсПродюсерМетрик.os:33) не содержит параметра ресурса, хотя возвращаемые ОтелДанныеМетрики несут Ресурс как обязательный параметр конструктора (ОтелДанныеМетрики.os:208) - батч включает информацию о ресурсе, но интерфейс не даёт вызывающему способа передать его продюсеру; читатель (ОтелПериодическийЧитательМетрик.СобратьДанныеПродюсеров) тоже не передаёт Ресурс продюсеру при вызове Произвести.

- ❌ **[Prometheus Compatibility]** [SHOULD] The resulting unit SHOULD be added to the metric as UNIT metadata.  
  UNIT-метаданные не выводятся. Семейство, которое строит СемействоМетрики (ОтелПрометеусЧитательМетрик.os:689-693), содержит только Имя, Тип, Справка и Сэмплы (поля единицы нет), а сериализатор библиотеки prometheus (PrometheusTextFormat.Сериализовать, oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:384-385) пишет только строки # HELP и # TYPE: читатель выдает text format 0.0.4, в котором комментария # UNIT нет. Переведенная единица используется только как суффикс имени (БазовоеИмя, стр. 1060-1072). Вывод OpenMetrics 1.0 (# UNIT, _created, exemplars) удален из читателя коммитом 328d385 и должен вернуться патчем библиотеки prometheus (docs/api/Метрики/ОтелПрометеусЧитательМетрик.md:20-22).

- ❌ **[Prometheus Compatibility]** [SHOULD] Monotonic Sum metric points with `StartTimeUnixNano` SHOULD transform `StartTimeUnixNano` into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol.  
  startTimeUnixNano точек читателем не используется: ОтелПрометеусЧитательМетрик.os не обращается к этому полю, сэмплы точки строятся только из value и attributes (ДобавитьСэмплыТочки, стр. 711-722). Выдача - text format 0.0.4 (Prometheus.СериализоватьВТекст), в котором нет StartTime; представление _created (OpenMetrics) и created_timestamp (protobuf) не реализовано: OpenMetrics 1.0 удален из читателя коммитом 328d385 и должен вернуться патчем библиотеки prometheus. В отличие от exemplars (правило отбрасывания при отсутствии поддержки формата есть в спецификации), для StartTime такого правила нет.

- ❌ **[Prometheus Compatibility]** [SHOULD] If set, `StartTimeUnixNano` SHOULD be transformed into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol.  
  startTimeUnixNano точки гистограммы не используется: ДобавитьСэмплыГистограммы (ОтелПрометеусЧитательМетрик.os:733-750) читает только bucketCounts, explicitBounds, sum и count. Выдача - text format 0.0.4, в котором нет StartTime; _created (OpenMetrics) и created_timestamp (protobuf) не реализованы: OpenMetrics 1.0 удален из читателя коммитом 328d385 и должен вернуться патчем библиотеки prometheus. В отличие от exemplars (правило отбрасывания при отсутствии поддержки формата есть в спецификации), для StartTime такого правила нет.

- ❌ **[Prometheus Exporter]** [SHOULD NOT] A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus m...  
  Экспортер использует неофициальную стороннюю клиентскую библиотеку prometheus для OneScript (yellow-hammer/prometheus 1.0.5, автор Ivan Karlo): в официальном списке клиентских библиотек Prometheus (Go, Java/Scala, Node.js, Python, Ruby, Rust) ее нет, официальной библиотеки для OneScript не существует. Зависимость времени выполнения объявлена в packagedef:32 и opm-metadata.xml:22 (dev=false); '#Использовать prometheus' (стр. 4), текст выдачи формирует Prometheus.СериализоватьВТекст (стр. 100), Content-Type берется из Prometheus.ContentTypeМетрик (стр. 109), для реестра библиотеки читатель отдает семейства через Collect() (стр. 207-209). Спецификация допускает вместо этого собственную реализацию формата экспозиции (документация Prometheus: если клиентской библиотеки для языка нет, формат экспозиции можно реализовать самостоятельно); ранее выдачу формировал встроенный сериализатор без библиотеки, теперь зависимость возвращена.

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:7,383` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:125-129,368-374` |  |
| 3 | MUST | ✅ found | In the cases where an extremely clear, pre-existing option is not available, OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:1-386` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: | `src/Ядро/Модули/ОтелКонтекст.os:42-44` |  |
| 5 | SHOULD NOT | ✅ found | Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. | `src/Ядро/Модули/ОтелКонтекст.os:34,42-44` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key. | `src/Ядро/Модули/ОтелКонтекст.os:42-44` |  |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:108-113` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the `Context` for the specified key. | `src/Ядро/Модули/ОтелКонтекст.os:108-113` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:125-129` |  |
| 10 | MUST | ✅ found | The API MUST return a new `Context` containing the new value. | `src/Ядро/Модули/ОтелКонтекст.os:125-129` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ➖ n_a | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries. | - | Требование - рекомендация по использованию (caller guidance) для авторов SDK-компонентов и instrumentation libraries о том, в каких случаях следует использовать глобальные операции (Get current Context/Attach/Detach), а не функциональное требование к реализации самого Context API. OneScript не может программно ограничить круг вызывающих код (нет разграничения SDK-only/пользовательский код на уровне рантайма, все Экспорт-функции модуля ОтелКонтекст доступны любому вызывающему коду одинаково). Аналогично паттерну 'ForceFlush SHOULD only be called in cases where it is absolutely necessary' из правил задания - caller guidance, не проверяемая по коду. |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the `Context` associated with the caller’s current execution unit. | `src/Ядро/Модули/ОтелКонтекст.os:58-64` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:245` |  |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:251` |  |

#### Detach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#detach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API MUST accept the following parameters: * A `Token` that was returned by a previous call to attach a `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:267` |  |

### Baggage Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Each name in `Baggage` MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23-27` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:37-39,67-71` |  |
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:37` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:16-18` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:151-162` |  |

#### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | the Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if the given name is not present. | `src/Ядро/Классы/ОтелBaggage.os:37-39` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. | `src/Ядро/Классы/ОтелBaggage.os:102-104` |  |

#### Set Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | To record the value for a name/value pair, the Baggage API MUST provide a function which takes a name, and a value as input. | `src/Ядро/Классы/ОтелBaggage.os:67-71` |  |

#### Remove Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#remove-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | To delete a name/value pair, the Baggage API MUST provide a function which takes a name as input. | `src/Ядро/Классы/ОтелBaggage.os:81-85` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the `Context`, it MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:154-159 (BaggageИзКонтекста = Extract), src/Ядро/Модули/ОтелКонтекст.os:185-189 (КонтекстСBaggage = Insert)` |  |
| 12 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:23,46-50` |  |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:95-97 (ТекущийBaggage = Get), src/Ядро/Модули/ОтелКонтекст.os:229-231 (СделатьBaggageТекущим = Set)` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:95-97,154-159,185-189,229-231; src/Ядро/Классы/ОтелBaggage.os:16-18,25-27` |  |

#### Clear Baggage in the Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#clear-baggage-in-the-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | To avoid sending any name/value pairs to an untrusted process, the Baggage API MUST provide a way to remove all baggage entries from a context. | `src/Ядро/Классы/ОтелBaggage.os:93-95 (Очистить - возвращает пустой Baggage), src/Ядро/Модули/ОтелКонтекст.os:185-189 (КонтекстСBaggage - устанавливает Baggage в контекст)` |  |

#### Propagation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#propagation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following `Propagator`s: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:31 (Внедрить/inject), :97 (Извлечь/extract) - TextMapPropagator реализующий W3C Baggage Specification, включён в основной пакет (lib.config:144)` |  |

#### Conflict Resolution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#conflict-resolution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23-27 (Установить: Значения.Вставить перезаписывает значение при существующем ключе - платформенная семантика Соответствие.Вставить)` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:102-107; src/Ядро/Классы/ОтелПостроительРесурса.os:77-83; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:30` |  |
| 2 | MUST | ✅ found | When associated with a `TracerProvider`, all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелТрассировщик.os:242; src/Трассировка/Классы/ОтелСпан.os:787-801` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:110-114 (ЗаполнитьАтрибутыПоУмолчанию); src/Ядро/Модули/ОтелУтилиты.os:476-495,531-549 (ВерсияSDK, ВерсияПакета: packagedef, в установленном пакете - opm-metadata.xml)` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a `TracerProvider`, `MeterProvider`, or `LoggerProvider` if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:495-499; src/Метрики/Классы/ОтелПровайдерМетрик.os:488-492; src/Логирование/Классы/ОтелПровайдерЛогирования.os:323-327` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource. | `src/Ядро/Классы/ОтелРесурс.os:102-107; src/Ядро/Классы/ОтелПостроительРесурса.os:77-83` |  |

#### Merge

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:41-66` |  |
| 7 | MUST | ✅ found | [...] otherwise merge behavior without Entities MUST be used. | `src/Ядро/Классы/ОтелРесурс.os:41-66` |  |

#### Merge behavior without Entities

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge-behavior-without-entities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:58-64` |  |
| 9 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:62-64; src/Ядро/Классы/ОтелАтрибуты.os:19-21` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелРесурс.os:116-119` |  |
| 11 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17-33; ОтелДетекторРесурсаПроцесса.os:17-27; ОтелДетекторРесурсаПроцессора.os:18-31` |  |
| 12 | MUST NOT | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:22-31 (аналогично ОтелДетекторРесурсаПроцесса.os:20-25, ОтелДетекторРесурсаПроцессора.os:21-29)` |  |
| 13 | SHOULD | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:22-31 (аналогично ОтелДетекторРесурсаПроцесса.os:20-25, ОтелДетекторРесурсаПроцессора.os:21-29)` |  |
| 14 | MUST | ✅ found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions... | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18-21 (аналогично ОтелДетекторРесурсаПроцесса.os:18-19, ОтелДетекторРесурсаПроцессора.os:19-20)` |  |
| 15 | SHOULD | ⚠️ partial | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will popula... | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:19-21` | АдресСхемыСемантическихСоглашений присваивается ресурсу безусловно в начале Обнаружить() во всех трёх генерик-детекторах (host/process/cpu), до Попытки заполнения атрибутов. Если Попытка завершается исключением и ни один атрибут не установлен (детектор фактически не узнал ни одного известного атрибута), итоговый ресурс всё равно получает non-empty Schema URL вместо пустой строки, как требует SHOULD. Отдельного детектора-обёртки над OTEL_RESOURCE_ATTRIBUTES (пример из самой спеки - 'детектор, который читает атрибуты из окружения, не будет знать, какую Schema URL использовать') с явной пустой схемой тоже нет: эти атрибуты применяются напрямую в ОтелРесурс.ПрименитьАтрибутыИзОкружения (строки 326-341) без какой-либо работы со Schema URL. |
| 16 | MUST | ✅ found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:42-56` |  |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user p... | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:173-210; src/Ядро/Классы/ОтелРесурс.os:135-158` |  |
| 18 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Ядро/Классы/ОтелРесурс.os:171-200; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:832-859` |  |
| 19 | MUST | ✅ found | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Ядро/Модули/ОтелУтилиты.os:323-343; src/Ядро/Классы/ОтелРесурс.os:171-200` |  |
| 20 | SHOULD | ✅ found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Ядро/Классы/ОтелРесурс.os:171-200; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:184-194` |  |
| 21 | SHOULD | ✅ found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Ядро/Классы/ОтелРесурс.os:192-196; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:190-192` |  |

#### Retrieve attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#retrieve-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:119-137` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:484-521; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:108-116` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: * Get a `Tracer` | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-115` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-75` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:159; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:62-66` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHO... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76-83` |  |
| 7 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHO... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:80-82` |  |
| 8 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHO... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:77-79` |  |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:95-99,209-221,456-461; src/Трассировка/Классы/ОтелТрассировщик.os:148-150` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: * Extract the `Span` from a `Context` instance * Combine the `Span` with a `Context` instance, creating a new `Context` instance | `src/Ядро/Модули/ОтелКонтекст.os:139-144,170-174` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:20-23,46-50` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:58-64,85-87,216-218` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:108-231` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The `Tracer` MUST provide functions to: * Create a new `Span` (see the section on `Span`) | `src/Трассировка/Классы/ОтелТрассировщик.os:74-98,113-128` |  |
| 15 | SHOULD | ✅ found | The `Tracer` SHOULD provide functions to: * Report if `Tracer` is `Enabled` | `src/Трассировка/Классы/ОтелТрассировщик.os:53-58` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:53-58` |  |
| 17 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:53` |  |
| 18 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:53-58` |  |
| 19 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:29-33` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | The API MUST implement methods to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252-272` |  |
| 21 | SHOULD | ✅ found | These methods SHOULD be the only way to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:230-236,252-272` |  |
| 22 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252-272` |  |
| 23 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252-272` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23-34,84-95` |  |
| 25 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23-25,176-194` |  |
| 26 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32-34,176-194` |  |
| 27 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84-86` |  |
| 28 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:93-95` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:3-12` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | An API called `IsValid`, that returns a boolean value, which is `true` if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70-77` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 31 | MUST | ✅ found | An API called `IsRemote`, that returns a boolean value, which is `true` if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60-62` |  |
| 32 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:163` |  |
| 33 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:256; src/Трассировка/Классы/ОтелСпан.os:817-818` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: Get value for a given key, Add a new key-value pair, Update an existing value for a given key, Delete a key-value pair. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:54-61 (Получить),76-118 (Установить - add/update),128-146 (Удалить)` |  |
| 35 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:110-117,434-449,483-509` |  |
| 36 | MUST | ✅ found | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:115-117,143-145` |  |
| 37 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:281-284,391-411,434-449,483-509` |  |
| 38 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:77-89,129-134` |  |
| 39 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:77-89` |  |
| 40 | MUST | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:78-89,104-107,130-133 (Лог.Предупреждение)` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | SHOULD | ➖ n_a | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Имя спана выбирает вызывающий код при вызове ПостроительСпана()/НачатьСпан(), SDK принимает любую переданную строку без ограничений. Собственных Instrumentation Libraries, которые бы сами формировали имена спанов, пакет не содержит (только API+SDK). |
| 42 | SHOULD | ➖ n_a | Generality SHOULD be prioritized over human-readability. | - | Требование является продолжением рекомендации по выбору имени спана - это caller guidance, а не поведение SDK; SDK не может программно обеспечить приоритет generality над читаемостью выбранного вызывающим кодом имени. |
| 43 | SHOULD | ✅ found | A `Span`'s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:822` |  |
| 44 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:309-316 (ИзменитьИмя),330-345 (УстановитьАтрибут),360-375 (ДобавитьСобытие),498-517 (УстановитьСтатус)` |  |
| 45 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`'s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:311,331,361,500 (проверка Завершен.Получить() перед изменением)` |  |
| 46 | SHOULD NOT | ➖ n_a | To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:5-14` | OneScript не поддерживает internal/package-private модификаторы; SDK-геттеры (Атрибуты(), События(), Линки() и т.п.) обязаны быть Экспорт, иначе процессоры/экспортёры не смогут читать данные спана. Ограничение явно задокументировано в шапке класса ОтелСпан.os:5-14 со ссылкой на это требование (§46) и в docs/spec-compliance.md. |
| 47 | MUST NOT | ➖ n_a | However, alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелСпан.os:760-766` | OneScript не поддерживает приватные конструкторы; ПриСозданииОбъекта всегда публичен, поэтому Новый ОтелСпан(...) технически вызываем из пользовательского кода. Ограничение документировано в самом классе (ОтелСпан.os:760-766) и в docs/spec-compliance.md; внутри SDK единственная точка создания - ОтелТрассировщик.НачатьСпанSdk(). |
| 48 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:74-77,91-98,113-128,213-249` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелСпан.os:760-766` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os:760-766) и docs/spec-compliance.md. Помимо платформенно-неустранимого публичного конструктора других API создания спана нет: ОтелСпаны.Обернуть()/Невалидный() лишь оборачивают уже существующий SpanContext в незаписывающий спан - это отдельное, специально требуемое спекой действие (Wrapping a SpanContext in a Span), а не конкурирующий способ создания записываемого Span. |
| 50 | MUST NOT | ✅ found | In languages with implicit `Context` propagation, `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default, but this functionality MAY be offered ... | `src/Трассировка/Классы/ОтелТрассировщик.os:74-77; src/Трассировка/Классы/ОтелСпан.os:464-484 (СделатьТекущим - отдельная операция)` |  |
| 51 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПостроительСпана.os:37-47,70-73,86-89,102-105,120-123; src/Трассировка/Классы/ОтелТрассировщик.os:74-77` |  |
| 52 | MUST NOT | ⚠️ partial | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелПостроительСпана.os:37-47; src/Трассировка/Классы/ОтелТрассировщик.os:113-128` | ОтелПостроительСпана.УстановитьРодителя() (ОтелПостроительСпана.os:37-47) корректно принимает только Context (Соответствие/ФиксированноеСоответствие) и выбрасывает исключение при попытке передать иной тип. Но публичный метод ОтелТрассировщик.НачатьДочернийСпан(ИмяСпана, РодительскийКонтекст, ...) (ОтелТрассировщик.os:113-128) принимает параметр РодительскийКонтекст именно как ОтелСпан или ОтелКонтекстСпана напрямую (проверка ТипЗнч на 'ОтелКонтекстСпана', иначе вызывается .КонтекстСпана() как у Span), а не как полный Context - это отдельный публичный путь создания дочернего спана, нарушающий требование. |
| 53 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:167-187 (НачатьСпанВКонтексте: Родитель = ОтелКонтекст.СпанИзКонтекста(Контекст))` |  |
| 54 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:75-77` |  |
| 55 | SHOULD | ➖ n_a | This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:107-119` | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно определить, совпадает ли момент вызова API с логическим стартом операции. Рекомендация отражена в документирующем комментарии УстановитьВремяНачала() (ОтелПостроительСпана.os:107-112); по умолчанию (аргумент не передан) используется текущее время (ОтелСпан.os:822). |
| 56 | MUST NOT | ➖ n_a | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:107-119` | Требование адресовано пользователю API («API user MUST NOT»), а не поведению SDK - это caller guidance, SDK не может программно принудить пользователя не вызывать УстановитьВремяНачала(). Комментарий метода (ОтелПостроительСпана.os:107-112) явно указывает: устанавливать время начала явно следует ТОЛЬКО если вызов API не совпадает с логическим стартом операции. |
| 57 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:91-98 (НачатьКорневойСпан); src/Трассировка/Классы/ОтелПостроительСпана.os:55-59 (БезРодителя)` |  |
| 58 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-229 (НачатьСпанSdk: ИдТрассировки = Провайдер.СгенерироватьИдТрассировки(), строка 226, когда ЕстьРодитель=Ложь)` |  |
| 59 | MUST | ✅ found | For a Span with a parent, the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:220-222 (ИдТрассировки = ВалидныйРодитель.ИдТрассировки())` |  |
| 60 | MUST | ✅ found | Also, the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:428-437 (ОпределитьСостояниеТрассировки)` |  |
| 61 | MUST | ➖ n_a | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:528-550` | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Спецификация прямо указывает: «This is the responsibility of the user». Для завершения SDK предоставляет метод ОтелСпан.Завершить() (ОтелСпан.os:528-550); при незавершённых спанах спека прямо допускает утечку ресурсов на стороне реализации, то есть не возлагает на SDK обязанность принудительного завершения. |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | `src/Трассировка/Классы/ОтелПостроительСпана.os:102-105; src/Трассировка/Классы/ОтелТрассировщик.os:74-77 (параметр Линки)` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | The Span interface MUST provide: An API that returns the `SpanContext` for the given `Span`. | `src/Трассировка/Классы/ОтелСпан.os:97-99` |  |
| 64 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:97-99,817-818` |  |

#### IsRecording

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:296-298,528-550` |  |
| 66 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:296-298,528-550` |  |
| 67 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:296-298` |  |
| 68 | SHOULD | ➖ n_a | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | - | Требование является рекомендацией по использованию флага IsRecording для инструментирующего кода/вызывающих (caller guidance) - оно советует авторам инструментирования проверять флаг перед дорогими вычислениями. SDK не может программно обеспечить это со стороны вызывающего кода; сам флаг (ЗаписьАктивна()) корректно реализован и доступен для такой проверки. |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:330-345` |  |
| 70 | MUST | ✅ found | The Span interface MUST provide: An API to set a single `Attribute` where the attribute properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:330-345` |  |
| 71 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute’s value. | `src/Трассировка/Классы/ОтелСпан.os:562-573; src/Ядро/Классы/ОтелАтрибуты.os:19-22` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | A `Span` MUST have the ability to add events. | `src/Трассировка/Классы/ОтелСпан.os:360-375` |  |
| 73 | MUST | ✅ found | The Span interface MUST provide: An API to record a single `Event` where the `Event` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:360-375` |  |
| 74 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:580-590` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:432-462` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | `Description` MUST only be used with the `Error` `StatusCode` value. | `src/Трассировка/Классы/ОтелСпан.os:498-517` |  |
| 77 | MUST | ✅ found | The Span interface MUST provide: An API to set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:498` |  |
| 78 | SHOULD | ✅ found | This SHOULD be called `SetStatus`. | `src/Трассировка/Классы/ОтелСпан.os:498` |  |
| 79 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:500-502,506-512` |  |
| 80 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:827` |  |
| 81 | SHOULD | ✅ found | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:500-502` |  |
| 82 | SHOULD | ➖ n_a | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | - | Требование адресовано Instrumentation Libraries (политика их поведения при документировании своих Description); данный пакет реализует только API+SDK, IL не включены. |
| 83 | SHOULD | ➖ n_a | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | - | Требование адресовано Instrumentation Libraries (политика их поведения по публикации собственных конвенций); данный пакет реализует только API+SDK, IL не включены. |
| 84 | SHOULD NOT | ➖ n_a | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены. |
| 85 | SHOULD | ➖ n_a | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены. |
| 86 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:504-514` |  |
| 87 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:504-514` |  |
| 88 | SHOULD | ➖ n_a | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | - | Требование адресовано внешним downstream Analysis tools (бэкендам/системам анализа телеметрии), а не Trace API/SDK - аналогично категории Instrumentation Libraries. Данный пакет реализует только API+SDK для генерации телеметрии; поведение сторонних систем анализа, потребляющих экспортированный статус, не является частью этого кода и не может быть в нём верифицировано. |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended (there might be exceptions when Tracer is streaming events an... | `src/Трассировка/Классы/ОтелСпан.os:528-550,296-298,330-345,360-375,432-462` |  |
| 90 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:528` |  |
| 91 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:528-550` |  |
| 92 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:528-550; src/Ядро/Классы/ОтелТокенКонтекста.os:40-44` |  |
| 93 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:97-99` |  |
| 94 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:482-484` |  |
| 95 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:528,534-538` |  |
| 96 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:528-550` |  |
| 97 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:543-546` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a `RecordException` method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:388` |  |
| 99 | MUST | ✅ found | The method MUST record an exception as an `Event` with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:393-417` |  |
| 100 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:388` |  |
| 101 | MUST | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:388` |  |
| 102 | SHOULD | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:360,388` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 103 | MUST | ✅ found | Start and end time as well as Event’s timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:822,535; src/Трассировка/Классы/ОтелСобытиеСпана.os:95` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 104 | MUST | ✅ found | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | `src/Трассировка/Модули/ОтелСпаны.os:36` |  |
| 105 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:260-267` | Требуемая функция-обертка есть (ОтелСпаны.Обернуть/Невалидный возвращают объект с интерфейсом Span), и комментарии в коде прямо не рекомендуют прямое создание класса. Но сам тип ОтелНезаписывающийСпан зарегистрирован в lib.config как обычный публичный класс (см. lib.config:38) наравне с ОтелСпан и может быть создан напрямую (Новый ОтелНезаписывающийСпан(...)) из любого вызывающего кода. OneScript не поддерживает package-private/internal классы - только общий реестр классов в lib.config, поэтому техническое сокрытие типа не достигнуто, только рекомендация через документацию. |
| 106 | SHOULD | ✅ found | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:260-267` |  |
| 107 | MUST | ✅ found | `GetContext` MUST return the wrapped `SpanContext`. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:29-31` |  |
| 108 | MUST | ✅ found | `IsRecording` MUST return `false` to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157` |  |
| 109 | MUST | ✅ found | The remaining functionality of `Span` MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:167-254` |  |
| 110 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:1-287` |  |
| 111 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:1-287` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 112 | SHOULD | ➖ n_a | In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | - | Требование адресовано вызывающему коду / авторам инструментирования (рекомендация по моделированию: не совмещать несколько ролей в одном Span), а не самой реализации Trace API/SDK. Это рекомендация по использованию (caller guidance), аналогичная 'ForceFlush SHOULD only be called...'; SDK не может программно обеспечить, что конкретный Span 'не служит более чем одной цели' - это архитектурное решение инструментирующего кода, а не функция библиотеки. |
| 113 | SHOULD NOT | ➖ n_a | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | - | Продолжение предыдущей рекомендации - пример правильного использования SpanKind для авторов инструментирования, а не требование к API/SDK реализации. SDK не может программно запретить использовать SERVER-спан для описания исходящего RPC-вызова - это caller guidance, а не функциональное требование к коду библиотеки. |

#### Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 114 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:432-462` |  |
| 115 | MUST | ✅ found | The API MUST provide: An API to record a single `Link` where the `Link` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:432; src/Трассировка/Классы/ОтелПостроительСпана.os:102-105` |  |
| 116 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:437-451,620-623,640-642` |  |
| 117 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:597-609,826` |  |
| 118 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can o... | `src/Трассировка/Классы/ОтелПостроительСпана.os:91-93` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 119 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:7; :15-19,100-114,209-221 (БлокировкаТрассировщиков, СинхронизированнаяКарта)` |  |
| 120 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3-4` |  |
| 121 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:5-6; :38-44,528-550 (Блокировка, АтомарноеБулево)` |  |
| 122 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 123 | SHOULD | ✅ found | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелЛинк.os:1-13` |  |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 124 | MUST | ✅ found | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:175-187,263-265` |  |
| 125 | SHOULD | ✅ found | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | `src/Трассировка/Классы/ОтелТрассировщик.os:176-178,121-123` |  |
| 126 | MUST | ✅ found | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFl... | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:275-284` |  |

### Trace Sdk

#### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API). | `src/Трассировка/Классы/ОтелТрассировщик.os:347-351; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:55-57,71-115` | OneScript не поддерживает приватные конструкторы: ПриСозданииОбъекта класса ОтелТрассировщик (ОтелТрассировщик.os:347-351) всегда публичен, поэтому запретить прямой вызов «Новый ОтелТрассировщик(...)» средствами языка невозможно (то же архитектурное ограничение задокументировано в проекте для ОтелСпан/ОтелЛоггер/ОтелМетр, см. docs/spec-compliance.md). Внутри SDK трассировщики создаются исключительно в ОтелПровайдерТрассировки.ПолучитьТрассировщик()/ПостроительТрассировщика().Построить() (ОтелПровайдерТрассировки.os:55-57,71-115) - это единственный документированный штатный путь получения Tracer. |
| 2 | MUST | ✅ found | The `TracerProvider` MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-115; src/Трассировка/Классы/ОтелПостроительТрассировщика.os:62-64` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:84-85,90-93,106; src/Трассировка/Классы/ОтелТрассировщик.os:139-141,326-328,347-350` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler` [...]) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9-42,484-521` |  |
| 5 | MUST | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:209-221,456-461,96-108` |  |
| 6 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from... | `src/Трассировка/Классы/ОтелТрассировщик.os:53-58,148-150; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:209-221,456-461` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165` |  |
| 8 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:86-94; src/Трассировка/Классы/ОтелТрассировщик.os:53-58,93-98,120-128,175-180` |  |
| 9 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165,198-201; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,215-236; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40` |  |
| 10 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114,330-339; oscript_modules/async/src/internal/Классы/Обещание.os:23-35` | TracerProvider.Закрыть(ТаймаутМс) принимает таймаут и корректно урезает остаток времени для каждого процессора (ОтелРезультатыЗакрытия.ОставшеесяВремя), но для ОтелПакетныйПроцессорСпанов Закрыть сначала останавливает фоновое задание периодического экспорта через ОстановитьФоновыйЭкспорт → Обещание.Получить(ТаймаутМс) → Задание.ОжидатьЗавершения(Таймаут) (oscript_modules async). OneScript ФоновоеЗадание не поддерживает принудительную отмену (нет Прервать()/ОтменитьЗадание(), см. github.com/EvilBeaver/OneScript/issues/1672): по истечении таймаута вызывающий поток просто перестаёт ждать (исключение перехватывается, Лог.Отладка), а само фоновое задание продолжает работу. Это soft-timeout: Shutdown гарантированно возвращает управление в пределах бюджета времени, но не гарантирует физическую остановку фоновой активности. |
| 11 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:158-165,397-399; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,192-202` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:145-147,175-180,187-191` |  |
| 13 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:145-147,409-411; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217; src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-30` |  |
| 14 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:145-147,409-411,397-399` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ❌ not_found | `Enabled` MUST return `false` when [...] there are no registered `SpanProcessors`. | - | Включен() трассировщика не проверяет зарегистрированные процессоры: делегирует в Провайдер.Включен() (ОтелПровайдерТрассировки.os:299-301), который возвращает признак SDK-режима, по умолчанию Истина независимо от числа процессоров (ОтелПровайдерТрассировки.os:520). У Logger такая проверка есть: «Если НЕ Провайдер.Процессор().ЕстьПроцессоры() Тогда Возврат Ложь» (ОтелЛоггер.os:82). |
| 16 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:53-58; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:299-301` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:88-298 (Имя, Атрибуты, События, Линки, КодСтатуса, СообщениеСтатуса, ВремяНачала, ВремяОкончания и др. - все Экспорт-геттеры на самом объекте Span, т.к. API и SDK объединены в одном классе)` |  |
| 18 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:210-212 (Ресурс), 219-221 (ОбластьИнструментирования)` |  |
| 19 | MUST | ✅ found | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:223-234 (БиблиотекаИнструментирования() возвращает тот же объект ОбластьИнструментирования, что и ОбластьИнструментирования() - гарантированно совпадающие name/version)` |  |
| 20 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended (some languages might implement this by having an end timestamp of `null`, others might have an expl... | `src/Трассировка/Классы/ОтелСпан.os:254-261 (Завершен() возвращает Завершен.Получить() - АтомарноеБулево)` |  |
| 21 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:263-288 (КоличествоОтброшенныхАтрибутов, КоличествоОтброшенныхСобытий, КоличествоОтброшенныхЛинков)` |  |
| 22 | MUST | ✅ found | As an exception to the authoritative set of span properties defined in the API spec, implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at le... | `src/Трассировка/Классы/ОтелСпан.os:113-120 (КонтекстРодительскогоСпана() возвращает полный ОтелКонтекстСпана родителя, а не только Context)` |  |
| 23 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user (for example, the `Span` c... | `src/Трассировка/Классы/ОтелСпан.os:787-872 (конструктор вызывает Процессор.ПриНачале(ЭтотОбъект,...) - тот же экземпляр); src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:5-31 (ПриНачале/ПриЗавершении принимают Спан параметром); src/Трассировка/Классы/ОтелТрассировщик.os:241-248 (Спан=Новый ОтелСпан(...); ...; Возврат Спан - тот же объект возвращается вызывающему)` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-249 (НачатьСпанSdk: при DROP-решении сэмплера возвращается СоздатьНезаписывающийСпанДляОтброшенного без создания ОтелСпан и без вызова процессора); src/Трассировка/Классы/ОтелСпан.os:869-871 (Процессор.ПриНачале(ЭтотОбъект,...) вызывается только внутри конструктора реального, записывающего спана)` |  |
| 25 | SHOULD NOT | ✅ found | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:55-74,120-137 (ПриЗавершении вызывает Экспортер.Экспортировать только если СпанСэмплирован(Спан)=Истина); src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:40-58 (та же проверка перед Родитель.Обработать(Спан))` |  |
| 26 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:55-74,120-137 (СпанСэмплирован проверяет бит Sampled во ФлагиТрассировки, экспорт происходит только при Истина)` |  |
| 27 | SHOULD NOT | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:55-74,120-137; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:40-58 (Если НЕ СпанСэмплирован(Спан) Тогда Возврат - не сэмплированные спаны не доходят до экспортера)` |  |
| 28 | MUST NOT | ✅ found | The flag combination `SampledFlag == true` and `IsRecording == false` could cause gaps in the distributed trace, and because of this the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:239-248,278-293 (ВычислитьФлагиТрассировки ставит Sampled-бит только для реального ОтелСпан; ФлагиUnsampled для незаписывающего спана никогда не содержит Sampled-бит); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:150-157 (ЗаписьАктивна() всегда возвращает Ложь)` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:213-249 (НачатьСпанSdk: TraceId разрешается из валидного родителя или генерируется ДО вызова сэмплера; НовыйИдСпана генерируется независимо от решения сэмплера - до факта вызова ПрошелСэмплирование и без использования его результата; ПрошелСэмплирование вызывает ОтелСэмплер.ДолженСэмплировать; итоговый спан создается по решению - ОтелСпан для RECORD_ONLY/RECORD_AND_SAMPLE, ОтелНезаписывающийСпан для DROP)` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:220-234 (при наличии валидного родителя ИдТрассировки = ВалидныйРодитель.ИдТрассировки() - используется тот же TraceId, который затем передается в ОтелСэмплер.ДолженСэмплировать)` |  |
| 31 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:389-416 (ВычислитьФлагиТрассировки: СэмплингБит=1 устанавливается только для РешениеЗаписатьИЭкспортировать; для РешениеЗаписать (RECORD_ONLY) остается 0)` |  |
| 32 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:389-416 (СэмплингБит=1 при РезультатСэмплирования.Решение()=ОтелСэмплер.РешениеЗаписатьИЭкспортировать())` |  |
| 33 | SHOULD | ✅ found | If the sampler returns an empty `Tracestate` here, the `Tracestate` will be cleared, so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Модули/ОтелСэмплер.os:163-186 (ДолженСэмплировать: Новый ОтелРезультатСэмплирования(Решение, , РодительскоеСостояниеТрассировки) - родительский TraceState передается в результат без изменений для всех встроенных стратегий)` |  |

#### GetDescription

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#getdescription)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD NOT | ➖ n_a | Callers SHOULD NOT cache the returned value. | - | Требование адресовано вызывающему коду (caller guidance): оно описывает, как потребитель API должен использовать значение, возвращаемое GetDescription/ОтелСэмплер.Описание(), а не требование к реализации самого метода в SDK. SDK не может программно запретить кеширование результата на стороне вызывающего кода (аналогично рекомендации 'ForceFlush SHOULD only be called...'). |

#### AlwaysOn

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | MUST | ✅ found | Description MUST be `AlwaysOnSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:119-122 (Описание(): Если Стратегия = ВсегдаВключен() Тогда Возврат "AlwaysOnSampler")` |  |

#### AlwaysOff

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysoff)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | Description MUST be `AlwaysOffSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:122-124 (Описание(): ИначеЕсли Стратегия = ВсегдаВыключен() Тогда Возврат "AlwaysOffSampler")` |  |

#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:271-272 (ВычислитьРешение передает в СэмплироватьПоДоле только Доля/ИдТрассировки/РодительскоеСостояниеТрассировки),370 (сигнатура СэмплироватьПоДоле не принимает РодительСэмплирован вовсе)` |  |
| 38 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance’s trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:125-126 (Возврат "TraceIdRatioBased{" + Формат(Доля,...) + "}")` |  |
| 39 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:126 (Формат(Доля, "ЧДЦ=6; ЧРД=.; ЧН=0; ЧГ=") - фиксированные 6 знаков после запятой, совпадает с точностью примера спецификации "0.000100")` |  |
| 40 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:126 (те же 6 знаков после запятой дают разрешение 0.000001 - достаточно для различения сэмплеров с разными долями)` |  |
| 41 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:370-394 (СэмплироватьПоДоле - чистая функция от Доля/ИдТрассировки, без обращения к времени или случайности)` |  |
| 42 | MUST | ✅ found | To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:388-393 (ОтелУтилиты.ИзШестнадцатеричнойСтроки(Прав(ИдТрассировки, ДлинаЗначенияСлучайности)) - детерминированное значение из правых 56 бит TraceId, тот же подход, что и в эталонных SDK, использующих часть байт TraceId как хэш-значение),449-455 (РешениеПоСлучайности - пороговое сравнение)` |  |
| 43 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:449-455 (РешениеПоСлучайности: Порог=(1-Доля)*ДиапазонСлучайности монотонно убывает при росте Доли, поэтому множество сэмплируемых значений для большей доли - надмножество для меньшей)` |  |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 44 | MUST | ✅ found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | `src/Трассировка/Модули/ОтелСэмплер.os:97-107 (ВсегдаЗаписывать - идентификатор стратегии),300-319 (СэмплироватьВсегдаЗаписывать: DROP поднимается до RECORD_ONLY через РешениеЗаписать(), RECORD_ONLY и RECORD_AND_SAMPLE возвращаются без изменений - точное соответствие таблице спецификации)` |  |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:330-345` |  |
| 46 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java exampl... | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:76-79` |  |
| 47 | SHOULD | ✅ found | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:103,113,138,151` |  |
| 48 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:251-279` |  |
| 49 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK’s log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:625-629` |  |
| 50 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:74-75,625-629` |  |

#### ID Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:117-137,147-167` |  |
| 52 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:98-101; src/Ядро/Модули/ОтелУтилиты.os:76-78` |  |
| 53 | MUST | ✅ found | The SDK MAY provide this functionality by allowing custom implementations of an interface like the Java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consisten... | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23,32; src/Ядро/Модули/ОтелУтилиты.os:117,147` |  |
| 54 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace ID generator MUST NOT be maintained or distributed as part of the OpenTelemetry Core packages. | `src/Ядро/Модули/ОтелУтилиты.os:105-168` |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:150-154; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:429-438` |  |
| 56 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:122-124; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:44-47` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11,30,41,54` |  |
| 58 | SHOULD | ✅ found | The `SpanProcessor` interface SHOULD declare the following methods: | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:22` |  |

#### OnStart

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onstart)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:5-12; src/Трассировка/Классы/ОтелСпан.os:330-345` |  |
| 60 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:5-12; src/Трассировка/Классы/ОтелСпан.os:330-345` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:547-549` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:102-105; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-100` |  |
| 63 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:56-58; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-51` |  |
| 64 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:102-109 (returns ОтелРезультатЗакрытия via ЗакрытьЭкспортерПослеЭкспорта); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114 (aggregates real export/close outcomes via РезультатФинальногоЭкспорта + ВызватьВПределахСрока)` |  |
| 65 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:109 -> src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121,89-95 (СброситьБуфер, затем Закрыть); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:105 вызывает тот же ЭкспортироватьВсеПакеты, что и СброситьБуфер на строке 80, перед Экспортер.Закрыть на строке 111` |  |
| 66 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:102 (ТаймаутМс -> БлокировкаЭкспорта.Захватить с ограничением); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-113 (ОставшееВремя/СрокИстек ограничивают ожидание фонового экспорта и финальный экспорт)` |  |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD | ⚠️ partial | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, pre... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:231-252; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85-90` | Пакетный процессор корректно ждёт: ЭкспортироватьПакет безусловно захватывает БлокировкаЭкспорта перед каждой попыткой извлечения (стр. 231-234), поэтому конкурентный фоновый экспорт, уже начатый до вызова ForceFlush, дожидается своего завершения прежде, чем ForceFlush продолжит и вернёт управление. Но ОтелПростойПроцессорСпанов.СброситьБуфер (стр. 85-90) вызывает Экспортер.СброситьБуфер() напрямую, не захватывая БлокировкаЭкспорта, которую ПриЗавершении использует вокруг Экспортер.Экспортировать (стр. 62-73): если ПриЗавершении в другом потоке в этот момент ещё выполняет Export, конкурентный ForceFlush не дожидается его завершения перед возвратом. На практике для встроенного ОтелЭкспортерСпанов не проявляется, так как сам Export ограничен собственным таймаутом. |
| 68 | SHOULD | ✅ found | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter’s `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217 (ЭкспортироватьВсеПакеты экспортирует буфер до опустошения, затем вызывает Экспортер.СброситьБуфер на стр. 211-214); src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85-90` |  |
| 69 | MUST | ✅ found | The built-in SpanProcessors MUST do so. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85-90; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |
| 70 | MUST | ✅ found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-252 (таймаут проверяется перед каждым пакетом, остаток передаётся и в захват БлокировкаЭкспорта, и в вызов Export); src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:108-127 (остаток общего таймаута делится между процессорами в цепочке)` |  |
| 71 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85-90; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217; src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-38` |  |
| 72 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` ex... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance) - о том, когда вызывающему стоит вызывать ForceFlush; SDK не может программно ограничить или проверить необходимость такого вызова. |
| 73 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85-90 (Экспортер.СброситьБуфер принимает ТаймаутМс); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217 (ЭкспортироватьВсеПакеты возвращает Таймаут при истечении срока вместо продолжения ожидания)` |  |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:149-154; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:65-71` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:62-73` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:231-252 (используется src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os через extends)` |  |
| 77 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69 (автозапуск фонового экспорта при первом элементе, стр. 66-68), 168-174 (переинтервал после завершения предыдущего экспорта), 351-368 (триггер по интервалу и по полному пакету), 79-81 (триггер ForceFlush)` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:7-8` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:14,26,35` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:33-52` |  |
| 81 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:33-52` |  |
| 82 | SHOULD NOT | ✅ found | The default SDK’s Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (нет логики повтора); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os (нет логики повтора); повтор реализован на уровне протокол-специфичного транспорта - src/Экспорт/Классы/ОтелHttpТранспорт.os:16,124-227; src/Экспорт/Классы/ОтелGrpcТранспорт.os:19,191-206` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this metho... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:145-147,401-411; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |
| 84 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-29; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:145-147` |  |
| 85 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports t... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance) о том, когда следует вызывать ForceFlush (например, только в FaaS-окружениях перед возможной приостановкой процесса), а не требованием к реализации SDK. SDK не может программно ограничить, в каких случаях вызывающий код решает вызвать ForceFlush. |
| 86 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:145,401-411; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217,231-252` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-115 (ПолучитьТрассировщик, double-checked locking через БлокировкаТрассировщиков),145-147 (СброситьБуфер),158-165 (Закрыть, АтомарноеБулево.СравнитьИУстановить)` |  |
| 88 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:163-186 (ДолженСэмплировать),119-140 (Описание),506-515 (константы модуля инициализируются один раз и далее только читаются)` |  |
| 89 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:55-74,102-110; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69,95-114,231-252,297-328; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:77-97` |  |
| 90 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:7-13 (док-комментарий явно фиксирует требование, Закрыт - АтомарноеБулево),63-76 (СброситьБуфер, Закрыть)` |  |

### Logs Api

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:147,157` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60` |  |

#### Get a Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#get-a-logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60-64` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:63; src/Ядро/Классы/ОтелАтрибуты.os:19` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: | `src/Логирование/Классы/ОтелЛоггер.os:104` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: | `src/Логирование/Классы/ОтелЛоггер.os:60-64` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:21,104; src/Логирование/Классы/ОтелЗаписьЛога.os:188-353` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:104,109-112` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:104,109-112` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:60-64,104` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:60-90` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:60-64` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:61` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:75` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:56-57,66-89` |  |
| 16 | SHOULD | ✅ found | The API documentation SHOULD state that calling `Enabled` is optional and is not required before emitting a `LogRecord`. | `src/Логирование/Классы/ОтелЛоггер.os:29-33` |  |
| 17 | SHOULD | ✅ found | The documentation SHOULD also state that the returned value is not static and can change over time, so a cached value can become stale. | `src/Логирование/Классы/ОтелЛоггер.os:36-37` |  |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:60-64,104` |  |
| 19 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:60-64,104` |  |
| 20 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:104; src/Логирование/Классы/ОтелПровайдерЛогирования.os:60-61` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7` |  |
| 22 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:320-324` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:317-339` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `LoggerProvider` MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:317-328; src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:22-25` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the `LogRecord`s produced by any `Logger` from the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:95-99; src/Логирование/Классы/ОтелЛоггер.os:105-106` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:317-339` |  |

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелЛоггер.os:334-341` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда Экспорт); технически Новый ОтелЛоггер(...) можно вызвать напрямую, в обход LoggerProvider. Единственный предусмотренный SDK путь создания логгера - ОтелПровайдерЛогирования.ПолучитьЛоггер() (ОтелПровайдерЛогирования.os:60) и ПостроительЛоггера().Построить() (ОтелПостроительЛоггера.os:62-64), который делегирует в Провайдер.ПолучитьЛоггер(); класс задокументирован комментарием «Получается из ОтелПровайдерЛогирования». Ограничение платформы, аналогичное уже задокументированному для Span/Counter/Histogram (docs/spec-compliance.md, например строка 891). |
| 6 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60-108` |  |
| 7 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-76,95-99; src/Логирование/Классы/ОтелЛоггер.os:308-310,334-341` |  |
| 8 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:65-76; tests/unit/Логирование/ТестПровайдерЛогирования.os:350-366,403-419` |  |
| 9 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:53-56; src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-76` |  |
| 10 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:65-68` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors [...]) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:11-23,317-339` |  |
| 12 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:207-219,292-297; src/Логирование/Классы/ОтелЛоггер.os:161-163` |  |
| 13 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:135-137; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:47-58` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159; tests/unit/Логирование/ТестПровайдерЛогирования.os:369-400` |  |
| 15 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:70-74; src/Логирование/Классы/ОтелЛоггер.os:66-68,135-137` |  |
| 16 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159,196-199; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,215-236` |  |
| 17 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,159-177,192-202` |  |
| 18 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:152-159; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-54,69-76` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138-140,171-188; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40` |  |
| 20 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:18-28; src/Ядро/Классы/ОтелРезультатЗакрытия.os:14-22` |  |
| 21 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:9-16; src/Ядро/Классы/ОтелРезультатЗакрытия.os:14-22` |  |
| 22 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138-140,273-275; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,159-177` |  |
| 23 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:273-275; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:112-131` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:130-133` |  |
| 25 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the `LogRecord` with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:128,264-275` |  |
| 26 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:277-281` |  |
| 27 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:277-281` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | `Enabled` MUST return `false` when either: there are no registered `LogRecordProcessors`; [...] all registered `LogRecordProcessors` implement `Enabled`, and a call to `Enabled` on each of them returns `false`. | `src/Логирование/Классы/ОтелЛоггер.os:60-90; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101` |  |
| 29 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101; src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:34-42` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:55-170,377-389` |  |
| 31 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the `LogRecord`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:141-152` |  |
| 32 | MUST | ✅ found | The trace context fields MUST be populated from the resolved `Context` (either the explicitly passed `Context` or the current `Context`) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:108-120` |  |
| 33 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:159-161,244-248; src/Экспорт/Классы/ОтелЭкспортерЛогов.os:257; src/Экспорт/Классы/ОтелПротоКодировщикLogs.os:158-161` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: `Timestamp`, `ObservedTimestamp`, `SeverityText`, `SeverityNumber`, `Body... | `src/Логирование/Классы/ОтелЗаписьЛога.os:188-195,205-211,222-228,239-253,265-271,282-289,299-305,315-321,331-337,347-353` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | MUST | ✅ found | `LogRecord` attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:249-251; src/Ядро/Модули/ОтелУтилиты.os:406` |  |
| 36 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the `LoggerProvider`, by allowing users to configure individual limits like in the Java exam... | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:41-53; src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:19-80` |  |
| 37 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `LogRecordLimits`. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1-103` |  |
| 38 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:427-432` |  |
| 39 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per `LogRecord` (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:36,246,427-432,454` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:165-170; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:429-449; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:47-58` |  |
| 41 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1-77; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:47-58; tests/unit/Логирование/fixtures/ИзменяющийПараметрыПроцессорЛогов.os:1-33` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 42 | SHOULD NOT | ✅ found | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:5-8, src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:39-56, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:41-69` |  |
| 43 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:21-29, src/Логирование/Классы/ОтелПровайдерЛогирования.os:115-117,333` |  |
| 44 | SHOULD | ✅ found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | `src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:13-21` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ✅ found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:19-42, src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101, src/Логирование/Классы/ОтелЛоггер.os:72-90` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:109-117, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114` |  |
| 47 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:39-42, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-51` |  |
| 48 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:56-67, src/Ядро/Модули/ОтелРезультатыЗакрытия.os:1-37` |  |
| 49 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:109-117, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114` |  |
| 50 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:109-117, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114, src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as pos... | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:91-97, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |
| 52 | SHOULD | ✅ found | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFl... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217, src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:91-97` |  |
| 53 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:91-97, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217` |  |
| 54 | MUST | ✅ found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-210` |  |
| 55 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:44-54, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81` |  |
| 56 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcesso... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance) о том, в каких случаях следует вызывать ForceFlush; SDK не может программно ограничить, когда пользователь вызывает ForceFlush. |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1-173, src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:1-71` |  |
| 59 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `src/Логирование/Классы/` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:43-55` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:29-31, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:231-252` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:6-7` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:14,26,35` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34-53` |  |
| 65 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34-53` |  |
| 66 | SHOULD NOT | ✅ found | The default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:39-56; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:263-279` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning fr... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:91-97` |  |
| 68 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-29` |  |
| 69 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports t... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance) о том, в каких случаях стоит вызывать ForceFlush; SDK не может программно ограничить, когда пользователь или инструментированное приложение решает вызвать этот метод. |
| 70 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:109-117; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121` |  |
| 72 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34-37,74-77` |  |
| 73 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:74-77` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60-108,138-140,152-160,334-336` |  |
| 75 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:7,60-141,324` |  |
| 76 | MUST | ✅ found | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:1,6-7,12,64-77,128` |  |

### Metrics Api

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:175-177,185-194` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `MeterProvider` MUST provide the following functions: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:61-128` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76-80` |  |
| 4 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:78` |  |
| 5 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:80` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:79; src/Ядро/Классы/ОтелОбластьИнструментирования.os:164` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Note: `Meter` SHOULD NOT be responsible for the configuration. | `src/Метрики/Классы/ОтелМетр.os:56-257 (public API limited to Create* instrument functions); src/Метрики/Классы/ОтелПровайдерМетрик.os:262-360 (View/reader/aggregation/configurator configuration owned by MeterProvider and pushed down)` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The `Meter` MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:80-82 (СоздатьСчетчик/Counter), 180-184 (СоздатьНаблюдаемыйСчетчик/Async Counter), 96-98 (СоздатьГистограмму/Histogram), 146-148 (СоздатьДатчик/Gauge), 251-255 (СоздатьНаблюдаемыйДатчик/Async Gauge), 131-133 (СоздатьРеверсивныйСчетчик/UpDownCounter), 216-220 (СоздатьНаблюдаемыйРеверсивныйСчетчик/Async UpDownCounter)` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ➖ n_a | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:1136-1147 (НайтиЗарегистрированныйИнструмент), 1272-1280 (ЗарегистрироватьДескриптор), 1305-1315 (ПроверитьКонфликтДескриптора)` | Ограничение платформы OneScript: единственный числовой тип - Число (System.Decimal), языкового различия integer/floating point не существует. API не предоставляет типизированных вариантов инструментов (нет аналога Java LongCounter/DoubleCounter) - СоздатьСчетчик/СоздатьГистограмму/СоздатьДатчик и т.д. не принимают параметр числового типа, поэтому такому признаку физически неоткуда взяться. Идентичность инструмента определяется по имени, виду, единице измерения, описанию и advisory (ЗарегистрироватьДескриптор/ПроверитьКонфликтДескриптора) - вид инструмента (Counter/Histogram/...) уже жёстко определяет представление данных (int/double при экспорте в OTLP), так что расщеплять его дополнительно по числовому типу нечем. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:620-621,631 (ЕдиницаИзмерения = НормализоватьСтроку(ЕдиницаИзмерения) - хранится и передаётся как есть, без семантического разбора)` |  |
| 11 | MUST | ✅ found | It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:620-621 (нет НРег/ВРег над ЕдиницаИзмерения), 1268-1270 (КлючПроходаНасквозь использует ЕдиницаИзмерения как есть, без приведения регистра)` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:9-10,50-52; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:9-10,62-64` |  |
| 13 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:9-10,50-52 (платформенная гарантия: Строка = .NET System.String, полный Unicode)` |  |
| 14 | MUST | ✅ found | It MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:9-10,50-52 (платформенная гарантия: длина строки до 2^31 символов)` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:1551-1597 (ПроверитьСовет); src/Метрики/Модули/ОтелПотокиМетрик.os:401 (ExplicitBucketBoundaries/ГраницыГистограммы применяются при разрешении потоков)` |  |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:80-148 (СоздатьСчетчик/СоздатьГистограмму/СоздатьРеверсивныйСчетчик/СоздатьДатчик: Имя, Описание, ЕдиницаИзмерения, Совет)` |  |
| 17 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (Имя - обязательный позиционный параметр без значения по умолчанию)` |  |
| 18 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:63-69 (doc-комментарий над СоздатьСчетчик); Имя дополнительно обязательно структурно (позиционный параметр)` |  |
| 19 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:63-69,1040-1063 (doc-комментарий + рантайм-предупреждение ВалидироватьИмяИнструмента с текстом regex)` |  |
| 20 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:1054-1063 (ВалидироватьИмяИнструмента)` |  |
| 21 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (ЕдиницаИзмерения = "" по умолчанию)` |  |
| 22 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:80 (ЕдиницаИзмерения - Строка, платформенная гарантия; значение хранится и сравнивается регистрозависимо)` |  |
| 23 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:1033-1038 (НормализоватьСтроку - только Неопределено->"", без иной валидации содержимого)` |  |
| 24 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (Описание = "" по умолчанию)` |  |
| 25 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:80 (Описание - Строка, платформенная гарантия полного Unicode и длины)` |  |
| 26 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (Совет = Неопределено по умолчанию)` |  |
| 27 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:1551-1597 (ПроверитьСовет - мягкая SDK-уровневая проверка: warning + очистка невалидных полей, без отклонения регистрации)` |  |
| 28 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:180-255 (СоздатьНаблюдаемыйСчетчик/СоздатьНаблюдаемыйРеверсивныйСчетчик/СоздатьНаблюдаемыйДатчик: Имя, Callback, Описание, ЕдиницаИзмерения, Совет)` |  |
| 29 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Имя - обязательный позиционный параметр)` |  |
| 30 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:63-69,1040-1063; Имя обязательно структурно и в async-создателях` |  |
| 31 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:658,1040-1063 (ВалидироватьИмяИнструмента вызывается из СоздатьАсинхронныйИнструмент с тем же текстом regex в предупреждении)` |  |
| 32 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:658,1054-1063 (та же мягкая SDK-уровневая валидация имени, что и для sync)` |  |
| 33 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (ЕдиницаИзмерения = "" по умолчанию)` |  |
| 34 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:180 (ЕдиницаИзмерения - Строка, платформенная гарантия)` |  |
| 35 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:1033-1038,659-660 (НормализоватьСтроку - без валидации содержимого)` |  |
| 36 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Описание = "" по умолчанию)` |  |
| 37 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:180 (Описание - Строка, платформенная гарантия)` |  |
| 38 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Совет = Неопределено по умолчанию)` |  |
| 39 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:669 (Совет = ПроверитьСовет(Совет, Вид) - та же мягкая проверка, что и для sync)` |  |
| 40 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:499-527 (Callback: Неопределено / одиночное Действие / Массив)` |  |
| 41 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:511-522 (callback-и из конструктора добавляются в Действия навсегда)` |  |
| 42 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127-143 (ДобавитьCallback)` |  |
| 43 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by s... | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14-20 (Закрыть); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:151-163 (УдалитьCallback)` |  |
| 44 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:389-409 (ВызватьCallbackи - снимок списка, каждый callback вызывается ровно один раз перед формированием данных)` |  |
| 45 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелМетр.os:157-170; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:109-118 (doc-комментарии перечисляют reentrant/no-indefinite-time/no-duplicates)` |  |
| 46 | SHOULD | ✅ found | Callback functions SHOULD be reentrant safe. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:109-113,254-275 (задокументировано; SDK вызывает callback-и отдельно на каждый читатель через СобратьДляЧитателя)` |  |
| 47 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT take an indefinite amount of time. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:88-146 (ВызватьСТаймаутом); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:349-364 (ТаймаутCallbackМс, по умолчанию 30000мс у инструментов метра)` | Реализован только soft-timeout: SDK перестает ждать callback и отбрасывает результат по истечении таймаута, но платформа OneScript не позволяет прервать ФоновоеЗадание (нет Прервать()/ОтменитьЗадание(), см. https://github.com/EvilBeaver/OneScript/issues/1672) - зависший callback продолжает выполняться в фоне до собственного завершения. |
| 48 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | `src/Метрики/Классы/ОтелМетр.os:161-164 (задокументировано в doc-комментарии); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:299-322 (ДобавитьНаблюдение агрегирует наблюдения с одинаковыми атрибутами в одну серию, не нарушая сбор)` |  |
| 49 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:511-522 (Callback конструктора регистрируется только в Действия этого инструмента)` |  |
| 50 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:71-82 (ВызватьМультиCallback - Соответствие Имя инструмента -> ОтелНаблюдениеМетрики)` |  |
| 51 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:529-557 (ЗарегистрироватьОбратныйВызов: проверка ПринадлежитМетру и ЭтоАсинхронныйИнструмент для каждого инструмента набора при регистрации)` |  |
| 52 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:389-409 (одно ВремяНаблюдения на все записи одного вызова callback-а)` |  |
| 53 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелМетр.os:771-791 (ВыполнитьОднуРегистрацию - одно ВремяНаблюдения на все инструменты одного мульти-callback)` |  |
| 54 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:53-61 (Состояние передается в Callback.Выполнить); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127 (ДобавитьCallback принимает Состояние)` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: * Report if instrument is `Enabled` | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253 (Функция Включен)` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 56 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:232-253 (Функция Включен(Атрибуты = Неопределено))` |  |
| 57 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250 (параметр Атрибуты зарезервирован для расширяемости)` |  |
| 58 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253 (возвращает Булево)` |  |
| 59 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:237-241 (doc-комментарий)` |  |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелСчетчик.os:70-73` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен/Экспорт): технически «Новый ОтелСчетчик()» вызываем напрямую из любого кода. Однако результат нефункционален - поле Родитель (аннотация &Родитель, extends-паттерн библиотеки extends) устанавливается только через ПостроительНаследника(...).Построить(), который использует исключительно ОтелМетр.СоздатьСчетчик(); при прямом вызове Родитель остается Неопределено, и любой вызов Добавить() упадет с исключением. Единственный документированный и работающий способ создания Counter - ОтелМетр.СоздатьСчетчик(). Ограничение платформы аналогично отсутствию приватных конструкторов у Span (см. правила n_a про приватные конструкторы). |

#### Counter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:34` |  |
| 62 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелСчетчик.os:34` |  |
| 63 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:34` |  |
| 64 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:30` |  |
| 65 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:30` |  |
| 66 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:35-41` |  |
| 67 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:34; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76` |  |
| 68 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:34; src/Метрики/Классы/ОтелМетр.os:80-82` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous Counter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:180` | Аналогично требованию Trace API «Span MUST NOT be created directly» (там же n_a) - OneScript не поддерживает приватные конструкторы: ПриСозданииОбъекта класса всегда публичен, поэтому Новый ОтелНаблюдаемыйСчетчик() вызываем языковыми средствами напрямую. Единственная предусмотренная в SDK фабрика асинхронного Counter - ОтелМетр.СоздатьНаблюдаемыйСчетчик() (src/Метрики/Классы/ОтелМетр.os:180-184); в ОтелПровайдерМетрик и ОтелГлобальный других фабрик асинхронных инструментов нет. Классы ОтелНаблюдаемыйСчетчик (lib.config:85) и ОтелБазовыйНаблюдаемыйИнструмент (lib.config:115) зарегистрированы с публичным ПриСозданииОбъекта (платформенное ограничение), но собранный в обход Meter объект без связывания через ПостроительНаследника (Родитель не установлен) нефункционален. |
| 70 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:396-401 (одиночный callback); src/Метрики/Классы/ОтелМетр.os:778-784 (мульти-callback)` |  |
| 71 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:396-401 (одиночный callback); src/Метрики/Классы/ОтелМетр.os:778-784 (мульти-callback)` |  |
| 72 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127; src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:53-59` |  |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Histogram` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:96` | Аналогично требованию Trace API «Span MUST NOT be created directly» (там же n_a) - OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Единственные фабрики Histogram в SDK - ОтелМетр.СоздатьГистограмму() (src/Метрики/Классы/ОтелМетр.os:96-98) и ОтелМетр.СоздатьЭкспоненциальнуюГистограмму() (ОтелМетр.os:115-120); в ОтелПровайдерМетрик/ОтелГлобальный других фабрик нет. Классы ОтелГистограмма (lib.config:76) и ОтелБазовыйСинхронныйИнструмент (lib.config:114) зарегистрированы с публичным ПриСозданииОбъекта (платформенное ограничение), но созданный в обход Meter объект без связывания через ПостроительНаследника (Родитель не установлен) нефункционален. |

#### Histogram operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелГистограмма.os:31` |  |
| 75 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелГистограмма.os:31` |  |
| 76 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:31` |  |
| 77 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:27` |  |
| 78 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелГистограмма.os:27` |  |
| 79 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:31-32` |  |
| 80 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:31; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Gauge` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:146` | Аналогично требованию Trace API «Span MUST NOT be created directly» (там же n_a) - OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Единственная фабрика Gauge в SDK - ОтелМетр.СоздатьДатчик() (src/Метрики/Классы/ОтелМетр.os:146-148); в ОтелПровайдерМетрик/ОтелГлобальный других фабрик нет. Классы ОтелДатчик (lib.config:84) и ОтелБазовыйСинхронныйИнструмент (lib.config:114) зарегистрированы с публичным ПриСозданииОбъекта (платформенное ограничение), но созданный в обход Meter объект без связывания через ПостроительНаследника (Родитель не установлен) нефункционален. |

#### Gauge operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 84 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 85 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:17` |  |
| 86 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76` |  |
| 87 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21; src/Метрики/Классы/ОтелМетр.os:146-148` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous Gauge other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:251` | Аналогично требованию Trace API «Span MUST NOT be created directly» (там же n_a) - OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Единственная фабрика Asynchronous Gauge в SDK - ОтелМетр.СоздатьНаблюдаемыйДатчик() (src/Метрики/Классы/ОтелМетр.os:251-255); в ОтелПровайдерМетрик/ОтелГлобальный других фабрик нет. Классы ОтелНаблюдаемыйДатчик (lib.config:88) и ОтелБазовыйНаблюдаемыйИнструмент (lib.config:115) зарегистрированы с публичным ПриСозданииОбъекта (платформенное ограничение), но собранный в обход Meter объект без связывания через ПостроительНаследника (Родитель не установлен) нефункционален. |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:131` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); ограничение документировано в коде (аналогично ОтелСпан.os) и docs/spec-compliance.md. Помимо этого платформенного ограничения, других документированных API создания UpDownCounter нет: единственная фабрика - ОтелМетр.СоздатьРеверсивныйСчетчик() (ОтелМетр.os:133-135). Классы-фасады ОтелРеверсивныйСчетчик (lib.config:75) и ОтелБазовыйСинхронныйИнструмент (lib.config:114) зарегистрированы с публичным ПриСозданииОбъекта, поэтому технически инструмент можно собрать в обход Meter через Новый ОтелБазовыйСинхронныйИнструмент(...) + ПостроительНаследника (так и делают тесты, напр. tests/unit/Метрики/ТестВременнаяАгрегация.os:273); голый Новый ОтелРеверсивныйСчетчик() без родителя нефункционален (переменная Родитель не инициализирована). |

#### UpDownCounter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 91 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 92 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 93 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:17` |  |
| 94 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:216` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); ограничение документировано в коде (аналогично ОтелСпан.os) и docs/spec-compliance.md. Единственная документированная фабрика создания ObservableUpDownCounter - ОтелМетр.СоздатьНаблюдаемыйРеверсивныйСчетчик() (ОтелМетр.os:218-222). Классы-фасады ОтелНаблюдаемыйРеверсивныйСчетчик (lib.config:87) и ОтелБазовыйНаблюдаемыйИнструмент (lib.config:115) зарегистрированы с публичным ПриСозданииОбъекта, поэтому технически инструмент можно собрать в обход Meter через Новый ОтелБазовыйНаблюдаемыйИнструмент(...) + ПостроительНаследника (тесты создают базовый инструмент напрямую, напр. tests/unit/Метрики/ТестБазовыйНаблюдаемыйИнструмент.os:24); голый Новый ОтелНаблюдаемыйРеверсивныйСчетчик() без родителя нефункционален. |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: | `src/Метрики/Классы/ОтелМетр.os:529` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:186-210; src/Метрики/Классы/ОтелПостроительМетра.os:26-55` |  |
| 98 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21; src/Метрики/Классы/ОтелМетр.os:80` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:41-42` |  |
| 100 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:58-59` |  |
| 101 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:33-34; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:43-46` |  |

### Metrics Sdk

#### Metrics SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metrics-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:468` |  |

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:28 (УстановитьРесурс); src/Метрики/Классы/ОтелПровайдерМетрик.os:483,489-493 (конструктор принимает Ресурс)` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелМетр.os:451-454 (Ресурс передаётся в Инструмент.СобратьДляЧитателя); src/Метрики/Классы/ОтелДанныеМетрики.os:208,217 (Ресурс - обязательный параметр данных метрики)` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:483-523 (всё состояние - переменные экземпляра, нет статики/синглтона); tests/unit/Метрики/ТестПровайдерМетрик.os (десятки независимых экземпляров провайдера в тестах)` |  |

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелМетр.os:1005` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Формально `Новый ОтелМетр(...)` можно вызвать напрямую, минуя MeterProvider - это ограничение платформы, а не архитектурное решение. Предусмотренный и документированный путь создания Meter - `ОтелПровайдерМетрик.ПолучитьМетр()` / `ПостроительМетра()` (аналогично ограничению для Span, см. docs/spec-compliance.md). |
| 6 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76-128 (ПолучитьМетр)` |  |
| 7 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:86-87,105-106; src/Ядро/Классы/ОтелОбластьИнструментирования.os:164-169; src/Метрики/Классы/ОтелМетр.os:901-903,1008 (УстановитьОбластьИнструментирования)` |  |
| 8 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:81-97,124-127 (проверка невалидного имени не прерывает создание, возвращается рабочий Метрика, а не Неопределено/исключение)` |  |
| 9 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ... | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:108-110,164-169 (УстановитьИмя сохраняет исходное значение как есть, включая Неопределено/"")` |  |
| 10 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:81-85 (Лог.Предупреждение о невалидном имени)` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views [...]) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:21-31 (Представления, ЧитателиМетрик - переменные экземпляра провайдера)` |  |
| 12 | MUST | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:269-360 (ЗарегистрироватьПредставление, УстановитьАгрегациюГистограммПоУмолчанию, УстановитьТаймаутОбратныхВызововМс - все проходят по Метрики.Значения() и обновляют уже выданные Meter)` |  |
| 13 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:102-118 (новые метры получают текущую конфигурацию при создании), :269-360 (уже выданные метры обновляются на месте) - поведение не зависит от момента получения Meter` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:191-194 (Закрыт.СравнитьИУстановить - идемпотентность через CAS)` |  |
| 15 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:88-90,456-460 (НоопМетр - после Закрыть возвращается выключенный Meter)` |  |
| 16 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40 (Успешно/ИстекТаймаут/Описание); src/Метрики/Классы/ОтелПровайдерМетрик.os:221 (Закрыть возвращает ОтелРезультатЗакрытия)` |  |
| 17 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:191-222 (Закрыть принимает ТаймаутМс); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:142-168 (Закрыть, Обещание.Получить с таймаутом на строке 152)` | Закрыть принимает ТаймаутМс и распределяет оставшееся время между читателями. Читатель ждёт фоновое задание периодического сбора через Обещание.Получить(timeout) - это soft-timeout: при истечении ожидание прекращается и результат отбрасывается, но само ФоновоеЗадание не может быть принудительно прервано (OneScript не поддерживает Прервать()/ОтменитьЗадание(), см. EvilBeaver/OneScript#1672) и продолжает выполняться в фоне. Вызывающий получает управление вовремя, но полное завершение операции внутри таймаута не гарантировано. |
| 18 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:207-220 (цикл по ЧитателиМетрик, вызов Закрыть у каждого); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:164-166 (читатель вызывает Закрыть у своего Экспортер)` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:375-386` |  |
| 20 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:179-181; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:18-39` |  |
| 21 | SHOULD | ✅ found | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model E... | `src/Ядро/Модули/ОтелРезультатыЭкспорта.os:18-39` |  |
| 22 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:451-470; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:192-202` |  |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:162-181; src/Метрики/Классы/ОтелПровайдерМетрик.os:269-291` |  |
| 24 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:269 (ЗарегистрироватьПредставление(Селектор, Представление))` |  |
| 25 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:269-291` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37-65` |  |
| 27 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164-174` |  |
| 28 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:40-42` |  |
| 29 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164 (Имя = Неопределено)` |  |
| 30 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164 (ТипИнструмента = Неопределено)` |  |
| 31 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:165 (Единица = Неопределено)` |  |
| 32 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:165 (ИмяМетра = Неопределено)` |  |
| 33 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:166 (ВерсияМетра = Неопределено)` |  |
| 34 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:166 (АдресСхемыМетра = Неопределено)` |  |
| 35 | MUST NOT | ✅ found | Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:1-177 (весь класс - дополнительные критерии не реализованы, обязательности нет ни для одного из 6 критериев)` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:162-181` |  |
| 37 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:328-331` |  |
| 38 | SHOULD | ✅ found | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелМетр.os:823-846 (ПроверитьУзостьСелектораView)` |  |
| 39 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:163 (НовоеИмя = Неопределено)` |  |
| 40 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Модули/ОтелПотокиМетрик.os:258-262,328-331` |  |
| 41 | MUST NOT | ✅ found | The `name` provided via stream configuration is NOT REQUIRED to conform to the instrument name syntax, and the SDK MUST NOT validate it against that syntax. | `src/Метрики/Модули/ОтелПотокиМетрик.os:326-354; src/Метрики/Классы/ОтелМетр.os:619,658,1054 (ВалидироватьИмяИнструмента применяется только к имени инструмента, не к View.НовоеИмя)` |  |
| 42 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:332-334` |  |
| 43 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164 (НовоеОписание = Неопределено)` |  |
| 44 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Модули/ОтелПотокиМетрик.os:258-262,332-334` |  |
| 45 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:22-56` |  |
| 46 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:22-56` |  |
| 47 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:165 (РазрешенныеКлючиАтрибутов = Неопределено)` |  |
| 48 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:22-28 (Обработать - при Разрешенные=Неопределено и Исключенные=Неопределено возвращаются все атрибуты)` |  |
| 49 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:51-58,108-110 (ИсключенныеКлючиАтрибутов)` |  |
| 50 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:51-56 (КлючСохраняется)` |  |
| 51 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:51-56 (КлючСохраняется)` |  |
| 52 | SHOULD | ✅ found | SDK documentation SHOULD inform users that attributes excluded from a metric stream by View configuration may still be exported on Exemplars as filtered attributes, and describe how to disable or othe... | `src/Метрики/Классы/ОтелПредставление.os:142-145 (комментарий-документация класса View)` |  |
| 53 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:167 (Агрегация = Неопределено)` |  |
| 54 | MUST | ✅ found | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Модули/ОтелПотокиМетрик.os:367-370,415-443 (АгрегацияЧитателя); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302-318 (АгрегацияПоУмолчанию)` |  |
| 55 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:169 (РезервуарЭкземпляров = Неопределено)` |  |
| 56 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Модули/ОтелПотокиМетрик.os:482-486; src/Метрики/Модули/ОтелАгрегация.os:254-266 (ФабрикаРезервуаровПоУмолчанию)` |  |
| 57 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:170 (ЛимитМощностиАгрегации = Неопределено)` |  |
| 58 | MUST | ✅ found | If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with. | `src/Метрики/Модули/ОтелПотокиМетрик.os:378-380,455-468 (ЛимитМощностиЧитателя)` |  |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Модули/ОтелПотокиМетрик.os:111-125,218-232 (СоздатьХранилища, ПотокиЧитателя)` |  |
| 60 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Модули/ОтелПотокиМетрик.os:356-382,394-402 (ЗавершитьПоток, ГраницыПотока - ЗначениеСовета)` |  |
| 61 | SHOULD | ✅ found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | `src/Метрики/Классы/ОтелМетр.os:848-891 (ЗарегистрироватьИменаПотоков, ПредупредитьОКонфликтеПотоков)` |  |
| 62 | SHOULD | ✅ found | If applying the View would produce semantic errors (for example, configuring an asynchronous instrument to use the Explicit bucket histogram aggregation), the implementation SHOULD emit a warning and ... | `src/Метрики/Модули/ОтелПотокиМетрик.os:288-314,246-256 (ПрименитьАгрегацию, ПотокПредставления)` |  |
| 63 | MUST | ✅ found | If both the View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Модули/ОтелПотокиМетрик.os:366-382,394-402 (ЗавершитьПоток, ГраницыПотока - advisory применяется только как fallback)` |  |
| 64 | SHOULD | ✅ found | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Модули/ОтелПотокиМетрик.os:218-232 (ПотокиЧитателя - ветка без совпавших View)` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:15-65,215-240 (Drop/Default/Sum/LastValue/ExplicitBucketHistogram, СоздатьАгрегаторПотока)` |  |
| 66 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: | `src/Метрики/Модули/ОтелАгрегация.os:76-81,232-237; src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD NOT | ✅ found | This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:64-68 (Записать); src/Метрики/Модули/ОтелАгрегация.os:216-218 (СобиратьSum = НЕ ЗаписываетОтрицательные(Вид))` |  |
| 68 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release... | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:172-190,262-266 (СтандартныеГраницы)` |  |
| 69 | SHOULD NOT | ➖ n_a | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | - | Ограничение платформы OneScript: Число = System.Decimal (не IEEE 754) - значения NaN, +Inf, -Inf физически непредставимы в типе Число, арифметические операции, которые в IEEE 754 дали бы такие значения, в OneScript выбрасывают исключение. SDK не может получить такие значения для записи в аккумулятор гистограммы, поэтому требование не может быть ни нарушено, ни осмысленно проверено на этой платформе. |
| 70 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302-308 (МинимальнаяШкала=-10), 395-408 (НачальнаяШкала=MaxScale)` |  |
| 71 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:123-127 (СформироватьТочкуДанных: count<=1 -> scale=НачальнаяШкала)` |  |
| 72 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:231-259,302-312 (ПонизитьШкалуПриНеобходимости, ПонизитьШкалуНа1)` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ✅ found | Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during co... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:254-275 (СобратьДляЧитателя); src/Метрики/Классы/ОтелМетр.os:439-470 (СобратьДляЧитателя)` |  |
| 74 | SHOULD | ✅ found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180-200 (ДобавитьВнешниеНаблюдения - проверка флага ВыполняетсяCallback)` |  |
| 75 | SHOULD | ✅ found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:108-146 (ВызватьСТаймаутом)` |  |
| 76 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:389-409 (ВызватьCallbackи - синхронный цикл); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:33-35,386-398 (БлокировкаСбора сериализует сборы)` |  |
| 77 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:251-266 (СгруппироватьНаблюдения - серии строятся заново из текущих Группы на каждом сборе)` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:224-240; src/Метрики/Классы/ОтелПредставление.os:92-93; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:257-280` |  |
| 79 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,305-319` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92-93,112-113,170-180; src/Метрики/Модули/ОтелПотокиМетрик.os:338-340,366-382` |  |
| 81 | SHOULD | ✅ found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:257-280; src/Метрики/Модули/ОтелПотокиМетрик.os:378-380,455-468` |  |
| 82 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:25-36; src/Метрики/Классы/ОтелХранилищеМетрики.os:537-538; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:745-764` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:305-319,521-525` |  |
| 84 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:305-319` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:139-153,350-378` |  |
| 86 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an ... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,305-319` |  |
| 87 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,305-319` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | SHOULD | ✅ found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:251-266,299-322` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:1005-1031; src/Метрики/Классы/ОтелПровайдерМетрик.os:76-128` |  |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:1136-1147,1230-1266` |  |
| 91 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:1282-1359 (ПроверитьКонфликтДескриптора)` |  |
| 92 | SHOULD | ✅ found | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:1683-1726 (ПостроитьРецептРазрешенияКонфликта)` |  |
| 93 | SHOULD | ✅ found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | `src/Метрики/Классы/ОтелМетр.os:1336-1341,1666-1681 (ОписаниеЗаданоЧерезView)` |  |
| 94 | SHOULD | ✅ found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | `src/Метрики/Классы/ОтелМетр.os:1700-1713 (ПостроитьРецептРазрешенияКонфликта, ветка Конфликт.Вида)` |  |
| 95 | SHOULD | ✅ found | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:1230-1266 (pass-through в ИнструментыПроходНасквозь),1282-1359 (предупреждение)` |  |
| 96 | MUST | ✅ found | To accommodate the recommendations from the data model, the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:1136-1147 (НайтиЗарегистрированныйИнструмент)` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:1160-1166 (ИмяПервойРегистрации),1311-1319 (лог конфликта регистра)` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax | `src/Метрики/Классы/ОтелМетр.os:1054-1093 (ВалидироватьИмяИнструмента, ИмяИнструментаВалидно)` |  |
| 99 | SHOULD | ✅ found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | `src/Метрики/Классы/ОтелМетр.os:1058-1062` |  |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:621,660,1033-1038 (НормализоватьСтроку - только null-коалесценция, без валидации формата/длины)` |  |
| 101 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:1033-1038 (НормализоватьСтроку); значения по умолчанию ЕдиницаИзмерения="" в СоздатьСчетчик и др.` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 102 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:620,659,1033-1038 (только нормализация, нет проверки содержимого/длины описания)` |  |
| 103 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:1033-1038 (НормализоватьСтроку); значения по умолчанию Описание="" в СоздатьСчетчик и др.` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 104 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:1551-1597 (ПроверитьСовет)` |  |
| 105 | SHOULD | ✅ found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:1566-1594 (Лог.Предупреждение + сброс поля в Неопределено внутри ПроверитьСовет)` |  |
| 106 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described... | `src/Метрики/Классы/ОтелМетр.os:1136-1147 (НайтиЗарегистрированныйИнструмент),1465-1471 (ЕстьНесовместимыйКонфликт - Совет не делает конфликт несовместимым),1282-1359 (лог конфликта)` |  |
| 107 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Модули/ОтелПотокиМетрик.os:366-402 (ЗавершитьПоток, ГраницыПотока - границы View приоритетнее advisory),252-253,375-376 (ключи атрибутов View приоритетнее advisory)` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:384-402 (ГраницыПотока: без границ View и без агрегации из View - используются advisory-границы)` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 109 | MUST | ✅ found | The synchronous instrument `Enabled` MUST return `false` when [...] all resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:322-333 (ВсеПотокиОтбрасывают, drop-агрегация)` |  |
| 110 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253 (Включен)` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-84; src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,460-471; src/Метрики/Модули/ОтелАгрегация.os:254-266` |  |
| 112 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:547-548; src/Метрики/Классы/ОтелПровайдерМетрик.os:498-501` |  |
| 113 | MUST NOT | ⚠️ partial | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-61,321-328,440-445` | Оверхед на горячем пути (per-measurement) действительно устраняется: ЗахватитьЭкземпляр = ЕстьРезервуар() И ОтелФильтрЭкземпляров.ДолженЗахватить(...) вычисляется до блокировки, и при ФильтрЭкземпляров=ВсегдаВыключен() ДолженЗахватить сразу возвращает Ложь (ОтелФильтрЭкземпляров.os:69-71), так что ПредложитьЭкземпляр (аллокация структуры экземпляра, вычисление filteredAttributes, RNG) не вызывается. Но per-series оверхед не устранён: ФабрикаРезервуаров по умолчанию не становится Неопределено при выключенном фильтре, поэтому НоваяСерия (ОтелХранилищеМетрики.os:321-328) всё равно создаёт полноценный объект ОтелРезервуарЭкземпляров (с СинхронизированнаяКарта x2, ГенераторСлучайныхЧисел, БлокировкаРесурса) для каждой новой серии атрибутов, даже если ни один exemplar никогда не будет захвачен. Единственный способ полностью убрать этот оверхед - явно задать ОтелФабрикаNoopРезервуаров на View, что не происходит автоматически при ФильтрЭкземпляров=ВсегдаВыключен(). |
| 114 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Модули/ОтелАгрегация.os:254-266` |  |
| 115 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: ExemplarFilter and ExemplarReservoir. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:65-77,114-129; src/Метрики/Классы/ОтелПредставление.os:15-16,78-85,128-130,156,169,179` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 116 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77,114-129; src/Метрики/Модули/ОтелФильтрЭкземпляров.os:39-52; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:673-687` |  |
| 117 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77; src/Метрики/Классы/ОтелПровайдерМетрик.os:483-502` |  |
| 118 | SHOULD | ✅ found | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:498-501; src/Метрики/Модули/ОтелФильтрЭкземпляров.os:26-29; src/Конфигурация/Классы/ОтелКонфигурацияПровайдераМетрик.os:22` |  |
| 119 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:892-900; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:673-687; src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:347` |  |
| 120 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-29` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-120; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50-102; src/Метрики/Классы/ОтелНоопРезервуарЭкземпляров.os:20-39` |  |
| 122 | MUST | ✅ found | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:316-328,440-445; src/Метрики/Модули/ОтелАгрегация.os:254-266` |  |
| 123 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the res... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39-56` |  |
| 124 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the res... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:460-471; src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-56,176-197` |  |
| 125 | MUST | ✅ found | The “collect” method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:104-120; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:84-102` |  |
| 126 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:226-249; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:246-269` |  |
| 127 | SHOULD | ✅ found | The “offer” method SHOULD accept measurements, including: the value, the complete set of Attributes, the Context (Baggage and current active Span), and a timestamp of the measurement. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-56; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50-54` |  |
| 128 | SHOULD | ✅ found | The “offer” method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:199-224; src/Метрики/Классы/ОтелХранилищеМетрики.os:460-483` |  |
| 129 | SHOULD | ✅ found | In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:92-111,139-153,380-390` |  |
| 130 | SHOULD | ✅ found | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:30-37,61-93` |  |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 131 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: `SimpleFixedSizeExemplarReservoir` and `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:255-277; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:275-289` |  |
| 132 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Модули/ОтелАгрегация.os:259-261` |  |
| 133 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. `min(20, max_buckets)`). | `src/Метрики/Модули/ОтелАгрегация.os:255,262-263` |  |
| 134 | SHOULD | ✅ found | All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Модули/ОтелАгрегация.os:264-265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:61-93` |  |
| 136 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:321-328,380-390,426-438` |  |
| 137 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Модули/ОтелАгрегация.os:265; src/Метрики/Классы/ОтелХранилищеМетрики.os:548; src/Метрики/Классы/ОтелФабрикаПростыхРезервуаров.os:46-48` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 138 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелФабрикаВыровненныхРезервуаровГистограммы.os:20-22,46-48; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:281-287` |  |
| 139 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has se... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:154-161,172-179` |  |
| 140 | SHOULD | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has se... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:132-143` |  |
| 141 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Модули/ОтелАгрегация.os:259-261; src/Метрики/Классы/ОтелФабрикаВыровненныхРезервуаровГистограммы.os:20-22` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:15-16,78-85,128-130,156,169,179; src/Метрики/Модули/ОтелПотокиМетрик.os:559-566` |  |
| 143 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелПредставление.os:156,169,179; src/Метрики/Модули/ОтелПотокиМетрик.os:341-346,482-484` |  |
| 144 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:316-328,440-445` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 145 | SHOULD | ✅ found | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:749-771` |  |
| 146 | SHOULD | ⚠️ partial | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:284-291,773-785` | Речь о default aggregation: селектор агрегации по умолчанию по виду инструмента задаётся самим читателем (ИнициализироватьСелекторАгрегации/УстановитьАгрегациюПоУмолчанию), а не запрашивается у экспортера. ИнтерфейсЭкспортерМетрик (src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os) не содержит метода получения агрегации по умолчанию - только temporality (ПолучитьВременнуюАгрегацию) действительно берётся из экспортера. |
| 147 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:773-785` |  |
| 148 | SHOULD | ✅ found | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:320-336` |  |
| 149 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:329-336; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:244-261` |  |
| 150 | SHOULD | ✅ found | If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:749-753` |  |
| 151 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1-806` |  |
| 152 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:92-111; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:62-84` |  |
| 153 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:92-104,350-378` |  |
| 154 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:350-378` |  |
| 155 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:43-46,222-240,299-322` |  |
| 156 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. `(T0, T1], (T0, T2], (T0, T3]`). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:356-368; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:279-281` |  |
| 157 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp (e.g. `(T0, T1], (T1, T2], (T2, T3]`). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:356-358; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:235-238,279-281` |  |
| 158 | MUST | ✅ found | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:354,397-398; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:415` |  |
| 159 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:26-27,503-513` |  |
| 160 | SHOULD NOT | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Модули/ОтелПотокиМетрик.os:71-149` |  |
| 161 | MUST NOT | ✅ found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:338-350; src/Метрики/Классы/ОтелПровайдерМетрик.os:462-466` |  |
| 162 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:179-222` |  |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | SHOULD | ✅ found | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:386-398; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:93-115,357-385` |  |
| 164 | SHOULD | ✅ found | `Collect` SHOULD invoke Produce on registered MetricProducers. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:688-725; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:378-414` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 165 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:142-146; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:235-238` |  |
| 166 | SHOULD | ✅ found | SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105-109,123-127; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:358-361` |  |
| 167 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:142-168; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-31` |  |
| 168 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:147-167` | OneScript ФоновоеЗадание не поддерживает жёсткую отмену (только ОжидатьЗавершения(timeout), нет Прервать()/ОтменитьЗадание() - см. issue EvilBeaver/OneScript#1672). Закрыть() реализует soft-timeout: Обещание.Получить(ОставшееcяВремя) перестаёт ждать по истечении срока (перехватывается исключение, пишется debug-лог) и переходит к следующему шагу с оставшимся бюджетом времени, но само фоновое задание периодического сбора/экспорта не прерывается принудительно и может доработать в фоне. Вызывающий получает результат в срок, но операция не 'abort', а лишь перестаёт ожидаться. |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 169 | MUST | ✅ found | When `maxExportBatchSize` is configured, the reader MUST ensure no batch provided to `Export` exceeds the `maxExportBatchSize` by splitting the batch of metric data points into smaller batches. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:543-574` |  |
| 170 | MUST | ✅ found | The initial batch of metric data MUST be split into as many "full" batches of size `maxExportBatchSize` as possible – even if this splits up data points that belong to the same metric into different batches. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:543-574,586-600` |  |
| 171 | MUST | ✅ found | The reader MUST ensure all batches produced from a single `Collect()` are provided to `Export` serially and in-order before metric data points from a subsequent `Collect()` are provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:386-398,451-470` |  |
| 172 | MUST NOT | ✅ found | The reader MUST NOT combine metrics from different `Collect()` calls into the same batch provided to `Export`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:386-398,400-436` |  |
| 173 | MUST | ✅ found | The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:481-504` |  |
| 174 | MUST | ✅ found | If an export is still in progress when the next scheduled interval occurs, the reader MUST either delay the subsequent collection and export until the in-progress export finishes, or skip the scheduled collection for that interval. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:386-398` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 175 | SHOULD | ✅ found | `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each batch serially, and call `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:180-198,787-803` |  |
| 176 | SHOULD | ✅ found | `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call `ForceFlush()` on the configured Push Metric Exporter even if the timeout has passed. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:191-198` |  |
| 177 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:180-198` |  |
| 178 | SHOULD | ✅ found | If any `Export(batch)` call fails or times out, or if the configured exporter's `ForceFlush()` fails or times out, `ForceFlush` SHOULD return some ERROR status. | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-236` |  |
| 179 | SHOULD | ✅ found | If all calls succeed, `ForceFlush` SHOULD return some NO ERROR status. | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-236` |  |
| 180 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:180-198` | Аналогично Shutdown: ПринудительноВыгрузитьСРезультатом задействует Обещание.Получить(timeout) внутри СбросБуфер/СобратьИЭкспортировать и Экспортер.Экспортировать без возможности жёстко отменить фоновое задание (ограничение платформы OneScript - ФоновоеЗадание не имеет Прервать()/ОтменитьЗадание()). Реализован soft-timeout: вызывающий получает результат в срок, но сама операция экспорта может доработать в фоне, а не быть прервана. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 181 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1-47; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:243-249` |  |
| 182 | SHOULD | ✅ found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:163-214` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 183 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1-47; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:38-159` |  |
| 184 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:48-56; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:338-364` |  |
| 185 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48-71` |  |
| 186 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48-71` |  |
| 187 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:154-157` |  |
| 188 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:73-87` |  |
| 189 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:111-127` |  |
| 190 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance: когда пользователю следует вызывать ForceFlush, например в FaaS-окружениях), а не требованием к реализации SDK. SDK не может программно ограничить, в каких случаях вызывающий код решает вызвать ForceFlush. |
| 191 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:73-87,111-127` |  |
| 192 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:89-109` |  |
| 193 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:100-109` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 194 | MUST | ✅ found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:1-46` |  |
| 195 | SHOULD | ✅ found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:5-36; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:602-634` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 196 | MUST | ✅ found | A `MetricProducer` MUST support the following functions: | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:33` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 197 | MUST | ✅ found | `Produce` MUST return a batch of Metric Points. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:33; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:704` |  |
| 198 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | - | Функция Произвести() (ИнтерфейсПродюсерМетрик.os:33) не содержит параметра ресурса, хотя возвращаемые ОтелДанныеМетрики несут Ресурс как обязательный параметр конструктора (ОтелДанныеМетрики.os:208) - батч включает информацию о ресурсе, но интерфейс не даёт вызывающему способа передать его продюсеру; читатель (ОтелПериодическийЧитательМетрик.СобратьДанныеПродюсеров) тоже не передаёт Ресурс продюсеру при вызове Произвести. |
| 199 | SHOULD | ✅ found | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелРезультатПроизводстваМетрик.os:20-49; src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:33` |  |
| 200 | SHOULD | ⚠️ partial | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:33; src/Метрики/Классы/ОтелДанныеМетрики.os:208-227; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:701-720` | ОтелДанныеМетрики принимает ОбластьИнструментирования вторым обязательным параметром конструктора (стр. 208), поэтому продюсер может передать InstrumentationScope. Но ни контракт ИнтерфейсПродюсерМетрик, ни читатель не требуют и не обеспечивают, чтобы это была единая область, идентифицирующая сам MetricProducer: СобратьДанныеПродюсеров добавляет данные продюсера как есть, без проверки или подстановки области, а собственной реализации продюсера с такой областью в SDK нет. |

#### Defaults and configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#defaults-and-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 201 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 202 | MUST | ✅ found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76-93` |  |
| 203 | MUST | ➖ n_a | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | - | OneScript Число = System.Decimal (не IEEE 754): NaN, Infinity и отрицательный ноль физически невозможны как значения - операции, которые в IEEE754 привели бы к NaN/Infinity, в Decimal выбрасывают исключение (перехватывается в ОтелБазовыйСинхронныйИнструмент.Записать, стр. 86-92). Инструменты (ОтелСчетчик.Добавить и др.) принимают только Число (Decimal), поэтому описанный в требовании сценарий получения NaN/Infinity от Instruments на этой платформе не может произойти. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 204 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:186-210` |  |
| 205 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:748-754` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 206 | MUST | ✅ found | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76-128,179-181,191-222` |  |
| 207 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-134; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50-116` |  |
| 208 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105-111,142-168,180-198,386-398` |  |
| 209 | MUST | ✅ found | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:84-127` |  |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:325-388; src/Экспорт/Классы/ОтелGrpcТранспорт.os:239-277` | Большинство опций (Endpoint, Insecure, Headers, Compression, Timeout, Protocol, Max Request/Response Size, Certificate File для gRPC) полностью настраиваемы и применяются. Но Client key file и Client certificate file (mTLS) принимаются как поля ОтелНастройкиTls, однако не применяются ни в ОтелHttpТранспорт (библиотека 1connector не поддерживает клиентский сертификат - предупреждение в ПриСозданииОбъекта, строки 379-383), ни в ОтелGrpcТранспорт (OPI_GRPC/tonic не поддерживает mTLS - предупреждение в ПроверитьНастройкиTls, строки 542-552); Certificate File (root CA) также не применяется в HTTP-транспорте (только в gRPC). Часть заявленных опций конфигурации принимается, но не оказывает эффекта. |
| 2 | MUST | ✅ found | Each configuration option MUST be overridable by a signal specific option. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:666-751 (СоздатьТранспортДляСигнала), 1267-1287 (ПараметрСигналаИлиОбщий), 1127-1130 (ЧислоСОткатом)` |  |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:204-209 (ВыполнитьОднуПопытку), src/Конфигурация/Модули/ОтелАвтоконфигурация.os:811-826 (РазобратьСхемуURL)` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:666-721 (СоздатьТранспортДляСигнала)` |  |
| 5 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:304-339 (ОткрытьСоединение)` |  |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:811-826 (РазобратьСхемуURL)` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:304-339 (комментарий и ОткрытьСоединение)` |  |
| 8 | MUST | ✅ found | Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:952-964 (РаспознатьПротоколOtlp)` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:251,261,713,715 (АдресПоУмолчанию = "http://localhost:4317" / "http://localhost:4318")` |  |
| 10 | SHOULD | ➖ n_a | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - | Требование условное ("if they are already implemented"): устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE в этом SDK никогда не поддерживались (в src/ не встречаются ни в одной версии), поэтому сохранять их поддержку не требуется. |
| 11 | SHOULD | ✅ found | The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:237-238; src/Экспорт/Классы/ОтелHttpТранспорт.os:332` |  |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:666-721 (СоздатьТранспортДляСигнала)` |  |
| 13 | MUST | ✅ found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:694-709 (ветка ЕстьАдресСигнала), 1298-1312 (НормализоватьURLДляPerSignal)` |  |
| 14 | MUST | ✅ found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1298-1312 (НормализоватьURLДляPerSignal)` |  |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1298-1312 (НормализоватьURLДляPerSignal); src/Экспорт/Классы/ОтелHttpТранспорт.os:204-209 (ПолныйURL = БазовыйURL + Путь)` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os (класс целиком, протокол grpc); src/Экспорт/Классы/ОтелHttpТранспорт.os (класс целиком, протоколы http/protobuf и http/json); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:250-267` |  |
| 17 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os (класс целиком, протокол grpc); src/Экспорт/Классы/ОтелHttpТранспорт.os (класс целиком, протоколы http/protobuf и http/json); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:250-267` |  |
| 18 | SHOULD | ✅ found | If they support only one, it SHOULD be `http/protobuf`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:237-238 (значение по умолчанию "http/protobuf")` |  |
| 19 | SHOULD | ✅ found | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:237-238; src/Экспорт/Классы/ОтелHttpТранспорт.os:332` |  |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:809-813 (РазобратьПарыКлючЗначение), 832-861 (РазобратьПары)` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:204-232 (коды 429/502/503/504 бросают исключение, перехватываемое стратегией повтора), 350-354; src/Экспорт/Классы/ОтелGrpcТранспорт.os:191-209 (ОшибкаПовторяемая), 256-259` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:350-354 (.УстановитьТипЗадержки(ТипыРасчетаЗадержки.Экспоненциальная).ИспользоватьРазбросЗадержки(Истина)); src/Экспорт/Классы/ОтелGrpcТранспорт.os:256-259 (аналогично)` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ✅ found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | `src/Ядро/Модули/ОтелУтилиты.os:508-519 (UserAgentЭкспортераOtlp -> "OTel-OTLP-Exporter-OneScript/<версия>"); src/Экспорт/Классы/ОтелHttpТранспорт.os:368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:300` |  |
| 24 | SHOULD | ✅ found | The format of the header SHOULD follow RFC 7231. | `src/Ядро/Модули/ОтелУтилиты.os:508-519 (формат product/version токена "OTel-OTLP-Exporter-OneScript/<версия>")` |  |
| 25 | SHOULD | ✅ found | The resulting User-Agent SHOULD include the exporter’s default User-Agent string. | `src/Ядро/Модули/ОтелУтилиты.os:508-519 (ИдентификаторПродукта + " " + СтандартныйUserAgent); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302 (СформироватьМетаданные)` |  |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63,99; src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:31,97; src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:20,41; src/Пропагация/Классы/ОтелНоопПропагатор.os:15,29` |  |
| 2 | MUST | ✅ found | Each `Propagator` type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:55-63 (Носитель + Сеттер/Геттер контракт, по умолчанию тип Соответствие)` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the `Context` first, such as `SpanContext`, `Baggage` or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:64 (Спан = ОтелКонтекст.СпанИзКонтекста(Контекст)); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:32 (ОбъектBaggage = ОтелКонтекст.BaggageИзКонтекста(Контекст))` |  |

#### Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any pre... | `src/Пропагация/Классы/ОтелW3CПропагатор.os:99-166 (Извлечь: все ветки невалидного traceparent возвращают исходный Контекст без исключений; подтверждено tests/unit/Пропагация/ТестW3CПропагатор.os, тесты Отклонение*)` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any pre... | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:97-150 (Извлечь: при отсутствии заголовка или отсутствии валидных записей возвращает исходный Контекст без исключений)` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:57-103 (КлючВалиден - RFC 9110 tchar; ЗначениеВалидно - VCHAR/SP/HTAB)` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:1-77 (без полей состояния); src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:13-18; сохраняются как константы ГеттерПоУмолчанию/СеттерПоУмолчанию, напр. src/Пропагация/Классы/ОтелW3CПропагатор.os:224-225` |  |

#### Setter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#setter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:33-41 (Установить: Носитель.Вставить(Ключ, Значение) - ключ вставляется без изменения регистра); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:147-159` |  |
| 9 | MUST | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:33-41 (Установить: casing сохраняется безусловно, независимо от регистрозависимости протокола)` |  |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The `Keys` function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59-65 (Функция Ключи)` |  |
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20-28 (Функция Получить); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:46-75` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20-28 (Получить: сравнение через НРег); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:29-41` |  |
| 13 | MUST | ✅ found | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49 (Функция ПолучитьВсе); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:78-94` |  |
| 14 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49 (ПолучитьВсе итерирует Носитель в порядке добавления); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:78-94 (Результат[0]="первое", Результат[1]="второе")` |  |
| 15 | SHOULD | ✅ found | If the key doesn’t exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49 (Результат = Новый Массив() возвращается пустым при отсутствии совпадений); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:97-109` |  |
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49 (ПолучитьВсе: сравнение через НРег)` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:1-94 (класс ОтелКомпозитныйПропагатор целиком)` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:89-92 (Create - ПриСозданииОбъекта), 20-28 (Inject - Внедрить), 41-51 (Extract - Извлечь)` |  |

#### Global Propagators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#global-propagators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:215-227 (Функция ПолучитьПропагаторы) - единственный поддерживаемый тип TextMapPropagator` |  |
| 20 | SHOULD | ➖ n_a | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | - | Требование адресовано Instrumentation Libraries (политика их поведения при вызове удалённых сервисов); данный пакет реализует только API+SDK, Instrumentation Libraries в составе отсутствуют. |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:215-227 (ПолучитьПропагаторы), 272-287 (ПолучитьИлиСоздатьПропагаторыПоУмолчанию возвращает Новый ОтелНоопПропагатор())` |  |
| 22 | SHOULD | ✅ found | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:558-600 (СоздатьПропагаторы: по умолчанию "tracecontext,baggage"), 1406-1419 (ДобавитьПропагатор создаёт ОтелW3CПропагатор + ОтелW3CBaggageПропагатор в ОтелКомпозитныйПропагатор)` |  |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:568-586 (значение "none" в otel.propagators отключает - возвращает ОтелНоопПропагатор; иные значения переопределяют состав); src/Ядро/Модули/ОтелГлобальный.os:202-204 (УстановитьПропагаторы - явное программное переопределение)` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | SHOULD | ✅ found | This method SHOULD exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:215` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD | ✅ found | This method SHOULD exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:202` |  |

#### Propagators Distribution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#propagators-distribution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ➖ n_a | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry Core packages: | - | Требование адресовано OpenTelemetry Organization (официальный реестр и порядок сопровождения пропагаторов), а не отдельным SDK-имплементациям. Данный пакет - независимая реализация OpenTelemetry для OneScript, а не официальный дистрибутив OTel Core packages. Для справки: W3C TraceContext и W3C Baggage входят в основной пакет (lib.config:143-144), B3 вынесен в отдельный пакет opentelemetry-propagator-b3 и подгружается рефлексивно (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397). |
| 27 | MUST | ➖ n_a | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry Core packages: | - | Требование адресовано OpenTelemetry Organization (порядок распространения официальных Core packages), а не отдельным SDK-имплементациям. Данный пакет не является официальным дистрибутивом OTel Core packages, поэтому эта политика распространения к нему не применима как к субъекту требования. |
| 28 | MUST NOT | ➖ n_a | It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | - | Требование адресовано OpenTelemetry Organization и описывает политику именования пропагатора OT Trace (deprecated) в официальном списке дополнительных Core packages. Пропагатор OT Trace (OpenTracing Basic Tracers) в этом репозитории не реализован вовсе (grep -rin "OpenTracing\|OT.Trace\|ot-trace" src/ - пусто), поэтому требование к его имени неприменимо ни как политика организации OTel, ни как поведение конкретного класса этого SDK. |
| 29 | MUST NOT | ✅ found | Additional `Propagator`s implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the OpenTelemetry Core packages. | `lib.config:141-147` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:99-167; src/Трассировка/Классы/ОтелСостояниеТрассировки.os:333-411` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:80-81` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty, in which case the `tracestate` header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:83-85` |  |

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST | ➖ n_a | MUST attempt to extract B3 encoded using single and multi-header formats. | - | Класс ОтелB3Пропагатор отсутствует в этом репозитории: его нет ни в src/Пропагация/Классы/ (только ОтелW3CПропагатор, ОтелW3CBaggageПропагатор, ОтелКомпозитныйПропагатор, ОтелНоопПропагатор, ОтелГеттерТекстовойКарты, ОтелСеттерТекстовойКарты), ни в lib.config (строки 141-147). ОтелАвтоконфигурация.СоздатьПропагаторB3() (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397) лишь рефлексивно подгружает класс ОтелB3Пропагатор из отдельного пакета opentelemetry-propagator-b3, если он установлен в окружении, и выводит мягкое предупреждение при его отсутствии. Фактическое извлечение single/multi-header форматов с приоритетом single-header реализуется в этом внешнем пакете и не может быть верифицировано по коду данного репозитория. |
| 34 | MUST | ➖ n_a | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (см. предыдущее требование); он поставляется отдельным пакетом opentelemetry-propagator-b3 и подгружается рефлексивно (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397). Сохранение debug-флага (X-B3-Flags/'d' в single-header) и его дальнейшая пропагация - логика этого внешнего класса, недоступного для верификации в данном репозитории. |
| 35 | MUST | ➖ n_a | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397). Установка sampled trace flag при наличии debug-флага - часть логики извлечения этого внешнего класса и не проверяема по коду данного репозитория. |
| 36 | MUST NOT | ➖ n_a | MUST NOT reuse `X-B3-SpanId` as the ID for the server-side span. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397); интерпретация X-B3-SpanId при извлечении - ответственность этого внешнего класса и не проверяема здесь. |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ➖ n_a | MUST default to injecting B3 using the single-header format | - | Класс ОтелB3Пропагатор (отдельный пакет opentelemetry-propagator-b3) отсутствует в репозитории; его собственное поведение по умолчанию (конструктор без явного формата) определяется в этом внешнем пакете. ОтелАвтоконфигурация.СоздатьПропагаторB3() (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1386) всегда передаёт явный параметр ('single' или 'multi'), поэтому фактический дефолт самого класса в данном репозитории не проверяем. |
| 38 | MUST | ✅ found | MUST provide configuration to change the default injection format to B3 multi-header | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1386` |  |
| 39 | MUST NOT | ➖ n_a | MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same ID for both sides of a request. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397); набор фактически внедряемых B3-заголовков (в т.ч. отказ от X-B3-ParentSpanId) определяется этим внешним классом и не проверяем в данном репозитории. |

#### Fields

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#fields)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ➖ n_a | Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation. | - | Требование относится к методу Поля() класса ОтелB3Пропагатор, которого нет в репозитории (grep -r "B3" src/ находит только рефлексивную загрузку по имени класса в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1378-1397, а не сам класс; в src/Пропагация/Классы/ и lib.config:141-147 B3 отсутствует). Метод Поля() для B3 реализуется в отдельном пакете opentelemetry-propagator-b3. В данном репозитории Поля() корректно реализован для W3C TraceContext (ОтелW3CПропагатор.os:174-179), W3C Baggage (ОтелW3CBaggageПропагатор.os:157-161), композитного (ОтелКомпозитныйПропагатор.os:58-67) и noop (ОтелНоопПропагатор.os:38-40) пропагаторов, но это не сам B3. |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-74,149-155,952-964,1074-1080,1094-1112,1205-1214,1249-1265` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130,1163-1172,1186-1193; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:272; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:524-532` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Ядро/Классы/ОтелПостроительSdk.os:26-99; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:135-141,385-395,536-541,642-648` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:894-898,920-926,953-955,1052-1054,1074-1080,1094-1097,1279-1287; src/Ядро/Классы/ОтелРесурс.os:143-158; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-119; src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:246-259` |  |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string `"true"`, meaning `"True"` or `"TRUE"` are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1249-1265,920-926,1337-1342` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1249-1265` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:920-926,1249-1265,1337-1342; src/Экспорт/Классы/ОтелНастройкиTls.os:49` |  |
| 8 | SHOULD | ✅ found | If any value other than a true value, case-insensitive string `"false"`, empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1259-1263` |  |
| 9 | SHOULD | ✅ found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:920-926,1337-1342; src/Экспорт/Классы/ОтелНастройкиTls.os:49` |  |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `packagedef:7` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | The following paragraph was added after stabilization and the requirements are thus qualified as “SHOULD” to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130` |  |
| 12 | MUST | ✅ found | For new implementations, these should be treated as MUST requirements. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130,1163-1172` |  |
| 13 | SHOULD | ✅ found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them ... | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1094-1112,1127-1130,978-987` |  |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ✅ found | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:307,498,570,591,956,1000,1055,1206; src/Метрики/Модули/ОтелФильтрЭкземпляров.os:54` |  |
| 15 | MUST | ✅ found | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:338-344,503-509,894-904,962-963,1005-1009,1059-1060,1210-1213,1417; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:121-126` |  |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | Values MUST be deduplicated in order to register a `Propagator` only once. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:588-597` |  |
| 17 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:981-985,1109-1110,1231-1233` |  |
| 18 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:984,1111,1224-1235` |  |
| 19 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:309,318-319,329-330,979-980` |  |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:613-649,765-780; src/Трассировка/Классы/ОтелСпан.os:333-335,365,446,562-573,580-590,597-609,664-683,694-705; src/Трассировка/Классы/ОтелСобытиеСпана.os:104-117; src/Логирование/Классы/ОтелЗаписьЛога.os:239-252; src/Ядро/Модули/ОтелУтилиты.os:406-408` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD NOT | ✅ found | It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:283-287,1205-1214` |  |
| 22 | SHOULD NOT | ✅ found | It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:483-487,1205-1214` |  |
| 23 | SHOULD NOT | ✅ found | It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:411-415,1205-1214` |  |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:104-126; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:73,784; src/Ядро/Классы/ОтелРесурс.os:102-106,138-140; src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:246` |  |

### Prometheus Compatibility

#### Differences between Prometheus formats

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#differences-between-prometheus-formats)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Exemplars MUST be dropped if they are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:699-722,752-772; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:342-399` |  |
| 2 | MUST | ✅ found | If the specification below requires producing a Prometheus Info-typed metric, a Prometheus Gauge with an additional `_info` name suffix MUST be produced if Info-typed metrics are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-500,512-531,542-550,717-718` |  |
| 3 | MUST | ✅ found | If the specification below requires producing a Prometheus StateSet-typed metric, a Prometheus Gauge MUST be produced instead if StateSet-typed metrics are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:512-531,542-550` |  |
| 4 | SHOULD | ✅ found | Exponential (Native) Histograms SHOULD be dropped if they are not supported, or MAY be converted to fixed-bucket histograms. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:609-611,651-658` |  |

#### Metric Metadata

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST NOT | ✅ found | Prometheus Pull exporters for OpenTelemetry metric data MUST NOT allow duplicate UNIT, HELP, or TYPE comments for the same metric name to be returned in a single scrape of the Prometheus endpoint. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:683-697,965-982; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:342-398` |  |
| 6 | MUST | ✅ found | Exporters MUST drop entire metrics to prevent conflicting TYPE comments, but SHOULD NOT drop metric points as a result of conflicting UNIT or HELP comments. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:609-620,965-982` |  |
| 7 | SHOULD NOT | ✅ found | Exporters MUST drop entire metrics to prevent conflicting TYPE comments, but SHOULD NOT drop metric points as a result of conflicting UNIT or HELP comments. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:683-697,837-843,1001-1024` |  |
| 8 | SHOULD | ✅ found | Instead, all but one of the conflicting UNIT and HELP comments (but not metric points) SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:683-697,837-843` |  |
| 9 | SHOULD | ⚠️ partial | If dropping a comment or metric points, the exporter SHOULD warn the user through error logging. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:618-631,683-697,837-843,965-982; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:351-355` | Во всех штатных путях отбрасывания пишется предупреждение (Лог.Предупреждение): конфликт TYPE - метрика отброшена целиком (стр. 618-620, 979-980), сэмплы с уже выведенными именем и лейблами - точки отброшены (стр. 624-631), отличающийся HELP - описание отброшено (стр. 837-843). Но есть путь без предупреждения: семейство info-метрики в text format называется база + _info, а датчик или stateset с таким именем имеет другую базу. ЕстьКонфликтТипа (стр. 965-982) находит семейство по имени в text format, видит тот же тип gauge и то же имя и конфликта не отмечает, а СемействоМетрики (стр. 683-697) ищет только по базовому имени и создает второе семейство с тем же именем. СобратьСемейства возвращает два семейства с одним именем, PrometheusTextFormat.Сериализовать (oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:351-355) оставляет последнее, серии первого теряются без предупреждения. Проверено запуском: info-метрика x (метка k=info-series) и датчик x_info (метка k=gauge-series) дали только x_info{k=gauge-series}, в логе ничего. |
| 10 | MUST | ✅ found | The Name of an OTLP metric MUST be added as the Prometheus Metric Name. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:609-616,1060-1072,1496-1514` |  |
| 11 | SHOULD | ✅ found | Discouraged characters in the metric name SHOULD be replaced with the `_` character by default, aiming for compatibility with Prometheus conventions. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1496-1514,1545` |  |
| 12 | SHOULD | ✅ found | Multiple consecutive `_` characters SHOULD be replaced with a single `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1496-1514,1546` |  |
| 13 | MUST | ✅ found | The Unit of an OTLP metric point MUST be converted from the UCUM unit to the equivalent unit word in Prometheus if it is included in the table in Metric Metadata above. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1085-1105,1134-1140,1458-1484` |  |
| 14 | MUST | ✅ found | Portions of the Unit within brackets (e.g. {packet}) MUST be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1085-1090,1549` |  |
| 15 | MUST | ✅ found | Units defined as rates over time (e.g. “m/s”) MUST be converted to words (e.g. “meters_per_second”). | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1090-1097,1116-1122,1486-1493` |  |
| 16 | SHOULD | ❌ not_found | The resulting unit SHOULD be added to the metric as UNIT metadata. | - | UNIT-метаданные не выводятся. Семейство, которое строит СемействоМетрики (ОтелПрометеусЧитательМетрик.os:689-693), содержит только Имя, Тип, Справка и Сэмплы (поля единицы нет), а сериализатор библиотеки prometheus (PrometheusTextFormat.Сериализовать, oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:384-385) пишет только строки # HELP и # TYPE: читатель выдает text format 0.0.4, в котором комментария # UNIT нет. Переведенная единица используется только как суффикс имени (БазовоеИмя, стр. 1060-1072). Вывод OpenMetrics 1.0 (# UNIT, _created, exemplars) удален из читателя коммитом 328d385 и должен вернуться патчем библиотеки prometheus (docs/api/Метрики/ОтелПрометеусЧитательМетрик.md:20-22). |
| 17 | SHOULD | ✅ found | A suffix to the metric name SHOULD be added unless the metric name already ends with the unit (before type-specific suffixes). | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1060-1072` |  |
| 18 | MUST | ✅ found | The description of an OTLP metrics point MUST be added as HELP metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:683-697; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:331-340,384` |  |
| 19 | MUST | ✅ found | The data point type of an OTLP metric MUST be added as TYPE metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:512-531,542-550,617; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:385` |  |

#### Instrumentation Scope

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | Prometheus exporters MUST by default add the scope name as the `otel_scope_name` label, the scope version as the `otel_scope_version` label, the scope schema URL as the `otel_scope_schema_url` label, ... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1154-1165,1265-1288,1320-1349` |  |
| 21 | MUST | ✅ found | Scope attributes that, after adding the `otel_scope_` prefix and applying the label-name conversion described in `Metric Attributes`, would conflict with `otel_scope_name`, `otel_scope_version`, or `o... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1265-1288` |  |

#### Gauges

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | An OpenTelemetry Gauge MUST be converted following a hint present in metric.metadata: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:512-531; src/Метрики/Классы/ОтелДанныеМетрики.os:133-150` |  |
| 23 | MUST | ✅ found | If the `prometheus.type` key is absent, or its value is equal to `gauge`, the datapoint MUST be transformed to a Prometheus Gauge. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:523-530` |  |
| 24 | MUST | ✅ found | If the `prometheus.type` key has value equal to `unkown`, the datapoint MUST be transformed to a Prometheus Unknown. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:523-525,542-544` |  |
| 25 | SHOULD | ✅ found | If the `prometheus.type` key has value equal to `info`, the datapoint SHOULD be transformed to a Prometheus Info. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-474,526-527,545-546,717-718` |  |
| 26 | SHOULD | ✅ found | If the `prometheus.type` key has value equal to `stateset`, the datapoint SHOULD be transformed to a Prometheus Stateset. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:526-527,545-546` |  |
| 27 | SHOULD | ✅ found | Exemplars on OpenTelemetry Gauges SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:699-722` |  |

#### Sums

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#sums)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | An OpenTelemetry Sum MUST be converted following the rules below: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:512-531,609-640` |  |
| 29 | MUST | ✅ found | If the aggregation temporality is cumulative and the sum is monotonic, it MUST be converted to a Prometheus Counter. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:338-340,520-522; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175` |  |
| 30 | SHOULD | ✅ found | If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-478,1060-1072` |  |
| 31 | MUST | ⚠️ partial | If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:467-478,1060-1072` | Имя без суффикса _total получает его, а имя с одним суффиксом _total остается без изменений (ИменаМетрики, стр. 467-478; БазовоеИмя, стр. 1060-1072). Но имя, оканчивающееся на _total дважды, теряет один суффикс: БазовоеИмя отрезает _total у счетчика (стр. 1063-1066), ИменаМетрики отрезает его повторно (БезСуффикса, стр. 475) и добавляет один _total. Проверено запуском: счетчик requests_total_total выдается как requests_total (# TYPE requests_total counter), хотя имя уже оканчивается на _total и по спецификации должно остаться без изменений. |
| 32 | SHOULD | ❌ not_found | Monotonic Sum metric points with `StartTimeUnixNano` SHOULD transform `StartTimeUnixNano` into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol. | - | startTimeUnixNano точек читателем не используется: ОтелПрометеусЧитательМетрик.os не обращается к этому полю, сэмплы точки строятся только из value и attributes (ДобавитьСэмплыТочки, стр. 711-722). Выдача - text format 0.0.4 (Prometheus.СериализоватьВТекст), в котором нет StartTime; представление _created (OpenMetrics) и created_timestamp (protobuf) не реализовано: OpenMetrics 1.0 удален из читателя коммитом 328d385 и должен вернуться патчем библиотеки prometheus. В отличие от exemplars (правило отбрасывания при отсутствии поддержки формата есть в спецификации), для StartTime такого правила нет. |
| 33 | MUST | ➖ n_a | If Sum is converted to a Prometheus Counter, then `Exemplars` MUST be converted as described in the Exemplar Conversion section. | - | Условное требование: exemplars конвертируются только для протокола, который их поддерживает (Exemplar Conversion). Читатель выдает только обязательный text format 0.0.4, в нем exemplars нет, и они отбрасываются, как требует Differences between Prometheus formats. Другие протоколы ради exemplars экспортер поддерживать не обязан (Version and Format: "MAY support Exemplars ... but is not required to implement them"). Требование станет применимым, когда читатель начнет выдавать OpenMetrics через библиотеку prometheus. |
| 34 | SHOULD | ✅ found | Otherwise, `Exemplars` SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:699-722` |  |
| 35 | SHOULD | ➖ n_a | If the Prometheus protocol only supports a single exemplar on the Counter sample, the latest exemplar SHOULD be converted. | - | Условное требование для протокола с одним exemplar на сэмпл счетчика (OpenMetrics). Читатель выдает только обязательный text format 0.0.4 без exemplars, другие протоколы ради exemplars экспортер поддерживать не обязан (Version and Format: "MAY support Exemplars ... but is not required to implement them"). |

#### Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | An OpenTelemetry Histogram with a cumulative aggregation temporality MUST be converted to a Prometheus Histogram by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:301-304,338-340,512-516,733-750; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175` |  |
| 37 | MUST | ⚠️ partial | OpenTelemetry Histograms with Delta aggregation temporality MAY be aggregated into a Cumulative aggregation temporality and follow the logic below, or MUST be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:338-340,395-406,609-640; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175` | Для метрик SDK временная агрегация читателя всегда кумулятивная (ВременнаяАгрегацияДляВида, стр. 338-340; ОтелПотокиМетрик.ВременнаяАгрегацияЧитателя, ОтелПотокиМетрик.os:162-175): SDK агрегирует гистограммы в кумулятивную сам, дельта-гистограммы инструментов в выдачу не попадают. Но метрики внешних продюсеров (ДобавитьПродюсер) читатель по временной агрегации не проверяет: ФильтрДляПродюсера (стр. 395-406) лишь передает предпочтение кумулятивной агрегации (фильтр с уже заданным предпочтением, в том числе дельта, передается как есть), а КонвертироватьИДобавить (стр. 609-640) не смотрит на ОтелДанныеМетрики.ВременнаяАгрегация(). Проверено запуском: гистограмма продюсера с временной агрегацией Дельта выводится как обычная кумулятивная Prometheus histogram - ее не агрегируют в кумулятивную и не отбрасывают (то же для дельта-суммы). |

#### Histograms as Prometheus Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms-as-prometheus-histograms)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 38 | MUST | ✅ found | When converting to a Prometheus Histogram, an OpenTelemetry Histogram MUST be converted following the rules below: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:733-750; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:199-264` |  |
| 39 | SHOULD | ❌ not_found | If set, `StartTimeUnixNano` SHOULD be transformed into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol. | - | startTimeUnixNano точки гистограммы не используется: ДобавитьСэмплыГистограммы (ОтелПрометеусЧитательМетрик.os:733-750) читает только bucketCounts, explicitBounds, sum и count. Выдача - text format 0.0.4, в котором нет StartTime; _created (OpenMetrics) и created_timestamp (protobuf) не реализованы: OpenMetrics 1.0 удален из читателя коммитом 328d385 и должен вернуться патчем библиотеки prometheus. В отличие от exemplars (правило отбрасывания при отсутствии поддержки формата есть в спецификации), для StartTime такого правила нет. |
| 40 | SHOULD | ➖ n_a | If the Prometheus protocol only supports a single exemplar per-bucket, the latest exemplar that falls into each bucket SHOULD be converted. | - | Условное требование для протокола с одним exemplar на бакет (OpenMetrics). Читатель выдает только обязательный text format 0.0.4 без exemplars, другие протоколы ради exemplars экспортер поддерживать не обязан (Version and Format: "MAY support Exemplars ... but is not required to implement them"). |

#### Summaries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | An OpenTelemetry Summary MUST be converted to a Prometheus Summary as follows: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:517-519,651-669,763-772` |  |
| 42 | MUST | ✅ found | The `quantile` label value MUST be the stringified floating point value of each quantile (between 0.0 and 1.0), starting from lowest to highest, and all being non-negative. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:763-772,782-796; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:275-329` |  |
| 43 | SHOULD NOT | ✅ found | Explicit timestamps SHOULD NOT be used for pull protocols, such as the Prometheus text exposition format, where Prometheus assigns the scrape timestamp. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:807-816; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:56-63` |  |
| 44 | SHOULD | ✅ found | Exemplars on OpenTelemetry Summaries SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:699-722,752-772` |  |

#### Metric Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST | ✅ found | OpenTelemetry Metric Attributes MUST be converted to Prometheus labels. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1154-1165,1320-1349` |  |
| 46 | MUST | ⚠️ partial | String Attribute values are converted directly to Metric Attributes, and non-string Attribute values MUST be converted to string attributes following the attribute specification. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1398-1433` | Строковые значения переносятся как есть, число, булево и массив - в JSON-представление (42 -> '42', true -> 'true', 2.5 -> '2.5', [1,2] и массив строк - в JSON-массив), как требует раздел AnyValue representation for non-OTLP protocols. Но ЗначениеВJSON (ОтелПрометеусЧитательМетрик.os:1409-1433) не знает kvlistValue (Соответствие/Структура), bytesValue (ДвоичныеДанные) и пустое значение: они дают 'null' вместо JSON-объекта, base64-строки и пустой строки (проверено запуском: map='null', bytes='null', empty='null'; так же вложенные в массив map/bytes). Спецификация (v1.61) допускает такие значения атрибутов. NaN/Infinity невозможны (Число = Decimal). |
| 47 | SHOULD | ✅ found | Discouraged characters SHOULD be replaced with the `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1496-1514,1525-1527,1545` |  |
| 48 | SHOULD | ✅ found | Multiple consecutive `_` characters SHOULD be replaced with a single `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1496-1514,1546` |  |
| 49 | MUST | ⚠️ partial | In such cases, the values MUST be concatenated together, separated by `;`, and ordered by the lexicographical order of the original keys. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1154-1165,1320-1349,1357-1363,1374-1387` | Значения атрибутов, чьи ключи дали одно имя лейбла, склеиваются через ';' в порядке исходных ключей (ЛейблыИзАтрибутовOtlp, стр. 1320-1349, ВставитьПоПорядкуКлюча, стр. 1357-1363; проверено запуском: a.b, a:b и a_b дали a_b='first;third;second'). Но коллизии с лейблами, которые добавляет сама спецификация (в тексте пример - otel_scope_name), не склеиваются: ЛейблыТочки (стр. 1154-1165) перезаписывает атрибут точки лейблом области (otel.scope.name='user' потерян, остался otel_scope_name='lib'), а атрибут точки с тем же именем, что и скопированный атрибут ресурса, вытесняет ресурсный (service.name='point-attr' без 'checkout'). |

#### Exemplar Conversion

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplar-conversion)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ➖ n_a | When an exemplar is converted per the metric-type-specific sections above, the OpenTelemetry Exemplar MUST be converted to a Prometheus exemplar if the Prometheus (push or pull) protocol being used su... | - | Условное требование (если протокол поддерживает exemplars). Читатель выдает только обязательный text format 0.0.4, в нем exemplars нет, и они отбрасываются, как требует Differences between Prometheus formats (ДобавитьСэмплыТочки, ОтелПрометеусЧитательМетрик.os:699-722; проверено запуском: точка с exemplar выводится без него). Другие протоколы ради exemplars экспортер поддерживать не обязан (Version and Format: "MAY support Exemplars ... but is not required to implement them"). Требование станет применимым, когда читатель начнет выдавать OpenMetrics через библиотеку prometheus: в 1.0.5 OpenMetrics нет. |
| 51 | MUST | ➖ n_a | If present, the OpenTelemetry Exemplar’s Trace ID and Span ID MUST be added as Exemplar labels using the `trace_id` and `span_id` keys, respectively. | - | Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываются; поддержка других протоколов ради exemplars не обязательна (Version and Format: MAY). |
| 52 | MUST | ➖ n_a | These labels MUST take precedence over labels from `filtered_attributes` in cases where there is a key collision. | - | Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываются; поддержка других протоколов ради exemplars не обязательна (Version and Format: MAY). |
| 53 | MUST | ➖ n_a | Timestamps MUST be added as timestamps on the Prometheus exemplar. | - | Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываются; поддержка других протоколов ради exemplars не обязательна (Version and Format: MAY). |
| 54 | MUST | ➖ n_a | `filtered_attributes` MUST be added as labels on the Prometheus exemplar, unless they would exceed the Prometheus protocol’s exemplar limits. | - | Правило конвертации exemplar применяется только для протокола с exemplars. Читатель выдает только обязательный text format 0.0.4, exemplars отбрасываются; поддержка других протоколов ради exemplars не обязательна (Version and Format: MAY). |

### Prometheus Exporter

#### Client Libraries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#client-libraries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus m... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4,95-110; packagedef:32` |  |
| 2 | SHOULD NOT | ❌ not_found | A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus m... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4,100,109,207-209; packagedef:32; opm-metadata.xml:22` | Экспортер использует неофициальную стороннюю клиентскую библиотеку prometheus для OneScript (yellow-hammer/prometheus 1.0.5, автор Ivan Karlo): в официальном списке клиентских библиотек Prometheus (Go, Java/Scala, Node.js, Python, Ruby, Rust) ее нет, официальной библиотеки для OneScript не существует. Зависимость времени выполнения объявлена в packagedef:32 и opm-metadata.xml:22 (dev=false); '#Использовать prometheus' (стр. 4), текст выдачи формирует Prometheus.СериализоватьВТекст (стр. 100), Content-Type берется из Prometheus.ContentTypeМетрик (стр. 109), для реестра библиотеки читатель отдает семейства через Collect() (стр. 207-209). Спецификация допускает вместо этого собственную реализацию формата экспозиции (документация Prometheus: если клиентской библиотеки для языка нет, формат экспозиции можно реализовать самостоятельно); ранее выдачу формировал встроенный сериализатор без библиотеки, теперь зависимость возвращена. |
| 3 | SHOULD | ✅ found | If a Prometheus client library is used, the OpenTelemetry Prometheus Exporter SHOULD be modeled as a custom Collector so it can be used in conjunction with existing Prometheus instrumentation. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:141-169,207-209; oscript_modules/prometheus/src/Классы/CollectorRegistry.os:3-7,22,50-65` |  |

#### Version and Format

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#version-and-format)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | Regardless of whether a Prometheus client library is used, the Prometheus Exporter MUST support version `0.0.4` of the Text-based format. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:95-110; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:6-8,342-399` |  |
| 5 | MUST NOT | ✅ found | A Prometheus Exporter for an OpenTelemetry metrics SDK MUST NOT use Prometheus Remote Write format or OpenMetrics protobuf format. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:95-110` |  |
| 6 | SHOULD NOT | ✅ found | A Prometheus Exporter for an OpenTelemetry metrics SDK SHOULD NOT add explicit timestamps on Metric points. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:807-816; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:56-63` |  |

#### Target

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#target)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | There MUST be at most one `target` info metric exposed by an SDK Prometheus exporter. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:141-169` |  |

#### Temporality

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#temporality)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | A Prometheus Exporter MUST set the MetricReader `temporality` as a function of instrument kind to be `cumulative` for all instrument kinds. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:122-124,338-340; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175` |  |

#### Default Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#default-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | A Prometheus Exporter SHOULD support a configuration option to set the MetricReader default `aggregation` as a function of instrument kind. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:301-328; src/Метрики/Модули/ОтелПотокиМетрик.os:415-443` |  |
| 10 | MUST | ✅ found | This option MAY be named `default_aggregation`, and MUST use the default aggregation by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:315-318,1556; src/Метрики/Модули/ОтелПотокиМетрик.os:429-434; src/Метрики/Модули/ОтелАгрегация.os:180-187` |  |

#### Resource Attributes as Metric Labels

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#resource-attributes-as-metric-labels)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST NOT | ✅ found | By default, it MUST NOT add any resource attributes as metric labels. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1176-1180,1553` |  |
| 12 | SHOULD | ✅ found | The configuration SHOULD allow the user to select resource attributes to include or exclude. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:221-227,1176-1252` |  |

#### Scope Info

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#scope-info)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The option MAY be named `scope_info_enabled`, and MUST be `true` by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:149-160,1154-1165,1265-1288` |  |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Prometheus Compatibility

#### Metric Metadata

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | The Prometheus Metric Name MUST be added as the Name of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Имя Prometheus-метрики в имя метрики OTLP не переносится. |
| 2 | SHOULD NOT | ➖ n_a | The name SHOULD NOT be altered. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Имена Prometheus-метрик в OTLP не переносятся, поэтому требование не применимо. Нормализация имени (БазовоеИмя/НормализоватьИмя, ОтелПрометеусЧитательМетрик.os:1045-1072,1496-1514) работает только в обратном направлении, OTLP → Prometheus, и относится к другому разделу спецификации (OTLP Metric points to Prometheus). |
| 3 | MUST | ➖ n_a | Prometheus UNIT metadata, if present, MUST be converted to the unit of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Таблица единиц ЗаполнитьСловаЕдиниц() (ОтелПрометеусЧитательМетрик.os:1454-1494) используется только для экспорта (UCUM → слово Prometheus), UNIT из Prometheus в единицу OTLP не переводится. |
| 4 | MUST | ➖ n_a | The unit MUST be translated from words to the UCUM abbreviation if it is in the following set of commonly-used units: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Перевода слов Prometheus в UCUM нет: таблица ЗаполнитьСловаЕдиниц() (ОтелПрометеусЧитательМетрик.os:1454-1494) работает только в обратную сторону (UCUM → слово Prometheus) при экспорте. |
| 5 | MUST | ➖ n_a | Prometheus HELP metadata, if present, MUST be added as the description of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). HELP из Prometheus не разбирается и в описание метрики OTLP не переносится; описание метрики OTel выводится в HELP только при экспорте. |
| 6 | MUST | ➖ n_a | Prometheus TYPE metadata, if present, MUST be used to determine the OTLP data type, and dictates type-specific conversion rules listed below. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). TYPE из Prometheus не разбирается, тип данных OTLP по нему не определяется. |
| 7 | MUST | ➖ n_a | The TYPE metadata MUST also be added to the OTLP metric.metadata under the `prometheus.type` key (e.g. `prometheus.type="unknown"`). | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Модель данных SDK поддерживает metric.metadata (ОтелДанныеМетрики.Метаданные, передача в поле metadata OTLP: ОтелЭкспортерМетрик.os:420-439), а читатель Prometheus использует ключ prometheus.type как подсказку типа при экспорте (ОтелПрометеусЧитательМетрик.os:512-531), но записывать в него TYPE из Prometheus некому: разбора экспозиции нет, метаданные может задать только внешний источник данных (MetricProducer). |

#### Timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#timestamps) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | If present, the Prometheus Metric Sample’s Start timestamp (also referred to as the Created timestamp) MUST be converted to the Start timestamp of the OTLP data point. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Start (Created) timestamp сэмпла Prometheus в Start timestamp точки OTLP не переводится. |
| 2 | SHOULD | ➖ n_a | If no start timestamp is present, the start time of the OTLP data point SHOULD be left unset. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Точки OTLP из сэмплов Prometheus не формируются, поэтому правило про незаполненное start time не применимо. |
| 3 | MUST | ➖ n_a | If present, the Prometheus Metric Sample’s Timestamp MUST be converted to the Timestamp of the OTLP data point. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Timestamp сэмпла Prometheus в Timestamp точки OTLP не переводится. |
| 4 | MUST | ➖ n_a | For metrics scraped from a Prometheus endpoint without an explicit timestamp, the timestamp of the OTLP data point MUST be set to the time of the scrape. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Scrape Prometheus-эндпоинта SDK не выполняет, времени скрейпа для точек OTLP нет. |

#### Counters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#counters) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Counter MUST be converted to an OTLP Sum with `is_monotonic` equal to `true`. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Prometheus Counter в OTLP Sum (is_monotonic=true) не переводится; читатель делает обратное: монотонная сумма OTel выводится как Prometheus counter (ОтелПрометеусЧитательМетрик.os:512-531). |
| 2 | MUST | ➖ n_a | Exemplars on the Prometheus Counter Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Sum data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Exemplars сэмплов Prometheus в OTel Exemplars не переводятся; в обратном направлении (экспорт в text format) exemplars отбрасываются (ОтелПрометеусЧитательМетрик.os:699-722). |

#### Gauges

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Gauge MUST be converted to an OTLP Gauge. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4 через библиотеку prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует) нет ни scrape, ни разбора экспозиции (# TYPE/# HELP/# UNIT, семплы). Prometheus Gauge в OTLP Gauge не переводится; читатель делает обратное: датчик OTel выводится как Prometheus gauge (ОтелПрометеусЧитательМетрик.os:512-531). |

#### Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Histogram MUST be converted to an OTLP Histogram. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. В src/ нет приемника/скрейпера и парсера форматов Prometheus. Есть лишь обратное направление: ДобавитьСэмплыГистограммы (ОтелПрометеусЧитательМетрик.os:733-750) переводит OTLP Histogram в сэмплы _bucket/_sum/_count, а перевода Prometheus Histogram → OTLP Histogram (границы le → explicit bounds без +Inf, счетчики бакетов, count и sum) нет. |
| 2 | MUST | ➖ n_a | In the text format, Prometheus histograms buckets, count and sum are sent as separate samples and they MUST be merged together when forming an OTLP Histogram. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Слияния отдельных сэмплов _bucket, _count и _sum text-формата в одну OTLP-гистограмму нет: text-формат Prometheus в SDK не разбирается, имена _bucket/_sum/_count в src/ только формируются при выдаче (ОтелПрометеусЧитательМетрик.os:482-486). |
| 3 | MUST | ➖ n_a | If `_count` is not present, the metric MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Правило отбрасывания метрики без _count относится к разбору входящего text-формата Prometheus, которого в SDK нет. |
| 4 | MUST | ➖ n_a | If `_sum` is not present, the histogram’s sum MUST be unset. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Правило «sum не задан при отсутствии _sum» относится к разбору входящего text-формата Prometheus, которого в SDK нет. |
| 5 | MUST | ➖ n_a | Exemplars on the Prometheus Histogram Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Histogram data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Exemplars Prometheus Histogram Sample не принимаются. Exemplars OTel SDK создает только резервуарами из собственных измерений (ОтелРезервуарЭкземпляров, ОтелВыровненныйРезервуарГистограммы), а читатель Prometheus в text format exemplars вообще не выводит (ОтелПрометеусЧитательМетрик.os:699-702). |

#### Native Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#native-histograms) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Native Histogram with standard (exponential) schema (i.e. schemas -4 to 8) and which are of the integer and counter flavor MUST be converted to an OTLP Exponential Histogram as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Native Histogram Prometheus (Schema, ZeroCount/ZeroThreshold, PositiveSpans/PositiveDeltas, ResetHint) не принимается и не разбирается: этих сущностей в src/ нет. Собственная экспоненциальная гистограмма SDK (ОтелАгрегаторЭкспоненциальнойГистограммы) строится из измерений OTel, а не из данных Prometheus; при выдаче в Prometheus text format она пропускается (ОтелПрометеусЧитательМетрик.os:654-658). |
| 2 | MUST | ➖ n_a | Overflow buckets MUST be dropped and not counted in the overall `Count`. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Отбрасывание overflow-бакетов относится к разбору native histogram Prometheus, которого в SDK нет. |
| 3 | MUST | ➖ n_a | A Native histogram with custom buckets (NHCB) schema (i.e. schema -53) and which are of the integer and counter flavor MUST be converted to an OTLP Histogram as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Native histogram с custom buckets (NHCB, schema -53, CustomValues) не принимается: перевода в OTLP Histogram нет. |
| 4 | MUST | ➖ n_a | Native histograms of the float or gauge flavors MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Native histograms Prometheus (в том числе float и gauge flavors) не принимаются, отбрасывать нечего: приема Prometheus-метрик нет. |
| 5 | MUST | ➖ n_a | Native Histograms with `Schema` outside of the range [-4, 8] and not equal to -53 MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Проверка Schema (вне [-4, 8] и не равна -53) относится к разбору native histogram Prometheus, которого в SDK нет. |
| 6 | MUST | ➖ n_a | Exemplars on the Prometheus Native Histogram Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Exponential Histogram data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Exemplars Prometheus Native Histogram Sample не принимаются; перевода в exemplars OTLP Exponential Histogram нет. |

#### Summaries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Prometheus Summary MUST be converted to an OTLP Summary. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. В src/ нет приемника/скрейпера и парсера форматов Prometheus. Есть лишь обратное направление: ДобавитьСэмплыСводки (ОтелПрометеусЧитательМетрик.os:763-772) выводит OTLP Summary (от MetricProducer) как Prometheus summary, а перевода Prometheus Summary → OTLP Summary нет. |
| 2 | MUST | ➖ n_a | In text formats where Prometheus Summaries are represented by multiple samples, samples with same metric family name MUST be merged together into a single OTLP Summary. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Слияния сэмплов quantile, _count и _sum с одним именем семейства в один OTLP Summary нет: text-формат Prometheus в SDK не разбирается. |
| 3 | MUST | ➖ n_a | If `_count` is not present, the metric MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Правило отбрасывания метрики без _count относится к разбору входящего text-формата Prometheus, которого в SDK нет. |
| 4 | MUST | ➖ n_a | If `_sum` is not present, the summary’s sum MUST be set to zero. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Правило «sum = 0 при отсутствии _sum» относится к разбору входящего text-формата Prometheus, которого в SDK нет. |

#### Dropped Types

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#dropped-types) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | The following Prometheus types MUST be dropped: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Типы GaugeHistogram и Native GaugeHistogram Prometheus не принимаются, отбрасывать нечего (GaugeHistogram в src/ не встречается). |

#### Exemplars

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplars) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Prometheus Exemplars MUST be converted to OpenTelemetry Exemplars as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Перевода Prometheus Exemplar → OpenTelemetry Exemplar нет. Exemplars OTel SDK создаются только резервуарами из собственных измерений (ОтелРезервуарЭкземпляров, ОтелВыровненныйРезервуарГистограммы), а читатель Prometheus text format exemplars не выводит (ОтелПрометеусЧитательМетрик.os:699-702). |
| 2 | MUST | ➖ n_a | If present, the timestamp MUST be used as the OpenTelemetry exemplar’s timestamp. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Timestamp exemplar Prometheus не принимается и не переносится в timestamp exemplar OTel. |
| 3 | MUST | ➖ n_a | If present, and if the values are valid Trace and Span IDs, the `trace_id` and `span_id` labels MUST be converted to the OpenTelemetry Exemplar’s Trace ID and Span ID, respectively. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Лейблы trace_id и span_id exemplar Prometheus не принимаются; trace_id/span_id в src/ берутся только из контекста спана измерения OTel (резервуары экземпляров) и кодируются OTLP-кодировщиками. |
| 4 | MUST | ➖ n_a | All labels other than `trace_id` and `span_id` MUST be added to the OpenTelemetry exemplar as filtered attributes. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Остальные лейблы exemplar Prometheus не принимаются и не переносятся в filteredAttributes: в SDK filteredAttributes вычисляются только из атрибутов измерений OTel (ВычислитьОтфильтрованныеАтрибуты в резервуарах экземпляров). |

#### Instrumentation Scope

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Labels with `otel_scope_` prefix MUST be dropped from all metric points and used as the Instrumentation Scope name (`otel_scope_name`), version (`otel_scope_version`), schema URL (`otel_scope_schema_u... | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Есть лишь обратное направление: ЛейблыОбласти (ОтелПрометеусЧитательМетрик.os:1265-1288) добавляет лейблы otel_scope_* при выдаче OTLP → Prometheus, а разбора входящих лейблов otel_scope_* (отбрасывание с точек, заполнение имени, версии, schema URL и атрибутов области) нет. |
| 2 | MUST | ➖ n_a | Metrics which do not have any label with `otel_scope_` prefix MUST be assigned an instrumentation scope identifying the entity performing the translation from Prometheus to OpenTelemetry (e.g. the col... | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus text 0.0.4), приема Prometheus-метрик и их перевода в OTLP нет. Назначения области инструментирования, идентифицирующей транслятор Prometheus → OpenTelemetry, метрикам без лейблов otel_scope_* нет: Prometheus-метрики в SDK не принимаются. |

### Сводка условных секций

| Раздел | Секция | Scope | Stability | Keywords | Ссылка |
|---|---|---|---|---|---|
| Prometheus Compatibility | Metric Metadata | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 7 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata) |
| Prometheus Compatibility | Timestamps | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#timestamps) |
| Prometheus Compatibility | Counters | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 2 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#counters) |
| Prometheus Compatibility | Gauges | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 1 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges) |
| Prometheus Compatibility | Histograms | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 5 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms) |
| Prometheus Compatibility | Native Histograms | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 6 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#native-histograms) |
| Prometheus Compatibility | Summaries | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries) |
| Prometheus Compatibility | Dropped Types | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 1 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#dropped-types) |
| Prometheus Compatibility | Exemplars | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplars) |
| Prometheus Compatibility | Instrumentation Scope | conditional:Prometheus Receiver (Prometheus → OTLP) | Stable | 2 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope) |

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

1. **Извлечение требований** (`extract_requirements.py`): загрузка 14 страниц спецификации, разбиение на секции, подсчёт MUST/SHOULD keywords
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
| Страниц спецификации | 14 |
| Stable universal секций с требованиями | 240 |
| Stable conditional секций | 10 |
| Stable universal keywords | 833 |

