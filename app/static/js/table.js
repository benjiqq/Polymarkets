var stocklist = []
var rectable
var chartContainer = null

var selectrow = -1

$(document).ready(function(){

    /*var svgc = d3.select("body").append("svg").attr("width", 50).attr("height", 50)
    svgc.style('position','absolute').style('left','50px').style('top','40px')
    var c = svgc.append("circle").attr("cx", 25).attr("cy", 25).attr("r", 25).style("fill", "purple");
    c.on('click',function(){

            var t = d3.selectAll(".chart").select("h1").text()
            //var s= "" + rectable.getRow(1).getContent()
    })*/


    var stock = $('#stock').html()

    var url = "/stocklist/";
    $.getJSON( url)
    .done(function( data ) {
      if (data == "error"){
        return
      }
      else if (data.length > 0){
         data.forEach(function(d) {
          stocklist.push(d)
        });
      }
      addWidgetTable(stocklist, function(){
        rectable.set('caption', stocklist.length + " stocks")
      })

    })
    .fail(function( jqxhr, textStatus, error ) {
      var err = textStatus + ', ' + error;
      console.log( "Request Failed: " + err);
    });



  //makePlot(stock)




    $('#searchbox_stock').on('input', function() {
      var val =$('#searchbox_stock').val();

      var sli = []
      if (val.length > 0 ){
        stocklist.forEach(function(el, i, arr){
          if (el['stock'].indexOf(val) == 0){
            sli.push({'stock':el['stock'],'4wk change':el['roc4'],'26wk change':el['roc26']})
          }
        })

      }
      else {
        stocklist.forEach(function(el, i, arr){
           sli.push({'stock':el['stock'],'4wk change':el['roc4'],'26wk change':el['roc26']})

        })

      }

        rectable.data.reset(sli)

        rectable.set('caption', sli.length + " stocks")

     })

})

var addWidgetTable = function(stocklist, callb){
  var id = "_table1"
  //"table_log"
  var gstr = '<div id="overlay' + id + '">'
  gstr += '<span></span>' /*<h1 id="headline' + id + '"></h1>'*/
  gstr += '<span id="log' + id + '"></span>'
  gstr += '</div>'

  $('body').append(gstr)

  YUI().use('overlay', /*'resize-plugin', 'dd-plugin',*/ 'datatable', 'datatable-scroll', 'gallery-datatable-selection',


    function(Y) {

    tableWidget = new Y.Overlay({
      width: 170 + "px",
      height: 670 + "px",
      srcNode: "#overlay" + id,
      visible: true,
      zIndex:5,
      xy: [20,80],
      align: {node:".example", points:["tc", "bc"]},

    });

    //Y.MyModule.sayHello();


    //overlay.plug(Y.Plugin.Resize);
    tableWidget.plug(Y.Plugin.Drag);

    tableWidget.render()


    // Columns must match data object property names
    var data = [
     /* {'stock':'AAPL','4wk change':100},*/
    ];

    stocklist.forEach(function(el, i, arr){
      data.push({'stock':el['stock'],'4wk change':el['roc4'],'26wk change':el['roc26']})
    })

    rectable = new Y.DataTable({
      columns: ["stock", "4wk change", "26wk change"],
      width: "170px",
      height: "670px",
      data: data,
      caption: "stocks",
      scrollable: "y",

      highlightMode: 'cell',
        selectionMode: 'row',
        selectionMulti: true

      /*caption: "Data",*/
      /*summary: "...",*/

    });



    rectable.after('render', callb);


    //handle click
    Y.delegate('click', function(e) {
        var target = e.currentTarget,
            modelList = this.get('data'),
            rows = this.get('rows'),
            columns = this.get('columns'),
            cellIndex = Y.Node.getDOMNode(target).cellIndex,
            rid = target.get('id'),
            r1 = this.getRecord(rid);

          cellIndex = 0  //take the ticker independent of the column clicked
          var selectedColumn = columns[cellIndex].key;
          var selectedCell = r1.get(selectedColumn);

          var selected_value = r1.get(selectedColumn)

          selectrow = e.index
          makePlot(selected_value)



    }, "#overlay" + id, 'td', rectable);






   rectable.render("#log" +id);



  });
}


function plotPrice(data, svgContainer, coords){
  var width = coords[0],
      height = coords[1]
      margin  = coords[2]

  var line = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.close); });

  var svg = svgContainer
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

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

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.close; }));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("class","y axis text")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Price ($)");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

}

function plotVolume(data, svglowContainer, coords) {


  var width = coords[0],
      height = coords[1]
      margin  = coords[2]

var svg = svglowContainer.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


 var barwidth = width/(data.length)

  var x = d3.time.scale()
      .range([0, width]);

    x.domain(d3.extent(data, function(d) {
      return d.date;
    }));


   var y = d3.scale.linear()
   .range([height,0]);

    y.domain(d3.extent(data, function(d) {
      return d.volume;
    }));



  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(6)


    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Volume M");



  svg.selectAll("rect")
     .data(data)
   .enter().append("rect")
     .attr("x", function(d) {
       return x(d.date) })
  .attr("y", function(d, i) {
    return y(d.volume);
  })
  .attr("width", barwidth)
  .attr("height", function(d){
    return height - y(d.volume);
  });

}


