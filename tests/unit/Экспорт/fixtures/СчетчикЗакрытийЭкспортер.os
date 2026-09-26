// Fixture: экспортер, атомарно считающий вызовы Закрыть.
// Используется для проверки однократного закрытия экспортера при конкурентном Закрыть процессора.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:ExportVariables-off
#Использовать atomic

Перем КоличествоЗакрытий Экспорт;

Функция Экспортировать(Элементы, ТаймаутМс = Неопределено) Экспорт // BSLLS:UnusedParameters-off
	Возврат Неопределено;
КонецФункции

Процедура СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Функция Закрыть() Экспорт
	КоличествоЗакрытий.ИнкрементироватьИПолучить();
	Возврат Неопределено;
КонецФункции

КоличествоЗакрытий = Новый АтомарноеЧисло(0);
