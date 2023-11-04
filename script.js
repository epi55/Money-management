const csvUrl = "C:\Users\malaf\OneDrive\Desktop\Workspace\Code\Projects\Money management\Website";

const layout = {
  title: "Money Management: Credit Cards, Edition 2023",
  xaxis: { title: "date" },
  yaxis: { title: "debit" }
};

Plotly.d3.csv(csvUrl, function (err, data) {
  if (err) {
    console.error(err);
  } else {
    const parseDate = d3.timeParse("%Y-%m-%d");
    data.forEach(function(d) {
      d.date = parseDate(d.date);
      d.debit = +d.debit;
    });

    const trace = {
      x: data.map((d) => d.date),
      y: data.map((d) => d.debit),
      type: "scatter",
      mode: "lines",
      name: "$$"
    };
    Plotly.newPlot("chart", [trace], layout);
  }
});