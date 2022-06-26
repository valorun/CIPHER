/* exported failAlert */
function failAlert(message) {
  alert('<i class=\'fas fa-times-circle\'></i> Attention !', message, 'fail');
}

/* exported successAlert */
function successAlert(message) {
  alert('<i class=\'fas fa-check-circle\'></i> Succès !', message, 'success');
}

function alert(title, message, additionnal_class) {
  const $el = document.getElementsByClassName('alert-modal')[0];
  $el.innerHTML = '';
  $el.insertAdjacentHTML('beforeend',
      '<div class=\'alert-modal-content ' + additionnal_class + '\'>' +
        '<header>' + title +
          '<a onclick=\'this.parentElement.parentElement.style.display=\"none\"\' >' +
          '&times;' +
          '</a>' +
        '</header>' +
        '<p>' +
          message +
        '</p>' +
      '</div>');
  setTimeout(() => {
    while ($el.firstChild) { $el.removeChild($el.firstChild); }
  }, 3000);
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
