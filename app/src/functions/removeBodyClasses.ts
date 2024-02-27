export default function removeBodyThemes() {
    const el = window.document.documentElement 
    for (var i = el.classList.length - 1; i >= 0; i--) {
      if (el.classList[i].startsWith("theme")) {
        el.classList.remove(el.classList[i]);
      }
    }
  }

