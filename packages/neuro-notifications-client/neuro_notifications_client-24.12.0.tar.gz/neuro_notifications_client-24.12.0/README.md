# Example

```python
async with Client(URL("http://localhost:8080")) as client:
    await client.ping()
    await client.notify(JobCannotStartQuotaReached("bob"))
    await client.notify(JobCannotStartLackResources("job-lack-resources-1"))
```
