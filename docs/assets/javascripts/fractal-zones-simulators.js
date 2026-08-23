(function () {
  "use strict";

  var SVG_NS = "http://www.w3.org/2000/svg";
  var simulatorInitializers = {
    "break-boundary": initBreakBoundary,
    "role-ended": initRoleEnded,
    "timeframe-parity": initTimeframeParity,
    "lifecycle": initLifecycle,
    "rendering-modes": initRenderingModes,
    "break-source": initBreakSource,
    "history-range": initHistoryRange
  };

  function html(tag, className, text) {
    var node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (text !== undefined) {
      node.textContent = text;
    }
    return node;
  }

  function svgNode(tag, attributes, text) {
    var node = document.createElementNS(SVG_NS, tag);
    Object.keys(attributes || {}).forEach(function (name) {
      node.setAttribute(name, String(attributes[name]));
    });
    if (text !== undefined) {
      node.textContent = text;
    }
    return node;
  }

  function chart(label, viewBox) {
    var node = svgNode("svg", {
      class: "fz-simulator__chart",
      viewBox: viewBox || "0 0 800 350",
      role: "img",
      "aria-label": label,
      preserveAspectRatio: "xMidYMid meet"
    });
    node.appendChild(svgNode("title", {}, label));
    return node;
  }

  function addLine(parent, x1, y1, x2, y2, className, attributes) {
    var values = Object.assign({ x1: x1, y1: y1, x2: x2, y2: y2, class: className || "" }, attributes || {});
    parent.appendChild(svgNode("line", values));
  }

  function addText(parent, x, y, value, className, attributes) {
    var values = Object.assign({ x: x, y: y, class: className || "" }, attributes || {});
    parent.appendChild(svgNode("text", values, value));
  }

  function addGrid(parent, width, height, left, top, right, bottom) {
    var index;
    for (index = 0; index <= 4; index += 1) {
      var y = top + ((bottom - top) * index / 4);
      addLine(parent, left, y, right, y, "fz-chart-grid");
    }
    for (index = 0; index <= 6; index += 1) {
      var x = left + ((right - left) * index / 6);
      addLine(parent, x, top, x, bottom, "fz-chart-grid");
    }
    addText(parent, left, height - 10, "Zeit", "fz-chart-muted");
    addText(parent, 10, top + 10, "Preis", "fz-chart-muted");
  }

  function yScale(value, minimum, maximum, top, bottom) {
    return bottom - ((value - minimum) / (maximum - minimum)) * (bottom - top);
  }

  function drawCandles(parent, values, options) {
    var left = options.left;
    var right = options.right;
    var top = options.top;
    var bottom = options.bottom;
    var minimum = options.minimum;
    var maximum = options.maximum;
    var width = (right - left) / values.length;
    values.forEach(function (close, index) {
      var open = index === 0 ? close - (values[1] - close) * 0.35 : values[index - 1];
      var high = Math.max(open, close) + (maximum - minimum) * 0.025;
      var low = Math.min(open, close) - (maximum - minimum) * 0.025;
      var x = left + width * index + width / 2;
      var candleClass = close >= open ? "fz-chart-up" : "fz-chart-down";
      addLine(parent, x, yScale(high, minimum, maximum, top, bottom), x, yScale(low, minimum, maximum, top, bottom), candleClass, { "stroke-width": 1.5 });
      parent.appendChild(svgNode("rect", {
        x: x - Math.max(2.5, width * 0.22),
        y: Math.min(yScale(open, minimum, maximum, top, bottom), yScale(close, minimum, maximum, top, bottom)),
        width: Math.max(5, width * 0.44),
        height: Math.max(2, Math.abs(yScale(open, minimum, maximum, top, bottom) - yScale(close, minimum, maximum, top, bottom))),
        class: candleClass
      }));
    });
  }

  function field(labelText, control) {
    var label = html("label", "fz-simulator__field");
    var caption = html("span", "", labelText);
    if (!control.id) {
      control.id = "fz-simulator-control-" + Math.random().toString(36).slice(2);
    }
    label.htmlFor = control.id;
    label.append(caption, control);
    return label;
  }

  function selectControl(options, value) {
    var select = document.createElement("select");
    options.forEach(function (entry) {
      var option = document.createElement("option");
      option.value = entry[0];
      option.textContent = entry[1];
      select.appendChild(option);
    });
    select.value = value;
    return select;
  }

  function rangeControl(minimum, maximum, step, value) {
    var input = document.createElement("input");
    input.type = "range";
    input.min = String(minimum);
    input.max = String(maximum);
    input.step = String(step);
    input.value = String(value);
    return input;
  }

  function statusRow(items) {
    var row = html("div", "fz-simulator__status");
    items.forEach(function (item) {
      var cell = html("div");
      cell.append(html("strong", "", item[0]), document.createTextNode(item[1]));
      row.appendChild(cell);
    });
    return row;
  }

  function lineDash(style) {
    return {
      solid: "",
      dash: "12 7",
      dot: "2 6",
      dashdot: "12 5 2 5"
    }[style] || "";
  }

  function formatPrice(value, decimals) {
    return value.toLocaleString("de-DE", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  }

  function initBreakBoundary(root) {
    var controls = html("div", "fz-simulator__controls");
    var mode = selectControl([
      ["fixed", "Fixed ticks"],
      ["percent", "Percent of level"],
      ["atr", "One-minute ATR"]
    ], "fixed");
    var side = selectControl([["resistance", "Resistance"], ["support", "Support"]], "resistance");
    var outcome = selectControl([
      ["fail", "Fehlversuch und Reset"],
      ["confirm", "Bestätigter Bruch"],
      ["fail-confirm", "Reset, danach bestätigter Bruch"]
    ], "fail-confirm");
    var style = selectControl([
      ["dash", "Gestrichelt"],
      ["solid", "Durchgezogen"],
      ["dot", "Gepunktet"],
      ["dashdot", "Strich-Punkt"]
    ], "dash");
    var color = document.createElement("input");
    color.type = "color";
    color.value = "#ffca28";
    var width = rangeControl(1, 4, 1, 2);
    controls.append(
      field("Bruchdistanz-Modus", mode),
      field("Zonenseite", side),
      field("Kursverlauf", outcome),
      field("Linientyp", style),
      field("Linienfarbe", color),
      field("Linienbreite: 2 px", width)
    );
    var output = html("div");
    root.replaceChildren(controls, output);

    function render() {
      width.parentElement.querySelector("span").textContent = "Linienbreite: " + width.value + " px";
      var definitions = {
        fixed: { instrument: "ES", level: 5250, distance: 0.5, decimals: 2, formula: "2 Ticks × 0,25 = 0,50 Punkte" },
        percent: { instrument: "DAX", level: 18000, distance: 9, decimals: 0, formula: "18.000 × 0,05 % = 9 Punkte" },
        atr: { instrument: "NQ", level: 18400, distance: 8, decimals: 2, formula: "MIN1-ATR 16 × 0,5 = 8 Punkte" }
      };
      var definition = definitions[mode.value];
      var direction = side.value === "resistance" ? 1 : -1;
      var boundary = definition.level + direction * definition.distance;
      var pathByOutcome = {
        fail: [-1.1, -0.7, -0.25, 0.35, 1.1, 0.55, -0.15, -0.45, -0.2, 0.05, -0.15, -0.3],
        confirm: [-1.1, -0.7, -0.25, 0.2, 0.75, 1.15, 1.35, 1.55, 1.7, 1.85, 1.95, 2.05],
        "fail-confirm": [-1.1, -0.7, -0.25, 0.35, 1.1, 0.45, -0.2, 0.25, 0.95, 1.3, 1.55, 1.8]
      };
      var normalized = pathByOutcome[outcome.value];
      var values = normalized.map(function (item) { return definition.level + direction * definition.distance * item; });
      var spread = definition.distance * 3.1;
      var minimum = definition.level - spread;
      var maximum = definition.level + spread;
      var node = chart("Bruchgrenze für " + definition.instrument + " als " + side.options[side.selectedIndex].text);
      addGrid(node, 800, 350, 65, 25, 770, 300);
      drawCandles(node, values, { left: 70, right: 765, top: 30, bottom: 295, minimum: minimum, maximum: maximum });
      var levelY = yScale(definition.level, minimum, maximum, 30, 295);
      var boundaryY = yScale(boundary, minimum, maximum, 30, 295);
      addLine(node, 65, levelY, 770, levelY, "fz-chart-level");
      addLine(node, 65, boundaryY, 770, boundaryY, "fz-chart-boundary", {
        stroke: color.value,
        "stroke-width": width.value,
        "stroke-dasharray": lineDash(style.value)
      });
      addText(node, 755, levelY - 7, "Level " + formatPrice(definition.level, definition.decimals), "", { "text-anchor": "end" });
      addText(node, 75, boundaryY - 7, "Bruchgrenze " + formatPrice(boundary, definition.decimals), "");
      if (outcome.value !== "confirm") {
        var resetX = 70 + (695 / values.length) * 5.5;
        var resetY = yScale(values[5], minimum, maximum, 30, 295);
        node.appendChild(svgNode("circle", { cx: resetX, cy: resetY, r: 7, class: "fz-chart-marker-reset" }));
        addText(node, resetX, resetY + 23, "Reset", "", { "text-anchor": "middle" });
      }
      if (outcome.value !== "fail") {
        var confirmIndex = outcome.value === "confirm" ? 8 : 10;
        var confirmX = 70 + (695 / values.length) * (confirmIndex + 0.5);
        var confirmY = yScale(values[confirmIndex], minimum, maximum, 30, 295);
        node.appendChild(svgNode("circle", { cx: confirmX, cy: confirmY, r: 7, class: "fz-chart-marker-confirm" }));
        addText(node, confirmX, confirmY - 14, "Commit", "", { "text-anchor": "middle" });
      }
      var result = outcome.value === "fail" ? "Attempt verworfen" : outcome.value === "confirm" ? "Bruch bestätigt" : "Erster Attempt verworfen, zweiter bestätigt";
      output.replaceChildren(
        node,
        statusRow([
          ["Berechnung", definition.formula],
          ["Grenze", formatPrice(boundary, definition.decimals)],
          ["Ergebnis", result]
        ])
      );
    }

    [mode, side, outcome, style, color, width].forEach(function (control) {
      control.addEventListener("input", render);
      control.addEventListener("change", render);
    });
    render();
  }

  var roleScenarios = {
    supportToResistance: {
      label: "Support → Resistance",
      origin: "Bottom-Origin bleibt rot",
      result: "RoleChange: ehemalige Unterstützung wird Widerstand",
      prices: [1.4, 1.1, 0.6, -0.2, -0.7, -1.0, -0.4, 0.1, -0.25, -0.65, -0.85, -1.0],
      events: ["Active Support", "Break committed", "Retest-Kontakt", "Resistance bestätigt"]
    },
    resistanceToSupport: {
      label: "Resistance → Support",
      origin: "Top-Origin bleibt grün",
      result: "RoleChange: ehemaliger Widerstand wird Unterstützung",
      prices: [-1.3, -1.0, -0.6, 0.15, 0.7, 1.0, 0.45, -0.05, 0.3, 0.65, 0.85, 1.0],
      events: ["Active Resistance", "Break committed", "Retest-Kontakt", "Support bestätigt"]
    },
    reaffirmResistance: {
      label: "Resistance bestätigt",
      origin: "Top-Origin bleibt grün",
      result: "RoleReaffirmation: Rolle bleibt Resistance",
      prices: [-1.0, -0.65, -0.2, 0.25, 0.7, 0.15, -0.35, 0.05, -0.25, -0.55, -0.7, -0.8],
      events: ["Active Resistance", "Break/Watch", "Retest derselben Seite", "Resistance reaffirmed"]
    },
    reaffirmSupport: {
      label: "Support bestätigt",
      origin: "Bottom-Origin bleibt rot",
      result: "RoleReaffirmation: Rolle bleibt Support",
      prices: [1.0, 0.65, 0.2, -0.25, -0.7, -0.15, 0.35, -0.05, 0.25, 0.55, 0.7, 0.8],
      events: ["Active Support", "Break/Watch", "Retest derselben Seite", "Support reaffirmed"]
    },
    rearm: {
      label: "Reset und Re-arm",
      origin: "Ursprung unverändert",
      result: "Neutralzone setzt den Timer zurück; neuer Kontakt startet später neu",
      prices: [-0.8, -0.35, 0.05, 0.35, 0.08, -0.12, -0.45, -0.05, 0.25, 0.55, 0.75, 0.85],
      events: ["Kontakt", "RetestPending", "Reset in Neutralzone", "Neu bestätigt"]
    },
    counterBreak: {
      label: "Gegenbruch-Priorität",
      origin: "Ursprung unverändert",
      result: "Der atomar bestätigte Gegenbruch gewinnt vor dem Retest-Ergebnis",
      prices: [-0.7, -0.25, 0.25, 0.7, 0.35, -0.1, -0.55, -0.9, -1.15, -1.3, -1.45, -1.55],
      events: ["BrokenWatch", "RetestPending", "Gegenbruch erkannt", "Gegenbruch committed"]
    },
    ended: {
      label: "Terminales Ended",
      origin: "Ursprung bleibt Historie",
      result: "Terminaler current-role break beendet die Linie am Commit",
      prices: [-0.8, -0.4, 0.1, 0.55, 0.9, 1.15, 1.3, 1.45, 1.6, 1.7, 1.8, 1.9],
      events: ["Zähler vor Grenze", "BreakPending", "Terminaler Commit", "Ended: kein Segment danach"]
    },
    noEvent: {
      label: "Synthetic NoEvent",
      origin: "Keine neue Preis-Evidenz",
      result: "Zeit darf fortschreiten, aber kein Kontakt oder Commit wird erfunden",
      prices: [-0.65, -0.5, -0.4, -0.35, -0.3, -0.28, -0.25, -0.23, -0.2, -0.18, -0.16, -0.14],
      events: ["Letzte reale Bar", "NoEvent-Slot", "NoEvent-Slot", "Zustand unverändert"]
    }
  };

  function initRoleEnded(root) {
    var controls = html("div", "fz-simulator__controls");
    var scenario = selectControl(Object.keys(roleScenarios).map(function (key) {
      return [key, roleScenarios[key].label];
    }), "supportToResistance");
    controls.appendChild(field("Szenario", scenario));
    var steps = html("div", "fz-simulator__steps");
    var previous = html("button", "fz-simulator__step-button", "Zurück");
    previous.type = "button";
    var stepLabel = html("div", "fz-simulator__step-label");
    var next = html("button", "fz-simulator__step-button", "Weiter");
    next.type = "button";
    steps.append(previous, stepLabel, next);
    var output = html("div");
    root.replaceChildren(controls, steps, output);
    var step = 0;

    function render() {
      var definition = roleScenarios[scenario.value];
      stepLabel.textContent = "Schritt " + (step + 1) + " von 4 · " + definition.events[step];
      previous.disabled = step === 0;
      next.disabled = step === 3;
      var node = chart(definition.label + ", Schritt " + (step + 1));
      addGrid(node, 800, 350, 65, 25, 770, 300);
      var visibleCount = scenario.value === "noEvent" ? 3 : 3 + step * 3;
      var values = definition.prices.slice(0, visibleCount);
      drawCandles(node, values, { left: 70, right: 765, top: 30, bottom: 295, minimum: -2.2, maximum: 2.2 });
      var levelY = yScale(0, -2.2, 2.2, 30, 295);
      var segmentEnd = scenario.value === "ended" && step >= 2 ? 70 + 695 * 0.68 : 770;
      var beforeBreak = 70 + 695 * 0.34;
      var retest = 70 + 695 * 0.66;
      if (scenario.value === "noEvent") {
        addLine(node, 65, levelY, 770, levelY, "fz-chart-level", { stroke: "#35c57a", "stroke-width": 3 });
      } else {
        addLine(node, 65, levelY, Math.min(beforeBreak, segmentEnd), levelY, "fz-chart-level", { stroke: scenario.value.indexOf("support") === 0 || scenario.value === "reaffirmSupport" ? "#ef5350" : "#35c57a", "stroke-width": 3 });
        if (step >= 1 && segmentEnd > beforeBreak) {
          addLine(node, beforeBreak, levelY, Math.min(retest, segmentEnd), levelY, "", { stroke: "#9aa0a6", "stroke-width": 3, "stroke-dasharray": "12 7" });
        }
        if (step >= 3 && segmentEnd > retest) {
          addLine(node, retest, levelY, segmentEnd, levelY, "", { stroke: scenario.value === "supportToResistance" || scenario.value === "reaffirmResistance" ? "#ef5350" : "#35c57a", "stroke-width": 3 });
        }
      }
      var eventX = 70 + 695 * (0.17 + step * 0.22);
      var markerClass = scenario.value === "noEvent" || (step === 2 && scenario.value === "counterBreak") ? "fz-chart-marker-pending" : step === 2 && scenario.value === "rearm" ? "fz-chart-marker-reset" : "fz-chart-marker-confirm";
      node.appendChild(svgNode("circle", { cx: eventX, cy: levelY, r: 7, class: markerClass }));
      addText(node, eventX, levelY - 15, definition.events[step], "", { "text-anchor": "middle" });
      output.replaceChildren(node, statusRow([
        ["Aktuelles Ereignis", definition.events[step]],
        ["Ergebnis", step === 3 ? definition.result : "Noch nicht vollständig bestätigt"],
        ["Farblogik", definition.origin]
      ]));
    }

    previous.addEventListener("click", function () { step = Math.max(0, step - 1); render(); });
    next.addEventListener("click", function () { step = Math.min(3, step + 1); render(); });
    scenario.addEventListener("change", function () { step = 0; render(); });
    render();
  }

  function initTimeframeParity(root) {
    var controls = html("div", "fz-simulator__controls");
    var after = rangeControl(15, 45, 15, 30);
    var pauseWrap = html("label", "fz-simulator__check");
    var pause = document.createElement("input");
    pause.type = "checkbox";
    pause.checked = true;
    pauseWrap.append(pause, document.createTextNode(" Sessionpause von 10:40–10:49"));
    controls.append(field("After: 30 offene Minuten", after), pauseWrap);
    var multiples = html("div", "fz-simulator__small-multiples");
    var status = html("div");
    root.replaceChildren(controls, multiples, status);

    function confirmationMinute(required) {
      var valid = 0;
      var minute = 30;
      while (valid < required) {
        minute += 1;
        if (!(pause.checked && minute >= 40 && minute <= 49)) {
          valid += 1;
        }
      }
      return minute;
    }

    function formatMinute(minute) {
      var total = 10 * 60 + minute;
      var hours = Math.floor(total / 60);
      var minutes = total % 60;
      return String(hours).padStart(2, "0") + ":" + String(minutes).padStart(2, "0");
    }

    function renderMini(timeframe, confirmAt) {
      var wrapper = html("div", "fz-simulator__mini-chart");
      wrapper.appendChild(html("h3", "", timeframe + "-Minuten-Chart"));
      var node = chart(timeframe + "-Minuten-Aggregation derselben MIN1-Reihe", "0 0 300 210");
      var left = 32;
      var right = 288;
      var top = 20;
      var bottom = 178;
      for (var gridIndex = 0; gridIndex <= 3; gridIndex += 1) {
        addLine(node, left, top + gridIndex * 52, right, top + gridIndex * 52, "fz-chart-grid");
      }
      var count = Math.ceil(90 / timeframe);
      var points = [];
      for (var index = 0; index < count; index += 1) {
        var minute = index * timeframe;
        var value = 0.45 + Math.sin(minute / 9) * 0.35 + (minute === 30 ? 0.7 : 0);
        var x = left + (right - left) * minute / 90;
        var y = yScale(value, -0.1, 1.6, top, bottom);
        points.push(x.toFixed(1) + "," + y.toFixed(1));
      }
      node.appendChild(svgNode("polyline", { points: points.join(" "), class: "fz-chart-price" }));
      var candidateX = left + (right - left) * 30 / 90;
      var confirmX = left + (right - left) * confirmAt / 90;
      addLine(node, candidateX, top, candidateX, bottom, "", { stroke: "#ffca28", "stroke-width": 2, "stroke-dasharray": "4 4" });
      addLine(node, confirmX, top, confirmX, bottom, "", { stroke: "#35c57a", "stroke-width": 2 });
      addText(node, candidateX, 198, "Kandidat", "", { "text-anchor": "middle" });
      addText(node, confirmX, 12, "Commit", "", { "text-anchor": "middle" });
      wrapper.appendChild(node);
      return wrapper;
    }

    function render() {
      var required = Number(after.value);
      after.parentElement.querySelector("span").textContent = "After: " + required + " offene Minuten";
      var confirmAt = confirmationMinute(required);
      multiples.replaceChildren(renderMini(1, confirmAt), renderMini(5, confirmAt), renderMini(15, confirmAt));
      status.replaceChildren(statusRow([
        ["Kandidat", "10:30 in allen Ansichten"],
        ["Bestätigung", formatMinute(confirmAt) + " in allen Ansichten"],
        ["Kerzenzahl", "Nur die sichtbare Aggregation unterscheidet sich"]
      ]));
    }

    after.addEventListener("input", render);
    pause.addEventListener("change", render);
    render();
  }

  function initLifecycle(root) {
    var definitions = [
      ["Candidate", "Striktes Extrem erkannt; noch keine veröffentlichte Linie"],
      ["Provisional", "Dot zeigt den sichtbaren, noch verwerfbaren Kandidaten"],
      ["Active", "Ab dem Maturity-Commit beginnt ein neues Solid-Segment"],
      ["BreakPending", "Interner Timer läuft; die Grenze ist eingefroren"],
      ["BrokenWatch", "Ab dem Break-Commit läuft die Linie Dash weiter"],
      ["RetestPending", "Realer Bar-Kontakt prüft die neue oder gleiche Rolle"],
      ["Active nach Retest", "Ab dem Retest-Commit beginnt wieder Solid"],
      ["Ended", "Die Linie endet exakt am terminalen Commit"]
    ];
    var steps = html("div", "fz-simulator__steps");
    var previous = html("button", "fz-simulator__step-button", "Zurück");
    previous.type = "button";
    var stepLabel = html("div", "fz-simulator__step-label");
    var next = html("button", "fz-simulator__step-button", "Weiter");
    next.type = "button";
    steps.append(previous, stepLabel, next);
    var output = html("div");
    root.replaceChildren(steps, output);
    var step = 0;

    function render() {
      var current = definitions[step];
      stepLabel.textContent = "Schritt " + (step + 1) + " von " + definitions.length + " · " + current[0];
      previous.disabled = step === 0;
      next.disabled = step === definitions.length - 1;
      var values = [-0.7, -0.35, 0.05, 0.28, 0.15, 0.48, 0.85, 1.1, 0.45, 0.05, -0.25, 0.2, 0.55, 0.7, 0.4, 0.1];
      var node = chart("Zustandsreise bis " + current[0]);
      addGrid(node, 800, 350, 65, 25, 770, 300);
      drawCandles(node, values.slice(0, Math.min(values.length, 3 + step * 2)), { left: 70, right: 765, top: 30, bottom: 295, minimum: -1.4, maximum: 1.6 });
      var levelY = yScale(0, -1.4, 1.6, 30, 295);
      var maturityX = 265;
      var breakX = 440;
      var retestX = 610;
      var endX = 720;
      if (step >= 1) {
        addLine(node, 120, levelY, Math.min(step >= 2 ? maturityX : 210, 770), levelY, "", { stroke: "#ffca28", "stroke-width": 3, "stroke-dasharray": "2 6" });
      }
      if (step >= 2) {
        addLine(node, maturityX, levelY, Math.min(step >= 4 ? breakX : endX, endX), levelY, "", { stroke: "#ffca28", "stroke-width": 3 });
      }
      if (step >= 4) {
        addLine(node, breakX, levelY, Math.min(step >= 6 ? retestX : endX, endX), levelY, "", { stroke: "#ffca28", "stroke-width": 3, "stroke-dasharray": "12 7" });
      }
      if (step >= 6) {
        addLine(node, retestX, levelY, step === 7 ? endX : 770, levelY, "", { stroke: "#ffca28", "stroke-width": 3 });
      }
      var markerXs = [120, 185, maturityX, 355, breakX, 535, retestX, endX];
      node.appendChild(svgNode("circle", { cx: markerXs[step], cy: levelY, r: 7, class: step === 0 || step === 1 || step === 3 || step === 5 ? "fz-chart-marker-pending" : "fz-chart-marker-confirm" }));
      addText(node, markerXs[step], levelY - 16, current[0], "", { "text-anchor": "middle" });
      output.replaceChildren(node, statusRow([
        ["Zustand", current[0]],
        ["Bedeutung", current[1]],
        ["Segmenttreue", "Frühere Dot-, Solid- und Dash-Abschnitte bleiben unverändert"]
      ]));
    }

    previous.addEventListener("click", function () { step = Math.max(0, step - 1); render(); });
    next.addEventListener("click", function () { step = Math.min(definitions.length - 1, step + 1); render(); });
    render();
  }

  function initRenderingModes(root) {
    var controls = html("div", "fz-simulator__controls");
    var mode = selectControl([
      ["adaptive", "Adaptive"],
      ["full", "Full"],
      ["focus", "Active focus"]
    ], "adaptive");
    var opacity = rangeControl(0.1, 1, 0.05, 0.35);
    var viewport = rangeControl(0, 60, 5, 20);
    controls.append(field("Rendering-Modus", mode), field("Inactive opacity: 0,35", opacity), field("Viewport-Position", viewport));
    var output = html("div");
    root.replaceChildren(controls, output);

    var segments = [
      [0, 18, 35, "active"], [8, 28, 62, "provisional"], [17, 37, 89, "broken"],
      [30, 51, 116, "active"], [40, 59, 143, "broken"], [48, 68, 170, "provisional"],
      [57, 76, 197, "active"], [65, 84, 224, "active"], [72, 91, 251, "broken"],
      [82, 100, 278, "provisional"], [0, 12, 305, "broken"], [88, 100, 332, "active"]
    ];

    function render() {
      opacity.parentElement.querySelector("span").textContent = "Inactive opacity: " + Number(opacity.value).toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      var start = Number(viewport.value);
      var end = start + 40;
      var visible = segments.filter(function (segment) { return segment[1] >= start && segment[0] <= end; });
      var candidates = mode.value === "full" ? segments.length : visible.length;
      var node = chart("Vergleich der Rendering-Modi", "0 0 800 370");
      addText(node, 65, 24, "Viewport " + start + "–" + end, "");
      addLine(node, 65, 35, 770, 35, "fz-chart-grid");
      visible.forEach(function (segment) {
        var x1 = 65 + 705 * (Math.max(segment[0], start) - start) / 40;
        var x2 = 65 + 705 * (Math.min(segment[1], end) - start) / 40;
        var state = segment[3];
        var alpha = mode.value === "focus" && state !== "active" ? Number(opacity.value) : 1;
        var dash = state === "provisional" ? "2 6" : state === "broken" ? "12 7" : "";
        addLine(node, x1, segment[2], x2, segment[2], "", {
          stroke: state === "active" ? "#35c57a" : "#ffca28",
          "stroke-width": 3,
          "stroke-dasharray": dash,
          opacity: alpha
        });
        addText(node, 70, segment[2] - 6, state === "active" ? "Active" : state === "provisional" ? "Provisional" : "BrokenWatch", "fz-chart-muted");
      });
      var plan = mode.value === "full" ? "Direkte Vollprojektion" : mode.value === "focus" ? "Optimierter Plan mit Fokus-Deckkraft" : "Viewport-Index und Cache-Wiederverwendung";
      output.replaceChildren(
        node,
        html("div", "fz-simulator__legend")
      );
      var legend = output.lastChild;
      legend.append(html("span", "", "Active/Solid"), html("span", "is-dot", "Provisional/Dot"), html("span", "is-dash", "BrokenWatch/Dash"));
      output.appendChild(statusRow([
        ["Semantische Segmente", segments.length + " in jedem Modus"],
        ["Im Viewport sichtbar", visible.length + " in jedem Modus"],
        ["Renderweg", plan + " · Beispielkandidaten " + candidates]
      ]));
    }

    [mode, opacity, viewport].forEach(function (control) {
      control.addEventListener("input", render);
      control.addEventListener("change", render);
    });
    render();
  }

  function initBreakSource(root) {
    var controls = html("div", "fz-simulator__controls");
    var source = selectControl([["close", "Close"], ["highlow", "High/Low"]], "close");
    var confirmation = rangeControl(0, 5, 1, 2);
    controls.append(field("Preisquelle", source), field("Bestätigung: 2 Minuten", confirmation));
    var output = html("div");
    root.replaceChildren(controls, output);
    function render() {
      confirmation.parentElement.querySelector("span").textContent = "Bestätigung: " + confirmation.value + " Minuten";
      var node = chart("Break-Preisquelle und Bestätigung");
      addGrid(node, 800, 350, 65, 25, 770, 300);
      var boundary = 135;
      addLine(node, 65, boundary, 770, boundary, "", { stroke: "#ffca28", "stroke-width": 3, "stroke-dasharray": "8 5" });
      addText(node, 70, boundary - 8, "Break-Grenze", "fz-chart-muted");
      var values = [-0.2, 0.1, 0.35, 0.2, 0.5, 0.65, 0.72, 0.78];
      drawCandles(node, values, { left: 80, right: 750, top: 35, bottom: 290, minimum: -0.5, maximum: 1 });
      var qualifies = source.value === "highlow" ? "Docht kann qualifizieren" : "Nur Schlusskurs qualifiziert";
      var timing = Number(confirmation.value) === 0 ? "erster qualifizierender Slot" : confirmation.value + " fortlaufende Slots";
      output.replaceChildren(node, statusRow([["Preisquelle", qualifies], ["Commit", timing], ["Neutralzone", "setzt den Timer strikt zurück"]]));
    }
    [source, confirmation].forEach(function (control) { control.addEventListener("input", render); control.addEventListener("change", render); });
    render();
  }

  function initHistoryRange(root) {
    var controls = html("div", "fz-simulator__controls");
    var mode = selectControl([["loaded", "Chart loaded range + warm-up"], ["rolling", "Rolling lookback days"], ["fixed", "Fixed calculation start"]], "loaded");
    var warmup = rangeControl(2, 30, 1, 10);
    controls.append(field("Berechnungsbereich", mode), field("Warm-up: 10 Tage", warmup));
    var output = html("div");
    root.replaceChildren(controls, output);
    function render() {
      warmup.parentElement.querySelector("span").textContent = "Warm-up: " + warmup.value + " Tage";
      var node = chart("Berechnungsbereich und Warm-up", "0 0 800 250");
      addLine(node, 70, 130, 750, 130, "fz-chart-grid");
      var start = mode.value === "fixed" ? 100 : mode.value === "rolling" ? 250 : 390;
      if (mode.value === "loaded") {
        addLine(node, 270, 130, 390, 130, "", { stroke: "#ffca28", "stroke-width": 12, opacity: 0.45 });
      }
      addLine(node, start, 130, 735, 130, "", { stroke: "#35c57a", "stroke-width": 12, opacity: 0.8 });
      addText(node, start, 105, "Berechnungsstart", "", { "text-anchor": "middle" });
      addText(node, 735, 105, "Jetzt", "", { "text-anchor": "middle" });
      var detail = mode.value === "fixed" ? "expliziter UTC-Anker" : mode.value === "rolling" ? "rollierendes Fenster (z. B. 90 Tage)" : "geladener Chartbereich plus Vorlauf";
      output.replaceChildren(node, statusRow([["Modus", detail], ["Semantik", "gemeinsamer Zeitraum bleibt source-identisch"], ["Darstellung", "kein Level-Clustering oder Löschen"]]));
    }
    [mode, warmup].forEach(function (control) { control.addEventListener("input", render); control.addEventListener("change", render); });
    render();
  }

  function init() {
    document.querySelectorAll("[data-fz-simulator]").forEach(function (root) {
      var initializer = simulatorInitializers[root.dataset.fzSimulator];
      if (initializer && root.dataset.fzInitialized !== "true") {
        root.dataset.fzInitialized = "true";
        initializer(root);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
}());
