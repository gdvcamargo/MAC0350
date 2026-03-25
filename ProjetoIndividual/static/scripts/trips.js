async function refreshTripsList() {
  const tripsList = document.getElementById('trips-list');
  if (!tripsList) {
    return;
  }

  const response = await fetch('/trips/list');
  if (!response.ok) {
    return;
  }

  tripsList.innerHTML = await response.text();
  tripsList.classList.add('trip-list');
}

function setTripUpdate(buttonElement) {
  const form = document.getElementById('trip-create-form');
  if (!form || !buttonElement) {
    return;
  }

  const isUpdateField = document.getElementById('trip-is-update');
  const tripIdField = document.getElementById('trip-id');
  const submitButton = document.getElementById('trip-submit-button');
  const cancelButton = document.getElementById('trip-cancel-update');

  form.querySelector('#name').value = buttonElement.dataset.name || '';
  form.querySelector('#destination').value = buttonElement.dataset.destination || '';
  form.querySelector('#start_date').value = buttonElement.dataset.startDate || '';
  form.querySelector('#end_date').value = buttonElement.dataset.endDate || '';
  form.querySelector('#budget').value = buttonElement.dataset.budget || '';

  if (isUpdateField) {
    isUpdateField.value = 'true';
  }
  if (tripIdField) {
    tripIdField.value = buttonElement.dataset.tripId || '';
  }
  if (submitButton) {
    submitButton.textContent = 'Salvar alteração';
  }
  if (cancelButton) {
    cancelButton.style.display = 'inline-block';
  }
}

function cancelTripUpdate() {
  const form = document.getElementById('trip-create-form');
  if (!form) {
    return;
  }

  form.reset();

  const isUpdateField = document.getElementById('trip-is-update');
  const tripIdField = document.getElementById('trip-id');
  const submitButton = document.getElementById('trip-submit-button');
  const cancelButton = document.getElementById('trip-cancel-update');

  if (isUpdateField) {
    isUpdateField.value = 'false';
  }
  if (tripIdField) {
    tripIdField.value = '';
  }
  if (submitButton) {
    submitButton.textContent = 'Criar viagem';
  }
  if (cancelButton) {
    cancelButton.style.display = 'none';
  }
}

async function submitTrip(event) {
  if (event) {
    event.preventDefault();
  }

  const form = document.getElementById('trip-create-form');
  if (!form) {
    return;
  }

  const data = new FormData(form);
  const isUpdate = (document.getElementById('trip-is-update')?.value || 'false') === 'true';
  const tripId = document.getElementById('trip-id')?.value;

  const payload = {
    name: data.get('name'),
    destination: data.get('destination'),
    start_date: data.get('start_date'),
    end_date: data.get('end_date'),
    budget: Number(data.get('budget')),
  };

  let url = '/trips/';
  let method = 'POST';

  if (isUpdate && tripId) {
    url = `/trips/${tripId}`;
    method = 'PUT';
  }

  const response = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    return;
  }

  cancelTripUpdate();
  await refreshTripsList();
}

async function deleteTrip(buttonElement) {
  const tripId = buttonElement ? buttonElement.dataset.tripId : null;
  if (!tripId) {
    return;
  }

  const response = await fetch(`/trips/${tripId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    return;
  }

  await refreshTripsList();
}

if (document.getElementById('trips-list')) {
  refreshTripsList();
}
