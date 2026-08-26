# Dialect Map — SQL Feature Comparison

| Feature | MySQL | MS SQL Server | PostgreSQL | Snowflake | Teradata | Spark SQL |
|---------|-------|---------------|------------|-----------|----------|-----------|
| Limit rows | `LIMIT n` | `TOP n` | `LIMIT n` | `LIMIT n` | `TOP n` / `SAMPLE` | `LIMIT n` |
| Full outer join | ❌ (UNION workaround) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Window filter inline | ❌ | ❌ | ❌ | `QUALIFY` ✅ | ❌ | ❌ |
| String concat | `CONCAT()` | `+` / `CONCAT()` | `\|\|` / `CONCAT()` | `\|\|` / `CONCAT()` | `\|\|` | `CONCAT()` / `\|\|` |
| Current timestamp | `NOW()` | `GETDATE()` | `NOW()` | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` |
| Auto-increment key | `AUTO_INCREMENT` | `IDENTITY(1,1)` | `SERIAL` / `GENERATED` | `AUTOINCREMENT` | `GENERATED ALWAYS` | N/A (managed) |
| Regex match | `REGEXP` | `LIKE` only | `~` / `SIMILAR TO` | `REGEXP_LIKE()` | `REGEXP_SUBSTR()` | `RLIKE` |
| Alias in HAVING | ✅ (MySQL specific) | ❌ | ❌ | ❌ | ❌ | ✅ |
| Recursive CTE | ✅ (v8+) | ✅ | ✅ | ✅ | ✅ | ✅ |

*Append rows as new features encountered.*
