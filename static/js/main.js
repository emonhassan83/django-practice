document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("main > *").forEach((el, i) => {
        el.classList.add("fade-in");
        el.style.animationDelay = `${i * 80}ms`;
    });
});
