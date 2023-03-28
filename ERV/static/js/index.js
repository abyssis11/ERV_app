"use strict";

let calendarSwitch = document.getElementById("showCal");
let calendarItem = document.getElementById("myCal");
let textItem = document.getElementById("textShow");
let containerCal = document.getElementById("containerCal");

window.onload = function () {
  if (!window.location.href.includes("filter")) {
    window.location.href += "filter";
  }
  calendarItem.style.display = "none";
  calendarItem.name = "";
  textItem.style.display = "block";
  containerCal.style.justifyContent = "space-evenly";
};

document.body.addEventListener("htmx:configRequest", (event) => {
  event.detail.headers["X-CSRFToken"] = "{{ csrf_token }}";
});

let dateStart =
  new Date().getUTCFullYear() +
  "-" +
  (new Date().getMonth() + 1) +
  "-" +
  new Date().getDate();
let dateEnd =
  new Date(dateStart).getUTCFullYear() +
  "-" +
  (new Date().getMonth() + 1) +
  "-" +
  new Date().getDate();

$(function containText() {
  $('input[name="daterange"]').daterangepicker(
    {
      opens: "left",
      showDropdowns: true,
      locale: {
        format: "YYYY-MM-DD",
      },
    },
    function (start, end, label) {
      dateStart = start.format("YYYY-MM-DD");
      dateEnd = end.format("YYYY-MM-DD");
      let month, day;
      if (new Date(dateStart).getMonth() + 1 < 10)
        month = "0" + (new Date(dateStart).getMonth() + 1);
      else month = new Date(dateStart).getMonth() + 1;
      if (new Date(dateStart).getDate() < 10)
        day = "0" + new Date(dateStart).getDate();
      else day = new Date(dateStart).getDate();
      let date1 = new Date(dateStart).getFullYear() + "-" + month + "-" + day;
      if (new Date().getMonth() + 1 < 10)
        month = "0" + (new Date().getMonth() + 1);
      else month = new Date().getMonth() + 1;
      if (new Date().getDate() < 10) day = "0" + new Date().getDate();
      else day = new Date().getDate();
      let date2 = new Date().getFullYear() + "-" + month + "-" + day;
      if (new Date(dateEnd).getMonth() + 1 < 10)
        month = "0" + (new Date(dateEnd).getMonth() + 1);
      else month = new Date(dateEnd).getMonth() + 1;
      if (new Date(dateEnd).getDate() < 10)
        day = "0" + new Date(dateEnd).getDate();
      else day = new Date(dateEnd).getDate();
      let date3 = new Date(dateEnd).getFullYear() + "-" + month + "-" + day;

      if (date1 > date2 || date3 > date2) {
        alert("Unesite važeći datum" + "današnji datum je: " + date2);
        dateStart = null;
        dateEnd = null;
      } else {
        dateStart = start.format("YYYY-MM-DD");
        dateEnd = end.format("YYYY-MM-DD");
      }
    }
  );
});

function calendar() {
  $('input[name="daterange"]').focus();
}

function check() {
  if (!calendarSwitch.checked) {
    calendarItem.style.display = "none";
    calendarItem.name = "";
    textItem.style.display = "block";
    containerCal.style.justifyContent = "space-evenly";
  } else {
    calendarItem.style.display = "block";
    calendarItem.name = "daterange";
    textItem.style.display = "none";
    containerCal.style.justifyContent = "space-between";
  }
}
