# NoteFlow

> **FORMAT CHANGE NOTICE**: As of version 0.3.0, the note separator has changed from `---` to `<!-- note -->`. Please update your notes.md file to use the new format.

NoteFlow is a lightweight, Markdown-based note-taking application with task management capabilities. It provides a clean interface for creating, viewing, and managing notes with support for tasks, images, files,and code snippets.

## Features
#### Initial View:
![Initial View](/screenshot_1.png)
#### Markdown Editor:
![Markdown Editor](/screenshot_2.png)
#### Upload Images and Files:
![Upload Images and Files](/screenshot_3.png)
#### Point in Time Site Copy/Bookmark:
![Point in Time Site Copy/Bookmark](/screenshot_4.png)
#### Multiple Themes:
![Multiple Themes](/screenshot_5.png)
#### Math Rendering:
![Math Rendering](/screenshot_6.png)

## Features

- **📝 One Big Markdown File**: All notes stream into a single Markdown file, creating a natural timeline
- **✅ Active Tasks Tracking**: Active tasks automatically surface to a dedicated panel
- **🔍 Pure Markdown**: Write in plain Markdown and use checkboxes for task management
- **💾 Zero Database**: Your entire note history lives in one portable Markdown file
- **🚀 Instant Start**: Zero configuration required - just launch and start writing
- **🔒 Privacy First**: Runs entirely local - your notes never leave your machine
- **✨ Modern / Retro Interface**: Clean, responsive design built with FastAPI
- **📚 Site Links and Archival**: Save site links, and generate a static HTML archive version of linked sites
- **🎨 Multiple Themes**: Choose from a variety of themes
- **🔗 Save Files/Images**: Archive files and images locally
- **🖥️ Multiple Instances**: Open multiple instances of Noteflow to take notes in different directories

## Quick Start

To quickly get started with Noteflow, follow these steps:

### Installation Options

#### Using pip (All Platforms)
```bash
pip install noteflow
```

#### Using Homebrew (macOS/Linux)
```bash
brew tap Xafloc/noteflow
brew install noteflow
```

### Running Noteflow

You can run Noteflow in several ways:

#### From Current Directory
```bash
noteflow
```

#### Specify a Notes Directory
```bash
# Linux/macOS
noteflow /path/to/notes/folder

# Windows
noteflow C:\path\to\notes\folder
```

#### Run Multiple Instances
You can run multiple instances by specifying different directories:
```bash
noteflow /path/to/notes/folder1  # First instance
noteflow /path/to/notes/folder2  # Second instance
```

4. **Access the Application**: Your web browser should open automatically. If not, open your browser and navigate to:
   - Default instance: `http://localhost:8000`
   - Additional instance ports: `http://localhost:<port>`

## Requirements

- Python 3.9+
- FastAPI
- uvicorn
- markdown-it-py
- mdit-py-plugins
- Other dependencies listed in `requirements.txt`

### Taking Notes

- Type your note in the content area
- Optionally add a title
- Click "Add Note" or press Ctrl+Enter to save

### Creating Tasks

- Use Markdown checkboxes:
  ```markdown
  - [ ] New task
  - [x] Completed task
  ```
- Tasks automatically appear in the Active Tasks panel
- Click checkboxes to mark tasks as complete

### Attaching Images and Files

- Drag and drop images or files into the Noteflow input box to attach them to your note
- Images and files are automatically embedded in the note and saved locally within the assets/images and assets/files folders

### Saving Site Links and Archiving

- Create a link in your note by typing + followed by the URL (e.g., `+https://www.google.com`)
- Site link will be saved and archived locally within the assets/sites folder

### Markdown Support

NoteFlow supports standard Markdown syntax including:
- Headers
- Lists (bulleted and numbered)
- Checkboxes
- Bold/Italic text
- Code blocks
- Strikethrough
- Tables
- Blockquotes
- Math (using [MathJax](https://www.mathjax.org/))
- And more!

## File Structure

Your notes are stored in `notes.md` in your working directory, or the passed path argument. The file format is simple:

```markdown
## 2024-10-30 12:34:56 - Optional Title

Your note content here...

<!-- note -->

## 2024-10-30 12:33:45

Another note...
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details. This license ensures that:

- You can freely use, modify, and distribute this software
- Any modifications or derivative works must also be licensed under GPL-3.0
- The source code must be made available when distributing the software
- Changes made to the code must be documented

For more information, see the [full license text](https://www.gnu.org/licenses/gpl-3.0.en.html).

<div align="center">
Made with ❤️ for note-taking enthusiasts
</div>
