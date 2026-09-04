(function () {
  "use strict";

  var marker = "/indicators/fractal-zones/";
  if (window.location.pathname.indexOf(marker) === -1) {
    return;
  }

  var storageKey = "fzdocs.preferences.v1";
  var allowedDepths = ["short", "practice", "technical"];
  var allowedModes = ["understand", "configure", "test", "troubleshoot"];
  var modeLabels = {
    understand: "Verstehen",
    configure: "Einstellen",
    test: "Testen",
    troubleshoot: "Fehlerbilder"
  };
  var modeTargets = {
    understand: "understand/time-and-fractals",
    configure: "configure/",
    test: "test/",
    troubleshoot: "troubleshoot/"
  };

  function loadPreferences() {
    try {
      var parsed = JSON.parse(window.localStorage.getItem(storageKey) || "{}");
      return {
        depth: allowedDepths.indexOf(parsed.depth) >= 0 ? parsed.depth : "practice",
        mode: allowedModes.indexOf(parsed.mode) >= 0 ? parsed.mode : inferMode()
      };
    } catch (_error) {
      return { depth: "practice", mode: inferMode() };
    }
  }

  function inferMode() {
    var path = window.location.pathname;
    for (var i = 0; i < allowedModes.length; i += 1) {
      if (path.indexOf("/" + allowedModes[i] + "/") >= 0) {
        return allowedModes[i];
      }
    }
    return "understand";
  }

  function persist(preferences) {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(preferences));
    } catch (_error) {
      /* The documentation remains usable when storage is unavailable. */
    }
  }

  function targetFor(mode) {
    var path = window.location.pathname;
    var prefix = path.slice(0, path.indexOf(marker));
    var offline = window.location.protocol === "file:" || /\.html$/.test(path);
    var target = prefix + marker + modeTargets[mode];
    if (offline) {
      target = target.replace(/\/$/, "/index");
      if (!/\.html$/.test(target)) {
        target += ".html";
      }
    } else if (!target.endsWith("/")) {
      target += "/";
    }
    return target;
  }

  function createButton(label, value, groupLabel, pressed, handler) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "fz-control";
    button.textContent = label;
    button.dataset.value = value;
    button.setAttribute("aria-label", groupLabel + ": " + label);
    button.setAttribute("aria-pressed", pressed ? "true" : "false");
    button.addEventListener("click", handler);
    return button;
  }

  function headingLabel(heading) {
    var copy = heading.cloneNode(true);
    copy.querySelectorAll(".headerlink").forEach(function (permalink) {
      permalink.remove();
    });
    return (copy.textContent || "").replace(/\s+/g, " ").trim() || "Fractal Zones";
  }

  function init() {
    var main = document.querySelector("article.md-content__inner");
    var heading = main && main.querySelector("h1");
    if (!main || !heading) {
      return;
    }
    var preferences = loadPreferences();
    document.body.dataset.fzDepth = preferences.depth;

    var bar = document.createElement("aside");
    bar.className = "fz-statusbar";
    bar.setAttribute("aria-label", "Dokumentationssteuerung");

    var where = document.createElement("div");
    where.className = "fz-statusbar__where";
    var label = document.createElement("strong");
    label.textContent = "Du bist hier";
    var page = document.createElement("span");
    page.textContent = headingLabel(heading);
    where.append(label, page);

    var controls = document.createElement("div");
    var depthLabel = document.createElement("span");
    depthLabel.className = "fz-statusbar__where";
    depthLabel.textContent = "Tiefe: ";
    var depthControls = document.createElement("span");
    depthControls.className = "fz-controls";
    [["Kurz", "short"], ["Praxis", "practice"], ["Technik", "technical"]].forEach(function (entry) {
      depthControls.appendChild(createButton(entry[0], entry[1], "Detailtiefe", preferences.depth === entry[1], function () {
        preferences.depth = entry[1];
        document.body.dataset.fzDepth = entry[1];
        depthControls.querySelectorAll("button").forEach(function (item) {
          item.setAttribute("aria-pressed", item.dataset.value === entry[1] ? "true" : "false");
        });
        persist(preferences);
      }));
    });
    depthLabel.appendChild(depthControls);

    var modeLinks = document.createElement("nav");
    modeLinks.className = "fz-mode-links";
    modeLinks.setAttribute("aria-label", "Dokumentationsmodus");
    allowedModes.forEach(function (mode) {
      var link = document.createElement("a");
      link.className = "fz-mode-link";
      link.href = targetFor(mode);
      link.textContent = modeLabels[mode];
      if (inferMode() === mode) {
        link.setAttribute("aria-current", "page");
      }
      link.addEventListener("click", function () {
        preferences.mode = mode;
        persist(preferences);
      });
      modeLinks.appendChild(link);
    });
    controls.append(depthLabel, modeLinks);
    bar.append(where, controls);
    heading.insertAdjacentElement("afterend", bar);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
}());
