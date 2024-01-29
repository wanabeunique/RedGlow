export default function removeBodyClasses() {
    const el = document.querySelector("html");
    if (el) {
      for (var i = el.classList.length - 1; i >= 0; i--) {
        if (el.classList[i].startsWith("theme")) {
          el.classList.remove(el.classList[i]);
        }
      }
    }
  }

