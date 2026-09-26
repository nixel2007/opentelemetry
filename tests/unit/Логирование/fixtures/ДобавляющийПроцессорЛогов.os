// Fixture: процессор, который при появлении записи добавляет в провайдер другой процессор.
// Детерминированная модель конкурентного ДобавитьПроцессор во время обработки записи.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:ExportVariables-off

Перем Провайдер Экспорт;
Перем ДобавляемыйПроцессор Экспорт;

Процедура ПриПоявлении(ЗаписьЛога, Контекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
    Провайдер.ДобавитьПроцессор(ДобавляемыйПроцессор);
КонецПроцедуры

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЭкспорта.Успех();
КонецФункции

Функция Закрыть(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЗакрытия.Успех();
КонецФункции
