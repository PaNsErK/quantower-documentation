(function () {
  "use strict";

  var legacyStorageKey = "fzdocs.manual-test-state.v1";
  var allowedStatuses = ["open", "pass", "fail", "blocked", "improvement"];
  var maximumImportBytes = 256 * 1024;
  var noteLimit = 1000;
  var forbiddenNotePatterns = [
    /[A-Z]:[\\/]/i,
    /(?:password|secret|token|api[_-]?key)\s*[:=]/i,
    /\b(?:PID|HWND)\s*[:=]/i,
    /\b(?:account|balance|position|order)\s*(?:id|number|name|value)?\s*[:=]/i,
    /https?:\/\//i
  ];

  function parseCatalog() {
    var element = document.getElementById("fz-manual-test-catalog");
    if (!element) {
      return [];
    }
    try {
      var value = JSON.parse(element.textContent || "[]");
      return Array.isArray(value) ? value : [];
    } catch (_error) {
      return [];
    }
  }

  function emptyState(catalog) {
    var state = {};
    catalog.forEach(function (test) {
      state[test.id] = { status: "open", note: "" };
    });
    return state;
  }

  function storageKey(suiteId) {
    return "fzdocs.manual-test-state.v3." + suiteId;
  }

  function loadState(catalog, suiteId) {
    var state = emptyState(catalog);
    try {
      var raw = window.localStorage.getItem(storageKey(suiteId));
      if (!raw && suiteId === "FZMT") {
        raw = window.localStorage.getItem(legacyStorageKey);
      }
      if (!raw && (suiteId === "FZMT" || suiteId === "FZV2-RM")) {
        raw = window.localStorage.getItem("fzdocs.manual-test-state.v2." + suiteId);
      }
      var parsed = JSON.parse(raw || "{}");
      Object.keys(state).forEach(function (id) {
        if (parsed[id] && allowedStatuses.indexOf(parsed[id].status) >= 0) {
          state[id].status = parsed[id].status;
          state[id].note = sanitizeNote(parsed[id].note || "", true);
        }
      });
    } catch (_error) {
      return state;
    }
    return state;
  }

  function saveState(state, suiteId) {
    try {
      window.localStorage.setItem(storageKey(suiteId), JSON.stringify(state));
    } catch (_error) {
      /* Local persistence is optional; no network fallback is used. */
    }
  }

  function sanitizeNote(value, quiet) {
    var note = String(value).replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, noteLimit);
    for (var i = 0; i < forbiddenNotePatterns.length; i += 1) {
      if (forbiddenNotePatterns[i].test(note)) {
        if (quiet) {
          return "";
        }
        throw new Error("Die Notiz enthält ein nicht erlaubtes sensibles oder lokales Datenmuster.");
      }
    }
    return note;
  }

  function buildResult(catalog, state, includeNotes, suiteId) {
    return {
      schema_version: "fz-manual-test-result-v3",
      indicator_id: "fractal-zones",
      indicator_version_state: "current_source_validated_runtime_inventory_pending",
      suite_id: suiteId,
      exported_at_utc: new Date().toISOString(),
      notes_included: includeNotes,
      results: catalog.map(function (test) {
        var result = { test_id: test.id, status: state[test.id].status };
        if (includeNotes) {
          var note = sanitizeNote(state[test.id].note, false);
          if (note) {
            result.note = note;
          }
        }
        return result;
      })
    };
  }

  function validateImport(value, catalog, suiteId) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new Error("Die Importdatei ist kein Objekt.");
    }
    var keys = Object.keys(value).sort();
    var expectedKeys = ["exported_at_utc", "indicator_id", "indicator_version_state", "notes_included", "results", "schema_version", "suite_id"].sort();
    if (JSON.stringify(keys) !== JSON.stringify(expectedKeys)) {
      throw new Error("Die Importdatei enthält fehlende oder unbekannte Felder.");
    }
    if (value.schema_version !== "fz-manual-test-result-v3" || value.indicator_id !== "fractal-zones" || value.indicator_version_state !== "current_source_validated_runtime_inventory_pending" || value.suite_id !== suiteId) {
      throw new Error("Schema oder Indikatoridentität passt nicht.");
    }
    if (typeof value.notes_included !== "boolean" || !Array.isArray(value.results) || value.results.length > 100) {
      throw new Error("Importstruktur ist ungültig.");
    }
    var known = {};
    catalog.forEach(function (test) { known[test.id] = true; });
    var seen = {};
    value.results.forEach(function (result) {
      if (!result || typeof result !== "object" || Array.isArray(result)) {
        throw new Error("Ein Testergebnis ist ungültig.");
      }
      var resultKeys = Object.keys(result).sort();
      var allowedKeys = result.note === undefined ? ["status", "test_id"] : ["note", "status", "test_id"];
      if (JSON.stringify(resultKeys) !== JSON.stringify(allowedKeys.sort())) {
        throw new Error("Ein Testergebnis enthält unbekannte Felder.");
      }
      if (!known[result.test_id] || seen[result.test_id] || allowedStatuses.indexOf(result.status) < 0) {
        throw new Error("Test-ID oder Status ist unbekannt oder doppelt.");
      }
      seen[result.test_id] = true;
      if (result.note !== undefined) {
        sanitizeNote(result.note, false);
      }
    });
    return value;
  }

  function download(name, type, content) {
    var blob = new Blob([content], { type: type });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = name;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  function markdownResult(result) {
    var lines = ["# Fractal Zones – manueller Teststand", "", "- Schema: `" + result.schema_version + "`", "- Suite: `" + result.suite_id + "`", "- Indikatorversion: `" + result.indicator_version_state + "`", "- Exportzeit (UTC): `" + result.exported_at_utc + "`", "- Notizen enthalten: `" + String(result.notes_included) + "`", "", "| Test | Status | Notiz |", "|---|---|---|"];
    result.results.forEach(function (item) {
      var note = (item.note || "").replace(/\|/g, "\\|").replace(/\r?\n/g, " ");
      lines.push("| " + item.test_id + " | " + item.status + " | " + note + " |");
    });
    return lines.join("\n") + "\n";
  }

  function init() {
    var root = document.getElementById("fz-manual-test-app");
    var catalog = parseCatalog();
    if (!root || !catalog.length) {
      return;
    }
    var suiteId = root.dataset.suiteId;
    if (suiteId !== "FZMT" && suiteId !== "FZV2-RM" && suiteId !== "FZCURRENT") {
      return;
    }
    var state = loadState(catalog, suiteId);
    var message = document.getElementById("fz-test-message");
    var progress = document.getElementById("fz-test-progress");
    var progressText = document.getElementById("fz-test-progress-text");
    var includeNotes = document.getElementById("fz-export-notes");

    function announce(text) {
      message.textContent = text;
    }

    function updateProgress() {
      var completed = catalog.filter(function (test) { return state[test.id].status !== "open"; }).length;
      progress.max = catalog.length;
      progress.value = completed;
      progressText.textContent = completed + " von " + catalog.length + " Tests bewertet";
    }

    catalog.forEach(function (test) {
      var card = document.createElement("section");
      card.className = "fz-test-card";
      card.dataset.status = state[test.id].status;
      card.dataset.testId = test.id;

      var heading = document.createElement("div");
      heading.className = "fz-test-card__heading";
      var title = document.createElement("h3");
      title.textContent = test.id + " · " + test.title;
      var select = document.createElement("select");
      select.className = "fz-status-select";
      select.setAttribute("aria-label", "Status für " + test.id);
      [["Offen", "open"], ["Bestanden", "pass"], ["Fehlgeschlagen", "fail"], ["Blockiert", "blocked"], ["Verbesserung", "improvement"]].forEach(function (entry) {
        var option = document.createElement("option");
        option.value = entry[1];
        option.textContent = entry[0];
        option.selected = state[test.id].status === entry[1];
        select.appendChild(option);
      });
      select.addEventListener("change", function () {
        state[test.id].status = select.value;
        card.dataset.status = select.value;
        saveState(state, suiteId);
        updateProgress();
        announce(test.id + " wurde als " + select.options[select.selectedIndex].text + " gespeichert.");
      });
      heading.append(title, select);

      var stepsHeading = document.createElement("h4");
      stepsHeading.textContent = "Schritte";
      var steps = document.createElement("ol");
      test.steps.forEach(function (item) {
        var li = document.createElement("li");
        li.textContent = item;
        steps.appendChild(li);
      });
      var expectedHeading = document.createElement("h4");
      expectedHeading.textContent = "Erwartet";
      var expected = document.createElement("ul");
      test.expected.forEach(function (item) {
        var li = document.createElement("li");
        li.textContent = item;
        expected.appendChild(li);
      });
      var restoration = document.createElement("p");
      restoration.innerHTML = "<strong>Wiederherstellung:</strong> ";
      restoration.appendChild(document.createTextNode(test.restoration));
      var noteLabel = document.createElement("label");
      noteLabel.setAttribute("for", "note-" + test.id);
      noteLabel.textContent = "Lokale Notiz (optional, keine sensiblen Daten)";
      var note = document.createElement("textarea");
      note.className = "fz-note";
      note.id = "note-" + test.id;
      note.maxLength = noteLimit;
      note.value = state[test.id].note;
      note.addEventListener("change", function () {
        try {
          state[test.id].note = sanitizeNote(note.value, false);
          note.value = state[test.id].note;
          saveState(state, suiteId);
          announce("Notiz für " + test.id + " wurde nur lokal gespeichert.");
        } catch (error) {
          note.value = state[test.id].note;
          announce(error.message);
        }
      });
      card.append(heading, stepsHeading, steps, expectedHeading, expected, restoration, noteLabel, note);
      root.appendChild(card);
    });

    document.getElementById("fz-export-json").addEventListener("click", function () {
      try {
        var result = buildResult(catalog, state, includeNotes.checked, suiteId);
        download("fractal-zones-" + suiteId.toLowerCase() + "-tests.json", "application/json", JSON.stringify(result, null, 2) + "\n");
        announce("JSON wurde lokal erzeugt. Es wurden keine Daten übertragen.");
      } catch (error) {
        announce(error.message);
      }
    });
    document.getElementById("fz-export-markdown").addEventListener("click", function () {
      try {
        var result = buildResult(catalog, state, includeNotes.checked, suiteId);
        download("fractal-zones-" + suiteId.toLowerCase() + "-tests.md", "text/markdown", markdownResult(result));
        announce("Markdown wurde lokal erzeugt. Es wurden keine Daten übertragen.");
      } catch (error) {
        announce(error.message);
      }
    });
    document.getElementById("fz-import-json").addEventListener("change", function (event) {
      var file = event.target.files && event.target.files[0];
      if (!file) {
        return;
      }
      if (file.size > maximumImportBytes) {
        announce("Import abgelehnt: Datei ist größer als 256 KiB.");
        event.target.value = "";
        return;
      }
      var reader = new FileReader();
      reader.addEventListener("load", function () {
        try {
          var imported = validateImport(JSON.parse(String(reader.result)), catalog, suiteId);
          imported.results.forEach(function (result) {
            state[result.test_id] = { status: result.status, note: result.note || "" };
          });
          saveState(state, suiteId);
          announce("Import validiert und nur lokal gespeichert. Seite wird aktualisiert.");
          window.setTimeout(function () { window.location.reload(); }, 250);
        } catch (error) {
          announce("Import abgelehnt: " + error.message);
        }
      });
      reader.readAsText(file, "utf-8");
      event.target.value = "";
    });
    document.getElementById("fz-reset-tests").addEventListener("click", function () {
      if (window.confirm("Nur den lokalen Testfortschritt dieses Browsers zurücksetzen?")) {
        window.localStorage.removeItem(storageKey(suiteId));
        window.location.reload();
      }
    });
    updateProgress();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
}());
