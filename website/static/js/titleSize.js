var input = document.querySelector('#title');
input.addEventListener('input', resizeInput);
resizeInput.call(input);

function resizeInput() {
  this.style.width = this.value.length + "ch";
}
