function main() {
  var dpTable = document.getElementById('table-container-1');
  var modalContainer = document.getElementById('summary-modal-container-1');
  var wrapper = document.getElementById('wrapper')
  var wrapperWidth = wrapper.clientWidth;
  var wrapperHeight = wrapper.clientHeight;
  var tableDims = dpTable.getBoundingClientRect();
  var tableHeight = tableDims.height;
  var tableWidth = tableDims.width;
  if (window.screen.width > 900) {
    modalContainer.style.width = (wrapperWidth - tableWidth - 10).toString() + 'px';
    modalContainer.style.maxWidth = (wrapperWidth - tableWidth - 10).toString() + 'px';
  }
  else {
    modalContainer.style.width = tableWidth.toString() + 'px';
    modalContainer.style.maxWidth = tableWidth.toString() + 'px';
  }
  modalContainer.style.height = tableHeight.toString() + 'px';
  modalContainer.style.maxHeight = tableHeight.toString() + 'px';

  var wrapperDims = wrapper.getBoundingClientRect();
  dpTitle = document.getElementById('dptitle');
  dpTitle.style.width = wrapperDims.width + 'px';

  function noScrollBar(parentId,childId) {
    var parentElement = document.getElementById(parentId);
    var childElement = document.getElementById(childId);
    var scrollbarWidth = (childElement.offsetWidth - childElement.clientWidth).toString() + "px";
    childElement.style.paddingRight = scrollbarWidth
  }

  function createImageLink(category,url) {
    var link = document.createElement("A");
    var imgTag = document.createElement("IMG");
    link.href = url;
    imgTag.src = 'images/' + category + "-button.png";
    imgTag.alt = category;
    link.appendChild(imgTag);
    return link
  }

  function fillSummary(category,content){
    category = category.split(' ')[0];
    var containerSelector = 'summary-' + category;
    var currentId = 'modal-' + category
    var old = document.getElementById(currentId);
    if (document.contains(old)) {
      old.remove();
    }
    if (content == '') {
      content = '---'
    }
    var toAdd;
    switch(category) {
      case 'ping':
        toAdd = document.createElement("P");
        var newTextContent = 'C: ' + content + 'ms';
        toAdd.textContent = newTextContent;
        break;
      case 'col-10':
        toAdd = document.createElement("P");
        var newTextContent = 'O: ' + content + 'ms';
        toAdd.textContent = newTextContent;
        break;
      case 'reddit-name':
        toAdd = createImageLink(category,'https://www.reddit.com/user/'+content);
        break;
      case 'tp-profile':
        toAdd = createImageLink(category,'http://tagpro-chord.koalabeast.com/profile/'+content);
        break;
      default:
        toAdd = document.createElement("P");
        var newTextContent = content;
        toAdd.textContent = newTextContent;
        break;
    }
    toAdd.id = currentId 
    document.getElementById(containerSelector).appendChild(toAdd);
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
    cells.push(parentRow.querySelector('.tp-profile'));

    var summarylen = cells.length;
    for (var i = 0; i < summarylen; i++) {
      fillSummary(cells[i].getAttribute('class'),cells[i].textContent);
    };

    var closeButton = document.querySelector('.close-button');
    var modalInnerContainer = document.getElementById('summary-modal-container-2');
    closeButton.onclick = function() {
      modalContainer.style.visibility = 'hidden';
    };

    noScrollBar('summary-modal-container-2','summary-modal')
    modalContainer.style.visibility = 'visible';

    if (window.screen.width < 900) {
      var mICWidth = modalInnerContainer.clientWidth;
      var mICHeight = modalInnerContainer.clientHeight;
      closeButton.style.top = (0.01*mICHeight).toString() + 'px';
      closeButton.style.right = (0.01*mICWidth).toString() + 'px';
    }

    else {
      closeButton.style.visibility = 'hidden';
    }
    
    window.onclick = function(event) {
      if (event.target == wrapper) {
        modalContainer.style.visibility = 'hidden';        
      }      
    }

  };
  var nameCells = document.querySelectorAll('td.tagpro-username');
  var len = nameCells.length;
  for (var i = 0; i < len; i++) {
    nameCells[i].onclick = summaryPopUp;
  };

  noScrollBar('table-container-1','table-container-2')

};

window.onload = main;
window.onresize = main;
