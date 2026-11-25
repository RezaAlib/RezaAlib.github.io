(function () {
  var root = document.querySelector("[data-collab]");
  if (!root) return;
  var groups = root.querySelectorAll("svg .person");
  var items = root.querySelectorAll(".collab-list li");

  function setActive(key) {
    root.classList.toggle("has-active", !!key);
    groups.forEach(function (g) { g.classList.toggle("is-active", g.dataset.person === key); });
    items.forEach(function (li) { li.classList.toggle("is-active", li.dataset.person === key); });
  }

  items.forEach(function (li) {
    li.addEventListener("mouseenter", function () { setActive(li.dataset.person); });
    li.addEventListener("focus", function () { setActive(li.dataset.person); });
    li.addEventListener("mouseleave", function () { setActive(null); });
    li.addEventListener("blur", function () { setActive(null); });
  });
  groups.forEach(function (g) {
    g.addEventListener("mouseenter", function () { setActive(g.dataset.person); });
    g.addEventListener("mouseleave", function () { setActive(null); });
  });
})();
