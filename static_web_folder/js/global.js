function loadHeader(doc) {
  const template = doc.createElement("template");
  template.innerHTML = `
      <header class="header">
      <div class="container"><a  href="../index.html" class="header-item">
      ППС
      </a>
      <a  href="../subjects_masters.html" class="header-item">
      Магистратура
      </a>
      <a  href="../subjects_bachelor.html" class="header-item">
      Бакалавриат
      </a>

      </div>
      </header>
      `;

  doc.body.prepend(template.content);
}
function currentPage() {
  const headerItems = $(".header-item");
  const heading = $(".heading")[0];
  for (let element of headerItems) {
    if (element.textContent.trim() == heading.textContent.trim()) {
      element.classList.add("active");
    }
  }
}

export { currentPage, loadHeader };
