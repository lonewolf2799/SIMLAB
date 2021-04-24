let container = document.getElementById('main');

let text = new Blotter.Text("SIMLAB", {
  family: 'Montserrat',
  size: 100,
  fill: "#fff",
  paddingLeft: 80,
  paddingRight: 80,
  paddingTop: 80,
  paddingBottom: 80,
})

var material = new Blotter.ChannelSplitMaterial();
material.uniforms.uOffset.value = 0.05;
material.uniforms.uRotation.value = 50;
material.uniforms.uApplyBlur.value = 1; // 0 false, 1 true
material.uniforms.uAnimateNoise.value = .3;


var blotter = new Blotter(material, {
  texts: text
})

var scope = blotter.forText(text);

scope.appendTo(container);
scope.context.canvas.style.position = 'absolute'
scope.context.canvas.style.left = '50%';
scope.context.canvas.style.top = '50%';
scope.context.canvas.style.transform = 'translate(-50%, -50%)'
let yOff = scope.context.canvas.offsetHeight;

document.onmousemove = moveIt;
function moveIt(event) {
  material.uniforms.uRotation.value = (event.clientX * .01);
  material.uniforms.uOffset.value = (event.clientX * .0001);

}



var tl = new TimelineMax({paused:true});
var dur = 20;

$(document).ready( function(){
  
  tl.to( scope.context.canvas , dur , {rotation: 360} )
  

});

$(window).scroll( function(){
  var scrollTop = $(window).scrollTop();
  var docHeight = $(document).height();
  var winHeight = $(window).height();
  if( scrollTop >= 0){
      tl.progress( scrollTop / ( docHeight - winHeight ) );
  }
}
);








