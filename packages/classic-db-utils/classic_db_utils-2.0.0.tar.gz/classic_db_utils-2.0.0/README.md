`classic-db-pool` — это библиотека для управления соединениями с базой данных
эффективным способом. Она позволяет создавать пул соединений с базой данных,
который может использоваться несколькими запросами или процессами одновременно.
Это гарантирует, что ваше приложение всегда имеет доступ к готовому
к использованию соединению без необходимости ожидания первоначальной
настройки соединения каждый раз.

## Вклад

Этот проект является форком проекта [Embrace](https://hg.sr.ht/~olly/embrace-sql).

## Установка

Для установки classic-db-pool вы можете использовать pip:

```bash
pip install classic-db-pool
```

## Использование

Вот несколько примеров использования classic-db-pool.

### Создание пула соединений

```python
from classic.db_utils import ConnectionPool
import pymssql


pool = ConnectionPool(
    lambda: pymssql.connect(
        server='server',
        database='database',
        user='user',
        password='password',
    ),
    limit=1,
)


with pool.connect() as conn:
    conn.cursor().execute('SQL query')
```

### Использование декоратора takes_connection

Декоратор `takes_connection` позволяет автоматически получать соединение из атрибута объекта и передавать его в метод. Это упрощает работу с соединениями в классах.

```python
from classic.db_utils import takes_connection

class SomeClass:
    def __init__(self, connect):
        self.connect = connect  # метод для получения соединения
    
    @takes_connection
    def get_user(self, user_id, connection):
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            return cur.fetchone()

# Можно настроить имена атрибута и параметра
class CustomClass:
    def __init__(self, db_connect):
        self.db_connect = db_connect
    
    @takes_connection(connect_attr='db_connect', connection_param='conn')
    def get_user(self, user_id, conn):
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            return cur.fetchone()
```

Декоратор принимает следующие параметры:
- `connect_attr` (по умолчанию 'connect'): имя атрибута объекта, содержащего метод для получения соединения
- `connection_param` (по умолчанию 'connection'): имя параметра, через который соединение будет передано в метод

