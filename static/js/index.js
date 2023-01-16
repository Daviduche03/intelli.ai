var btn_menu = document.querySelector('#menu');
var body = document.querySelector('body');
// to store the corresponding effect
var effect;

// adding a click event to all the buttons

btn_menu.addEventListener('click', addClass)



function addClass(e) {
  // to get the correct effect
  effect = e.target.getAttribute('data-effect');
  // adding the effects
  body.classList.toggle(effect);
  body.classList.toggle('st-menu-open');
  
  //console.log(e.target.getAttribute('data-effect'));
}

var select = document.querySelector('#select').value;

window.addEventListener('click', ()=>{
  console.log(select)
})