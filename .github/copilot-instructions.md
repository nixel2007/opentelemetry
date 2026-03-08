# OpenTelemetry SDK для OneScript

Библиотека на OneScript (oscript.io) для использования OpenTelemetry в оскриптовых проектах. Отправляет телеметрию (трассировку, логи, метрики) в формате OTLP HTTP JSON.

**IMPORTANT: Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Current Environment (GitHub Actions)
The repository runs in a GitHub Actions environment with OneScript installed via `otymko/setup-onescript`:
- **OneScript Version**: 2.0.0 (matches packagedef requirement)
- **Test Framework**: OneUnit (sfaqer/oneunit)
- **Installation Method**: via `otymko/setup-onescript@v1.5` action

### Using GitHub Actions (Recommended)
- The repository includes `.github/workflows/copilot-setup-steps.yml` for automated setup
- This workflow uses `otymko/setup-onescript@v1.5` action for proper OneScript installation
- Run from Actions tab: "OneScript Development Environment Setup" workflow

### Install Dependencies
```bash
opm install opm
opm install -l --dev
opm install oneunit
```

### Build and Syntax Checking
- Check syntax of individual files: `oscript -check src/Классы/ОтелСпан.os` -- takes ~0.3 seconds
- Check all source files: `find src -name "*.os" -exec oscript -check {} \;` -- takes 1-2 seconds
- Build: No explicit build step required - OneScript is interpreted

### Testing and Validation
- Run tests: `oneunit execute` -- runs all tests in ./tests directory
- Test framework: sfaqer/oneunit with asserts library
- Tests use `#Использовать ".."` to reference src and `#Использовать asserts` for assertions
- Tests follow `&Тест` annotation pattern from OneUnit

## Repository Structure

```
/
├── .github/
│   ├── workflows/
│   │   └── copilot-setup-steps.yml  # GitHub Actions setup workflow
│   └── copilot-instructions.md      # This file
├── .vscode/                         # VS Code configuration
├── src/
│   ├── Классы/                      # Classes directory
│   │   ├── ОтелАтрибуты.os          # Attributes (key-value pairs)
│   │   ├── ОтелРесурс.os            # Resource description
│   │   ├── ОтелКонтекстСпана.os     # SpanContext (trace/span IDs)
│   │   ├── ОтелСобытиеСпана.os      # Span event
│   │   ├── ОтелПровайдерТрассировки.os # TracerProvider
│   │   ├── ОтелТрассировщик.os      # Tracer
│   │   ├── ОтелСпан.os              # Span
│   │   ├── ОтелПростойПроцессорСпанов.os # SimpleSpanProcessor
│   │   ├── ОтелПровайдерЛогирования.os # LoggerProvider
│   │   ├── ОтелЛоггер.os            # Logger
│   │   ├── ОтелЗаписьЛога.os        # LogRecord
│   │   ├── ОтелПровайдерМетрик.os   # MeterProvider
│   │   ├── ОтелМетрика.os           # Meter
│   │   ├── ОтелСчетчик.os           # Counter
│   │   ├── ОтелГистограмма.os       # Histogram
│   │   ├── ОтелHttpТранспорт.os     # OTLP HTTP transport
│   │   ├── ОтелHttpЭкспортерСпанов.os # Span exporter (OTLP HTTP)
│   │   ├── ОтелHttpЭкспортерЛогов.os # Log exporter (OTLP HTTP)
│   │   └── ОтелHttpЭкспортерМетрик.os # Metric exporter (OTLP HTTP)
│   └── Модули/                      # Modules directory
│       ├── ОтелВидСпана.os          # SpanKind enum constants
│       ├── ОтелКодСтатуса.os        # StatusCode enum constants
│       ├── ОтелСтепеньСерьезности.os # SeverityNumber enum constants
│       └── ОтелУтилиты.os           # Utility functions (ID generation, timestamps)
├── tests/
│   ├── oscript.cfg                  # Test configuration
│   ├── ТестАтрибуты.os              # Attribute tests
│   ├── ТестРесурс.os                # Resource tests
│   ├── ТестТрассировка.os           # Tracing tests
│   ├── ТестЛогирование.os           # Logging tests
│   ├── ТестМетрики.os               # Metrics tests
│   └── ТестПровайдеры.os            # Provider tests
├── packagedef                       # OPM package definition
├── .bsl-language-server.json        # BSL language server config
├── .gitignore                       # Git ignore rules
└── README.md                        # Documentation
```

