# Young Lion Python Library

The **Young Lion Python Library** is designed to simplify the work of developers, especially *Young Lion Developers*. This library provides a wide range of functionalities for handling various file formats, managing directories, and executing file-related operations efficiently.

This library is under development and will be expanded with more features in the future.

# Attention! 
If an error or problem occurs during the installation, you may need to run this code in the terminal:
```
pip cache purge
python -m pip install --upgrade pip
pip install YoungLion
```
---

## Modules

### `function`
The `function` module contains a versatile `File` class that provides advanced file manipulation capabilities. The class supports operations for file formats such as JSON, TXT, CSV, PDF, XML, YAML, INI, Markdown, HTML, and more.
### `VISTA`
`VISTA` stands for (Visual Information System and Technological Analysis). This module contains the functions required to create Visual, Video, Audio and Analytical tables.
---
# YoungLion function
## File Class

The `File` class includes methods for handling various file types and operations with robust error handling, flexible path management, and default value support. Below is a breakdown of the supported features:

### Supported File Formats
- `.json`, `.txt`, `.log`, `.pdf`, `.xml`, `.csv`
- `.yml`, `.yaml`, `.ini`, `.properties`, `.md`, `.rtf`
- `.html`, `.css`, `.js`

### Key Functionalities
#### Initialization
- **`__init__(filefolder: Optional[str])`**
  - Initializes the `File` object with an optional root directory for default path handling.

#### JSON File Operations
- **`json_read(path: str, default: Optional[dict]) -> dict`**
  - Reads JSON data into a dictionary. Creates a file if missing.
- **`json_write(path: str, data: dict)`**
  - Writes a dictionary to a JSON file.

#### TXT File Operations
- **`txt_read_str(path: str) -> str`**
  - Reads a text file as a single string.
- **`txt_write_str(path: str, content: str)`**
  - Writes string content to a text file.

#### CSV File Operations
- **`csv_read(path: str, delimiter: str = ',', quotechar: str = '"') -> List[Dict[str, str]]`**
  - Reads a CSV file into a list of dictionaries.
- **`csv_write(path: str, data: List[Dict[str, str]], fieldnames: Optional[List[str]])`**
  - Writes a list of dictionaries to a CSV file.

#### PDF File Operations
- **`pdf_read(path: str) -> str`**
  - Reads text from a PDF file.
- **`pdf_write(path: str, content: str)`**
  - Writes text content to a PDF file.

#### XML File Operations
- **`xml_read(path: str) -> Optional[Dict[str, Any]]`**
  - Reads an XML file and parses it into a dictionary.
- **`xml_write(path: str, data: Dict[str, Any])`**
  - Writes a dictionary to an XML file.

#### YAML and INI Operations
- **`yaml_read(path: str, default: Optional[dict]) -> dict`**
  - Reads YAML content into a dictionary.
- **`ini_read(path: str, default: Optional[Dict[str, Dict[str, str]]]) -> Dict[str, Dict[str, str]]`**
  - Reads INI files into a dictionary structure.

#### Markdown Operations
- **`md_read(path: str) -> str`**
  - Reads a Markdown file.
- **`md_write(path: str, content: str, append: bool)`**
  - Writes or appends content to a Markdown file.

#### SQL Operations
- **`sql_execute(path: str, query: str, params: tuple)`**
  - Executes SQL queries on a database file.

#### Compressed File Handling
- **`handle_compressed(path: str, action: str, target: Optional[str])`**
  - Compresses directories or extracts files from archives.

---

## Installation
To include the library in your project:
1. Clone this repository.
2. Import the module:
   ```python
   from YoungLion.function import File
   ```

---

Here is the complete example section for all functions in the **File** class. These examples are ready to be included in your README file.

---

## Usage Examples

Below are examples for using each function in the `File` class.

### JSON File Operations

#### `json_read`
```python
file_handler = File()

# Reading a JSON file
default_data = {"name": "Unknown", "age": 0}
data = file_handler.json_read("data.json", default=default_data)
print(data)
```

#### `json_write`
```python
# Writing to a JSON file
data_to_save = {"name": "John", "age": 30}
file_handler.json_write("data.json", data_to_save)
```

### TXT File Operations

#### `txt_read_str`
```python
# Reading text from a file
content = file_handler.txt_read_str("example.txt")
print(content)
```

#### `txt_write_str`
```python
# Writing text to a file
file_handler.txt_write_str("example.txt", "Hello, World!")
```

### CSV File Operations

#### `csv_read`
```python
# Reading a CSV file
csv_data = file_handler.csv_read("data.csv")
print(csv_data)
```

#### `csv_write`
```python
# Writing to a CSV file
csv_content = [{"name": "Alice", "age": "25"}, {"name": "Bob", "age": "30"}]
file_handler.csv_write("data.csv", csv_content, fieldnames=["name", "age"])
```

### PDF File Operations

#### `pdf_read`
```python
# Reading a PDF file
pdf_text = file_handler.pdf_read("example.pdf")
print(pdf_text)
```

#### `pdf_write`
```python
# Writing to a PDF file
file_handler.pdf_write("example.pdf", "This is a sample PDF content.")
```

