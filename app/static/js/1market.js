/*
//timing
*/

var rectable

$(document).ready(function(){
  addToolBar()
})

function ajaxServertime(){

  var jqxhr = $.ajax( "/servertime/" )
  .done(function(data) {  })
  .fail(function(jqXHR, textStatus) { alert("request failed " + jqXHR); })
  .always(function() {  });
}

var tableWidget
var svgWidget
var chartWidget
var wid = 0

function plotTS(id, data, widgetx, widgety){
  var margin = {top: 20, right: 0, bottom: 70, left: 40},
      width = 440 - margin.left - margin.right,
      height = 320 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y-%m-%d").parse;

  var x = d3.time.scale()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var line = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.close); });


  addWidgetChart(widgetx,widgety,id, function(){


/*  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  */
    var svg = d3.select('#graph' + id)

    data.forEach(function(d) {
      d.date = parseDate(d.date);
      d.close = +d.close;
    });

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.close; }));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + margin.left + "," + (height+20) + ")")
        .call(xAxis);


    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Price ($)");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .attr("d", line);
  })

}

var addWidgetChart = function(x,y,id, callback){

  var widget_width = 440
  var widget_height = 320
  var head_offset = 20
  var tail_offset = 10
  var svg_width = widget_width
  var svg_height = widget_height - head_offset - tail_offset

  var gstr = '<div id="overlay' + id + '">'
  gstr += '<div><h1 id="headline' + id + '">'
  gstr += '</h1><svg id="graph' + id + '" style="margin-top:2px"'
  gstr += ' width="' + svg_width + '"'
  gstr += ' height="' + svg_height + '"'
  gstr += '></svg>'
  gstr += '</div></div>';

  $('body').append(gstr)

  YUI().use('overlay', 'resize-plugin', 'dd-plugin',function(Y) {
    console.log("yui called")


    chartWidget = new Y.Overlay({
      width: widget_width + "px",
      height: widget_height + "px",
      srcNode: "#overlay" + id,
      visible: true,
      zIndex:5,
      xy: [x,y],
      align: {node:".example", points:["tc", "bc"]},

    });
    chartWidget.plug(Y.Plugin.Drag);
    chartWidget.render()

    //overlay.plug(Y.Plugin.Resize);

    $('#headline' + id).html(id)

    chartWidget.after('render', callback);


/*

    var svg = d3.select('#graph' + id)

    //return svg

    drawBox(svg, svg_width,svg_height,0,0)


    */
  })
}

var addWidgetTable = function(callb){
  var id = "z1"
  //"table_log"
  var gstr = '<div id="overlay' + id + '">'
  gstr += '<div><h1 id="headline' + id + '"></h1>'
  gstr += '<div id="log' + id + '"></div>'
  gstr += '</div></div>'

  $('body').append(gstr)

  YUI().use('overlay', 'resize-plugin', 'dd-plugin','datatable', 'datatable-scroll', function(Y) {

    tableWidget = new Y.Overlay({
      width: 300 + "px",
      height: 470 + "px",
      srcNode: "#overlay" + id,
      visible: false,
      zIndex:5,
      xy: [900,80],
      align: {node:".example", points:["tc", "bc"]},

    });


    //overlay.plug(Y.Plugin.Resize);
    tableWidget.plug(Y.Plugin.Drag);


    $('#headline' + id).html(" data log")
//    tableWidget.set('visible', true);

    tableWidget.render()


    // Columns must match data object property names
    var data = [

    ];

    rectable = new Y.DataTable({
      columns: ["stock", "52whigh"],
      width: "300px",
      height: "400px",
      data: data,

      scrollable: "y",


      /*caption: "Data",*/
      /*summary: "...",*/

    });

    /*rectable.on('click',function(oArgs) {
      alert("click" + oArgs.currentTarge)

    })*/

    rectable.after('render', callb);

    Y.delegate('click', function(e) {
        var target = e.currentTarget,
            modelList = this.get('data'),
            columns = this.get('columns'),
            cellIndex = Y.Node.getDOMNode(target).cellIndex,
            rid = target.get('id'),
            r1 = this.getRecord(rid);

          var selectedColumn = columns[cellIndex].key;
           var selectedCell = r1.get(selectedColumn);

          var selected_value = r1.get(selectedColumn)

          makePlot(selected_value)
          wid +=1





    }, "#overlay" + id, 'td', rectable);


    rectable.render("#log" +id);

  });
}


