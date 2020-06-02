/* exported failAlert */
function failAlert(message) {
  alert('<i class=\'fas fa-times-circle\'></i> Attention !', message, 'dark-red');
}

/* exported successAlert */
function successAlert(message) {
  alert('<i class=\'fas fa-check-circle\'></i> Succès !', message, 'green');
}

function alert(title, message, color) {
  const $el = document.getElementsByClassName('alert-modal')[0];
  $el.innerHTML = '';
  $el.insertAdjacentHTML('beforeend',
    '<div class=\'display-bottomright\'>' +
      '<div class=\'panel card-4 animate-bottom display-container ' + color + '\'>' +
        '<span onclick=\'this.parentElement.style.display=\'none\'\' ' +
        'class=\'button large display-topright ' + color + '\'>&times;' +
        '</span>' +
        '<h4>' + title + '</h4>' +
        '<p>' +
          message +
        '</p>' +
      '</div>' +
    '</div>');
  setTimeout(() => {
    while ($el.firstChild) { $el.removeChild($el.firstChild); }
  }, 3000);
}

/* exported isVisible */
function isVisible($el) {
  return ($el.offsetParent !== null);
}

/* exported empty */
function empty($el) {
  while ($el.firstChild) { $el.removeChild($el.firstChild); }
}

/* exported fetchJson */
function fetchJson(path, method, body) {
  const headers = new Headers();
  headers.append('Content-Type', 'application/json');
  let response = null;
  return fetch(path, {
    method: method,
    headers: headers,
    body: JSON.stringify(body)
  })
    .then(responseObject => {
      response = responseObject;
      return responseObject.json();
    })
    .then(parsedResponse => {
      if (!response.ok) {
        throw new APIError(parsedResponse, response.statusText, response.status);
      }
      return parsedResponse;
    })
    .catch(error => {
      console.error(error);
      failAlert(error.message);
      throw error;
    });
}

class APIError extends Error {
  constructor(message, name, code) {
    super(message);
    this.name = name;
    this.code = code;
  }
}
