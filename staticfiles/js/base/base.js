


document.querySelectorAll('.media img').forEach((ele)=>ele.addEventListener('mouseover', changePicture));
document.querySelectorAll('.media-hover-effect img').forEach((ele)=>ele.addEventListener('mouseout', changePictureOut));

function changePicture(ev) {
  const media = ev.target.parentElement;
  const mediaHidden = ev.target.parentElement.parentElement.querySelector('.media-hover-effect');
  media.style.display = 'none';
  mediaHidden.style.display = 'block';
  console.log('hovered');
}

function changePictureOut(ev) {
  const media = ev.target.parentElement.parentElement.querySelector('.media');
  const mediaHidden = ev.target.parentElement;
  media.style.display = 'block';
  mediaHidden.style.display = 'none';
  console.log('hovered out');
}