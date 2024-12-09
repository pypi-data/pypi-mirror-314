# Configuration

The **config** folder contains configuration settings and parameters for Visibl Docs.

## **Components**

### **1. `settings.py`**

- **Purpose**: Defines configurable parameters for the application.
- **Functions**:
  - Stores paths, API keys, and other settings.
  - Allows for customization of behavior, such as output directories or LLM settings.

## **Data Flow**

- Configuration settings are loaded at application startup.
- Accessible by all components (controllers, models, views) as needed.
- Centralizes configuration to simplify maintenance and updates.

---

**Note**: Proper configuration is crucial for the application to function correctly and adapt to different environments or user preferences.