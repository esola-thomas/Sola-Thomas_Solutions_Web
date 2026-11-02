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

    // This script is deferred and may run before or after site.js: read shared globals at call time.
    function config() { return window.ST_CONFIG || {}; }
    function track() {
        if (typeof window.stTrack === "function") { window.stTrack.apply(null, arguments); }
    }
    var REQUEST_TIMEOUT_MS = 30000;
    var REQUEST_TIMEOUT_WITH_PHOTOS_MS = 60000;
    var form = document.getElementById("serviceRequestForm");
    var submitBtn = document.getElementById("submitBtn");
    var errorBox = document.getElementById("formError");
    var summary = document.getElementById("errorSummary");
    var liveStatus = document.getElementById("submitStatus");
    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
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
        var cryptoApi = window.crypto || window.msCrypto;
        if (cryptoApi && cryptoApi.getRandomValues) {
            cryptoApi.getRandomValues(bytes);
        } else {
            for (var j = 0; j < bytes.length; j++) { bytes[j] = Math.floor(Math.random() * 256); }
        }
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

    function formatMb(bytes) { return (bytes / (1024 * 1024)).toFixed(1) + " MB"; }

    // Returns "" when the selection is fine, otherwise a specific message naming the problem.
    function photosProblem() {
        var files = photos.files ? Array.prototype.slice.call(photos.files) : [];
        var notImages = files.filter(function (f) { return !/^image\//.test(f.type); });
        if (notImages.length) {
            return notImages.map(function (f) { return f.name; }).join(", ") + (notImages.length > 1 ? " are not images." : " is not an image.");
        }
        if (files.length > MAX_PHOTOS) {
            return "You selected " + files.length + " photos. Attach up to " + MAX_PHOTOS + ".";
        }
        var total = files.reduce(function (sum, f) { return sum + f.size; }, 0);
        if (total > MAX_PHOTO_BYTES) {
            var biggest = files.slice().sort(function (x, y) { return y.size - x.size; })[0];
            return "The selected photos total " + formatMb(total) + "; the limit is 10 MB. Largest: " +
                biggest.name + " (" + formatMb(biggest.size) + ").";
        }
        return "";
    }

    // Phone: free text, but it must contain at least 10 digits.
    function phoneValid(input) {
        return input.value.replace(/\D/g, "").length >= 10 && /^[0-9()+.\-\s]+$/.test(input.value.trim());
    }

    // aria-describedby keeps any static hint id and adds the error id only while the field is invalid.
    function setFieldState(input, valid) {
        var field = input.closest(".field");
        if (!field) { return; }
        field.classList.toggle("invalid", !valid);
        input.setAttribute("aria-invalid", valid ? "false" : "true");
        var errorEl = document.getElementById(input.id + "-error");
        if (!errorEl) { return; }
        if (input.__baseDescribedBy === undefined) {
            input.__baseDescribedBy = (input.getAttribute("aria-describedby") || "").split(/\s+/).filter(function (id) {
                return id && id !== errorEl.id;
            });
        }
        var ids = input.__baseDescribedBy.slice();
        if (!valid) { ids.push(errorEl.id); }
        if (ids.length) { input.setAttribute("aria-describedby", ids.join(" ")); }
        else { input.removeAttribute("aria-describedby"); }
    }

    function validateInput(input) {
        var valid = input.checkValidity();
        if (valid && input.type === "text" && input.required) { valid = input.value.trim().length > 0; }
        if (valid && input.name === "phone") { valid = phoneValid(input); }
        if (input === photos) {
            var problem = photosProblem();
            valid = !problem;
            if (problem) { document.getElementById("photos-error").textContent = problem; }
        }
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

    function labelFor(input) {
        var label = form.querySelector('label[for="' + input.id + '"]');
        return label ? label.textContent.replace("*", "").trim() : input.name;
    }

    function validateForm() {
        var invalid = [];
        form.querySelectorAll("input, select, textarea").forEach(function (input) {
            if (input.type === "checkbox" || input.name === "_gotcha") { return; }
            if (!validateInput(input)) { invalid.push(input); }
        });
        if (invalid.length) {
            // role="alert" summary is announced; the first invalid field then takes focus.
            summary.textContent = (invalid.length === 1 ? "1 field needs attention: " : invalid.length + " fields need attention: ") +
                invalid.map(labelFor).join(", ") + ".";
            invalid[0].focus();
        } else {
            summary.textContent = "";
        }
        return invalid.length === 0;
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

    function send(data, timeoutMs) {
        var controller = typeof AbortController === "function" ? new AbortController() : null;
        var timer = controller ? setTimeout(function () { controller.abort(); }, timeoutMs) : null;
        var options = { method: "POST", body: data, headers: { "Accept": "application/json" } };
        if (controller) { options.signal = controller.signal; }
        return fetch(config().formEndpoint, options).then(function (res) {
            if (!res.ok) { throw new Error("HTTP " + res.status); }
            return res;
        }).then(function (res) {
            clearTimeout(timer);
            return res;
        }, function (err) {
            clearTimeout(timer);
            throw err;
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
        liveStatus.textContent = busy ? "Submitting your request." : "";
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
        box.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    }

    var requestId = null;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        errorBox.classList.remove("show");
        if (!validateForm()) { return; }
        requestId = requestId || newRequestId();
        if (value("_gotcha")) {
            // Likely browser autofill into the hidden field: do not send, but never fail silently.
            document.getElementById("mailFallback").href = mailtoFallback(requestId);
            errorBox.classList.add("show");
            errorBox.focus();
            return;
        }

        // The same reference is reused on retries so the office can de-duplicate.
        var hasPhotos = photos.files && photos.files.length > 0;
        setBusy(true);

        send(buildPayload(requestId, true), hasPhotos ? REQUEST_TIMEOUT_WITH_PHOTOS_MS : REQUEST_TIMEOUT_MS)
            .then(function () { return false; })
            .catch(function (err) {
                // An upload problem must not lose the request: retry once without photos.
                if (!hasPhotos) { throw err; }
                var data = buildPayload(requestId, false);
                data.set("photos_not_uploaded", String(photos.files.length));
                return send(data, REQUEST_TIMEOUT_MS).then(function () { return true; });
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
                errorBox.focus();
                track("form_error", { form_name: "service_request" });
                setBusy(false);
            });
    });
})();
