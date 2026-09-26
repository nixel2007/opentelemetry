// Fixture: считает количество вызовов ПриПоявлении.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:ExportVariables-off

Перем КоличествоВызовов Экспорт;

Процедура ПриПоявлении(ЗаписьЛога, Контекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
    КоличествоВызовов = КоличествоВызовов + 1;
КонецПроцедуры

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЭкспорта.Успех();
КонецФункции

Функция Закрыть(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЗакрытия.Успех();
КонецФункции

КоличествоВызовов = 0;
