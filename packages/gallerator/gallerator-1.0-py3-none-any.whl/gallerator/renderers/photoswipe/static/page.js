import PhotoSwipeLightbox from './photoswipe-lightbox.esm.min.js';

const custom_zoom_fraction = 0.9

const lightbox = new PhotoSwipeLightbox({
  gallery: '#my-gallery',
  children: 'a',
  pswpModule: () => import('./photoswipe.esm.min.js'),
  initialZoomLevel: (zoomLevelObject) => {
    const zooms = []
    for (const dim of ['x', 'y']) {
      zooms.push(
        zoomLevelObject.panAreaSize[dim] / zoomLevelObject.elementSize[dim]
      )
    }
    return custom_zoom_fraction * Math.min(...zooms);
  },
  secondaryZoomLevel: 'fit',
});

// Show the current file name as a caption
lightbox.on('uiRegister', function () {
  lightbox.pswp.ui.registerElement({
    name: 'custom-caption',
    order: 9,
    isButton: false,
    appendTo: 'root',
    html: '',
    onInit: (el, pswp) => {
      lightbox.pswp.on('change', () => {
        const currSlideElement = lightbox.pswp.currSlide.data.element;
        let captionHTML = '';
        if (currSlideElement) {
          captionHTML = currSlideElement.getAttribute('data-file-name');
        }
        el.innerHTML = captionHTML;
      });
    }
  });
});

// Show video link button for videos
lightbox.on("uiRegister", function () {
  lightbox.pswp.ui.registerElement({
    name: "video-button",
    ariaLabel: "Video link",
    order: 10,
    isButton: true,
    html: ``,
    onInit: (el, pswp) => {
      lightbox.pswp.on('change', () => {
        const currSlideElement = lightbox.pswp.currSlide.data.element;
        let videoButtonHTML = ''
        if (currSlideElement.hasAttribute('data-video')) {
          let videoURL = currSlideElement.getAttribute('data-video')
          videoButtonHTML = `
            <a href='${videoURL}' target="_blank">
              <i class="fa fa-video-camera" aria-hidden="true">
            </a>`
        }
        el.innerHTML = videoButtonHTML;
      });
    }
  });
});

// Set window hash when we viewing an image in the lightbox
lightbox.on("change", (el) => {
  const currSlideElement = lightbox.pswp.currSlide.data.element;
  // Don't modify history, so don't use window.location.hash = ...
  // https://stackoverflow.com/a/23924886/345716
  history.replaceState(
    undefined,
    undefined,
    "#" + currSlideElement.getAttribute('data-file-name')
  )
});

// Remove window hash when we close the lightbox
lightbox.on("close", function () {
  // https://stackoverflow.com/a/49373716/345716
  history.replaceState(null, null, " ");
});

lightbox.init();

// If the window opens with a window hash, open that image in the lightbox.
if (window.location.hash != '') {
  const source = window.location.hash
  const containers = document.querySelectorAll('.image-container')
  let foundIndex = null
  for (let i = 0; i < containers.length; i++) {
    if ('#' + containers[i].getAttribute('data-file-name') == source) {
      foundIndex = i
    }
  }
  if (foundIndex == null) {
    console.error(`Couldn't find ${source} to open`)
  } else {
    lightbox.loadAndOpen(foundIndex, {
      gallery: document.querySelector("#my-gallery"),
    });
  }
}

window.addEventListener('keydown', (event) => {
  const key = event.key; // "ArrowRight", "ArrowLeft", "ArrowUp", or "ArrowDown"
  if (key != "ArrowLeft" && key != "ArrowRight") {
    return
  }
  if (lightbox.pswp) {
    // lightbox is open and handles left/right
    return
  }
  const paginations = document.querySelectorAll("li.page-item")
  if (paginations.length == 0) {
    return
  }
  let pagination
  if (key == "ArrowLeft") {
    pagination = paginations[0]
  } else if (key == "ArrowRight") {
    pagination = paginations[paginations.length-1]
  }
  const a = pagination.querySelector('a')
  if (a) {
    a.click()
  }
});