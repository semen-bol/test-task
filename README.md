# Тестовое задание

Сервис для автоматического распределения обращений лидов между операторами с учётом весов и лимитов нагрузки.

## Запуск проекта

```bash
$ make build up
```

Документация API: http://localhost:8000/docs

## Модели данных
- Operator - операторы (активность, лимит нагрузки)

- Lead - клиенты (идентифицируются по external_id)

- Source - источники/боты

- SourceOperator - связь операторов с источниками и их весами

- Contact - обращения лидов

## Связи:

- Operator ↔ SourceOperator ↔ Source (многие-ко-многим с весами)

- Lead → Contact (один-ко-многим)

- Source → Contact (один-ко-многим)

- Operator → Contact (один-ко-многим)

## Алгоритм распределения
### Лиды определяются по external_id
```python
lead = await db.execute(select(Lead).where(Lead.external_id == external_id))
```
### Для каждого оператора рассчитывается score
```python
score = assigned_contacts / weight
```
### Выбирается оператор с минимальным score
```python
candidates.sort(key=lambda x: x[1])
```
### Нагрузка = количество активных обращений
```python
load = count(contacts where operator_id=X and status="active")
```
### Проверка лимита
```python
if load >= operator.max_leads:
    continue  # оператор исключается
```
### Если нет доступных операторов
```python
if not candidates:
    contact = Contact(operator_id=None)
    return {"status": "no_operators_available"}
```