### XML File Operations

#### `xml_read`
```python
# Reading XML content
xml_data = file_handler.xml_read("data.xml")
print(xml_data)
```

#### `xml_write`
```python
# Writing to an XML file
xml_content = {"person": {"name": "Alice", "age": "25"}}
file_handler.xml_write("data.xml", xml_content)
```

### YAML File Operations

#### `yaml_read`
```python
# Reading a YAML file
yaml_data = file_handler.yaml_read("config.yaml")
print(yaml_data)
```

#### `yaml_write`
```python
# Writing to a YAML file
yaml_content = {"database": {"host": "localhost", "port": 3306}}
file_handler.yaml_write("config.yaml", yaml_content)
```

### INI File Operations

#### `ini_read`
```python
# Reading an INI file
ini_data = file_handler.ini_read("settings.ini")
print(ini_data)
```

#### `ini_write`
```python
# Writing to an INI file
ini_content = {"Section1": {"key1": "value1", "key2": "value2"}}
file_handler.ini_write("settings.ini", ini_content)
```

### Markdown File Operations

#### `md_read`
```python
# Reading a Markdown file
markdown_content = file_handler.md_read("README.md")
print(markdown_content)
```

#### `md_write`
```python
# Writing to a Markdown file
file_handler.md_write("README.md", "# Hello World\nThis is a markdown file.")
```

### Log File Operations

#### `log_read`
```python
# Reading a log file
log_content = file_handler.log_read("app.log")
print(log_content)
```

#### `log_write`
```python
# Writing a log entry
file_handler.log_write("app.log", "Application started.")
```

### HTML File Operations

#### `html_read`
```python
# Reading an HTML file
html_content = file_handler.html_read("index.html")
print(html_content)
```

#### `html_write`
```python
# Writing to an HTML file
file_handler.html_write("index.html", "<h1>Hello World</h1>")
```

### Compressed File Handling

#### `handle_compressed`
```python
# Compressing a directory
file_handler.handle_compressed("example_folder", "compress", "archive.zip")

# Extracting from a compressed file
file_handler.handle_compressed("archive.zip", "extract", "output_folder")
```
---

# YoungLion VISTA

Here’s a detailed explanation of the **VISTA** classes, describing their purpose, functionality, and available methods:

---

## **1. ImageTool Class**

### Description:
The **ImageTool** class is designed for handling image processing tasks. It allows developers to perform common operations such as loading, saving, resizing, and text recognition with images.

### Key Features:
- Load images from disk or URLs.
- Save images in multiple formats.
- Resize images or convert them to grayscale.
- Perform Optical Character Recognition (OCR) to extract text from images.
- Overlay text on images or convert them to binary (black-and-white).

### Methods:
1. **`load(path: str)`**  
   Loads an image from the specified path. If the file doesn’t exist, it creates a placeholder black image.
   
2. **`save(image, path: str, format: str = 'PNG', optimize: bool = True, quality: int = 85)`**  
   Saves an image with options for format, optimization, and quality.

3. **`load_url(url: str, mode: str = 'RGBA')`**  
   Fetches an image from a URL and converts it to a specified mode.

4. **`resize(image, size: tuple)`**  
   Changes the dimensions of an image.

5. **`convert_to_grayscale(image)`**  
   Converts the image to grayscale.

6. **`read_text_from_image(image)`**  
   Extracts text from an image using OCR.

7. **`draw_text_on_image(image, text: str, position: tuple, font_size: int, color: str)`**  
   Adds text to an image at a specified position.

8. **`convert_to_binary(image, threshold: int = 128)`**  
   Converts an image to black-and-white based on a threshold.

---

## **2. VideoTool Class**

### Description:
The **VideoTool** class provides utilities for working with video files. It supports creating videos, adding audio, extracting frames, and manipulating existing videos.

### Key Features:
- Generate videos from images or waveforms.
- Add or replace audio tracks in video files.
- Resize or convert video formats.
- Combine multiple videos into one.
- Trim or annotate videos with text.

### Methods:
1. **`image_to_video(image_path: str, duration: int, output_path: str, fps: int = 24)`**  
   Creates a video from a single image with a set duration.

2. **`audio_to_waveform_video(audio_path: str, output_path: str, sample_rate: int, fps: int)`**  
   Converts an audio file into a waveform video.

3. **`add_audio_to_video(video_path: str, audio_path: str, output_path: str)`**  
   Combines a video file with an audio file.

4. **`resize_video(video_path: str, output_path: str, size: tuple)`**  
   Resizes a video to new dimensions.

5. **`trim_video(video_path: str, start_time: float, end_time: float, output_path: str)`**  
   Extracts a specific segment from a video.

6. **`concatenate_videos(video_paths: list, output_path: str)`**  
   Joins multiple videos into one.

7. **`extract_audio_from_video(video_path: str, output_audio_path: str)`**  
   Saves the audio track of a video as a separate file.

---

## **3. AudioTool Class**

### Description:
The **AudioTool** class focuses on audio processing tasks. It enables developers to manipulate audio files, including trimming, merging, adjusting pitch, and generating sine waves.

