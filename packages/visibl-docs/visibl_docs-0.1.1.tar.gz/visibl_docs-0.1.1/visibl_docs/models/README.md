# Models

The **models** contain the core business logic of Visibl Docs. They handle data processing, interactions with local repositories, LLM-based functions, and markdown file generation.

## **Components**

### **1. `repository_processor.py`**

- **Purpose**: Processes the user's local repository to prepare for documentation generation.
- **Functions**:
  - Scans the repository for source files (`.sv`, `.v`, etc.).
  - Extracts relevant data and metadata.
  - Prepares data structures for markdown generation.

### **2. `ollama_processor.py`**

- **Purpose**: Handles LLM-based processing using the Ollama framework.
- **Functions**:
  - **Chat Module**: Generates changes to markdown files, answers user questions.
  - **Search Module**: Implements search functionality within the documentation.
  - **Gen and AutoGen Modules**: Automatically generate documentation content using deterministic logic and LLM assistance.
- **Data Flow**:
  - Receives input from controllers.
  - Streams responses back to the controllers for real-time UI updates.

### **3. `markdown_generator.py`**

- **Purpose**: Generates markdown files based on processed data.
- **Functions**:
  - Creates one-to-one markdown files corresponding to each source file.
  - Generates folder-level documentation that describes component interconnections.
  - Manages metadata for navigation and page configuration.

## **Data Flow**

1. **Documentation Generation**
   - Controllers invoke functions in `repository_processor.py` to analyze the repository.
   - Extracted data is passed to `markdown_generator.py`.
   - `ollama_processor.py` may be called to enhance content using LLMs.
   - Markdown files are generated and saved in the `docs/` folder within the user's repository.

2. **LLM-Based Processing**
   - User commands or UI interactions trigger LLM functions.
   - `ollama_processor.py` processes the input and streams responses.
   - Responses are used to update markdown files and provide real-time UI feedback.

---

**Note**: The models are crucial for the core functionality, transforming user inputs and repository data into comprehensive documentation.