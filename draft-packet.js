window.onload = function(){
  var firstCells = document.querySelectorAll('td:first-child');
  function expandRow(){
      if(this.parentElement.className.match('tr-collapsed')) {
        this.parentElement.className = 'tr-expanded';
      }
      else {
        this.parentElement.className = 'tr-collapsed';
      }
  };
  for (i = 0, len = firstCells.length; i < len; i++) {
    firstCells[i].onclick = expandRow;
  }
};