### Key Features:
- Trim audio or extract segments.
- Adjust playback speed or pitch.
- Merge multiple audio files or create waveforms.
- Generate tones or rhythms programmatically.

### Methods:
1. **`trim_audio(audio_path: str, output_path: str, target_duration: float)`**  
   Shortens the audio file to a specified duration.

2. **`change_speed(audio_path: str, output_path: str, speed_factor: float)`**  
   Speeds up or slows down the audio.

3. **`change_pitch(audio_path: str, output_path: str, n_steps: int)`**  
   Modifies the pitch of the audio.

4. **`merge_audios(audio_paths: list, output_path: str)`**  
   Combines multiple audio files into one.

5. **`generate_sine_wave(frequency: float, duration: float, output_path: str)`**  
   Creates a pure sine wave audio file.

6. **`extract_segment(audio_path: str, output_path: str, start_time: float, end_time: float)`**  
   Extracts a section of audio between specific time intervals.

---

## **4. AnalysisTableTool Class**

### Description:
The **AnalysisTableTool** class provides utilities for creating graphical representations of data, including graphs, charts, and scatter plots. It’s ideal for visualizing data in analytics and reports.

### Key Features:
- Create bar, pie, scatter, and line charts.
- Visualize graphs with nodes and curved edges.
- Save charts as images or display them interactively.

### Methods:
1. **`plot_graph(nodes: dict, edges: list, title: str, rad: int)`**  
   Visualizes a graph with curved edges connecting nodes.

2. **`generate_bar_chart(data: dict, x_axis_label: str, y_axis_label: str)`**  
   Creates a bar chart from a dictionary of data.

3. **`generate_pie_chart(data: dict, title: str)`**  
   Generates a pie chart.

4. **`generate_line_chart(x_data: list, y_data: list, title: str, x_axis_label: str, y_axis_label: str)`**  
   Plots a line chart.

5. **`generate_scatter_plot(x_data: list, y_data: list, title: str)`**  
   Creates a scatter plot to visualize relationships.

6. **`generate_histogram(data: list, num_bins: int, title: str)`**  
   Creates a histogram to display data distribution.

7. **`generate_box_plot(data: list, labels: list, title: str)`**  
   Produces a box plot for statistical analysis.

---

## Installation
To include the library in your project:
1. Clone this repository.
2. Import the module:
   ```python
   from YoungLion import VISTA
   ```

---

## Usage Examples

---

Usage of `ImageTool` and `Image` class:

### Examples

#### 1. **Loading and Saving a Local Image**
```python

# Loading and saving an image using the ImageTool class
tool = VISTA.ImageTool()
image = tool.load("example.jpg") # Loads a local file
tool.save(image, "output.png") # Saves in a different format
```

```python
# Using the Image class
img = VISTA.Image()
img.load("example.jpg").save("output.png")
```

---

#### 2. **Loading an Image from a URL**
```python
# Using ImageTool
image = tool.load_url("https://example.com/image.png")
tool.save(image, "downloaded_image.png")
```

```python
# Use with Image class
img = VISTA.Image()
img.load_from_url("https://example.com/image.png").save("downloaded_image.png")
```

---

#### 3. **Resize Image**
```python
# Using ImageTool
resized_image = tool.resize(image, (100, 100))
tool.save(resized_image, "resized_image.png")
```

```python
# Use with Image class
img = VISTA.Image()
img.load("example.jpg").resize((100, 100)).save("resized_image.png")
```

---

#### 4. **Converting an Image to Grayscale**
```python
# Using ImageTool
grayscale_image = tool.convert_to_grayscale(image)
tool.save(grayscale_image, "grayscale_image.png")
```

```python
# Using Image class
img = VISTA.Image()
img.load("example.jpg").convert_to_grayscale().save("grayscale_image.png")
```

---

#### 5. **Writing Text on an Image**
```python
# Using ImageTool
text_image = tool.draw_text_on_image(image, "Hello World!", position=(50, 50), font_size=20, color="red")
tool.save(text_image, "text_on_image.png")
```

```python
# Using with Image class
img = VISTA.Image()
img.load("example.jpg").draw_text("Hello World!", position=(50, 50), font_size=20, color="red").save("text_on_image.png")
```

---

#### 6. **Reading Text from Image with OCR**
```python
# Using ImageTool
extracted_text = tool.read_text_from_image(image)
print("Text Read from Image:", extracted_text)
```

```python
# Using with Image class
img = VISTA.Image()
img.load("text_image.png")
extracted_text = img.read_text()
print("Read from Image Text:", extracted_text)
```

---

#### 7. **Converting Image to Binary Format**
```python
# Using ImageTool
binary_image = tool.convert_to_binary(image, threshold=128)
tool.save(binary_image, "binary_image.png")
```

```python
# Using with Image class
img = VISTA.Image()
img.load("example.jpg").convert_to_binary(threshold=128).save("binary_image.png")
```

---

Usage of `VideoTool` class:


## Contribution
Contributions to the **Young Lion Python Library** are welcome! Please open issues or submit pull requests to suggest enhancements or report bugs.

---

## License
This project is licensed under the MIT License.
