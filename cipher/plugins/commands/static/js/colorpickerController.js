/* exported colorpickerController */
const colorpickerController = (() => {
    'use strict';

    const DOM = {};

    /* PUBLIC METHODS */
    function init() {
        cacheDom();
        bindUIEvents();
    }

    function getSelectedColor() {
        return DOM.$color.dataset.color;
    }

    /* PRIVATE METHODS */
    function bindUIEvents() {
        DOM.$color.addEventListener('click', () => {
            DOM.$colorPicker.style.display = 'block';
        });

        // select a color and change the color of the button
        [...document.getElementsByClassName('color-item')].forEach(e => {
            const newColor = e.dataset.color;
            e.addEventListener('click', () => {
                DOM.$colorPicker.style.display = 'none';
                DOM.$color.classList.remove(DOM.$color.dataset.color); // delete the color previous color class
                DOM.$color.dataset.color = newColor;
                DOM.$color.classList.add(newColor); // add the new color
            });
        });
    }

    function cacheDom() {
        DOM.$color = document.getElementById('color');
        DOM.$colorPicker = document.getElementById('color-picker');
    }

    return {
        init: init,
        getSelectedColor: getSelectedColor
    };
})();