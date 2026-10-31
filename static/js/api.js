(function () {
  async function request(url, options) {
    const response = await fetch(url, options || {});
    const data = await response.json().catch(function () { return {}; });
    if (!response.ok) throw new Error(data.detail || data.message || ("Request failed (" + response.status + ")"));
    return data;
  }
  window.GhostAPI = {
    get: function (url) { return request(url, { method: "GET" }); },
    post: function (url, body) {
      return request(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body) });
    },
    upload: function (url, formData) { return request(url, { method: "POST", body: formData }); }
  };
})();