# warprouter

A Python library for managing Cloudflare WARP routing on Windows.

## Installation

```bash
pip install warprouter
```

## Usage

```python
from warprouter import WARPRouter

# Create router instance
router = WARPRouter()

# Get list of processes
processes = router.get_user_processes()
print("Available processes:", processes)

# Exclude specific processes from WARP
router.exclude_process(1234)  # Replace with actual PID

# Or include processes in WARP
router.include_process(5678)  # Replace with actual PID

# Apply configuration
success, message = router.apply_configuration()
print(message)

# Check WARP status
status, message = router.get_warp_status()
print(message)

# Reset all settings
router.reset_configuration()
```

## Features

- Get list of user processes
- Exclude/include specific processes from WARP
- Save and load configurations
- Check WARP status
- Reset to defaults

## License

MIT License - see LICENSE file for details.