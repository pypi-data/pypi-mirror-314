# UI

The **ui** folder contains the user interface components of Visibl Docs. It includes static assets, templates, and the application logic to run the UI server.

## **Components**

### **1. `app.py`**

- **Purpose**: Serves as the entry point for the UI application.
- **Functions**:
  - Initializes the Flask application.
  - Registers routes and controllers.
  - Runs the local server to host the UI.

### **2. `templates/`**

- **Purpose**: Contains HTML templates used by the UI.
- **Components**:
  - Base templates for consistent layout.
  - Page templates for rendering documentation pages.
  - Navigation templates for menus and sidebars.

### **3. `static/`**

- **Purpose**: Holds static assets required by the UI.
- **Components**:
  - CSS files for styling.
  - JavaScript files for interactivity.
  - Images and icons used in the UI.

## **Data Flow**

1. **Launching the UI**
   - User runs `docs view`.
   - `app.py` starts the Flask server.
   - UI is accessible via a web browser or Electron application.

2. **Rendering Pages**
   - UI controllers handle requests for documentation pages.
   - Templates render the content using data from markdown files.
   - Static assets provide styling and interactivity.

3. **Real-Time Updates**
   - UI receives streamed data from models during processes like `docs gen`.
   - UI components update to reflect the current state of documentation generation.

---

**Note**: The UI provides a graphical interface for users to interact with their documentation, offering features beyond what is available in the terminal.