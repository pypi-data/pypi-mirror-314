# Judges

Types:

```python
from haizelabs_api.types import JudgeCallResponse
```

Methods:

- <code title="post /judges/call">client.judges.<a href="./src/haizelabs_api/resources/judges.py">call</a>(\*\*<a href="src/haizelabs_api/types/judge_call_params.py">params</a>) -> <a href="./src/haizelabs_api/types/judge_call_response.py">JudgeCallResponse</a></code>

# Testing

Types:

```python
from haizelabs_api.types import TestingUpdateResponse, TestingStartResponse
```

Methods:

- <code title="post /testing/update">client.testing.<a href="./src/haizelabs_api/resources/testing.py">update</a>(\*\*<a href="src/haizelabs_api/types/testing_update_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_update_response.py">TestingUpdateResponse</a></code>
- <code title="post /testing/start">client.testing.<a href="./src/haizelabs_api/resources/testing.py">start</a>(\*\*<a href="src/haizelabs_api/types/testing_start_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_start_response.py">TestingStartResponse</a></code>

# Monitoring

Types:

```python
from haizelabs_api.types import MonitoringLogResponse
```

Methods:

- <code title="post /monitoring/log">client.monitoring.<a href="./src/haizelabs_api/resources/monitoring.py">log</a>(\*\*<a href="src/haizelabs_api/types/monitoring_log_params.py">params</a>) -> <a href="./src/haizelabs_api/types/monitoring_log_response.py">object</a></code>
