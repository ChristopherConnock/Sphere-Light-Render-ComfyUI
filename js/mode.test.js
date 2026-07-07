import { test } from "node:test";
import assert from "node:assert/strict";
import { pickSunSource, visibleWidgets } from "./mode.js";

test("pickSunSource: manual mode returns null", () => {
  assert.equal(
    pickSunSource({ sunMode: "manual", locationMode: "city", location: "Austin, TX", lat: 30, lng: -97 }),
    null
  );
});

test("pickSunSource: city mode blanks the coordinates", () => {
  assert.deepEqual(
    pickSunSource({ sunMode: "date/time", locationMode: "city", location: "Austin, TX", lat: 30.27, lng: -97.74 }),
    { location: "Austin, TX", lat: 0, lng: 0 }
  );
});

test("pickSunSource: coords mode blanks the city text", () => {
  assert.deepEqual(
    pickSunSource({ sunMode: "date/time", locationMode: "coords", location: "Austin, TX", lat: 30.27, lng: -97.74 }),
    { location: "", lat: 30.27, lng: -97.74 }
  );
});

test("visibleWidgets: manual shows only the angle sliders", () => {
  assert.deepEqual(visibleWidgets({ sunMode: "manual", locationMode: "city" }), ["rotation", "elevation"]);
});

test("visibleWidgets: date/time + city shows the search, not lat/lon or angles", () => {
  const v = visibleWidgets({ sunMode: "date/time", locationMode: "city" });
  assert.ok(v.includes("location_search"));
  assert.ok(v.includes("compass"));
  assert.ok(v.includes("location_mode"));
  assert.ok(!v.includes("latitude"));
  assert.ok(!v.includes("rotation"));
});

test("visibleWidgets: date/time + coords shows lat/lon, not the search", () => {
  const v = visibleWidgets({ sunMode: "date/time", locationMode: "coords" });
  assert.ok(v.includes("latitude"));
  assert.ok(v.includes("longitude"));
  assert.ok(!v.includes("location_search"));
});
