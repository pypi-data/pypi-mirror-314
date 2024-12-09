# confcogs

`confcogs` is a lightweight Python library for managing `.cogs` configuration files. It allows you to easily add, edit, fetch, and remove key-value pairs in `.cogs` files.

---

## Installation

Install `confcogs` using pip:
```bash
pip install confcogs
```

---

## Usage

### Import the Library
```python
import confcogs
```

### Setting the Path
Set the path to your `.cogs` file:
```python
path = 'settings/load.cogs'
```

### Adding Key-Value Pairs
Add new key-value pairs:
```python
confcogs.acog(path, 'loaded', 'True')
confcogs.acog(path, 'debug', 'False')
```

### Fetching a Value
Retrieve a value from the `.cogs` file:
```python
value = confcogs.fcog(path, 'loaded')  # Output: 'True'
```

### Editing a Value
Edit an existing value:
```python
confcogs.ecog(path, 'debug', 'True')
```

### Removing a Key
Remove a key-value pair:
```python
confcogs.rcog(path, 'debug')
```

### Loading All Configurations
Load the entire `.cogs` file as a dictionary:
```python
config = confcogs.lcog(path)  # Output: {'loaded': 'True'}
```

---

## Example
Here’s a complete example:
```python
import confcogs

path = 'settings/load.cogs'

# Add key-value pairs
confcogs.acog(path, 'loaded', 'True')
confcogs.acog(path, 'debug', 'False')

# Fetch a value
print(confcogs.fcog(path, 'loaded'))  # Output: True

# Edit a value
confcogs.ecog(path, 'debug', 'True')

# Remove a key
confcogs.rcog(path, 'debug')

# Load all configurations
print(confcogs.lcog(path))  # Output: {'loaded': 'True'}
```

---

## File Format
`.cogs` files use a simple key-value format:
```plaintext
key: 'value';
```

Example:
```plaintext
loaded: 'True';
debug: 'False';
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
