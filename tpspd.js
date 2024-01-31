console.log("Top Speed JS")
const RHO = 1.3,    // Air Density
  kW2W = 1000,
  ms2kmh = 3.6,
  speed_decimal_places = 2;

var inp_power = document.querySelector("#tpspd_power"),
  inp_cda = document.querySelector("#tpspd_cda"),
  inp_tpspd = document.querySelector("#tpspd_topspeed"),
  out_plot = document.querySelector("#tpspd_plot");

inp_power.addEventListener("input", e => {
  inp_update();
})

inp_cda.addEventListener("input", e => {
  inp_update();
})

function inp_update() {
  var tpspd = calc_topspeed(inp_cda.value, inp_power.value);
  inp_tpspd.value = tpspd.toFixed(speed_decimal_places);

  plotly_graph();
}

/*
  Top Speed = (power/(1/2*cda*rho))^(1/3)
    power [W]
    cda [m^2]
    rho [kg/m^3]
    top speed [m/s
*/
function calc_topspeed(cda, power) {
  return ms2kmh*Math.cbrt(power*kW2W/(0.5*cda*RHO));
}

/*
  Creates and displays a Plotly graph based on input data.
*/
function plotly_graph() {
  var cda_m2 = inp_cda.value,
    pwr_kw = inp_power.value,
    mass_kg = 200,
//     api_host = "http://localhost:8123",   // Testing
    api_host = "https://us-central1-axial-camp-412420.cloudfunctions.net",  // Production
    data_url = `${api_host}/accel-sol?power_kw=${pwr_kw}&mass_kg=${mass_kg}&cda_m2=${cda_m2}`;
  // TODO: Don't hardcode URL, and use authentication

  fetch(data_url)
    .then((response) => response.json())
    .then((json) => {
      console.log(json)
      var speed_trace = {
        x: json["time_s"],
        y: json["velocity_ms"].map(v => v*ms2kmh),
        mode: 'lines+markers',
        type: 'scatter'
      };

      var data = [speed_trace],
        layout = {
          title: {text: "Acceleration Plot"},
          xaxis: {title: {text: "Time [s]"}},
          yaxis: {title: {text: "Speed [km/h]"}},
        };

      Plotly.newPlot('tpspd_plot', data, layout);
    })
    .catch((error) => {
      console.error(error)
      console.error(data_url)
    });


}

