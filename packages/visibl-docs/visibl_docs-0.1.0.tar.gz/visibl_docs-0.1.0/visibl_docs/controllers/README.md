# Controllers

The **controllers** manage the interaction between the user inputs (from the terminal and UI) and the system's business logic defined in the models. They interpret user commands, invoke the necessary model functions, and pass data to the views for presentation.

## **Components**

### **1. `terminal_controller.py`**

- **Purpose**: Handles terminal commands entered by the user.
- **Functions**:
  - Captures and interprets commands like `docs init`, `docs gen`, `docs autogen`, and `docs view`.
  - Interacts with models to perform actions based on commands.
  - Sends output data to `terminal_view.py` for display.

### **2. `ui_controller.py`**

- **Purpose**: Manages routes and interactions within the UI.
- **Functions**:
  - Handles HTTP requests from the UI.
  - Calls model functions to process data requests.
  - Provides data to `ui_view.py` for rendering.
  - Sends real-time updates to the UI during processes like documentation generation.

## **Data Flow**

1. **Terminal Interaction**
   - User enters a command in the terminal.
   - `terminal_controller.py` interprets the command.
   - Invokes appropriate model functions.
   - Receives data/results from models.
   - Passes data to `terminal_view.py` for display.

2. **UI Interaction**
   - User interacts with the UI.
   - UI sends requests to `ui_controller.py`.
   - `ui_controller.py` interacts with models as needed.
   - Receives data/results from models.
   - Passes data to `ui_view.py` for rendering.

---

**Note**: The controllers act as the central hub for user interactions, ensuring that inputs are correctly processed and appropriate responses are generated.