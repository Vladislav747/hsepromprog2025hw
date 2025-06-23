Проверка что данные есть в бд
```bash
docker-compose exec postgres psql -U postgres -d postgres -c "SELECT * FROM users;"
```