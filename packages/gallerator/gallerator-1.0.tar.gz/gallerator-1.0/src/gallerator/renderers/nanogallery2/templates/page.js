    {# code: language=jinja-js #}
    let items = {{ media_items_json | safe }}
    let thumbnailHeight = {{ thumbnail_height | tojson }}

    jQuery(document).ready(function () {
      jQuery("#nanogallery2").nanogallery2({
        items, // From another variable on this page
        thumbnailHeight, // From another variable on this page
        thumbnailWidth: 'auto',
        viewerTools: {
          topLeft: 'pageCounter,playPauseButton,label',
          topRight: 'custom1,rotateLeft,rotateRight,zoomButton,closeButton'
        },
        fnImgToolbarCustClick: videoCB,
        // itemsBaseURL: 'https://nanogallery2.nanostudio.org/samples/',
        icons: {
          viewerCustomTool1: '<i class="nGY2Icon-video"></i>'
        },
        locationHash: true
      });
    });

    function videoCB($e, bogus, item) {
      if (item.customData && "video" in item.customData) {
        url = item.customData.video
      } else {
        url = item.src
      }
      window.open(url)
    }
