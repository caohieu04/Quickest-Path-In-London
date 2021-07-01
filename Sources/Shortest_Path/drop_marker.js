var wnd = window.open("http://stackoverflow.com");
setTimeout(function () {
  wnd.close();
}, 10000);
// window.open(`http://127.0.0.1:8000/byPos/?p1lat=${p1lat}&p1lon=${p1lon}&p2lat=${p2lat}&p2lon=${p2lon}`);