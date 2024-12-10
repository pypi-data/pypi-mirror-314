### README.md

# PyChromeController

The **PyChromeController** is a Python-based utility class designed to streamline and automate interactions with Google Chrome through Selenium. It provides an extensive set of features for managing browser sessions, tabs, URLs, and elements, making it ideal for web automation, testing, and browsing control.

---

## Features

- **Browser Session Management**:
  - Start a new browser session.
  - Attach to an existing session using a session ID.
  - Save and retrieve session IDs from files.

- **Window and Tab Controls**:
  - Open, close, maximize, and minimize browser windows and tabs.
  - Switch between tabs using index, URL, title, or a visual reference (image).
  - Fetch all open tab titles and URLs.

- **URL Management**:
  - Open new tabs with specified URLs.
  - Change the URL of any tab using index, title, or current URL.
  - Check if a specific URL or title is open.

- **Element Interactions**:
  - Enter text into input fields.
  - Click buttons, checkboxes, links, and radio buttons.
  - Select dropdown options by value or visible text.
  - Upload files to input fields.
  - Verify the text of elements.

- **Advanced Features**:
  - Hover over elements.
  - Scroll to elements.
  - Take screenshots of the browser.
  - Control browser actions using image recognition (via PyAutoGUI).
  - Fetch titles and URLs of tabs via PyAutoGUI and system commands.

---

## Requirements

- **Python 3.7+**
- **Selenium** (Install with `pip install selenium`)
- **Google Chrome** (Latest version)
- **ChromeDriver** (Ensure it matches your Chrome version)
- **PyAutoGUI** (Install with `pip install pyautogui`)
- **Pyperclip** (Install with `pip install pyperclip`)

Optional dependencies:
- **xdotool** (Linux) for fetching window titles.
- **Subprocess** for executing system commands.

---

## Pre-Installation

### Selenium standalone server

You need `Selenium` as standalone server. At first you have to install `Java`:

```
sudo apt update
sudo apt install openjdk-11-jdk
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.bashrc
source ~/.bashrc
```

Then you have to download and install the `Selenium Server` (`Selenium Grid`):

```
wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.27.0/selenium-server-4.27.0.jar
mv selenium-server-4.27.0.jar /usr/local/bin
```

You can start and run it with:

```
java -jar /usr/local/bin/selenium-server-4.27.0.jar standalone
```

### Chrome and chromedriver

For `Chrome` you need a compatible `chromedriver`, otherwise it is not possible to control the browser remotely. First of all, I will show you how to install `Chrome` manually:

```
wget https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
sudo dpkg -i google-chrome-stable_114.0.5735.90-1_amd64.deb
sudo apt-mark hold google-chrome-stable
```

Then you have to download and install the `chromedriver`:

```
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin
```

---

## Installation

### Install via pip

To install the package using pip, simply run:

```bash
pip install PyChromeController
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Michdo93/PyChromeController.git
   cd PyChromeController
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that ChromeDriver is accessible in your PATH or specify its location when starting a session.

---

## Usage

### 1. Initialize the Controller

```python
from PyChromeController import PyChromeController

controller = PyChromeController(headless=False)
```

### 2. Start a New Browser Session

```python
if controller.start_browser_session():
    print("Browser session started successfully.")
else:
    print("Failed to start browser session.")
