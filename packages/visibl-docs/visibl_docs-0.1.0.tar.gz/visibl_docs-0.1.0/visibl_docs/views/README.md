# Views

The **views** are responsible for presenting data to the user. They format and display information received from the controllers, whether in the terminal or the UI.

## **Components**

### **1. `terminal_view.py`**

- **Purpose**: Displays output and messages in the terminal.
- **Functions**:
  - Formats messages, errors, and process updates.
  - Ensures that terminal outputs are user-friendly and informative.

### **2. `ui_view.py`**

- **Purpose**: Renders data in the UI using templates.
- **Functions**:
  - Converts markdown files into HTML for display.
  - Utilizes templates to present documentation and navigation.
  - Updates UI elements in real-time based on streamed data from models.
  - Manages the presentation of process updates during documentation generation.

## **Data Flow**

1. **Terminal Output**
   - Receives data from `terminal_controller.py`.
   - Formats and displays the information to the user.

2. **UI Rendering**
   - Receives data from `ui_controller.py`.
   - Reads markdown files from the `docs/` folder.
   - Renders documentation pages and navigation menus.
   - Updates the UI in response to real-time data streams.

---

**Note**: The views ensure that users have a clear and intuitive experience when interacting with Visibl Docs, whether through the terminal or the UI.