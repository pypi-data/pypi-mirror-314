# NotipyDesktop

NotipyDesktop is a simple Python library for sending desktop notifications using [libnotify](https://developer.gnome.org/libnotify/).

## Features

- Send desktop notifications with a title and message.
- Easy-to-use API with just one function.
- Uses [PyGObject](https://pygobject.readthedocs.io/en/latest/) to interact with GNOME notifications.

---

## Installation

Install the library via `pip`:

```bash
pip install NotipyDesktop
```

---

## Usage

Here's an example of how to use `notifier`:

```python
from NotipyDesktop import notify

# Send a notification
notify("MyApp", "Test Notification", "This is a test message.")
```

### CLI Usage

#### local path

You can also use the library as a command-line tool. Run the following command to send a notification:

```bash
python3 NotipyDesktop.py MyApp "Test Notification" "This is a test message."
```

---

#### sytem wide

You can make the program system wide executable with:

```bash
chmod +x /path/to/NotipyDesktop/NotipyDesktop.py
```

After that you have to add the path to `$PATH`:

```bash
export PATH=$PATH:/path/to/NotipyDesktop
```

Then you can run:

```bash
NotipyDesktop.py MyApp "Test Notification" "This is a test message."
```

## Requirements

- Python 3.6 or higher
- GNOME Desktop Environment (or a compatible Linux desktop environment)
- `libnotify` installed on your system

Install the required Python dependencies:

```bash
pip install PyGObject
```

For most Linux distributions, you can install `libnotify` with your package manager. Example for Ubuntu/Debian:

```bash
sudo apt install libnotify-bin
```

---

## Development

To set up the project locally for development:

1. Clone the repository:

   ```bash
   git clone https://github.com/Michdo93/NotipyDesktop.git
   cd NotipyDesktop
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests or use the CLI to validate functionality.

---

## Contributing

Contributions are welcome! If you find a bug or have a feature request, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [PyGObject Documentation](https://pygobject.readthedocs.io/en/latest/)
- [GNOME libnotify](https://developer.gnome.org/libnotify/)
```
