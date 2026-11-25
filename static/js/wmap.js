(function () {
  var root = document.querySelector("[data-wmap]");
  if (!root) return;
  var svg = root.querySelector("svg");
  var vb = svg.viewBox.baseVal;
  var pinned = null;
  var centres = {};
  root.querySelectorAll("circle.hit").forEach(function (c) {
    centres[c.dataset.country] = [+c.getAttribute("cx"), +c.getAttribute("cy")];
  });

  function hideAll() {
    root.querySelectorAll(".wmap-tip").forEach(function (t) { t.hidden = true; });
    root.querySelectorAll(".country.is-active").forEach(function (p) { p.classList.remove("is-active"); });
  }

  function show(id) {
    hideAll();
    var tip = root.querySelector('.wmap-tip[data-for="' + id + '"]');
    if (!tip || !centres[id]) return;
    root.querySelectorAll('.country[data-country="' + id + '"]').forEach(function (p) { p.classList.add("is-active"); });
    tip.hidden = false;
    var scale = svg.clientWidth / vb.width;
    var x = centres[id][0] * scale, y = centres[id][1] * scale;
    var w = tip.offsetWidth, h = tip.offsetHeight, W = root.clientWidth;
    var left = x + 18;
    if (left + w > W) left = Math.max(0, x - w - 18);
    var top = Math.max(0, Math.min(y - 24, svg.clientHeight - h));
    tip.style.left = left + "px";
    tip.style.top = top + "px";
  }

  function hide() { if (!pinned) hideAll(); }

  root.querySelectorAll("[data-country]").forEach(function (el) {
    var id = el.dataset.country;
    el.addEventListener("mouseenter", function () { if (!pinned) show(id); });
    el.addEventListener("mouseleave", hide);
    el.addEventListener("focus", function () { show(id); });
    el.addEventListener("blur", function () { if (!pinned) hideAll(); });
    el.addEventListener("click", function (e) {
      e.stopPropagation();
      if (pinned === id) { pinned = null; hideAll(); } else { pinned = id; show(id); }
    });
  });

  document.querySelectorAll(".wmap-list li").forEach(function (li) {
    var id = li.dataset.country;
    li.addEventListener("mouseenter", function () { if (!pinned) show(id); });
    li.addEventListener("mouseleave", hide);
  });

  document.addEventListener("click", function () { if (pinned) { pinned = null; hideAll(); } });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { pinned = null; hideAll(); } });
  window.addEventListener("resize", function () { if (pinned) show(pinned); });
})();