function drawBox(svgContainer, w, h, offsetx, offsety) {

  // borders of the svg box
  var boxcolor = d3.rgb(80,80,80);

  offsetx = 0

  var left = svgContainer.append("rect").attr("width", 1).attr("height", h)
  .attr("x", offsetx + 0).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 1.0);

  var right = svgContainer.append("rect").attr("width", 1).attr("height", h)
  .attr("x", offsetx + (w-1)).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 1.0);

  var top = svgContainer.append("rect").attr("width", w).attr("height", 1)
  .attr("x", offsetx + 0).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 1.0);

  var down = svgContainer.append("rect").attr("width", w).attr("height", 1)
  .attr("x", offsetx + 0).attr("y", (h - 1)).attr("fill", boxcolor).attr("fill-opacity", 1.0);


  //selection box
  var box = svgContainer.append("rect") //.attr("class","brush")
  .attr("width", w).attr("height", h)
  .attr("x", 0).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 0.00);

}

function plotData(graph, data){
  var svgw = graph.attr('width')
  var svgh = graph.attr('height')


  //top, left, low, right
  var m = [10, 10, 20, 70];
  var w = svgw - m[1] - m[3];
  var h = svgh - m[0] - m[2];


  var x = d3.scale.linear().domain([0, data.length]).range([0, w]);
  var y = d3.scale.linear().domain([d3.min(data),d3.max(data)]).range([h, 0]);

  var line = d3.svg.line()
  .x(function(d,i) {
    return x(i);
  })
  .y(function(d) {
    return y(d);
  })


  graph.selectAll('.graphline').remove()

  // Add an SVG element with the desired dimensions and margin.
  var graph = graph.append("svg:svg")
  .attr("width", w + m[1] + m[3])
  .attr("height", h + m[0] + m[2])
  .attr("class", "graphline")
  .append("svg:g")
  .attr("transform", "translate(" + m[3] + "," + m[0] + ")")


  // create yAxis
  var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
  // Add the x-axis.
  graph.append("svg:g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + h + ")")
  .call(xAxis);


  // create left yAxis
  var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
  // Add the y-axis to the left
  graph.append("svg:g")
  .attr("class", "y axis")
  .attr("transform", "translate(-25,0)")
  .call(yAxisLeft);

  // Add the line by appending an svg:path element with the data line we created above
  // do this AFTER the axes above so that the line is above the tick-lines
  graph.append("svg:path").attr("d", line(data));


}

var makePlot = function(stock, x, y){
  var url = "/stock/" + stock

  $.getJSON( url)
  .done(function( data ) {
    // var stock ="AAPL"
     var id = "chart" + stock
    if (x == null)
      x = 100
    if (y == null)
      y = 100
    plotTS(id, data, x, y)

  })

  .fail(function( jqxhr, textStatus, error ) {
    var err = textStatus + ', ' + error;
    console.log( "Request Failed: " + err);

  });
}

var addToolBar = function (){

YUI().use("node-focusmanager", function (Y) {

  //  Retrieve the Node instance representing the toolbar
  //  (<div id="toolbar">) and call the "plug" method
  //  passing in a reference to the Focus Manager Node Plugin.

  var toolbar = Y.one("#toolbar-1"),
      out     = Y.one("#out");

  toolbar.plug(Y.Plugin.NodeFocusManager, {

    descendants: "input",
    keys: { next: "down:39", // Right arrow
           previous: "down:37" },  //  Left arrow
    focusClass: "focus",
    circular: true

  });


  //  Set the ARIA "role" attribute of the Node instance representing the
  //  toolbar to "toolbar" to improve the semantics of the markup for
  //  users of screen readers.

  toolbar.set("role", "toolbar");


  //  Listen for the click event on each button via the use of the
  //  "delegate" method

  toolbar.delegate("click", function (event) {

    var actionButton = this.one("input").get("value")

    out.setHTML("You clicked " + actionButton);

    if (actionButton == "Add"){

      var stock = $('#textbox').val()

      makePlot(stock)
      wid  +=1

    }

    if (actionButton == "Eval"){

      var codeval = editor.getValue()
      alert("evaluating code " + codeval)
      eval(codeval)
      //addWidgetSvg(100,100,wid, codeval)
      //wid +=1
    }

    if (actionButton == "Stocklist"){

      var callb = function(){

        var url = "/stocklist/"

        $.getJSON( url)
        .done(function( data ) {

          var start = new Date().getTime();

          data = data.slice(1,100)

		  var alldata = []
		  data.forEach(function(item){
			  alldata.push({'stock':item,'52whigh':'234'})
		  })

          rectable.data.reset(alldata)

          //don't use add
          /*data.forEach(function(item){
            rectable.data.add({ 'stock': item,'52whigh': "2" });
          })*/

          tableWidget.set('visible', true);
          tableWidget.render()
          var end = new Date().getTime();
          var dif = end - start;
          alert("adding data took: " + dif)


        })

        .fail(function( jqxhr, textStatus, error ) {
          var err = textStatus + ', ' + error;
          console.log( "Request Failed: " + err);

        });

      }


      addWidgetTable(callb)

    }

  }, ".yui3-toolbar-button");

});

}
