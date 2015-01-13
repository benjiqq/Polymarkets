<script type="text/javascript">

//Width and height
var w = 510;
var h = 330;
var radius = 10;

var dataset = [];
for (var i = 0; i < 10; i++) { 
    var a = Math.random() * w -20;
    var b = Math.random() * h -20;
    var el = [a,b];
    dataset = dataset.concat([el]); //Add new number to array

}



//Create SVG element
var svg = d3.select("body")
            .append("svg")
            .attr("width", w)
            .attr("height", h);


svg.selectAll("circle")
   .data(dataset)
   .enter()
   .append("circle")
.attr("cx", function(d) {
        return d[0];
   })
   .attr("cy", function(d) {
        return d[1];
   })
   .attr("r", radius);



var main = svg.append("rect").attr("width",100).attr("height",100).attr("x",100).attr("y",100).attr("fill","grey").attr("fill-opacity",0.3);

var mousedown = false;
var downxy;

   svg.on('mousemove', move) 
      .on('mousedown', clicked) 
      .on("mouseup", up);

function up(){
  

  //alert(x1 + " > " + x2); 
  mousedown = false;
}

function clicked(){
  //alert("click: " + d3.mouse(this)[0]); 
  downxy = d3.mouse(this);
  mousedown = true;
}

function move(){
  if (mousedown){
    var m = d3.mouse(this);
    //d3.select('body').append('p').text(m[0] + ":" + m[1]);
   // main.attr("x",m[0]);

   var x2 = d3.mouse(this)[0];
  var x1 = downxy[0];
  var y2 = d3.mouse(this)[1];
  var y1 = downxy[1];

  var minx = x2;
  var maxx = x1;
  if (x1 < x2){
    minx = x1;
    maxx = x2;
  }else{
    minx = x2;
    maxx = x1;
  }

  var miny = y2;
  var maxy = y1;
  if (y1 < y2){
    miny = y1;
    maxy = y2;
  }else{
    miny = y2;
    maxy = y1;
  }
  
  main.attr("width",maxx-minx);
  main.attr("x",minx);
  main.attr("y",miny);
  main.attr("height",maxy-miny);

  var circles = svg.selectAll("circle");

  circles.attr("fill","black");
  var odds = circles.select(function(d, i) { 
    var hit = d[0] > minx && d[0] < maxx && d[1] > miny && d[1]<maxy;
    return hit ? this : null; }
  );

  odds.attr("fill","red");

  svg.selectAll("circle").attr("fill", function(d) {
    d3.select('body').append('p').text(p.x);
      return minx <= dataset[p.x] && dataset[p.x] <= maxx
          && miny <= d[p.y] && d[p.y] <= maxy
          ? "red" : "blue";
    });
}
}





</script>