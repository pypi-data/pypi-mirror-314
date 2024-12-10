/**
 * Usage Example:
 * TARGET_URL=http://localhost:8080 K6_VUS=20 K6_DURATION=1m k6 run k6_loadtest.js
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';

// Configuration from environment variables
const targetUrl = __ENV.TARGET_URL || 'http://localhost:8080';
const vus = parseInt(__ENV.K6_VUS || '1');
const duration = __ENV.K6_DURATION || '10m';

// Define K6 options
export let options = {
  vus: vus,
  duration: duration,
};

// Global variable to store the response (per VU context)
let storedGraphData = null;

// Load JSON and CSV payloads
const jsonPayloads = {
  emptyGraph: loadJSON('./small/empty_graph.json'),
  randomField: loadJSON('./small/random_field_example_vfg_v1.json'),
  insurance: loadJSON('./medium/insurance_vfg_v1.json'),
  sprinkler: loadJSON('./small/sprinkler_factor_graph_vfg.json'),
  gridWorld: loadJSON('./small/grid_world.json'),
  actionSelection: loadJSON('./payloads/action_selection.json'),
  inferSprinkler: loadJSON('./payloads/infer_sprinkler_wet_grass_simple.json'),
  sprinklerObservations: loadJSON('./payloads/sprinkler_observations_csv.json'),
};

const csvPayloads = ['./orders.csv', './mushrooms.csv'].map((file) => open(file));

// Headers
const jsonHeaders = { 'Content-Type': 'application/json' };
const csvHeaders = { 'Content-Type': 'application/csv' };

// Main Execution Function
export default function () {
  getGraphDataToStore();
  validateAndSetGraph();
  importCSV();
  postActionSelection();
  postInfer();
  postStoredGraphData();
}

// Scenario: GET /graph and store response
function getGraphDataToStore() {
  group('GET /graph and store response', () => {
    const response = http.get(`${targetUrl}/graph`, jsonHeaders);

    check(response, {
      'GET /graph status is 200': (r) => r.status === 200,
    });

    if (response.status === 200) {
      try {
        // Parse and store the response payload in a variable
        if(storedGraphData == null){
          storedGraphData = response.json();
          console.log(`Stored Graph Data: ${JSON.stringify(storedGraphData)}`);
        }
      } catch (e) {
        console.error(`Failed to parse response JSON: ${e.message}`);
      }
    }
  });
}

// Scenario: POST the stored graph data
function postStoredGraphData() {
  group('POST /graph with stored payload', () => {
    if (storedGraphData) {     
      const payload = JSON.stringify(storedGraphData); // Convert the stored data to JSON
      const response = postRequest('/graph', payload, jsonHeaders);

    } else {
      console.warn('No graph data available to send in POST request.');
    }
  });
}

// Scenario: Validate and Set Graph
function validateAndSetGraph() {
  Object.entries(jsonPayloads).forEach(([key, payload]) => {
    if (key === 'actionSelection' || key === 'inferSprinkler' || key === 'sprinklerObservations') {
      // Skip payloads not relevant for this scenario
      return;
    }
    group(`Handling JSON payload: ${key}`, () => {
      postRequest('/validate', wrapVFG(payload), jsonHeaders);
      postRequest('/graph', wrapVFG(payload), jsonHeaders);
    });
  });
}

// Scenario: Import CSV
function importCSV() {
  csvPayloads.forEach((csvPayload, index) => {
    group(`POST: Import CSV file ${index + 1}`, () => {
      postRequest('/import', csvPayload, csvHeaders);
    });
  });
}

// Scenario: Action Selection
function postActionSelection() {
  group('POST to /graph and /actionselection', () => {
    postRequest('/graph', wrapVFG(jsonPayloads.gridWorld), jsonHeaders);
    postRequest('/actionselection', jsonPayloads.actionSelection, jsonHeaders);
  });
}

// Scenario: Infer
function postInfer() {
  group('POST to /infer', () => {
    postRequest('/graph', wrapVFG(jsonPayloads.sprinkler), jsonHeaders);
    postRequest('/learn', jsonPayloads.sprinklerObservations, jsonHeaders);
    postRequest('/infer', jsonPayloads.inferSprinkler, jsonHeaders);
  });
}

// Utility functions
function loadJSON(filePath) {
  return JSON.stringify(JSON.parse(open(filePath)));
}

// Wrap VFG function to transform payloads
function wrapVFG(jsonData) {
  return JSON.stringify({ vfg: JSON.parse(jsonData) });
}

function postRequest(endpoint, payload, headers) {
  sleep(1);
  const response = http.post(`${targetUrl}${endpoint}`, payload, { headers });
  check(response, { [`POST ${endpoint} status is 200`]: (r) => r.status === 200 });

  if (response.status !== 200) {
    console.error(`POST ${endpoint} failed with status ${response.status}`);
    console.error(`Response body: ${response.body}`);
    console.error(`Response headers: ${JSON.stringify(response.headers)}`);
  }

  return response;
}