function plotROC(data, svglowContainer, coords) {
  var width = coords[0],
      height = coords[1]
      margin  = coords[2]

var svg = svglowContainer.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


 var barwidth = width/(data.length)

  var x = d3.time.scale()
      .range([0, width]);

    x.domain(d3.extent(data, function(d) {
      return d.date;
    }));


   var y = d3.scale.linear()
   .range([height,0]);

    y.domain(d3.extent(data, function(d) {
      return d.roc;
    }));



  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(6)


    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("roc %");

      svg.selectAll("rect")
         .data(data)
       .enter().append("rect")
          .attr("class", function(d) { return d.roc < 0 ? "bar negative" : "bar positive"; })
         .attr("x", function(d) {
           return x(d.date) })
      .attr("y", function(d, i) {
        //positive values have smaller offset
        return y(Math.max(0, d.roc));
      })
      .attr("width", barwidth)
      .attr("height", function(d){
        return Math.abs(y(d.roc) - y(0));
      });

}

function drawBox(svgContainer) {

  var w = svgContainer.attr('width')
  var h = svgContainer.attr('height')

  var boxcolor = d3.rgb(0,0,0);

  offsetx = 0

  var borderwidth = 2

  var left = svgContainer.append("rect").attr("width", borderwidth).attr("height", h)
  .attr("x", 0).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 1.0)
  .attr("class","border")

  var right = svgContainer.append("rect").attr("width", borderwidth).attr("height", h)
  .attr("x",  (w-borderwidth)).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 1.0)
    .attr("class","border")

  var top = svgContainer.append("rect").attr("width", w).attr("height", borderwidth)
  .attr("x", 0).attr("y", 0).attr("fill", boxcolor).attr("fill-opacity", 1.0)
    .attr("class","border")

  var down = svgContainer.append("rect").attr("width", w).attr("height", borderwidth)
  .attr("x", 0).attr("y", (h - borderwidth)).attr("fill", boxcolor).attr("fill-opacity", 1.0)
    .attr("class","border")

}



function makePlot(stock){

   var coords = {}

  var topwidth = 960
  var topheight = 450

  var margin = {top: 15, right: 8, bottom: 30, left: 50},
      width = topwidth - margin.left - margin.right,
      height = topheight - margin.top - margin.bottom;

  var svgContainer
  var chartContainer

  //if container there remove it
  if (chartContainer !== null){
    chartContainer = d3.select("body").select(".chart")

    d3.selectAll("chartContainer").select("h1").text(stock)

    svgContainer = chartContainer.selectAll("svg")
    svgContainer.remove()
    chartContainer.remove()

  }


    chartContainer = d3.select("body").append("div").attr("class","chart")
    chartContainer.append("h1").text(stock)

   svgContainer = chartContainer.append("svg")
      .attr("class","chart_price")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)

  $('#stock').remove()

  coords['pricechart'] = [width, height, margin]



  drawBox(svgContainer, width, height)


     var margin = {top: 10, right: 8, bottom: 10, left: 50},
      width = 960 - margin.left - margin.right,
      height = 200 - margin.top - margin.bottom;

  coords['volumechart'] = [width, height, margin]

  var svglowContainer = chartContainer.append("svg")
/*      .attr("class","chart_volume")*/
      .attr("class","chart_roc")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)


  drawBox(svglowContainer, width, height)

       var margin = {top: 10, right: 8, bottom: 10, left: 50};
  var svglowContainer2 = chartContainer.append("svg")
      .attr("class","chart_volume")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)


  drawBox(svglowContainer2, width, height)


    var url = "/stock/" + stock + "/closes/";
    $.getJSON( url)
    .done(function( data ) {

      if (data == "error"){
        $('#stock').html("stock does not exist")
        return
      }

      else if (data.length > 0){
          var parseDate = d3.time.format("%Y-%m-%d").parse;

         data.forEach(function(d) {
          d.date = parseDate(d.date);
          d.close = +d.close;
        });

        plotPrice(data, svgContainer, coords['pricechart'])
      }
    })

    .fail(function( jqxhr, textStatus, error ) {
      var err = textStatus + ', ' + error;
      console.log( "Request Failed: " + err);

    });



    var url = "/stock/" + stock + "/volume/";
    $.getJSON( url)
    .done(function( data ) {

      if (data == "error"){
        $('#stock').html("stock does not exist")
        return
      }

      else if (data.length > 0){
          var parseDate = d3.time.format("%Y-%m-%d").parse;

         data.forEach(function(d) {
          d.date = parseDate(d.date);
          d.volume = d.volume;
        });

        plotVolume(data, svglowContainer2, coords['volumechart'])
      }
    })

    .fail(function( jqxhr, textStatus, error ) {
      var err = textStatus + ', ' + error;
      console.log( "Request Failed: " + err);

    });


  var url = "/stock/" + stock + "/roc/";
    $.getJSON( url)
    .done(function( data ) {

      if (data == "error"){
        $('#stock').html("stock does not exist")
        return
      }

      else if (data.length > 0){
          var parseDate = d3.time.format("%Y-%m-%d").parse;

         data.forEach(function(d) {
          d.date = parseDate(d.date);
          d.roc = d.roc;
        });

        plotROC(data, svglowContainer, coords['volumechart'])
      }
    })

    .fail(function( jqxhr, textStatus, error ) {
      var err = textStatus + ', ' + error;
      console.log( "Request Failed: " + err);

    });

}

