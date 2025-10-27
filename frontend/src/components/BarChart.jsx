// components/BarChart.js
import React from "react";
import Chart from "react-apexcharts";

export default function BarChart({
  // Basic props
  title,
  categories,
  series,
  height = 350,
  width = "100%",

  // Chart configuration
  type = "bar",
  stacked = false,
  stackType = "normal",

  // Styling
  colors = ["#1E90FF"],
  background = "#ffffff",
  foreColor = "#373d3f",

  // Chart behavior
  animationsEnabled = true,
  toolbar = {
    show: true,
    tools: {
      download: true,
      selection: true,
      zoom: true,
      zoomin: true,
      zoomout: true,
      pan: true,
      reset: true,
    },
  },
  zoom = {
    enabled: true,
  },

  // Plot options
  plotOptions = {
    bar: {
      horizontal: false,
      columnWidth: "55%",
      endingShape: "rounded",
    },
  },

  // Data labels
  dataLabels = {
    enabled: false,
  },

  // Stroke
  stroke = {
    show: true,
    width: 2,
    colors: ["transparent"],
  },

  // Axes
  xaxis = {
    categories: categories,
    title: {
      text: "Category",
    },
  },
  yaxis = {
    title: {
      text: "Values",
    },
  },

  // Fill
  fill = {
    opacity: 1,
    type: "solid",
  },

  // Tooltip
  tooltip = {
    y: {
      formatter: (val) => val.toString(),
    },
  },

  // Legend
  legend = {
    show: true,
    position: "top",
    horizontalAlign: "center",
  },

  // Grid
  grid = {
    show: true,
    borderColor: "#e7e7e7",
    strokeDashArray: 0,
    position: "back",
  },

  // Responsive
  responsive = [],

  // Additional options
  ...restOptions
}) {
  const options = {
    chart: {
      type: type,
      height: height,
      width: width,
      background: background,
      foreColor: foreColor,
      stacked: stacked,
      stackType: stackType,
      animations: {
        enabled: animationsEnabled,
      },
      toolbar: toolbar,
      zoom: zoom,
      ...restOptions.chart,
    },
    plotOptions: plotOptions,
    dataLabels: dataLabels,
    stroke: stroke,
    xaxis: {
      ...xaxis,
      categories: categories || xaxis.categories,
    },
    yaxis: yaxis,
    colors: colors,
    fill: fill,
    tooltip: tooltip,
    title: {
      text: title,
      align: "center",
      margin: 10,
      style: {
        fontSize: "16px",
        fontWeight: "bold",
        color: foreColor,
      },
      ...restOptions.title,
    },
    legend: legend,
    grid: grid,
    responsive: responsive,
    ...restOptions,
  };

  return (
    <Chart
      options={options}
      series={series}
      type={type}
      height={height}
      width={width}
    />
  );
}
