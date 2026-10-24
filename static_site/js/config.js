/*
 * Site configuration. Edit here, not in the page markup.
 *
 * formEndpoint: where service requests are POSTed (multipart/form-data, JSON response).
 *   Today: Formspree. Later: the service-management app intake API. Field names are a
 *   stable contract, documented in docs/service-request-contract.md.
 * teamLoginUrl: private app login. Leave empty to hide the "Team Login" link.
 */
window.ST_CONFIG = {
    formEndpoint: "https://formspree.io/f/xgoaqvvd",
    teamLoginUrl: ""
};
