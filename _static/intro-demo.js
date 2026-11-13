// Terminal recording for the intro page: shows the source of a small PySide6
// program, the Nuitka command compiling it, and the resulting program window.
// The log lines are Nuitka's own messages, timings are shortened.

const initIntroDemo = () => {
  const demo = document.getElementById("intro-demo");
  if (!demo) {
    return;
  }

  const screen = demo.querySelector(".intro-term-screen");
  const playButton = demo.querySelector(".intro-play");
  const progress = demo.querySelector(".intro-progress");
  const progressFill = demo.querySelector(".intro-progress-fill");
  const timeLabel = demo.querySelector(".intro-time");
  const stepButtons = demo.querySelectorAll(".intro-step");
  const programWindow = demo.querySelector(".intro-window");

  const prompt = "PS C:\\work\\stock-viewer> ";

  const code = `import csv
import sys

from PySide6.QtWidgets import (QApplication, QLineEdit, QMainWindow,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

STOCK = [
    ("BRG-6204", "Ball bearing 6204-2RS", 412, "A-03"),
    ("BLT-M8x30", "Hex bolt M8 x 30, zinc", 2380, "B-11"),
    ("SEN-PT100", "PT100 temperature sensor", 37, "C-02"),
    ("FLT-HY10", "Hydraulic filter 10 um", 64, "A-07"),
    ("VLV-BV25", "Ball valve DN25", 18, "D-01"),
    ("CBL-CAT6", "Cat6 patch cable 2 m", 155, "C-09"),
]


class StockViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Viewer")
        self.search = QLineEdit(placeholderText="Search parts...")
        self.search.textChanged.connect(self.filter)
        self.table = QTableWidget(len(STOCK), 4)
        self.table.setHorizontalHeaderLabels(
            ["Part", "Description", "In stock", "Location"])
        for row, item in enumerate(STOCK):
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        export = QPushButton("Export CSV")
        export.clicked.connect(self.export)
        layout = QVBoxLayout()
        for widget in (self.search, self.table, export):
            layout.addWidget(widget)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.statusBar().showMessage(f"{len(STOCK)} items")

    def filter(self, text):
        for row, item in enumerate(STOCK):
            hidden = text.lower() not in " ".join(map(str, item)).lower()
            self.table.setRowHidden(row, hidden)

    def export(self):
        with open("stock.csv", "w", newline="") as f:
            csv.writer(f).writerows(STOCK)
        self.statusBar().showMessage(f"Exported {len(STOCK)} rows to stock.csv")


app = QApplication(sys.argv)
window = StockViewer()
window.show()
sys.exit(app.exec())`;

  const command =
    "python -m nuitka --mode=onefile --enable-plugins=pyside6 " +
    "--windows-console-mode=disable --output-filename=StockViewer.exe stock_viewer.py";

  const compileLog = [
    "Nuitka-Options: Used command line options:",
    "Nuitka-Options:   --mode=onefile --enable-plugins=pyside6 --windows-console-mode=disable",
    "Nuitka-Options:   --output-filename=StockViewer.exe stock_viewer.py",
    "Nuitka: Starting Python compilation with: Version '4.3' on Python 3.13 (flavor 'CPython Official') commercial grade 'not installed'.",
    "Nuitka: Completed Python level compilation and optimization.",
    "Nuitka-Plugins:pyside6: Including Qt plugins 'iconengines,imageformats,platforms,styles,tls' below 'PySide6\\qt-plugins'.",
    "Nuitka: Generating source code for C backend compiler.",
    "Nuitka: Running data composer tool for optimal constant value handling.",
    "Nuitka: Running C compilation via Scons.",
    "Nuitka-Scons: Backend C compiler: cl (cl 14.4).",
  ];

  const finishLog = [
    "Nuitka-Scons: Backend C linking with 214 files (no progress information available for this stage).",
    "Nuitka-Onefile: Creating single file from dist folder, this may take a while.",
    "Nuitka-Onefile: Running bootstrap binary compilation via Scons.",
    "Nuitka-Onefile: Using compression for onefile payload.",
    "Nuitka: Successfully created 'StockViewer.exe'.",
  ];

  // Small Python highlighter, only what the demo program needs.
  const keywords = new Set(["import", "from", "class", "def", "for", "in", "not", "return", "with", "as", "self"]);

  const highlightPython = (line) => {
    const parts = [];
    const pattern = /(f?"(?:[^"\\]|\\.)*")|(\b\d+\b)|([A-Za-z_]\w*)(?=\()|([A-Za-z_]\w*)|(\s+|[^\w\s])/g;
    let match;
    while ((match = pattern.exec(line))) {
      if (match[1]) {
        parts.push(["intro-t-str", match[1]]);
      } else if (match[2]) {
        parts.push(["intro-t-num", match[2]]);
      } else if (match[3]) {
        parts.push([keywords.has(match[3]) ? "intro-t-kw" : "intro-t-fn", match[3]]);
      } else if (match[4]) {
        parts.push([keywords.has(match[4]) ? "intro-t-kw" : "", match[4]]);
      } else {
        parts.push(["", match[5]]);
      }
    }
    return parts;
  };

  const logParts = (line) => {
    const match = /^(Nuitka[\w-]*(?::[\w-]+)?:)(.*)$/.exec(line);
    if (!match) {
      return [["", line]];
    }
    const success = match[2].includes("Successfully created");
    return [
      ["intro-t-tag", match[1]],
      [success ? "intro-t-ok" : "", match[2]],
    ];
  };

  // Build the recording as a list of timed events.
  const events = [];
  const stepStarts = [];
  let clock = 0;

  const add = (event) => {
    event.time = clock;
    events.push(event);
  };
  const wait = (ms) => {
    clock += ms;
  };
  const typeCommand = (text, speed) => {
    add({ kind: "line", parts: [["intro-t-p", prompt]] });
    wait(400);
    for (const char of text) {
      add({ kind: "type", char });
      wait(speed);
    }
    wait(350);
  };
  const print = (lines, gap, partsOf) => {
    for (const line of lines) {
      add({ kind: "line", parts: partsOf(line) });
      wait(gap);
    }
  };
  const progressBar = (total, ms) => {
    const steps = 25;
    add({ kind: "line", parts: [] });
    for (let i = 0; i <= steps; i++) {
      const done = Math.round((total * i) / steps);
      add({
        kind: "replace",
        parts: [
          ["intro-t-tag", "Nuitka-Scons:Backend C: "],
          ["intro-t-bar", "\u2501".repeat(i)],
          ["intro-t-dim", "\u2501".repeat(steps - i)],
          ["", ` ${done}/${total} files`],
        ],
      });
      wait(ms / steps);
    }
  };

  stepStarts.push(clock);
  wait(300);
  typeCommand("type stock_viewer.py", 45);
  print(code.split("\n"), 40, highlightPython);
  wait(900);

  stepStarts.push(clock);
  typeCommand(command, 20);
  print(compileLog, 450, logParts);
  progressBar(214, 2500);
  print(["\u22ef recording shortened, the C compilation takes longer"], 300, (line) => [["intro-t-note", line]]);
  print(finishLog, 600, logParts);

  stepStarts.push(clock);
  typeCommand(".\\StockViewer.exe", 60);
  add({ kind: "launch" });
  wait(200);
  add({ kind: "line", parts: [["intro-t-p", prompt]] });
  wait(1000);

  const duration = clock;

  // Playback state.
  let position = 0;
  let nextEvent = 0;
  let playing = false;
  let lastFrame = 0;
  let windowOpen = false;

  const renderLine = (parts) => {
    const div = document.createElement("div");
    for (const [cls, text] of parts) {
      const span = document.createElement("span");
      if (cls) {
        span.className = cls;
      }
      span.textContent = text;
      div.appendChild(span);
    }
    return div;
  };

  const setWindow = (open) => {
    if (open === windowOpen) {
      return;
    }
    windowOpen = open;
    if (open) {
      resetProgram();
    }
    programWindow.hidden = !open;
  };

  const apply = (event) => {
    if (event.kind === "line") {
      screen.appendChild(renderLine(event.parts));
    } else if (event.kind === "replace") {
      screen.replaceChild(renderLine(event.parts), screen.lastChild);
    } else if (event.kind === "type") {
      screen.lastChild.appendChild(document.createTextNode(event.char));
    } else if (event.kind === "launch") {
      setWindow(true);
    }
  };

  const formatTime = (ms) => {
    const seconds = Math.floor(ms / 1000);
    return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
  };

  const updateControls = () => {
    progressFill.style.width = `${(position / duration) * 100}%`;
    progress.setAttribute("aria-valuenow", String(Math.round((position / duration) * 100)));
    timeLabel.textContent = `${formatTime(position)} / ${formatTime(duration)}`;

    let step = 0;
    stepStarts.forEach((start, index) => {
      if (position >= start) {
        step = index;
      }
    });
    stepButtons.forEach((button, index) => {
      button.classList.toggle("intro-step-active", index === step);
    });

    const ended = position >= duration;
    playButton.innerHTML = playing
      ? '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="2.5" width="3" height="11" fill="currentColor"></rect><rect x="9.5" y="2.5" width="3" height="11" fill="currentColor"></rect></svg>'
      : '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z" fill="currentColor"></path></svg>';
    playButton.setAttribute("aria-label", playing ? "Pause" : ended ? "Replay" : "Play");
  };

  const advance = () => {
    while (nextEvent < events.length && events[nextEvent].time <= position) {
      apply(events[nextEvent]);
      nextEvent += 1;
    }
    screen.scrollTop = screen.scrollHeight;
  };

  const seek = (target) => {
    position = Math.max(0, Math.min(duration, target));
    screen.textContent = "";
    nextEvent = 0;
    setWindow(false);
    advance();
    updateControls();
  };

  const frame = (now) => {
    if (!playing) {
      return;
    }
    position = Math.min(duration, position + Math.min(100, now - lastFrame));
    lastFrame = now;
    advance();
    if (position >= duration) {
      playing = false;
    }
    updateControls();
    if (playing) {
      requestAnimationFrame(frame);
    }
  };

  const play = () => {
    if (position >= duration) {
      seek(0);
    }
    playing = true;
    lastFrame = performance.now();
    updateControls();
    requestAnimationFrame(frame);
  };

  const pause = () => {
    playing = false;
    updateControls();
  };

  playButton.addEventListener("click", () => (playing ? pause() : play()));

  progress.addEventListener("click", (event) => {
    const box = progress.getBoundingClientRect();
    seek(((event.clientX - box.left) / box.width) * duration);
  });

  progress.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
      seek(position + 2000);
      event.preventDefault();
    } else if (event.key === "ArrowLeft") {
      seek(position - 2000);
      event.preventDefault();
    }
  });

  stepButtons.forEach((button) => {
    button.addEventListener("click", () => {
      seek(stepStarts[Number(button.dataset.step)] + 1);
      play();
    });
  });

  // The compiled program: search, row selection, export and close work.
  const search = programWindow.querySelector(".intro-window-search");
  const rows = programWindow.querySelectorAll("tbody tr");
  const status = programWindow.querySelector(".intro-window-status");

  const resetProgram = () => {
    search.value = "";
    rows.forEach((row) => {
      row.hidden = false;
      row.classList.remove("intro-row-selected");
    });
    status.textContent = `${rows.length} items`;
  };

  search.addEventListener("input", () => {
    const text = search.value.toLowerCase();
    rows.forEach((row) => {
      row.hidden = !row.textContent.toLowerCase().includes(text);
    });
  });

  rows.forEach((row) => {
    row.addEventListener("click", () => {
      rows.forEach((other) => other.classList.remove("intro-row-selected"));
      row.classList.add("intro-row-selected");
    });
  });

  programWindow.querySelector(".intro-window-export").addEventListener("click", () => {
    status.textContent = `Exported ${rows.length} rows to stock.csv`;
  });

  programWindow.querySelector(".intro-window-close").addEventListener("click", () => {
    windowOpen = false;
    programWindow.hidden = true;
  });

  // Start at the end, so the page shows the result without JavaScript
  // running the recording, then play once it becomes visible.
  seek(duration);

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          observer.disconnect();
          seek(0);
          play();
        }
      },
      { threshold: 0.4 },
    );
    observer.observe(demo);
  } else {
    seek(0);
    play();
  }
};

// Scripts are combined and loaded async, so the document may be ready already.
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initIntroDemo);
} else {
  initIntroDemo();
}
