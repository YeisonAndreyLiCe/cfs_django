/* eslint-disable-next-line */
function autoGrow(element){
  element.style.height = "5px";
  element.style.height = (element.scrollHeight)+"px";
  element.style.overflow = "hidden";
}