(function () {
  function escapeHTML(value) {
    return String(value === null || value === undefined ? "" : value).replace(/[&<>"']/g, function (char) {
      return {
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
      }[char];
    });
  }

  function metric(label, value, detail) {
    return [
      '<article class="metric-card">',
      '<span class="metric-label">', escapeHTML(label), '</span>',
      '<strong class="metric-value">', escapeHTML(value), '</strong>',
      '<span class="metric-detail">', escapeHTML(detail || ""), '</span>',
      '</article>'
    ].join("");
  }

  function intro(kicker, title, description) {
    return [
      '<section class="page-intro motion-block">',
      '<span class="eyebrow">', escapeHTML(kicker), '</span>',
      '<h1>', escapeHTML(title), '</h1>',
      '<p>', escapeHTML(description), '</p>',
      '</section>'
    ].join("");
  }

  function panel(title, content, extraClass) {
    return [
      '<section class="content-panel motion-block ', escapeHTML(extraClass || ""), '">',
      '<div class="panel-heading"><h2>', escapeHTML(title), '</h2></div>',
      content,
      '</section>'
    ].join("");
  }

  function emptyState(title, detail) {
    return [
      '<div class="empty-state motion-block">',
      '<span class="empty-state-mark" aria-hidden="true">—</span>',
      '<h3>', escapeHTML(title), '</h3>',
      '<p>', escapeHTML(detail), '</p>',
      '</div>'
    ].join("");
  }

  function statusLine(label, value, detail) {
    return [
      '<div class="status-line">',
      '<div><strong>', escapeHTML(label), '</strong><span>', escapeHTML(detail || ""), '</span></div>',
      '<span class="status-value">', escapeHTML(value), '</span>',
      '</div>'
    ].join("");
  }

  function errorPanel(error) {
    return [
      '<section class="content-panel error-panel">',
      '<h2>Unable to load this page</h2>',
      '<p>', escapeHTML(error && error.message ? error.message : "An unexpected error occurred."), '</p>',
      '<button class="button button-secondary" type="button" data-action="refresh-page">Retry</button>',
      '</section>'
    ].join("");
  }

  window.GhostUI = {
    escapeHTML: escapeHTML,
    metric: metric,
    intro: intro,
    panel: panel,
    emptyState: emptyState,
    statusLine: statusLine,
    errorPanel: errorPanel
  };
})();