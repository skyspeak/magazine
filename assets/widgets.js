/* The Big Ask - five small widgets, declared in HTML, no dependencies.
   Every widget is progressive: the page reads fine with JS off.
   Nothing is transmitted. Only "streak" persists, and only on this device. */
(function () {
  "use strict";
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var store = (function () {
    try { var k = "__ba"; localStorage.setItem(k, "1"); localStorage.removeItem(k); return localStorage; }
    catch (e) { return null; }
  })();
  var esc = function (s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
  var data = function (el) { try { return JSON.parse(el.getAttribute("data-w") || "{}"); } catch (e) { return {}; } };

  /* ---- 1. CHECKLIST: tick things, get a verdict ------------------------ */
  function checklist(el) {
    var d = data(el), items = d.items || [], id = el.id || "ck";
    el.innerHTML =
      '<ul class="w-check">' + items.map(function (it, i) {
        return '<li><input type="checkbox" id="' + id + '-' + i + '"><label for="' + id + '-' + i + '">' +
          '<span class="w-lab">' + it.t + '</span>' +
          (it.why ? '<span class="w-why">' + it.why + '</span>' : '') + '</label></li>';
      }).join("") + '</ul><p class="w-out" role="status" aria-live="polite"></p>';
    var boxes = $$("input", el), out = el.querySelector(".w-out");
    function paint() {
      var n = boxes.filter(function (b) { return b.checked; }).length, t = items.length;
      var v = d.verdicts || [];
      var msg = d.empty || "Tick what is true today.";
      for (var i = 0; i < v.length; i++) if (n >= v[i].min) { msg = v[i].say; break; }
      out.innerHTML = (n ? "<b>" + n + " of " + t + ".</b> " : "") + msg;
    }
    boxes.forEach(function (b) { b.addEventListener("change", paint); });
    paint();
  }

  /* ---- 2. CHOOSER: pick one, get the answer for that one --------------- */
  function chooser(el) {
    var d = data(el), opts = d.options || [];
    el.innerHTML =
      '<div class="w-opts">' + opts.map(function (o, i) {
        return '<button type="button" class="w-opt" data-i="' + i + '" aria-pressed="false">' +
          (o.n ? '<span class="w-n">' + o.n + '</span>' : '') + '<span class="w-t">' + o.t + '</span></button>';
      }).join("") + '</div>' +
      '<div class="w-out w-panel" role="status" aria-live="polite"><p class="w-hint">' + (d.empty || "Pick one.") + '</p></div>';
    var btns = $$(".w-opt", el), out = el.querySelector(".w-out");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        var o = opts[+b.dataset.i];
        out.innerHTML = '<span class="w-head">' + o.head + '</span>' +
          (o.body || []).map(function (p) { return "<p>" + p + "</p>"; }).join("");
      });
    });
  }

  /* ---- 3. STREAK: N days, saved on this device ------------------------- */
  function streak(el) {
    var d = data(el), n = d.days || 14, key = "ba_" + (d.key || el.id || "s");
    var days = [];
    try { days = JSON.parse((store && store.getItem(key)) || "[]"); } catch (e) { days = []; }
    if (!Array.isArray(days)) days = [];
    days = days.map(function (v) { return parseInt(v, 10); })
               .filter(function (v, i, a) { return !isNaN(v) && v >= 0 && v < n && a.indexOf(v) === i; });
    el.innerHTML = '<p class="w-out w-streak" role="status" aria-live="polite"></p><div class="w-dots"></div>' +
      '<p class="w-note"></p><button type="button" class="w-reset">Start again</button>';
    var dots = el.querySelector(".w-dots"), out = el.querySelector(".w-streak");
    function run() { var b = 0, r = 0; for (var i = 0; i < n; i++) { if (days.indexOf(i) > -1) { r++; if (r > b) b = r; } else r = 0; } return b; }
    function paint() {
      dots.innerHTML = "";
      for (var i = 0; i < n; i++) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "w-dot"; b.dataset.d = i;
        b.setAttribute("aria-pressed", String(days.indexOf(i) > -1));
        b.setAttribute("aria-label", (d.unit || "Day") + " " + (i + 1));
        b.textContent = i + 1; dots.appendChild(b);
      }
      var r = run(), v = d.verdicts || [], msg = d.empty || "Tap one each time you do it.";
      for (var j = 0; j < v.length; j++) if (r >= v[j].min) { msg = v[j].say; break; }
      out.innerHTML = (days.length ? "<b>" + r + " in a row.</b> " : "") + msg;
      el.querySelector(".w-note").textContent = store
        ? "Saved on this device only. Nobody else can see it."
        : "This browser will not remember your taps, so keep a paper copy too.";
    }
    dots.addEventListener("click", function (e) {
      var b = e.target.closest(".w-dot"); if (!b) return;
      var i = days.indexOf(+b.dataset.d);
      if (i > -1) days.splice(i, 1); else days.push(+b.dataset.d);
      if (store) { try { store.setItem(key, JSON.stringify(days)); } catch (e2) {} }
      paint();
    });
    el.querySelector(".w-reset").addEventListener("click", function () {
      days = []; if (store) { try { store.removeItem(key); } catch (e3) {} } paint();
    });
    paint();
  }

  /* ---- 4. DIAL: a number you set, a sentence you get ------------------- */
  function dial(el) {
    var d = data(el);
    el.innerHTML =
      '<div class="w-dial"><label for="' + el.id + '-r">' + d.label + '</label>' +
      '<input id="' + el.id + '-r" type="range" min="' + d.min + '" max="' + d.max + '" step="' + (d.step || 1) + '" value="' + d.value + '">' +
      '<output class="w-val" id="' + el.id + '-v"></output></div>' +
      '<p class="w-out" role="status" aria-live="polite"></p>';
    var r = el.querySelector("input"), v = el.querySelector(".w-val"), out = el.querySelector(".w-out");
    function paint() {
      var n = +r.value;
      v.textContent = (d.prefix || "") + n + (d.suffix || "");
      var bands = d.bands || [], msg = "";
      for (var i = 0; i < bands.length; i++) if (n <= bands[i].upto) { msg = bands[i].say; break; }
      if (!msg && bands.length) msg = bands[bands.length - 1].say;
      out.innerHTML = msg;
    }
    r.addEventListener("input", paint); paint();
  }

  /* ---- 5. SORTER: put each thing in a bucket -------------------------- */
  function sorter(el) {
    var d = data(el), items = d.items || [], buckets = d.buckets || [];
    el.innerHTML = '<ul class="w-sort">' + items.map(function (it, i) {
      return '<li><span class="w-item">' + it.t + '</span><span class="w-picks">' +
        buckets.map(function (b, j) {
          return '<button type="button" class="w-pick" data-i="' + i + '" data-b="' + j + '" aria-pressed="false">' + b.t + '</button>';
        }).join("") + '</span><span class="w-mark" aria-live="polite"></span></li>';
    }).join("") + '</ul><p class="w-out" role="status" aria-live="polite"></p>';
    var picked = {}, out = el.querySelector(".w-out");
    el.addEventListener("click", function (e) {
      var b = e.target.closest(".w-pick"); if (!b) return;
      var i = +b.dataset.i, j = +b.dataset.b;
      picked[i] = j;
      $$('.w-pick[data-i="' + i + '"]', el).forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
      var li = b.closest("li"), right = items[i].bucket;
      var mark = li.querySelector(".w-mark");
      var ok = (right === undefined) || j === right;
      mark.textContent = (right === undefined) ? "" : (ok ? "yes" : "actually: " + buckets[right].t);
      mark.className = "w-mark " + (right === undefined ? "" : (ok ? "w-ok" : "w-no"));
      var done = Object.keys(picked).length;
      out.innerHTML = done < items.length
        ? "<b>" + done + " of " + items.length + " sorted.</b>"
        : "<b>All sorted.</b> " + (d.done || "");
    });
  }

  /* ---- copy-to-clipboard: <button data-copy="#id"> ------------------- */
  $$("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = document.querySelector(btn.getAttribute("data-copy"));
      if (!src) return;
      var text = (src.innerText || src.textContent || "").trim();
      var done = function () {
        var was = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = was; }, 1600);
      };
      var fallback = function () {
        var ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); }
        catch (e) { btn.textContent = "Select and copy"; }
        document.body.removeChild(ta);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
    });
  });

  var KIND = { checklist: checklist, chooser: chooser, streak: streak, dial: dial, sorter: sorter };
  $$("[data-widget]").forEach(function (el) {
    var fn = KIND[el.getAttribute("data-widget")];
    if (fn) { try { fn(el); } catch (e) { el.hidden = true; } }
  });
})();
