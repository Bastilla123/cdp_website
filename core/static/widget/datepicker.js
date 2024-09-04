const days = () => {
  const days = [];
  for (let i = 1; i <= 31; i++) {
    days.push(i);
  }
  return days;
};

const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const years = () => {
  const years = [];
  for (let i = 1900; i <= 2023; i++) {
    years.push(i);
  }
  return years;
};

const hours = () => {
  const hours = [];
  for (let i = 0; i <= 23; i++) {
    hours.push(i > 9 ? i : "0" + i);
  }
  return hours;
};

const minutes = () => {
  const minutes = [];
  for (let i = 0; i <= 59; i++) {
    minutes.push(i > 9 ? i : "0" + i);
  }
  return minutes;
};

const appendChildren = (time_duration_array, selectedElement) => {
  time_duration_array.forEach((time_duration) => {
    const option = document.createElement("li");
    option.value = time_duration;
    option.innerHTML = time_duration;
    for (let i = 0; i < selectedElement.length; i++) {
      const clonedOption = option.cloneNode(true);
      selectedElement[i].appendChild(clonedOption);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {

  const daysSelect = document.querySelectorAll(".dropdownlist.data-day");
  const monthsSelect = document.querySelectorAll(".dropdownlist.data-month");
  const yearsSelect = document.querySelectorAll(".dropdownlist.data-year");
  const hoursSelect = document.querySelectorAll(".dropdownlist.data-hour");
  const minutesSelect = document.querySelectorAll(".dropdownlist.data-minute");
  const secondsSelect = document.querySelectorAll(".dropdownlist.data-second");

  appendChildren(days(), daysSelect);
  appendChildren(months, monthsSelect);
  appendChildren(years(), yearsSelect);
  appendChildren(hours(), hoursSelect);
  appendChildren(minutes(), minutesSelect);
  appendChildren(minutes(), secondsSelect);

  const form = document.getElementById("Form");

  form.addEventListener('submit', function() {
    document.querySelectorAll('.dropdown-input.data').forEach((dateSelectorsDiv) => {
      const hiddenInput = form.querySelector(`input[type='hidden'][name='${dateSelectorsDiv.id}']`);
      const daysInput = dateSelectorsDiv.querySelector('.data-day.datetime-picker').value;
      const monthInput = dateSelectorsDiv.querySelector('.data-month.datetime-picker').value;
      const yearInput = dateSelectorsDiv.querySelector('.data-year.datetime-picker').value;
      const hourInput = dateSelectorsDiv.querySelector('.data-hour.datetime-picker').value;
      const minuteInput = dateSelectorsDiv.querySelector('.data-minute.datetime-picker').value;
      const secondInput = dateSelectorsDiv.querySelector('.data-second.datetime-picker').value;

      hiddenInput.value = `${daysInput}/${monthInput}/${yearInput}`;
      if (hourInput) {
        hiddenInput.value +=  ` ${hourInput}:${minuteInput}:${secondInput}`
      }
    });
  });

  document.addEventListener("click", function (e) {
    const customSelects = document.querySelectorAll(".custom-select.open");

    for (let i = 0; i < customSelects.length; i++) {
      const select = customSelects[i];

      if (!select.contains(e.target)) {
        select.classList.remove("open");

        const dropdownDateInput = select.closest(
            ".input-container.dropdown-input"
        );
        const inputs = dropdownDateInput.querySelectorAll("input");
        const allInputsNotEmpty = Array.from(inputs).every(function (input) {
          return input.value.trim() !== "";
        });

        const allInputsEmpty = Array.from(inputs).every(function (input) {
          return input.value.trim() === "";
        });

        if (allInputsEmpty || allInputsNotEmpty) {
          if (!dropdownDateInput.classList.contains("hidden")) {
            const dateClass = dropdownDateInput.classList
                .toString()
                .split(" ");
            const dateInput = document.querySelector(
                'input[name="' + dateClass[dateClass.length - 1] + '"]'
            );
            dropdownDateInput.classList.add("hidden");
            dateInput
                .closest(".input-container")
                .classList.remove("hidden");
          }
        }
      }
    }
  });

  const selectTriggers = document.querySelectorAll(".dropdown-input");
  for (let i = 0; i < selectTriggers.length; i++) {
    selectTriggers[i].addEventListener("click", function (e) {
      e.stopPropagation();
      const customSelect = this.closest(".custom-select");

      const isAlreadyOpen = customSelect?.classList.contains("open");

      const allCustomSelects = document.querySelectorAll(".custom-select");
      for (let j = 0; j < allCustomSelects.length; j++) {
        allCustomSelects[j].classList.remove("open");
      }

      if (!isAlreadyOpen) {
        customSelect?.classList?.add("open");
      }
    });
  }

  const selectOptions = document.querySelectorAll(".dropdownlist li");
  for (let i = 0; i < selectOptions.length; i++) {
    selectOptions[i].addEventListener("click", function () {
      this.closest(".dropdownlist")
          .querySelectorAll(".dropdownlist li")
          .forEach((option) => option.classList.remove("selected"));
      const customSelect = this.closest(".custom-select");
      const input = customSelect.querySelector("input");
      input.value = this.textContent;
      this.classList.add("selected");
      customSelect.classList.remove("open");

      const inputDateContainer = this.closest(".dropdown-input.data");
      const dateInputs = inputDateContainer?.querySelectorAll("input");

      if (dateInputs) {
        const allInputsNotEmpty = Array.from(dateInputs).every(function (
            input
        ) {
          return input.value.trim() !== "";
        });
        const allInputsEmpty = Array.from(dateInputs).every(function (input) {
          return input.value.trim() === "";
        });

        if (allInputsEmpty || allInputsNotEmpty) {
          const dateClass = inputDateContainer.classList
              .toString()
              .split(" ");
          const dateInput = document.querySelector(
              'input[name="' + dateClass[dateClass.length - 1] + '"]'
          );

          dateInput.value = `${dateInputs[0].value} ${dateInputs[1].value} ${dateInputs[2].value}`;
          if (dateInputs.length === 6) {
            dateInput.value += ` ${dateInputs[3].value}:${dateInputs[4].value}:${dateInputs[5].value}`
          }
          if (!inputDateContainer.classList.contains("hidden")) {
            inputDateContainer.classList.add("hidden");
            dateInput
                .closest(".input-container")
                .classList.remove("hidden");
          }
        }
      }
    });
  }
});

const showDateSelectorsHandler = (el) => {
  const dateSelectorsDiv = document.querySelector(
      `.dropdown-input.data.${el.name}`
  );

  dateSelectorsDiv.classList.remove("hidden");
  el.closest(".input-container").classList.add("hidden");

  const dataDayDropdown = dateSelectorsDiv.querySelector(
      ".custom-select.data-day"
  );
  setTimeout(() => {
    dataDayDropdown.classList.add("open");
  }, 100);
};