export default function removeBodyClasses() {
    const el = document.querySelector("html");
    if (el) {
      console.log(el);
      for (var i = el.classList.length - 1; i >= 0; i--) {
        console.log(el.classList[i].startsWith("theme"));
        if (el.classList[i].startsWith("theme")) {
          el.classList.remove(el.classList[i]);
        }
      }
    }
  }

