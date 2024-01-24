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

  TODO: Currently its a nonsense graph!
*/
function plotly_graph() {
  var cda = inp_cda.value,
    pwr = inp_power.value;
  var trace3 = {
    x: [0, 1, 2, 3, 4].map(x => pwr/100*x),
    y: [0, 12, 9, 15, 12].map(x => cda*x),
    mode: 'lines+markers',
    type: 'scatter'
  };

  var data = [trace3];

  Plotly.newPlot('tpspd_plot', data);
}

