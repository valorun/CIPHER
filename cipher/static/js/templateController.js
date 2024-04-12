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
      this.$content.classList.add('opened');
      this.$element.dispatchEvent(openEvent);

      const currentHeight = getComputedStyle(this.$content).height;
      this.$content.style.height = 'fit-content';
      // retrieve the maximum height computed before reopening
      const maxHeight = getComputedStyle(this.$content).height;
      // set height to current height since transition cannot be triggered from a non specified value like 'fit-content'
      this.$content.style.height = currentHeight;

      getComputedStyle(this.$content).height; // small hack to allow smooth transition
      this.$content.style.height = maxHeight;
    }

    close() {
      this.$content.style.height = '0px';
      this.$icon.classList.add('fa-angle-right');
      this.$icon.classList.remove('fa-angle-down');
      this.$content.classList.remove('opened')
      this.$element.dispatchEvent(closeEvent);
    }

    get isOpen() {
      return this.$content.classList.contains('opened');
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
      if (!document.body.classList.contains('no-sidebar')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });

    document.getElementById('close-sidebar-button').addEventListener('click', () => {
      closeSidebar();
    });

    // setup collapse on accordions
    [...document.getElementsByClassName('accordion-header')].forEach($header =>
      accordions.push(new Accordion($header))
    );
  }

  function cacheDom() {
    DOM.$sidebarButton = document.getElementById('sidebar-button');
  }

  function openSidebar() {
    document.body.classList.remove('no-sidebar');
  }

  function closeSidebar() {
    document.body.classList.add('no-sidebar');
  }

  return {
    init: init,
    getAccordion: getAccordion
  };
})();