## Architecture Overview

The SDK follows OpenTelemetry SDK Specification, modeled after Java SDK:

### Signals
1. **Traces**: TracerProvider → Tracer → Span → SimpleSpanProcessor → HttpSpanExporter
2. **Logs**: LoggerProvider → Logger → LogRecord → HttpLogExporter
3. **Metrics**: MeterProvider → Meter → Counter/Histogram → HttpMetricExporter

### OTLP HTTP JSON Endpoints
- Traces: POST `/v1/traces` (ExportTraceServiceRequest)
- Logs: POST `/v1/logs` (ExportLogsServiceRequest)
- Metrics: POST `/v1/metrics` (ExportMetricsServiceRequest)

### Core Concepts
- **Resource** (`ОтелРесурс`): Describes the entity producing telemetry (service name, version, etc.)
- **Attributes** (`ОтелАтрибуты`): Key-value pairs stored in a Map (Соответствие)
- **SpanContext** (`ОтелКонтекстСпана`): Contains traceId (32 hex chars) and spanId (16 hex chars)
- **ID Generation**: Uses `УникальныйИдентификатор` (GUID) stripped of hyphens
- **Timestamps**: Unix epoch nanoseconds as strings (seconds from date arithmetic + "000000000")

## Development Guidelines

### Code Standards
- Source code and comments in Russian language
- Follow OneScript naming conventions (CamelCase with Russian characters)
- Private fields prefixed with `м` (e.g., `мИмя`, `мАтрибуты`)
- Export methods with `Экспорт` keyword
- Constructor: `Процедура ПриСозданииОбъекта()`
- Fluent API pattern: methods return `ЭтотОбъект` for chaining

### Adding New Classes
1. Create `.os` file in `src/Классы/`
2. Register in `packagedef` with `.ОпределяетКласс("ClassName", "path")`
3. Add tests in `tests/` directory

### Adding New Modules
1. Create `.os` file in `src/Модули/`
2. Modules are automatically available via `#Использовать`

### Test Pattern (OneUnit)
```bsl
#Использовать ".."
#Использовать asserts

&Тест
Процедура НазваниеТеста() Экспорт
    // Дано
    // ... setup ...

    // Когда
    // ... action ...

    // Тогда
    Ожидаем.Что(Результат).Равно(Ожидаемое);
КонецПроцедуры
```

### Dependencies
- **Runtime**: None (zero external dependencies)
- **Development**: oneunit 0.2.4+ (testing), asserts 1.5.0+ (assertions)
- **OneScript**: 2.0.0+

### Validation Commands
```bash
# Check syntax of all source files
find src -name "*.os" -exec oscript -check {} \;

# Check syntax of all test files
find tests -name "*.os" -exec oscript -check {} \;

# Run all tests
oneunit execute
```

## Important Notes

### Timeout Requirements
- **NEVER CANCEL** opm package installations - can take 1+ minutes
- Set timeouts of 60+ seconds for package installation commands
- Syntax checking is fast (0.3s per file)

### Language and Encoding
- All source code, comments, and variable names in Russian
- Files use Cyrillic characters and must be properly encoded
- Package uses Russian method names in packagedef

### No External Runtime Dependencies
The library has zero runtime dependencies - it only uses built-in OneScript capabilities (HTTP connections, JSON, UUID generation). Development dependencies (oneunit, asserts) are only needed for running tests.
