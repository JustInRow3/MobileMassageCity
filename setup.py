from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna", "selenium", "openpyxl", "time", "webdriver_manager", "Keys", "NoSuchElementException", "WebDriverWait", "expected_conditions",
            "webdriver", "Service", "By", "ChromeDriverManager", "Options", "configparser", "os", "misc", "pandas", "BeautifulSoup", "sys"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "main.py",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)