// Fixture: генератор с правильным ID трассировки, но некорректным ID спана.
// Используется для тестирования ветки валидации СгенерироватьИдСпана в ОтелПровайдерТрассировки.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off

Функция СгенерироватьИдТрассировки() Экспорт
	Возврат "a1b2c3d4e5f6a7b8a1b2c3d4e5f6a7b8";
КонецФункции

Функция СгенерироватьИдСпана() Экспорт
	Возврат "badspan";
КонецФункции
