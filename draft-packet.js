window.onload = function(){
  var dpTable = document.getElementById('table-container1');
  var modal = document.getElementById('summary-modal-container')
  var windowWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
  var windowHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
  var tableHeight = dpTable.offsetHeight;
  var tableWidth = dpTable.offsetWidth;
  modal.style.maxHeight = tableHeight.toString() + 'px';
  modal.style.maxWidth = (windowWidth - tableWidth - 1).toString() + 'px';

  function fillSummary(category,content,amount){
    category = category.split(' ')[0];
    var selector = 'summary-' + category;
    var old = document.getElementById('modal' + category);
    if (document.contains(old)) {
      old.remove();
    }
    var para = document.createElement("P");
    para.id = 'modal' + category;
    if (content == '') {
      content = '---'
    }
    if (category == 'ping') {
      para.textContent = 'C:' + content + 'ms';
    }
    else if (category == 'col-10') {
      para.textContent = 'O:' + content + 'ms';
    }
    else {
      para.textContent = content;
    }
    document.getElementById(selector).appendChild(para);
  };

  function summaryPopUp() {
    var parentRow = this.parentNode;
    var cells = [];
    cells.push(parentRow.querySelector('.tagpro-username'));
    cells.push(parentRow.querySelector('.reddit-name'));
    cells.push(parentRow.querySelector('.rating'));
    cells.push(parentRow.querySelector('.position'));
    cells.push(parentRow.querySelector('.microphone'));
    cells.push(parentRow.querySelector('.location'));
    cells.push(parentRow.querySelector('.ping'));
    cells.push(parentRow.querySelector('.col-10'));
    cells.push(parentRow.querySelector('.availability'));
    cells.push(parentRow.querySelector('.extra-information'));
    cells.push(parentRow.querySelector('.comment'));

    var summarylen = cells.length;
    for (var i = 0; i < summarylen; i++) {
      fillSummary(cells[i].getAttribute('class'),cells[i].textContent,summarylen);
    };
    modal.style.visibility = 'visible';
  };
  var nameCells = document.querySelectorAll('td.tagpro-username');
  var len = nameCells.length;
  for (var i = 0; i < len; i++) {
    nameCells[i].onclick = summaryPopUp;
  };

  var parent = document.getElementById('table-container1');
  var child = document.getElementById('table-container2');
  var scrollbarWidth = (child.offsetWidth - child.clientWidth).toString() + "px";
  child.style.paddingRight = scrollbarWidth

};
