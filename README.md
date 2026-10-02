# GENESIS — уровень 2: numeric и evaluator v1

Первый модуль подключается к [core v1](https://github.com/kirillpistol/pistol-genesis-ai).
Алгоритмы и данные остаются отдельно от ядра.

| Компонент | Реализация |
|---|---|
| numeric/1 | Число записей, среднее, выборочная дисперсия по потоку |
| evaluator/1 | MAE и RMSE по явным prediction/target |
| Обучение, предиктор, обмен состояниями | Пока отсутствуют |
| Text и sequence | Дальнейшие сборки после проверки числового этапа |

numeric — агрегирование, не ML-обучение. evaluator не обучает predictor и не доказывает
улучшения модели: источник должен предоставить независимые тестовые targets.

## Запуск

Python 3.10+, зависимостей нет:

```sh
python -m unittest discover -s tests -v
```

Из папки соседнего pistol-genesis-ai задайте PYTHONPATH на этот репозиторий:

```sh
export PYTHONPATH=../genesis-level-2
python -m level1_core.server --dev-local --algorithm-module level2_algorithms.numeric
```

PowerShell: `$env:PYTHONPATH = '../genesis-level-2'`.
Для mTLS вместо --dev-local используйте --tls-config, как описано в core README.
На источник и приёмник устанавливается одна версия модуля; загрузки кода по сети нет.

Подключите POST /v1/algorithms/attach: {"api_version":"1.0","name":"numeric"}.
Далее POST /v1/tasks: {"api_version":"1.0","algorithm":"numeric","data":10}.
Для evaluator data={"prediction":2,"target":1}, имя алгоритма evaluator.

## Контракт и состояние

REGISTRY экспортирует доверенные классы. Каждый класс имеет version,
__init__(state=None), process(value), state(). Методов train и merge нет.
Схемы входов: contracts/v1; данные ограничены диапазоном ±1e40.
Количество записей до 1e9, состояние проверяется на конечность и допустимый диапазон.
Сохраняются агрегаты, сырые записи не включаются в state().

Core v1 использует exact API 1.0, state_version=1, exact версии алгоритмов.
Snapshot numeric/1 или evaluator/1 восстанавливается только совместимым классом.
При ошибке кандидат состояния не становится текущим состоянием ядра.
Алгоритмы пока in-process: являются доверенным кодом, не изолированы.

## Последовательность следующих этапов

1. Проверить numeric/evaluator на HTTPS+mTLS core и измерить ошибки/перенос.
2. Определить train/evaluate контракты и изолированное исполнение.
3. Добавить обучение с независимым контролем качества и ограниченным состоянием.
4. Только затем определить математически допустимое объединение независимых состояний.

Решения по транспорту и границам: [ADR-0001](https://github.com/kirillpistol/pistol-genesis-ai/blob/main/docs/adr/0001-transport-boundaries-versioning.md).
Внешние источники: [уровень 3](https://github.com/kirillpistol/genesis-level-3).
