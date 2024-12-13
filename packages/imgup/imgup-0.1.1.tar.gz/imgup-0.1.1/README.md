<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.ibb.co.com/4dPHMNg/imgup.png" alt="imgup"></a>
</p>

<h3 align="center">IMGUP</h3>

<div align="center">

> pip install imgup

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/decryptable/imgup.svg)](https://github.com/decryptable/imgup/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/decryptable/imgup.svg)](https://github.com/decryptable/imgup/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> IMGUP is a simple CLI tool for uploading images to imgbb with ease.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](#contributing)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

IMGUP is a command-line interface (CLI) tool designed to simplify image uploads to the imgbb image hosting service. It supports single and multiple file uploads, providing URLs of the hosted images after successful uploads.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will guide you on how to set up and use IMGUP on your local machine.

### Prerequisites

Ensure you have Python 3.6 or newer installed.

```
pip install requests
```

### Installing

#### Install via pip (PyPI):

```bash
pip install imgup
```

#### Install from source:

1. Clone the repository:

   ```bash
   git clone https://github.com/decryptable/imgup.git
   ```

2. Navigate to the project directory:

   ```bash
   cd imgup
   ```

3. Install the package locally:
   ```bash
   pip install .
   ```

## 🎈 Usage <a name="usage"></a>

To upload a single image:

```bash
imgup /path/to/image.png
```

To upload multiple images:

```bash
imgup /path/to/image1.png /path/to/image2.png
```

Example output:

```plaintext
Total of 2 file paths and URLs
Uploading...
Uploading 1/2
Uploading 2/2
Output URLs:
https://i.ibb.co.com/tcnKMN8/1733997716.png
https://i.ibb.co.com/zHcswJN/typora-icon-png.png
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.python.org/) - Programming Language
- [Requests](https://docs.python-requests.org/en/latest/) - HTTP Library

## ✍️ Authors <a name = "authors"></a>

- [@decryptable](https://github.com/decryptable) - Creator & Maintainer

See also the list of [contributors](https://github.com/decryptable/imgup/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Inspiration from similar CLI tools
- Special thanks to the imgbb API team for their service
