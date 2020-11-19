/* exported templateController */
const templateController = (() => {
  'use strict';

  const DOM = {};
  const accordions = [];

  const openEvent = new CustomEvent('open', { bubbles: true, cancelable: true });
  const closeEvent = new CustomEvent('close', { bubbles: true, cancelable: true });

  /**
   * Class used to represent the accordions containers in the page.
   */
  class Accordion {
    /**
     * Instanciate the accordion
     * @param {*} $header header element with class 'accordion-header'
     */
    constructor($header) {
      this.$element = $header.parentNode;
      this.$content = this.$element.getElementsByClassName('accordion-content')[0];
      this.$icon = this.$element.getElementsByClassName('accordion-icon')[0];
      this.$icon.classList.add('fas', 'fa-angle-right');
      this.$icon.classList.remove('fa-angle-down');
      this.$content.style.display = 'none';

      $header.addEventListener('click', () => {
        if (this.isOpen) {
          this.close();
        } else {
          this.open();
        }
      });
    }

    open() {
      this.$icon.classList.add('fa-angle-down');
      this.$icon.classList.remove('fa-angle-right');
      this.$content.style.display = 'block';
      this.$element.dispatchEvent(openEvent);
    }

    close() {
      this.$icon.classList.add('fa-angle-right');
      this.$icon.classList.remove('fa-angle-down');
      this.$content.style.display = 'none';
      this.$element.dispatchEvent(closeEvent);
    }

    get isOpen() {
      return this.$content.style.display !== 'none';
    }
  }

  /* PUBLIC METHODS */
  function init() {
    cacheDom();
    bindUIEvents();
  }

  /**
   * Return the accordion with the given ID.
   * @param {*} accordionId ID of the accordion.
   */
  function getAccordion(accordionId) {
    return accordions.filter(a => a.$element.id === accordionId)[0];
  }

  /* PRIVATE METHODS */
  function bindUIEvents() {
    DOM.$sidebarButton.addEventListener('click', () => {
      if (DOM.$sidebar.style.display !== 'none') {
        closeSidebar();
      } else {
        openSidebar();
      }
    });

    document.getElementById('closeSidebarButton').addEventListener('click', () => {
      closeSidebar();
    });

    DOM.$overlayBg.addEventListener('click', () => {
      closeSidebar();
    });

    // setup collapse on accordions
    [...document.getElementsByClassName('accordion-header')].forEach($header =>
      accordions.push(new Accordion($header))
    );
  }

  function cacheDom() {
    DOM.$sidebar = document.getElementById('sidebar');
    DOM.$sidebarButton = document.getElementById('sidebarButton');
    DOM.$overlayBg = document.getElementById('overlay');
  }

  function openSidebar() {
    DOM.$sidebar.style.display = 'block';
    DOM.$overlayBg.style.display = 'block';
  }

  function closeSidebar() {
    DOM.$sidebar.style.display = 'none';
    DOM.$overlayBg.style.display = 'none';
  }

  return {
    init: init,
    getAccordion: getAccordion
  };
})();
