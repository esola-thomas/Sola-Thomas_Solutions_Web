/* Shared behavior: mobile nav, Team Login link, lead attribution, call tracking. */
(function () {
    "use strict";

    var config = window.ST_CONFIG || {};
    var ATTR_KEY = "st_attribution";
    var UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid", "msclkid"];

    function track(eventName, params) {
        if (typeof window.gtag === "function") {
            window.gtag("event", eventName, params || {});
        }
    }
    window.stTrack = track;

    function readStore() {
        try {
            return JSON.parse(window.localStorage.getItem(ATTR_KEY)) || null;
        } catch (e) {
            return null;
        }
    }

    function writeStore(value) {
        try {
            window.localStorage.setItem(ATTR_KEY, JSON.stringify(value));
        } catch (e) { /* storage blocked: attribution falls back to this page view */ }
    }

    // First touch is kept; last touch is replaced whenever a visit arrives with campaign params
    // or from an external referrer. Both travel with the service request.
    function captureAttribution() {
        var params = new URLSearchParams(window.location.search);
        var touch = {};
        UTM_KEYS.forEach(function (key) {
            var v = params.get(key);
            if (v) { touch[key] = v.slice(0, 200); }
        });
        var ref = document.referrer;
        var external = ref && ref.indexOf(window.location.host) === -1;
        var hasCampaign = Object.keys(touch).length > 0;

        var stored = readStore();
        if (!hasCampaign && !external && stored) { return stored; }

        touch.referrer = external ? ref.slice(0, 300) : "";
        touch.landing_page = window.location.pathname + window.location.search;
        touch.ts = new Date().toISOString();

        var next = { first: (stored && stored.first) || touch, last: touch };
        writeStore(next);
        return next;
    }
    window.stAttribution = captureAttribution();

    document.addEventListener("DOMContentLoaded", function () {
        var toggle = document.querySelector(".nav-toggle");
        var nav = document.getElementById("site-nav");
        if (toggle && nav) {
            toggle.addEventListener("click", function () {
                var open = nav.classList.toggle("open");
                toggle.setAttribute("aria-expanded", open ? "true" : "false");
            });
            nav.addEventListener("click", function (e) {
                if (e.target.tagName === "A") {
                    nav.classList.remove("open");
                    toggle.setAttribute("aria-expanded", "false");
                }
            });
        }

        if (config.teamLoginUrl) {
            document.querySelectorAll("[data-team-login]").forEach(function (el) {
                el.href = config.teamLoginUrl;
                el.hidden = false;
            });
        }

        document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
            a.addEventListener("click", function () {
                track("click_to_call", { link_location: a.getAttribute("data-cta") || "inline" });
            });
        });
        document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
            a.addEventListener("click", function () { track("click_email"); });
        });

        var year = document.querySelectorAll("[data-year]");
        year.forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
    });
})();
