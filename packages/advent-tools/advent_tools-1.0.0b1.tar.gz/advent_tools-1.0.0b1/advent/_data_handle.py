"""
MIT License

Copyright (c) 2022-present Achyuth Jayadevan <achyuth@jayadevan.in>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ._config_reader import CONFIGURATION, UnformattedPath, get_session_token
from ._downloader import Downloader


def get(year: int, day: int) -> str | None:
    fullpath = UnformattedPath.join_path(year, day, *CONFIGURATION.download_path())
    if fullpath.exists():
        return fullpath.read_text() or None


def fetch(year: int, day: int) -> str:
    fullpath = UnformattedPath.join_path(year, day, *CONFIGURATION.download_path())
    token = get_session_token()
    content: str = Downloader(token).get_content_for_date(year, day)
    fullpath.parent.mkdir(parents=True, exist_ok=True)
    fullpath.write_text(content)
    return content


def getch(year: int, day: int) -> str:
    if data := get(year, day):
        return data
    return fetch(year, day)


def get_example_data(year: int, day: int) -> str:
    raise NotImplementedError("Example data not implemented yet")
