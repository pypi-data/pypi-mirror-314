# **MF4Processor**

`MF4Processor` is a Python library for working with `.mf4` files, enabling you to extract channel names, convert specific channel data into CSV format, and retrieve signal data as NumPy arrays.

---

## **Features**
- Extract all channel names from `.mf4` files and save them to a `.txt` file.
- Convert a specific channel's signal data to a CSV file.
- Retrieve signal data as a NumPy array for further analysis.

---

## **Installation**

Install the library using `pip`:

```bash
pip install mf4processor
```

---

## **Usage**

### **1. Import the Library**

```python
from mf4processor.processor import MF4Processor
```

### **2. Load an `.mf4` File**

```python
processor = MF4Processor("path/to/your/file.mf4")
```

### **3. Save All Channel Names to a `.txt` File**

```python
processor.save_channel_names_to_txt("output_channels.txt")
```

### **4. Convert a Channel to CSV**

```python
processor.convert_channel_to_csv("Channel_Name", "output.csv")
```

### **5. Retrieve Signal Data as a NumPy Array**

```python
signal_data = processor.get_signal_as_numpy("Channel_Name")
print(signal_data)
```

---

## **Dependencies**

- `asammdf`
- `pandas`
- `numpy`

These dependencies are installed automatically with the library.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**

Contributions, issues, and feature requests are welcome! Feel free to open an issue on the [GitHub repository](https://github.com/varshithvhegde/mf4processor).

---

## **Author**

- **Varshith V Hegde**
- Email: varshithvh@gmail.com

---