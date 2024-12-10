# Easy DateTime

A simple Python package to automatically detect and convert datetime strings to Unix timestamps.
处理日期字符串真的是蛋疼。让我们一劳永逸地解决这个问题。

## Installation

```bash
pip install easy_datetime
```

## Usage

```python
from easy_datetime import to_unix

# Different format examples
unix_time = to_unix("2021-01-01 00:00:00")        # 1609459200
unix_time = to_unix("2021/01/01 00:00:00")        # 1609459200
```

## Features

- Automatic datetime string format detection
- Supports various date formats (YYYY-MM-DD, DD-MM-YYYY, MM/DD/YYYY, etc.)
- Returns Unix timestamp (seconds since epoch)
- Simple and easy to use

## Requirements

- Python >= 3.6
- python-dateutil >= 2.8.2

## License

MIT License