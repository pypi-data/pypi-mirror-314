console.log("pg")
import PhotoSwipeLightbox from './photoswipe-lightbox.esm.min.js';
const lightbox = new PhotoSwipeLightbox({
  gallery: '#my-gallery',
  children: 'a',
  pswpModule: () => import('./photoswipe.esm.min.js')
});


lightbox.on('uiRegister', function() {
  lightbox.pswp.ui.registerElement({
    name: 'custom-caption',
    order: 9,
    isButton: false,
    appendTo: 'root',
    html: 'Caption',
    onInit: (el, pswp) => {
      lightbox.pswp.on('change', () => {
        const currSlideElement = lightbox.pswp.currSlide.data.element;
        let captionHTML = '';
        if (currSlideElement) {
          // get caption from alt attribute
          captionHTML = currSlideElement.querySelector('img').getAttribute('alt');
        }
        el.innerHTML = captionHTML;
      });
    }
  });
});


document.getElementById('open-1').addEventListener('click', (e) => {
  e.preventDefault()
  console.log('Open button')
  return false
})
lightbox.init();
