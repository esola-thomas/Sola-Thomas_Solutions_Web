/*
 * Service request form: validation, emergency handling, attribution, and submission.
 * Payload contract: docs/service-request-contract.md (keep field names stable; the
 * service-management app will consume the same fields).
 */
(function () {
    "use strict";

    var MAX_PHOTOS = 5;
    var MAX_PHOTO_BYTES = 10 * 1024 * 1024;
    var SERVICE_EMAIL = "service@solathomas.com";

    var config = window.ST_CONFIG || {};
    var track = window.stTrack || function () {};
    var form = document.getElementById("serviceRequestForm");
    var submitBtn = document.getElementById("submitBtn");
    var errorBox = document.getElementById("formError");
    var emergency = document.getElementById("emergency");
    var emergencyCallout = document.getElementById("emergencyCallout");
    var photos = document.getElementById("photos");
    var preferredDate = document.getElementById("preferred_date");
    var started = false;

    function pad(n) { return (n < 10 ? "0" : "") + n; }

    function localDate(d) {
        return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
    }

    // Reference shown to the customer and carried into email, Formspree, and the app.
    function newRequestId() {
        var alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
        var bytes = new Uint8Array(5);
        (window.crypto || window.msCrypto).getRandomValues(bytes);
        var suffix = "";
        for (var i = 0; i < bytes.length; i++) { suffix += alphabet[bytes[i] % alphabet.length]; }
        return "ST-" + localDate(new Date()).replace(/-/g, "") + "-" + suffix;
    }

    preferredDate.min = localDate(new Date());

    emergency.addEventListener("change", function () {
        emergency.closest(".emergency-check").classList.toggle("checked", emergency.checked);
        emergencyCallout.classList.toggle("show", emergency.checked);
        if (emergency.checked) { track("emergency_checked"); }
    });

    form.addEventListener("input", function () {
        if (!started) {
            started = true;
            track("form_start", { form_name: "service_request" });
        }
    });

    function photosValid() {
        var files = photos.files ? Array.prototype.slice.call(photos.files) : [];
        var total = files.reduce(function (sum, f) { return sum + f.size; }, 0);
        var allImages = files.every(function (f) { return /^image\//.test(f.type); });
        return files.length <= MAX_PHOTOS && total <= MAX_PHOTO_BYTES && allImages;
    }

    function setFieldState(input, valid) {
        var field = input.closest(".field");
        if (!field) { return; }
        field.classList.toggle("invalid", !valid);
        input.setAttribute("aria-invalid", valid ? "false" : "true");
    }

    function validateInput(input) {
        var valid = input.checkValidity();
        if (valid && input.type === "text" && input.required) { valid = input.value.trim().length > 0; }
        if (valid && input === photos) { valid = photosValid(); }
        setFieldState(input, valid);
        return valid;
    }

    form.querySelectorAll("input, select, textarea").forEach(function (input) {
        if (input.type === "checkbox" || input.name === "_gotcha") { return; }
        input.addEventListener("blur", function () {
            if (input.value) { validateInput(input); }
        });
        input.addEventListener("change", function () {
            if (input.closest(".field.invalid")) { validateInput(input); }
        });
    });

    function validateForm() {
        var firstInvalid = null;
        form.querySelectorAll("input, select, textarea").forEach(function (input) {
            if (input.type === "checkbox" || input.name === "_gotcha") { return; }
            if (!validateInput(input) && !firstInvalid) { firstInvalid = input; }
        });
        if (firstInvalid) { firstInvalid.focus(); }
        return !firstInvalid;
    }

    function value(name) {
        var el = form.elements[name];
        return el ? String(el.value || "").trim() : "";
    }

    function buildPayload(requestId, includePhotos) {
        var data = new FormData(form);
        if (!includePhotos) { data.delete("photos"); }
        var isEmergency = emergency.checked;
        var place = [value("site_city"), value("site_state")].filter(Boolean).join(", ");
        var who = value("company_name") || value("contact_name");

        data.set("emergency", isEmergency ? "yes" : "no");
        data.set("priority", isEmergency ? "EMERGENCY" : "standard");
        data.set("request_id", requestId);
        data.set("submitted_at", new Date().toISOString());
        data.set("_subject", (isEmergency ? "[EMERGENCY] " : "") + "Service Request " + requestId + ": " + who + " (" + place + ")");
        data.set("_replyto", value("email"));

        var attr = window.stAttribution || {};
        var last = attr.last || {};
        ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid", "msclkid"].forEach(function (k) {
            if (last[k]) { data.set(k, last[k]); }
        });
        data.set("referrer", last.referrer || "");
        data.set("landing_page", last.landing_page || "");
        data.set("attribution_first", attr.first ? JSON.stringify(attr.first) : "");
        data.set("attribution_last", attr.last ? JSON.stringify(attr.last) : "");
        data.set("page_url", window.location.href);
        return data;
    }

    function send(data) {
        return fetch(config.formEndpoint, {
            method: "POST",
            body: data,
            headers: { "Accept": "application/json" }
        }).then(function (res) {
            if (!res.ok) { throw new Error("HTTP " + res.status); }
            return res;
        });
    }

    function mailtoFallback(requestId) {
        var lines = [
            "Reference: " + requestId,
            "Emergency: " + (emergency.checked ? "YES" : "no"),
            "Company: " + value("company_name"),
            "Contact: " + value("contact_name"),
            "Phone: " + value("phone"),
            "Email: " + value("email"),
            "Site: " + value("site_name"),
            "Address: " + [value("site_address"), value("site_city"), value("site_state"), value("site_zip")].filter(Boolean).join(", "),
            "Equipment: " + [value("equipment_type"), value("equipment_model")].filter(Boolean).join(" / "),
            "Preferred date: " + value("preferred_date"),
            "",
            "Description:",
            value("description")
        ];
        var subject = (emergency.checked ? "[EMERGENCY] " : "") + "Service Request " + requestId;
        return "mailto:" + SERVICE_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
    }

    function setBusy(busy) {
        submitBtn.disabled = busy;
        submitBtn.querySelector("span").textContent = busy ? "Submitting..." : "Submit Service Request";
    }

    function showConfirmation(requestId, photosDropped) {
        form.hidden = true;
        var box = document.getElementById("confirmation");
        document.getElementById("refNumber").textContent = requestId;
        document.getElementById("confirmEmail").textContent = value("email");
        document.getElementById("photoNote").hidden = !photosDropped;
        document.getElementById("confirmEmergency").hidden = !emergency.checked;
        box.hidden = false;
        box.focus();
        box.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    var requestId = null;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        errorBox.classList.remove("show");
        if (!validateForm()) { return; }
        if (value("_gotcha")) { return; }

        // Reuse the same reference on retries so the office can de-duplicate.
        requestId = requestId || newRequestId();
        var hasPhotos = photos.files && photos.files.length > 0;
        setBusy(true);

        send(buildPayload(requestId, true))
            .then(function () { return false; })
            .catch(function (err) {
                // An upload problem must not lose the request: retry once without photos.
                if (!hasPhotos) { throw err; }
                var data = buildPayload(requestId, false);
                data.set("photos_not_uploaded", String(photos.files.length));
                return send(data).then(function () { return true; });
            })
            .then(function (photosDropped) {
                track("generate_lead", {
                    form_name: "service_request",
                    emergency: emergency.checked ? "yes" : "no",
                    site_state: value("site_state"),
                    lead_source: value("lead_source") || "unspecified"
                });
                showConfirmation(requestId, photosDropped);
            })
            .catch(function () {
                document.getElementById("mailFallback").href = mailtoFallback(requestId);
                errorBox.classList.add("show");
                track("form_error", { form_name: "service_request" });
                setBusy(false);
            });
    });
})();
