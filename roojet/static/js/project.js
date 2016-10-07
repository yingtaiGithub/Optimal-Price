/* Project specific Javascript goes here. */

Chart.defaults.Line = {
    responsive: true,
    scaleFontSize: 14,
    scaleFontColor: "#363636",
    pointDot: true,
    pointDotRadius: 4,
    pointDotStrokeWidth: 1,
    pointHitDetectionRadius: 20,
    scaleGridLineColor: "rgba(54,54,54,.05)",
    scaleGridLineWidth: 1,
    scaleShowGridLines: true,
    scaleShowHorizontalLines: true,
    scaleShowVerticalLines: true,
    bezierCurve: true,
    bezierCurveTension: 0.4,
    datasetFill: true,
    datasetStroke: true,
    datasetStrokeWidth: 2
}
function SelectAll(id)
{   
    document.getElementById(id).focus();
    document.getElementById(id).select();
}
