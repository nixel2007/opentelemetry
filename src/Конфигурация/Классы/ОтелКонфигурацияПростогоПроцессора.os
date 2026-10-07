// BSLLS:UnusedLocalVariable-off
// BSLLS:ExportVariables-off
// Конфигурация простого процессора (SimpleSpanProcessor / SimpleLogRecordProcessor).
//
// Используется для tracer_provider.processors и logger_provider.processors.

#Область ОписаниеПеременных

// exporter - ОтелКонфигурацияЭкспортераOtlpHttp - конфигурация экспортера
// Union-тип разрешается парсером, хранится конкретная реализация
Перем Экспортер Экспорт;

#КонецОбласти

#Область ОбработчикиСобытий

Процедура ПриСозданииОбъекта()
	Экспортер = Неопределено;
КонецПроцедуры

#КонецОбласти
