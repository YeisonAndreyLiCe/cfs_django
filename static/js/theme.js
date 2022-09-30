/* eslint-disable-next-line */
$(document).ready(function() {
  const preferColorScheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  const themeSwitcher = document.querySelector("#theme-switcher");
  const setTheme = (theme) => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    if(theme === "dark") {
      themeSwitcher.checked = true;
    }
  };
  themeSwitcher.addEventListener("click", () => {
    const switchToTheme = localStorage.getItem("theme") === "dark" ? "light" : "dark";
    setTheme(switchToTheme);
    document.body.classList.toggle("dark");
    const btnSwitch = document.querySelector("#theme-switcher");
    btnSwitch.classList.toggle("active");
  });
  setTheme(localStorage.getItem("theme")|| preferColorScheme);
});

