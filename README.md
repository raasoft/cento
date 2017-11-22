# Cento

![](https://www.rd.com/wp-content/uploads/2016/04/06-cat-wants-to-tell-you-gift.jpg)

Cento is a cute dependency hunter.
It will go out in the wild and will catch all the dependencies that you need for your project.

Built with 💜 by [Riccardo Ancona](https://github.com/raasoft).

## Table of Contents
- [Philosophy](#philosophy)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Credits](#credits)
- [License](#license)

## 🐣 Philosophy

We believe programming should be fun and light, not stern and stressful. It's cool to be cute; using serious words without explaining them doesn't make for better results - if anything it scares people off. We don't want to be scary, we want to be nice and fun, and then _casually_ be the best choice around. _Real casually._

## 💾 Installation

### Dependencies

To launch *Cento*, you must install:

```bash
sudo apt-get install python-pip
sudo pip --upgrade pip
sudo pip install urlgrabber
sudo pip install patool
sudo pip install pyunpack
```

## ▶️ Usage

Just launch from the terminal:

```bash
sudo python ./cento.py
```

## ⚙ Configuration

_Cento_ needs **food** and a **litter**.

Put all the dependencies into the file `food.cento` in the project root. Example:

```
{
    "wkhtmltopdf": {
        "url": "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz", 
        "md5": "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz.md5", 
        "download_folder": "./DependencyTemp/wkhtmltopdf", 
        "unzip_folder": "/opt/", 
        "environment_variable": "WKHTMLTOPDF", 
        "environment_variable_path": "wkhtmltopdf"
    },

        "pandoc": {
            "url": "https://github.com/jgm/pandoc/releases/download/2.0.3/pandoc-2.0.3-linux.tar.gz", 
            "md5": "https://github.com/jgm/pandoc/releases/download/2.0.3/pandoc-2.0.3-linux.tar.gz.md5", 
            "download_folder": "./DependencyTemp/pandoc", 
            "unzip_folder": "/opt/", 
            "environment_variable": "PANDOC", 
            "environment_variable_path": "pandoc"
    }
}
```

Put http_proxy and https_proxy into `litter.cento` in the project root. If you think that _Cento_ does not need a litter, just leave those values empty. Example:

```
{
    "http_proxy": {
        "url": "http://user:pass@proxy:port"
    },

    "https_proxy": {
        "url": ""
    }
}
```


## ❤ Credits

Big hugs to:

* Sivi the unicorn 💛
* Cento the cat 🐱

Major dependencies:

* [pip](https://pypi.python.org/pypi/pip)
* [urlgrabber](http://urlgrabber.baseurl.org/)
* [pyunpack](https://pypi.python.org/pypi/pyunpack)

The following websites were a source of inspiration:

* [conan](https://www.conan.io/)

## 🎓 License

[MIT](http://webpro.mit-license.org/)
