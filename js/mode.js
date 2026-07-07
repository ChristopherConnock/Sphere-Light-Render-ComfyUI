// Pure mode / visibility logic for the Sphere Light node. No DOM, no ComfyUI
// dependency, so it is unit-testable in plain Node (like solar.js / geo.js).

// Which source drives the sun in date/time mode. Returns the {location,lat,lng}
// triple to feed computeSunAngles, with the INACTIVE source blanked so exactly
// one drives — or null in manual mode (the caller uses the rotation/elevation
// sliders instead). Blanking lat/lng to 0/0 makes computeSunAngles treat coords
// as "unset"; blanking location makes it skip the city match.
export function pickSunSource({ sunMode, locationMode, location, lat, lng }) {
  if (sunMode !== "date/time") return null;
  if (locationMode === "coords") return { location: "", lat, lng };
  return { location, lat: 0, lng: 0 };
}

// Names of the TOGGLEABLE widgets that should be visible for the given modes.
// Excludes always-on widgets (sun_mode, intensity) and always-off ones
// (render_b64, plus the native `location`/`heading` widgets that the DOM widgets
// replace). "location_search" and "compass" are the DOM widgets' names.
export function visibleWidgets({ sunMode, locationMode }) {
  if (sunMode !== "date/time") return ["rotation", "elevation"];
  const base = ["location_mode", "year", "month", "day", "hour", "minute", "compass"];
  return locationMode === "coords"
    ? [...base, "latitude", "longitude"]
    : [...base, "location_search"];
}
