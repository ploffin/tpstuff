window.onload = function(){
  function fillSummary(category,content,amount){
    category = category.split(' ')[0];
    toFill = document.querySelectorAll('div.summary').length;
    if (toFill < amount) {
      var modal = document.getElementById('summary-modal');
      var newDiv = document.createElement("DIV");
      modal.appendChild(newDiv);
      newDiv.className = category + ' summary'
      newDiv.textContent = content;
    }
    else {
      var selector = '[class^=' + '\'' + category + '\'][class$=\'summary\']';
      console.log(selector);
      document.querySelector(selector).textContent = content;
    }
  };

  function summaryPopUp() {
    var parentRow = this.parentNode;
    var cells = [];
    cells.push(parentRow.querySelector('.col-2'));
    cells.push(parentRow.querySelector('.reddit'));
    cells.push(parentRow.querySelector('.position'));
    cells.push(parentRow.querySelector('.microphone'));
    cells.push(parentRow.querySelector('.ping'));
    cells.push(parentRow.querySelector('.col-11'));
    cells.push(parentRow.querySelector('.experience'));
    cells.push(parentRow.querySelector('.availability'));
    cells.push(parentRow.querySelector('.extra-information'));
    cells.push(parentRow.querySelector('.comment'));

    var summarylen = cells.length;
    for (var i = 0; i < summarylen; i++) {
      fillSummary(cells[i].getAttribute('class'),cells[i].textContent,summarylen);
    };
  };
  var nameCells = document.querySelectorAll('td.col-2');
  var len = nameCells.length;
  for (var i = 0; i < len; i++) {
    nameCells[i].onclick = summaryPopUp;
  };
};
