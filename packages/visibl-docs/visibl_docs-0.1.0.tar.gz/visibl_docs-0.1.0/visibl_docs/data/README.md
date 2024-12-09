# Data

The **data** folder stores data generated and used by Visibl Docs during operation. This includes processed repositories and generated markdown files.

## **Components**

### **1. `repositories/`**

- **Purpose**: (Optional) May store temporary data or caches of the user's repositories during processing.
- **Note**: Depending on implementation, repository data might be processed in place or stored here for intermediate processing.

### **2. `markdown_files/`**

- **Purpose**: Stores the generated markdown files before they are moved to the user's `docs/` folder.
- **Functions**:
  - Acts as a staging area for markdown content.
  - Ensures that generated documentation is properly formatted before deployment.

## **Data Flow**

1. **Repository Processing**
   - Source files from the user's repository are read and processed.
   - Any necessary data is temporarily stored or cached.

2. **Markdown Generation**
   - Generated markdown files are saved in `markdown_files/`.
   - Once verified, they are moved to the `docs/` folder in the user's repository.

---

**Note**: The `data/` folder is essential for handling intermediate data during processing but may vary based on specific implementation choices.