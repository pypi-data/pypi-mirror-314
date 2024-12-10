"use strict";
function copyToClipboard(text) {
    const selection = document.getSelection();
    const el = document.createElement("textarea");
    el.value = text;
    document.body.appendChild(el);
    const selected = selection.rangeCount > 0 ? selection.getRangeAt(0) : false;
    el.select();
    document.execCommand("copy");
    el.remove();
    if (selected) {
        selection.removeAllRanges();
        selection.addRange(selected);
    }
}
function copyHeaders(headers) {
    copyToClipboard(headers.join("\t"));
}