```

### 3. Open and Switch Tabs

```python
controller.open_url("https://example.com") # Open a URL in the first tab
controller.open_new_tab("https://example.com")  # Open a new tab with a URL
controller.open_blank_tab()                # Open a blank tab
controller.switch_tab(1)                   # Switch to the second tab (index starts at 0)
controller.close_tab_by_title("Example")   # Close tab based on title
```

### 4. Interact with Web Elements

```python
controller.enter_text(By.ID, "username", "admin")  # Enter text into an input field
controller.click_button(By.ID, "submit")          # Click a button
controller.toggle_checkbox(By.NAME, "terms", True)  # Check a checkbox
controller.select_dropdown(By.ID, "country", value="US")  # Select a dropdown option
```

### 5. Take Screenshots

```python
controller.take_screenshot("screenshot.png")
```

### 6. Close Browser

```python
controller.close_browser()
```

---

## Full List of Methods

### Browser Management

| **Method**                          | **Description**                                               | **Arguments**                                                                                                                                   | **Returns**                                    |
|-------------------------------------|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `start_browser_session()`           | Starts a new Chrome browser session.                          | None                                                                                                                                            | `None`                                         |
| `attach_browser_session(session_id)`| Attaches to an existing browser session.                      | `session_id`: The session ID to attach to.                                                                                                     | `None`                                         |
| `close_browser()`                   | Closes the browser and ends the session.                      | None                                                                                                                                            | `None`                                         |
| `get_browser_info()`                | Returns browser version and user-agent.                       | None                                                                                                                                            | `dict`: A dictionary with `browser_version`, `platform_name`, `user_agent`. |


### Session Management

| **Method**                                      | **Description**                                             | **Arguments**                                                                                                                                   | **Returns**                                    |
|-------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `write_session_id_to_file(path_to_file)`        | Saves the current session ID to a file.                     | `path_to_file`: Path to the file where session ID will be saved.                                                                                | `None`                                         |
| `read_session_id_from_file(path_to_file)`       | Reads the session ID from a file.                           | `path_to_file`: Path to the file containing the session ID.                                                                                    | `str`: The session ID read from the file.      |
| `add_cookie(name, value, domain=None, path="/")` | Adds a cookie to the current session.                        | `name`: Cookie name <br> `value`: Cookie value <br> `domain`: Optional domain (default is `None`) <br> `path`: Cookie path (default is `/`) | `bool`: `True` if successful, `False` otherwise |
| `delete_cookie(name)`                          | Deletes a cookie by name.                                    | `name`: Cookie name                                                                                                                                                  | `bool`: `True` if successful, `False` otherwise |
| `get_all_cookies()`                            | Returns all cookies in the current session.                 | None                                                                                                                                            | `list`: List of cookies retrieved from the browser |
| `recover_session()`                 | Attempts to recover the browser session after a crash.       | None                                                                                                                                            | `bool`: `True` if successful, `False` otherwise |

### Window Management

| **Method**                          | **Description**                                               | **Arguments**                                                                                                                                | **Returns**                                    |
|-------------------------------------|---------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `minimize_window()`                 | Minimizes the current window.                                 | None                                                                                                                                           | `None`                                         |
| `maximize_window()`                 | Maximizes the current window.                                 | None                                                                                                                                           | `None`                                         |
| `close_window()`                    | Closes the current window.                                    | None                                                                                                                                           | `None`                                         |

### Tab Management

| **Method**                                                 | **Description**                                                                                                                                   | **Arguments**                                                                                                                                    | **Returns**                                    |
|------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `open_url(url)`                                            | Opens the specified URL inside the first tab.                                                                                                    | `url`: URL to open in the new tab.                                                                                                                | `None`                                         |
| `open_new_tab(url)`                                        | Opens a new tab with the specified URL.                                                                                                           | `url`: URL to open in the new tab.                                                                                                                | `None`                                         |
| `open_blank_tab()`                                         | Opens a new blank tab.                                                                                                                            | None                                                                                                                                             | `None`                                         |
| `close_tab()`                                              | Closes the currently active tab.                                                                                                                  | None                                                                                                                                             | `None`                                         |
| `close_first_tab()`                                        | Closes the first tab.                                                                                                                             | None                                                                                                                                             | `None`                                         |
| `close_last_tab()`                                         | Closes the last tab.                                                                                                                              | None                                                                                                                                             | `None`                                         |
| `close_tab_by_index(index)`                                | Closes a tab by its index.                                                                                                                        | `index`: Index of the tab to close.                                                                                                              | `None`                                         |
| `close_tab_by_url(target_url)`                             | Closes a tab based on a URL.                                                                                                                      | `target_url`: URL of the tab to close.                                                                                                           | `None`                                         |
| `close_tab_by_title(target_title)`                         | Closes a tab based on a title.                                                                                                                    | `target_title`: Title of the tab to close.                                                                                                       | `None`                                         |
| `close_tab_by_image(image_path)`                           | Closes a tab based on an image of the searched tab.                                                                                               | `image_path`: Path to the image used to identify the tab.                                                                                        | `None`                                         |
| `switch_tab(index)`                                        | Switches to a tab by index.                                                                                                                       | `index`: Index of the tab to switch to.                                                                                                          | `None`                                         |
| `switch_tab_by_url(url)`                                   | Switches to a tab containing a specific URL.                                                                                                      | `url`: URL of the tab to switch to.                                                                                                              | `None`                                         |
| `switch_tab_by_title(title)`                               | Switches to a tab containing a specific title.                                                                                                    | `title`: Title of the tab to switch to.                                                                                                          | `None`                                         |
| `switch_tab_by_image(image_path)`                          | Switches to a tab using an image reference.                                                                                                       | `image_path`: Path to the image used to switch tabs.                                                                                             | `None`                                         |
| `check_and_open_tab_by_url(target_url)`                    | Checks if a specific URL is open. If yes, it switches to it; otherwise, it opens a new tab with the URL.                                          | `target_url`: URL to check and open if not found.                                                                                                | `None`                                         |
| `check_and_open_tab_by_title(target_title, target_url)`    | Checks if a specific title is open. If yes, it switches to it; otherwise, it opens a new tab with the title.                                      | `target_title`: Title to check and open if not found. <br> `target_url`: URL to open if a new tab is created.                                    | `None`                                         |
| `close_all_other_tabs()`                                   | Closes all tabs except the current one.                                                                                                           | None                                                                                                                                             | `bool`: `True` if successful, `False` otherwise|

### URL and Title Management

| **Method**                                           | **Description**                                                       | **Arguments**                                                                                                                               | **Returns**                                    |
|------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `change_url(new_url)`                                | Changes the URL of the current tab.                                   | `new_url`: The new URL to navigate to.                                                                                                      | `None`                                         |
| `check_url_in_list(url)`                             | Checks if a specific URL is open.                                     | `url`: URL to check in the list of open tabs.                                                                                                | `bool`: `True` if found, `False` otherwise    |
| `check_title_in_list(target_title)`                  | Checks if a specific title is open.                                   | `target_title`: Title to check in the list of open tabs.                                                                                    | `bool`: `True` if found, `False` otherwise    |
| `get_all_urls()`                                     | Retrieves all URLs from open tabs.                                    | None                                                                                                                                         | `list`: List of URLs of open tabs             |
| `get_all_titles()`                                   | Retrieves all titles from open tabs.                                  | None                                                                                                                                         | `list`: List of titles of open tabs           |
| `fetch_tab_urls()`                                   | Fetches the URLs of the open Chrome tabs.                             | None                                                                                                                                         | `list`: List of URLs of open tabs             |
| `fetch_tab_titles()`                                 | Fetches the titles of the open Chrome tabs.                           | None                                                                                                                                         | `list`: List of titles of open tabs           |
| `write_and_enter_url(url)`                           | Writes and enters the URL in the address bar of the selected tab.     | `url`: URL to write and enter in the selected tab.                                                                                           | `None`                                         |
| `change_url_of_tab(new_url, index)`                  | Switches to a tab by index and changes the URL.                        | `new_url`: New URL to navigate to. <br> `index`: Index of the tab to switch to.                                                            | `None`                                         |
| `change_url_of_tab_by_url(old_url, new_url)`         | Switches to a tab by URL and changes the URL.                         | `old_url`: URL of the tab to switch to. <br> `new_url`: New URL to navigate to.                                                            | `None`                                         |
| `change_url_of_tab_by_title(target_title, new_url)`  | Switches to a tab by title and changes the URL.                       | `target_title`: Title of the tab to switch to. <br> `new_url`: New URL to navigate to.                                                      | `None`                                         |
| `change_url_of_tab_by_image(new_url, image_path)`    | Switches to a tab by image and changes the URL.                       | `new_url`: New URL to navigate to. <br> `image_path`: Path to the image of the tab to switch to.                                              | `None`                                         |

### Element Interactions

| **Method**                                              | **Description**                                                       | **Arguments**                                                                                                                               | **Returns**                                    |
|---------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `enter_text(by, locator, text)`                         | Enters text into a specified field.                                   | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string. <br> `text`: The text to enter.                         | `None`                                         |
| `click_button(by, locator)`                             | Clicks a button.                                                      | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string.                                                          | `None`                                         |
| `toggle_checkbox(by, locator, state)`                   | Toggles a checkbox (checks or unchecks it).                            | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string. <br> `state`: Desired checkbox state (`True` for checked, `False` for unchecked). | `None`                                         |
| `select_dropdown(by, locator, value, visible_text)`     | Selects an option from a dropdown.                                    | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string. <br> `value`: The option value to select. <br> `visible_text`: Option text to select. | `None`                                         |
| `hover_over_element(by, locator)`                       | Hovers the mouse over a specified element.                            | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string.                                                          | `None`                                         |
| `click_link(by, locator)`                               | Finds the link element by the specified locator and clicks it.        | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string.                                                          | `None`                                         |
| `upload_file(by, locator, file_path)`                   | Finds the file input element by the specified locator and uploads a file. | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string. <br> `file_path`: Path to the file to upload.            | `None`                                         |
| `verify_text(by, locator, expected_text)` | Verifies that the text of the specified element matches the expected text. | `by`: Method to locate the element (e.g., `By.ID`, `By.XPATH`) <br> `locator`: Locator string <br> `expected_text`: The text to verify against | `None`                                            |
| `take_element_screenshot(by, locator, file_name)` | Takes a screenshot of a specific element and saves it to a file. | `by`: Method to locate the element (e.g., `By.ID`, `By.XPATH`) <br> `locator`: Locator string <br> `file_name`: The file to save the screenshot | `bool`: `True` if successful, `False` otherwise |
| `drag_and_drop(source_locator, target_locator)` | Performs a drag-and-drop operation between two elements.       | `source_locator`: Locator of the source element <br> `target_locator`: Locator of the target element                                         | `bool`: `True` if successful, `False` otherwise |
| `send_keys_to_body(keys)`          | Sends keyboard input to the body of the page.                 | `keys`: Keys to send (e.g., `'a'`, `'enter'`, etc.)                                                                                                | `bool`: `True` if successful, `False` otherwise |
| `accept_cookies(id_name="cookie", class_name="cookie", accept_name="accept")` | Accepts cookies if the button is present, with customizable selectors. | `id_name`: Selector for the ID (default is `"cookie"`) <br> `class_name`: Selector for the class (default is `"cookie"`) <br> `accept_name`: Selector for the accept button (default is `"accept"`) | `None` |
| `wait_for_element(by, locator, timeout=10)`  | Waits for an element to be present on the page within a specified timeout. | `by`: Method to locate the element (e.g., `By.ID`, `By.XPATH`) <br> `locator`: Locator string <br> `timeout`: Time to wait (default is `10` seconds) | `WebElement`: If found, returns the element, otherwise `None` |
| `click_by_image(image_path)`        | Clicks an element based on an image located on the screen.    | `image_path`: Path to the image to be located and clicked                                   | `bool`: `True` if successful, `False` if timeout occurs |

### Utilities

| **Method**                               | **Description**                                               | **Arguments**                                                                                                                                   | **Returns**                                    |
|------------------------------------------|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `take_screenshot(file_name)`             | Captures a screenshot of the browser.                        | `file_name`: The name of the file to save the screenshot.                                                                                       | `None`                                         |
| `scroll_to_element(by, locator)`         | Scrolls to a specific element on the page.                    | `by`: Locator method (e.g., `By.ID`, `By.XPATH`). <br> `locator`: Locator string.                                                              | `None`                                         |
| `is_valid_ip_address(ip)`         | Checks whether the input is a valid IP address.                    | `by`: IP address (e.g., `192.168.0.1`).                                                             | `bool`: `True` if it is an IP address, `False` if it not an IP address.                                         |
| `prepare_url(input_path_or_url)`        Checks an input to see whether it is a URL or a local file path,
    and adds 'file://' for local paths if necessary.                    | `input_path_or_url`: The URL or local path (e.g., `www.google.com`, `/var/www/index.html`).                                                              | `str`: A valid URL or a file path with 'file://'                                        |


### Console and Network Logs

| **Method**                          | **Description**                                               | **Arguments**                                                                                                                                   | **Returns**                                    |
|-------------------------------------|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| `get_console_logs()`                | Fetches the console logs from the browser.                    | None                                                                                                                                            | `list`: List of console log entries from the browser |
| `get_network_logs()`                | Fetches the network logs (if supported by the driver).        | None                                                                                                                                            | `list`: List of network log entries                 |

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to suggest improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 

---

Enjoy automated browsing with **PyChromeController**! 🚀
