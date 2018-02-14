// костыль - my_script_scrolling недокручивает по верхнему тегу 

var timeOut;
function scrollToTop() {
	if (document.body.scrollTop!=0 || document.documentElement.scrollTop!=0){
	  window.scrollBy(0,-50);
	  timeOut=setTimeout('scrollToTop()',25);
	}
	else clearTimeout(timeOut);
}
