// Fixture: продюсер метрик для тестов фабрики: считает вызовы Произвести и возвращает пустые данные.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:ExportVariables-off
// BSLLS:UnusedParameters-off

Перем КоличествоВызовов Экспорт;

Функция Произвести(Ресурс, ТаймаутМс = 0) Экспорт
	КоличествоВызовов = КоличествоВызовов + 1;
	Возврат Новый Массив;
КонецФункции

Процедура ПриСозданииОбъекта()
	КоличествоВызовов = 0;
КонецПроцедуры
