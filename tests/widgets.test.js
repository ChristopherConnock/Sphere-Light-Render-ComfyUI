import { test } from "node:test";
import assert from "node:assert/strict";
import { getVal, getStr } from "../js/widgets.js";

const node = (widgets) => ({ widgets });

test("getVal parses the named widget's value as a number", () => {
  assert.equal(getVal(node([{ name: "rotation", value: "12.5" }]), "rotation", 0), 12.5);
  assert.equal(getVal(node([{ name: "rotation", value: 90 }]), "rotation", 0), 90);
});

test("getVal falls back to the default when the widget is missing", () => {
  assert.equal(getVal(node([]), "rotation", 45), 45);
  assert.equal(getVal({}, "rotation", 45), 45);
});

test("getVal falls back to the default when the value isn't a finite number", () => {
  assert.equal(getVal(node([{ name: "rotation", value: "garbage" }]), "rotation", 45), 45);
  assert.equal(getVal(node([{ name: "rotation", value: "" }]), "rotation", 45), 45);
  assert.equal(getVal(node([{ name: "rotation", value: null }]), "rotation", 45), 45);
});

test("getStr returns the named widget's value as a string", () => {
  assert.equal(getStr(node([{ name: "city", value: "Austin, TX" }]), "city", ""), "Austin, TX");
  assert.equal(getStr(node([{ name: "city", value: 7 }]), "city", ""), "7");
});

test("getStr falls back to the default when the widget is missing", () => {
  assert.equal(getStr(node([]), "city", "London"), "London");
});
