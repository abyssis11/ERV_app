const modal = new bootstrap.Modal(document.getElementById("modal"))

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response && e.detail.xhr.status==200) {
    modal.hide()
    e.detail.shouldSwap = false
  }
})

// empty the dialog
htmx.on("hidden.bs.modal", () => {
  document.getElementById("dialog").innerHTML = ""
})


const modal_graph = new bootstrap.Modal(document.getElementById("modal-graph"))

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "graph") {
    modal_graph.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "graph" && !e.detail.xhr.response && e.detail.xhr.status==200) {
    modal_graph.hide()
    e.detail.shouldSwap = false
  }
})

// empty the dialog
htmx.on("hidden.bs.modal", () => {
  document.getElementById("graph").innerHTML = ""
})